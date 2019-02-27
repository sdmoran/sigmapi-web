/*
Code for rendering the family tree.

Algorithm for tree node placement:
(backup pdf placed on the drive since this site seems like it could go away)
https://rachel53461.wordpress.com/2014/04/20/algorithm-for-drawing-trees/

The algorithm is decently complicated overall, but each individual step should
make sense intuitively, the tutorial has a simpler example
 */

let canvas, board;

function initFamilyTree() {
  fabric.Object.prototype.selectable = false;
  canvas = new fabric.Canvas('tree', {
    renderOnAddRemove: false
  });
  canvas.setZoom(0.25);
  canvas.selection = false;
  addPanning(canvas);
  initResizeCanvas(canvas);
  initZooming(canvas);

  canvas.imageSmoothingEnabled = false;

  board = new WoodBoard(canvas);

  const imagePromise = new Promise((resolve) => {
    fabric.Image.fromURL('/static/img/wood3.png', function (img) {
      resolve(img);
    });
  });


  Promise.all([
    imagePromise,
    $.ajax("/brothers/family-tree/data/"),
    document.fonts.load('1em Pangolin'),
    document.fonts.ready
  ]).then((values) => {
    board.init(values[0]);

    let data = values[1].tree.children;

    const urlParams = new URLSearchParams(window.location.search);
    const selectedTree = urlParams.get('tree');
    if(selectedTree !== "All") {
      for(let node of data) {
        console.log(node.name, selectedTree);
        if(node.name === selectedTree) {
          data = [node];
          break;
        }
      }
    }

    new SmartTreeGenerator(data, board).drawBrothersSmart();
    canvas.renderAll();

    // setupSearchTools(data, board);
  });
}

$(document).ready(initFamilyTree);


function setupSearchTools(data, board) {
  const {x, y} = board.transform(data[0].renderX, data[0].renderY);
  console.log(x, y);
  console.log(data[0]);
  const newP = fabric.util.transformPoint(new fabric.Point(x, y), canvas.viewportTransform);
  console.log(newP);
  // canvas.setZoom(1);
  // canvas.absolutePan({x: x, y: y});
  canvas.absolutePan(newP);
}

function reloadAll() {
  canvas.clear();
  initFamilyTree();
  canvas.renderAll();
}

function formatName(str) {
  let spaceIndex = str.indexOf(' ');
  if(spaceIndex === -1)
    return str;
  return str.substr(0, spaceIndex) + '\n' + str.substr(spaceIndex+1, str.length);
}

class SmartTreeGenerator {
  constructor(data, board) {
    this.data = data;
    this.board = board;
    this.levelMap = new Map();
    this.maxLevel = 0;
  }

  drawBrothersSmart() {
    this.sortAlphas();

    this.assignLocalXValues();
    this.centerParentsUnderChildren();
    this.applyNodeMods();

    let changes = true;
    while(changes) {
      changes = false;
      for (let i = this.maxLevel; i >= 0; i--) {
        if(this.fixConflicts(this.levelMap.get(i)))
          changes = true;
        this.applyNodeMods();
      }
    }

    let rightContour = this.getRightContour(this.data[this.data.length-1]);
    let maxX = this.transformToRenderX(Math.max(...rightContour));

    // this.board.treeOffsetX = (Math.ceil(maxX / this.board.imgWidth) - (maxX / this.board.imgWidth)) * this.board.imgWidth / 4.0;

    this.board.drawTiles(maxX);

    this.render();
  }

  render() {
    this._renderNames();
    this._renderLines();
  }

  _renderNames(data = this.data, yLevel = 0) {
    for(let child of data) {
      child.renderX = this.transformToRenderX(child.x);
      child.renderY = this.transformToRenderY(yLevel);
      child.renderHeight = 65;
      this.board.addText(child.renderX,child.renderY, formatName(child.name));

      this._renderNames(child.children, yLevel+1);
    }
  }

  _renderLines(data = this.data) {
    for (let child of data) {
      const numGrandchildren = child.children.length;
      for (let i = 0; i < numGrandchildren; i++) {
        let grandchild = child.children[i];
        let xStartOffset = (i- (0.5 * (numGrandchildren - 1))) * 20;
        board.addLine(
          child.renderX + xStartOffset,
          child.renderY + child.renderHeight,
          grandchild.renderX,
          grandchild.renderY
        );
      }
      this._renderLines(child.children);
    }
  }

  transformToRenderX(x) {
    const blockWidth = 160, xOffset = blockWidth / 2;
    return x * blockWidth + xOffset
  }

  transformToRenderY(y) {
    const blockHeight = 125, yOffset = 15;
    return y * blockHeight + yOffset;
  }

  assignLocalXValues(data = this.data, parent = null, level=0) {
    if(!this.levelMap.has(level)) {
      this.levelMap.set(level, []);
      if(level > this.maxLevel)
        this.maxLevel = level;
    }

    for(let i = 0; i < data.length; i++) {
      data[i].localX = i;
      data[i].x = i;
      data[i].mod = 0;
      data[i].parent = parent;
      this.levelMap.get(level).push(data[i]);

      this.assignLocalXValues(data[i].children, data[i], level+1);
    }
  }

  centerParentsUnderChildren(data = this.data) {
    for (let i = 0; i < data.length; i++) {
      const node = data[i];
      const children = data[i].children;

      if (children.length > 0) {
        this.centerParentsUnderChildren(children);

        let desiredX = (children[0].x + children[children.length-1].x) / 2.0;

        if(i === 0)
          node.x = desiredX;
        else
          node.mod = node.x - desiredX;
      }
    }
  }

  fixConflicts(data = this.data) {
    let changes = false;
    for(let i = 1; i < data.length; i++) {
      let leftContour = this.getLeftContour(data[i]);

      let maxDiff = -1;

      for(let p = 0; p < i; p++) {
        let rightContour = this.getRightContour(data[p]);

        for(let j = 0; j < rightContour.length && j < leftContour.length; j++) {
          if(rightContour[j] - leftContour[j] > maxDiff)
            maxDiff = rightContour[j] - leftContour[j];
        }
      }

      // If maxDiff is 0, then the items exactly overlap
      maxDiff = Math.ceil(maxDiff + 1);

      if(maxDiff > 0) {
        data[i].mod += maxDiff;
        data[i].x += maxDiff;

        this.bubbleCorrectionMods(data[i], maxDiff);

        this.applyNodeMods([data[i]]);
        changes = true;
      }
    }

    return changes;
  }

  bubbleCorrectionMods(node, amount) {
    if(node.parent) {
      let shiftAmount = amount * 1.0 / node.parent.children.length;
      node.parent.x += shiftAmount;
      this.bubbleCorrectionMods(node.parent, shiftAmount);
    }
  }

  getRightContour(node) {
    if(node.children.length > 0)
      return [node.x].concat(this.getRightContour(node.children[node.children.length-1]));
    return [node.x];
  }

  getLeftContour(node) {
    if (node.children.length > 0)
      return [node.x].concat(this.getLeftContour(node.children[0]));
    return [node.x];
  }

  applyNodeMods(data = this.data, mod=0) {
    for(let node of data) {
      // if(mod !== 0)
        // console.log("Modding " + node.name + " " + mod + " over");
      node.x += mod;
      this.applyNodeMods(node.children, mod + node.mod);
      node.mod = 0;
    }
  }

  nameCompareFormat(str) {
    let temp = str.split(' ');
    return temp[temp.length - 1];
  }

  sortAlphas(array = this.data) {
    array.sort((node1, node2) => {
      return this.nameCompareFormat(node1.name).localeCompare(this.nameCompareFormat(node2.name));
    });
  }
}


/**
 * WoodBoard
 * Takes care of rendering the wooden tiles, and transforming
 * points into a coordinate plane with the bottom left of the board as the origin
 */
class WoodBoard {
  constructor(canvas = null, offsetX = 20, offsetY = 20) {
    if(canvas == null) {
      throw "Must supply a canvas";
    }

    this.canvas = canvas;
    this.offsetX = offsetX;
    this.offsetY = offsetY;
    this.treeOffsetX = 0;
    this.rows = 4;
    this.cols = 17;
  }

  init(img) {
    this.woodImage = img;
    this.imgWidth = img.getWidth();
    this.imgHeight = img.getHeight();
  }

  getNumberOfTilesFor(xWidth) {
    return Math.ceil((xWidth) / this.imgWidth);
  }

  drawTiles(maxX) {
    this._drawTiles(4, this.getNumberOfTilesFor(maxX));
  }

  _drawTiles(rows = 4, cols = 17) {
    this.rows = rows;
    this.cols = cols;
    // The tiling needs to be done manually because
    // of sucky canvas rendering for textures :(
    for (let i = 0; i < this.cols; i++) {
      for (let p = 0; p < this.rows; p++) {
        this.woodImage.clone((imgClone) => {
          imgClone.set('left', this.imgWidth * i + this.offsetX);
          imgClone.set('top', this.imgHeight * p + this.offsetY);
          this.canvas.add(imgClone);
          this.canvas.sendToBack(imgClone);
        });
      }
    }

    const borderWidth = 10;

    // This is just a border around the board
    this.rect = new fabric.Rect({
      width: this.imgWidth * this.cols + borderWidth,
      height: this.imgHeight * this.rows + borderWidth,
      left: this.offsetX - borderWidth,
      top: this.offsetY - borderWidth,
      strokeWidth: borderWidth,
      stroke: '#474846',
      fill: 'transparent',
    });
    this.canvas.add(this.rect);

    this.canvas.renderAll();
  }

  /**
   * Get the width of the board
   * @returns {number} The width of the board in pixels
   */
  get width() {
    return this.imgWidth * this.cols;
  }

  /**
   * Gets the height of the board
   * @returns {number} The height of the board in pixels
   */
  get height() {
    return this.imgHeight * this.rows;
  }

  /**
   * Adds text to the board
   * @param x The x coordinate of the text
   * @param y The y coordinate of the text
   * @param str The text to render
   * @param transform True if the first two arguments are in the board's coordinate plane
   * (as opposed to the canvas' coordinate plane)
   * @returns {fabric.Text} The FabricJS Text object created
   */
  addText(x, y, str, transform=true) {
    const transformed = this.transform(x, y);
    const text = new fabric.Text(str, {
      left: transformed.x + this.treeOffsetX,
      top: transformed.y,
      fontFamily: 'Pangolin',
      stroke: '#000000',
      opacity: '0.6',
      fontSize: '24',
      originX: 'center',
      originY: 'bottom',
      textAlign: 'center',
      lineHeight: 1,
      shadow: new fabric.Shadow('black 0 0 4px'),
      objectCaching: false
    });
    this.canvas.add(text);
    return text;
  }


  addLine(x1, y1, x2, y2, transform=true) {
    const p1 = this.transform(x1, y1);
    const p2 = this.transform(x2, y2);
    const line = new fabric.Line([p1.x + this.treeOffsetX, p1.y, p2.x + this.treeOffsetX, p2.y], {
      fill: 'black',
      stroke: 'black',
      opacity: '0.6',
      strokeWidth: 5,
      strokeLineCap: "round",
      shadow: new fabric.Shadow('black 0 0 3px'),
      objectCaching: false
    });

    this.canvas.add(line);
    return line;
  }

  transform(x, y) {
    return {
      x: x + this.offsetX,
      y: this.offsetY + this.height - y
    }
  }
}


function initResizeCanvas(canvas) {
  window.addEventListener('resize', _.debounce(_resizeCanvas, 150), false);

  function _resizeCanvas() {
    canvas.setHeight($('#tree-container').height());
    canvas.setWidth(window.innerWidth);
    canvas.renderAll();
  }

  // resize on init
  _resizeCanvas();
}

function addPanning(canvas) {
  function startPan(event) {

    let x0 = event.screenX,
      y0 = event.screenY;

    function continuePan(event) {
      let x = event.screenX,
        y = event.screenY;
      let deltaX = x - x0;
      let deltaY = y - y0;

      if(canvas.viewportTransform[4] + deltaX > 0) {
        // canvas.relativePan(new fabric.Point(-canvas.viewportTransform[4], 0));
        // deltaX = 0;
        // console.log('reset x')
      }
      if (canvas.viewportTransform[5] + deltaY > 0) {
        // canvas.relativePan(new fabric.Point(0, -canvas.viewportTransform[5]));
        // deltaY = 0;
        // console.log('reset y')
      }
      canvas.relativePan(new fabric.Point(deltaX, deltaY));

      x0 = x;
      y0 = y;
    }

    function stopPan(event) {
      $(window).off('mousemove', continuePan);
      $(window).off('mouseup', stopPan);
    }
    $(window).mousemove(continuePan);
    $(window).mouseup(stopPan);
    $(window).contextmenu(cancelMenu);
  }

  function cancelMenu() {
    $(window).off('contextmenu', cancelMenu);
    return false;
  }

  $('#tree-container').mousedown(startPan);
}

function initZooming(canvas) {
  canvas.on('mouse:wheel', function (opt) {
    let delta = opt.e.deltaY;
    let pointer = canvas.getPointer(opt.e);
    let zoom = canvas.getZoom();
    zoom = zoom + delta / 800;
    if (zoom > 1) zoom = 1;
    if (zoom < 0.2) zoom = 0.2;
    canvas.zoomToPoint({x: opt.e.offsetX, y: opt.e.offsetY}, zoom);
    console.log(canvas);
    console.log(opt.e.offsetX, opt.e.offsetY);
    opt.e.preventDefault();
    opt.e.stopPropagation();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}