$(document).ready(function() {
	// Add form-control class to all input elements that are populated by django templating.
	$("input[type='text']").addClass("form-control");
	$("input[type='url']").addClass("form-control");
	$("input[type='password']").addClass("form-control");
	$("input[type='number']").addClass("form-control");
	$("textarea").addClass("form-control");
	$("select").addClass("form-control");
});