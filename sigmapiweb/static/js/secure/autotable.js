$(document).ready(function() {
	// Initialize all datatable class elements to data table. (Used to Style the Data Table)
	$.fn.dataTableExt.oStdClasses["sFilter"] = "dataTable-filter"
	$.fn.dataTableExt.oStdClasses["sLength"] = "dataTable-length"
	$.fn.dataTableExt.oStdClasses["sInfo"] = "dataTable-message"
	$.fn.dataTableExt.oStdClasses["sPagePrevEnabled"] = "btn btn-primary dataTable-button-left"
	$.fn.dataTableExt.oStdClasses["sPagePrevDisabled"] = "btn btn-primary disabled dataTable-button-left"
	$.fn.dataTableExt.oStdClasses["sPageNextEnabled"] = "btn btn-primary dataTable-button-right"
	$.fn.dataTableExt.oStdClasses["sPageNextDisabled"] = "btn btn-primary disabled dataTable-button-right"
	$.fn.dataTableExt.oStdClasses["sSortAsc"] = "dataTable-sort-asc"
	$.fn.dataTableExt.oStdClasses["sSortDesc"] = "dataTable-sort-desc"

	
	// Initialize all data table instances.
	$(".dataTable").dataTable();
});