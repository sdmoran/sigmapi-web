const boxWidth = 130, boxHeight = 40, spacing = 40;

function generateFamilyTree(containerID, tree)
{
    const widestLevel = widestLevelWidth(tree);
    const contentWidth = (widestLevel * boxWidth) + ((widestLevel+1) * spacing);

    let graph = new joint.dia.Graph;

    let paper = new joint.dia.Paper({
        el: $(`#${containerID}`),
        model: graph,
        gridSize: 1,
        interactive: false
    });

    joint.shapes.custom = {};
    // The following custom shape creates a link out of the whole element.
    joint.shapes.custom.ElementLink = joint.shapes.basic.Rect.extend({
        // Note the `<a>` SVG element surrounding the rest of the markup.
        markup: '<a><g class="rotatable"><g class="scalable"><rect/></g><text/></g></a>',
        defaults: joint.util.deepSupplement({
            type: 'custom.ElementLink'
        }, joint.shapes.basic.Rect.prototype.defaults)
    });

    // Perform all the drawing for boxes and links
    createLevel(tree, spacing, contentWidth, graph); // Recursively draws levels in the tree
    drawConnections(tree, graph); // Draws all the connections between brothers

    let oldOriginX;
    let oldOriginY;
    paper.on('blank:pointerdown',
        function(event, x, y) {
            oldOriginX = paper.options.origin.x;
            oldOriginY = paper.options.origin.y;
            dragStartPosition = { x: event.pageX, y: event.pageY};
        }
    );

    paper.on('cell:pointerup blank:pointerup', function(cellView, x, y) {
        delete dragStartPosition;
    });

    let initialYOffset = paper.getContentBBox().y;

    $('body').mousemove(function(event)
    {
        if (typeof dragStartPosition !== 'undefined')
        {
            let originX = event.pageX - dragStartPosition.x + oldOriginX;
            let originY = event.pageY - dragStartPosition.y + oldOriginY;
            // //Prevent dragging outside the left or right
            // if(originX > 0) originX = 0;
            // else if((originX < $('#myholder').width() - paper.getContentBBox().width) && oldOriginX-originX > 0)
            //     originX = Math.min($('#myholder').width() - paper.getContentBBox().width, oldOriginX);

            //Prevent dragging outside the top or bottom
            // if(originY < -initialYOffset) originY = -initialYOffset;
            // else if((originY+initialYOffset > $('#myholder').height() - paper.getContentBBox().height) && originY+initialYOffset - oldOriginY > 0)
            //     originY = Math.min($('#myholder').height() - paper.getContentBBox().height - initialYOffset, oldOriginY+initialYOffset);

            paper.setOrigin(originX, originY);
        }
    });
}

function createLevel(tree, yCoord, contentWidth, graph)
{
    let newLevel = [];
    for(let i = 0; i < tree.length; i++)
    {
        let text = joint.util.breakText(tree[i].name, { width: boxWidth });
        xCoord = (contentWidth / (tree.length+1) * (i+1)) - (boxWidth/2);
        let rect = new joint.shapes.custom.ElementLink({
            position: { x: xCoord, y: yCoord },
            size: { width: boxWidth, height: boxHeight },
            attrs: {
                rect: { fill: 'white' },
                a: { 'xlink:href': 'http://www.google.com', 'xlink:show': 'new', cursor: 'pointer' },
                text: { text: text, fill: 'black', fontSize: "12px" } }
        });
        tree[i].rect = rect;

        graph.addCell(rect);

        newLevel = newLevel.concat(tree[i].littles);
    }
    if(newLevel.length !== 0)
        createLevel(newLevel, yCoord + boxHeight + spacing, contentWidth, graph);
}

function drawConnections(tree, graph)
{
    let newLevel = [];
    for(let i = 0; i < tree.length; i++)
    {
        for(let p = 0; p < tree[i].littles.length; p++)
        {
            let link = new joint.dia.Link({
                source: { id: tree[i].rect.id },
                target: { id: tree[i].littles[p].rect.id }
            });
            graph.addCell(link);
        }
        newLevel = newLevel.concat(tree[i].littles);
    }
    if(newLevel.length !== 0)
        drawConnections(newLevel, graph);
}

function levelWidth(tree, level)
{
    if(level === 0)
        return tree.length;

    let sum = 0;
    for(let i = 0; i < tree.length; i++)
    {
        sum += levelWidth(tree[i].littles);
    }
    return sum;
}

function widestLevelWidth(tree)
{
    let max = tree.length;

    let newLevel = [];
    for(let i = 0; i < tree.length; i++)
    {
        newLevel = newLevel.concat(tree[i].littles);
    }

    if(newLevel.length !== 0)
    {
        max = Math.max(widestLevelWidth(newLevel), max);
    }
    return max;
}
