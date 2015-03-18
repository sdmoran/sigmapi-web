var requests_table;
var changes_table;
var points_table;

$(document).ready(function() {
  setupClickListeners();

  requests_table = $("#requests-table").DataTable();
  changes_table = $("#changes-table").DataTable();
  points_table = $("#points-table").DataTable();
});

/**
 * Sets up click listeners
 */
function setupClickListeners()
{
  $("#add-brother-form-submit").click(submitAddBrotherForm);
  $("#modify-points-form-submit").click(submitModifyPointsForm);
  $(".approve-points-button").click(approveRequest);
  $(".deny-request-button").click(denyPointsRequest);


  $("#points-table").on('click', 'a.modify-points-button', showModifyPointsForm);
}

/**
 * Submits the add brother form
 */
function submitAddBrotherForm()
{
  var userid = $("#id_brother").val();
  var points = $("#id_piPoints").val();
  modifyPiPoints(userid, points);

  $("#id_brother").val("");
  $("#id_piPoints").val("");
  $(this).modal("hide");
}

/**
 * Displays form to modify user's points
 */
function showModifyPointsForm()
{
  var id = $(this).attr("id"); // Retrieve user ID
  var cur_points = $("#"+id+".points-points-field").first().text(); // Retrieve current points
  var user = $("#"+id+".points-name-field").first().text(); // Retrieve username

  $("#modify-points-form-user").html(user); // Set username in form
  $(".modify-points-form-userid").attr("id", id); // Set user ID in form
  $("#modify-points-form-points").val(cur_points); // Set current points in form
  $("#modify-points").modal("show"); // Finally display the form
}

/**
 * Submit the modify points form
 */
function submitModifyPointsForm()
{
  var userid = $(".modify-points-form-userid").attr("id"); // Get user ID
  var points = $("#modify-points-form-points").val(); // Get new points
  modifyPiPoints(userid, points); // Send modify points request

  $("#modify-points").modal("hide"); // Hide form
}

/**
 * Deny a points request
 */
function denyPointsRequest()
{
  var id = $(this).attr("id");
  deleteRequest(id);
}

/**
 * Modifies the pi points for the given user id to the given new point value
 */
function modifyPiPoints(userid, newpoints)
{
  var url = userid+"/";
  var csrftoken = $.cookie('csrftoken');
  $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
     },
    url: url,
    data: {
      "piPoints":newpoints,
    },
  }).done(function( data ) {
    var id = data['id'];
    var name = data['name'];
    var oldPoints = data['old_points'];
    var points = data['points'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".points-row").length > 0)
    {
      $("#"+id+".points-points-field").first().html(points);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, points, '<a id='+id+' class="btn btn-primary btn-sm modify-points-button">Modify Points</a>'];
      points_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldPoints, points];
    changes_table.fnAddData(change_data);

  });
}

/**
 * Approves a pi point request
 */
function approveRequest()
{
  var request_id = $(this).attr("id");
  var url = "request/"+request_id+"/accept/";
  var csrftoken = $.cookie('csrftoken');
  $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
     },
    url: url,
  }).done(function( data ) {
    var pos = requests_table.fnGetPosition($("#"+request_id+".requests_row").get(0));
    requests_table.fnDeleteRow(pos);
    var id = data['id'];
    var name = data['name'];
    var oldPoints = data['old_points'];
    var points = data['points'];
    var date = data['date'];
    var modifier = data['modifier'];

    //Update the standings if it exists.
    //Check if exists
    if($("#"+id+".points-row").length > 0)
    {
      $("#"+id+".points-points-field").first().html(points);
    }
    else
    {
      //Otherwise create it.
      var standings_data = [name, points, '<a id='+id+' class="ui tiny red button modify-points-button">Modify Points</a>'];
      points_table.fnAddData(standings_data);
    }

    //Update the change log
    var change_data = [date, modifier, name, oldPoints, points];
    changes_table.fnAddData(change_data);

    //Update the count
    $("#pprCount").first().html(data.pprCount);
    $("#pprCount2").first().html(data.pprCount);
  });
}

/**
 * Deletes a Pi Point request
 */
function deleteRequest(requestid)
{
  var url = "request/"+requestid+"/delete/";
  var csrftoken = $.cookie('csrftoken');
  $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
     },
    url: url,
  }).done(function( data ) {
    var pos = requests_table.fnGetPosition($("#"+requestid+".requests_row").get(0));
    requests_table.fnDeleteRow(pos);
    $("#pprCount").first().html(data.pprCount);
    $("#pprCount2").first().html(data.pprCount);
  });
}


/***********************************
 * Util functions for csrf
 ***********************************/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
