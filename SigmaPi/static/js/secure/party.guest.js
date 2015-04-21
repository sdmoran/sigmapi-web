// Define party module namespace
var PartyModule = PartyModule || {};

PartyModule.POLLING_TIMEOUT = 10000; // 10 seconds

PartyModule.MESSAGE_UX_TIMEOUT = 5000; // 5 seconds

PartyModule.displayError = function(errorText)
{
	$("#message-ux").removeClass('alert-info');
	$("#message-ux").addClass('alert-danger');
	$("#message-ux").html(errorText);

	PartyModule.showMessageUX(PartyModule.MESSAGE_UX_TIMEOUT);
}

PartyModule.displayMessage = function(msgText)
{
	$("#message-ux").removeClass('alert-danger');
	$("#message-ux").addClass('alert-info');
	$("#message-ux").html(msgText);

	PartyModule.showMessageUX(PartyModule.MESSAGE_UX_TIMEOUT);
}

PartyModule.showMessageUX = function(timeout)
{
	$("#message-ux").fadeIn();

	clearTimeout(PartyModule.messageUXTimeout);

	PartyModule.messageUXTimeout = setTimeout(function() {
		$("#message-ux").fadeOut();
	}, timeout);
}

PartyModule.messageUXTimeout = null;

/*
 * Guest Class Definition
 */

PartyModule.Guest = function(id, name, addedByName, addedByID, signedIn)
{
	this.name = name;
	this.addedByName = addedByName;
	this.addedByID = addedByID;
	this.signedIn = signedIn;
	this.id = id;

	this.signedInCallback = function() {};
	this.signedOutCallback = function() {};
}

/*
 * Toggles signing in a guest
 */
PartyModule.Guest.prototype.toggleSignedIn = function()
{
	var thisOuter = this;

	// Figure out the base signin URL.
	var url = "signIn/";

	if (this.signedIn)
	{
		url = "signOut/";
	}

	// Send the ajax request to sign in / out
	$.ajax({
		type: "POST",
	    url: url + this.id + "/",
	}).done(function( data ) {
		// If succeeded, change the status accordingly
		thisOuter.signedIn = !thisOuter.signedIn;

		// Show the checked in status appropriately
		if (thisOuter.signedIn)
		{
			$(".guest#" + thisOuter.id + " > .status.checked-in").addClass("present");
			thisOuter.signedInCallback();
		}
		else
		{
			$(".guest#" + thisOuter.id + " > .status.checked-in").removeClass("present");
			thisOuter.signedOutCallback();
		}

	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});
};

/**
 * Comparison function
 */
PartyModule.Guest.prototype.compareTo = function(otherGuest)
{
	if (this.name.toLowerCase() < otherGuest.name.toLowerCase()) return -1;
	if (this.name.toLowerCase() > otherGuest.name.toLowerCase()) return 1;
	return 0;
};

/*
 * Guest List Class Definition
 */

 /*
  * Constructor
  * Takes in string ID of the list this guest list is controlling.
  */
PartyModule.GuestList = function(userID, partyMode, listID, guestSignedInCallback, guestSignedOutCallback, listCountChangedCallback)
{
	this.userID = userID;
	this.partyMode = partyMode;
	this.listID = listID;

	this.userGuestCount = 0;

	this.currentFilter = "";
	this.viewAllGuests = true;

	this.initialLoad = true;

	this.list = [];

	this.lastTimePollSucceeded = 0;
	this.lastTimePollTried = 0;

	this.guestSignedInCallback = guestSignedInCallback;
	this.guestSignedOutCallback = guestSignedOutCallback;
	this.listCountChangedCallback = listCountChangedCallback;
};

/*
 * Methods
 */

/*
 * Polls the server continuously, checking for new guests since last poll
 * Note: This polling does not occur during party mode
 */
PartyModule.GuestList.prototype.pollServer = function()
{
	var thisOuter = this;

	$.ajax({
		type: "GET",
	    url: "poll/",
	    data: {
	    	"gender": this.listID,
	    	"last": this.lastTimePollSucceeded
	    }
	}).done(function( data ) {
		thisOuter.lastTimePollSucceeded = thisOuter.lastTimePollTried;

		// Add each of the "new" guests to the list
		for (var i = 0; i < data.guests.length; i++)
		{
			var currentGuest = data.guests[i];

			var guestObj = new PartyModule.Guest(currentGuest.id, currentGuest.name,
				currentGuest.addedByName, currentGuest.addedByID, currentGuest.signedIn)

			thisOuter.addGuest(guestObj);
		}

		// If this is the first time we have polled, hide the loader
		if (thisOuter.initialLoad)
		{
			$(".loader#"+thisOuter.listID).addClass("hidden");

			thisOuter.initialLoad = false;
		}

		// Dont poll if in party mode
		if (!thisOuter.partyMode)
		{
			setTimeout(
				function(){
					thisOuter.pollServer();
				}
				, PartyModule.POLLING_TIMEOUT);
		}
	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});

	this.lastTimePollTried = new Date().getTime();
};

/*
 * Adds a guest to the guest list
 */
PartyModule.GuestList.prototype.addGuest = function(guest)
{
	// Insert the guest at the correct sorted location in the guest list
	function locationOf(element, array, start, end) {
		if (array.length === 0)
	    	return -1;

		start = start || 0;
		end = end || array.length;
		var pivot = (start + end) >> 1;

		var c = element.compareTo(array[pivot]);

		if (c == 0)
			return -100; // Already exists - duplicate

		if (end - start <= 1) return c == -1 ? pivot - 1 : pivot;

		switch (c) {
	    	case -1: return locationOf(element, array, start, pivot);
	    	case 1: return locationOf(element, array, pivot, end);
		};
	};
	var location = locationOf(guest, this.list); // Find sorted location for guest

	if (location == -100)
	{
		return; // Don't add duplicates.
	}

	// Insert guest if new
	this.list.splice(location + 1, 0, guest);

	// Now add an object to the page.
	var clonedTemplate = $("#guest-template").clone();

	// Set the ID appropriately
	clonedTemplate.attr("id", guest.id);
	clonedTemplate.removeClass("hidden"); // Make the object visible

	// Set the name and details to the guest's
	clonedTemplate.find(".name").html(guest.name);
	clonedTemplate.find(".details").html("Added by " + guest.addedByName + ".");

	// If not being added to the start, add after the one before.
	if (location >= 0)
	{
		var priorID = this.list[location].id;

		clonedTemplate.insertAfter(".guest#" + priorID);
	}
	else
	{
		// Otherwise, add to the start of the guest list
		clonedTemplate.prependTo(".guest-list#" + this.listID);
	}

	// Setup party mode click listeners
	if (this.partyMode)
	{
		// Show guest as signed in if already done so
		if (guest.signedIn)
			clonedTemplate.find(".status.checked-in").addClass("present");

		// When template is clicked, sign the guest in
		clonedTemplate.click(function() {
			guest.toggleSignedIn();
		});

		// Add signed in/signed out callback
		guest.signedInCallback = this.guestSignedInCallback;
		guest.signedOutCallback = this.guestSignedOutCallback;
	}
	else
	{
		// Setup removal click listeners, if applicable

		var removeButton = clonedTemplate.find(".status.remove-guest");

		// Remove the remove button if user does not have permission to remove this guest
		if (this.userID != guest.addedByID)
		{
			removeButton.remove();
		}
		else // Otherwise, make it remove when clicked
		{
			var outerThis = this;

			removeButton.attr("id", guest.id);

			removeButton.click(function() {
				outerThis.removeGuest(parseInt($(this).attr("id")));
			});
		}
	}

	// If we have a current filter, hide/filter the guest if needed
	if (this.currentFilter.length > 0)
	{
		if(!(this.fuzzySearch(guest.name.toLowerCase(), this.currentFilter)
			|| this.fuzzySearch(guest.addedByName.toLowerCase(), this.currentFilter)))
		{
			clonedTemplate.addClass("filtered");
		}
	}

	if (guest.addedByID == this.userID)
		this.userGuestCount++;

	// List count changed callback
	this.listCountChangedCallback();
};

/*
 * Removes a guest from the guest list
 */
PartyModule.GuestList.prototype.removeGuest = function(guestID)
{
	var thisOuter = this;

	$.ajax({
		type: "DELETE",
	    url: "destroy/" + guestID + "/",
	}).done(function( data ) {

		// Find the location of the guest
		var location = -1;
		for (var i = 0; i < thisOuter.list.length; i++)
		{
			if (thisOuter.list[i].id == guestID)
			{
				location = i;
				break;
			}
		}

		// Remove it from the list if we found it
		if (location != -1)
		{
			// Decrement the user's guest count if applicable
			if (thisOuter.list[location].addedByID == thisOuter.userID)
				thisOuter.userGuestCount--;

			thisOuter.list.splice(location, 1);
		}

		// Always try to remove it from view in case it somehow got
		// orphaned
		$(".guest#" + guestID).remove();

		// List count changed callback
		thisOuter.listCountChangedCallback();

		PartyModule.displayMessage("Guest removed.");

	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});
};

/**
 * Filters the list for the given query
 */
PartyModule.GuestList.prototype.filterList = function(query)
{
	query = query.toLowerCase().trim();

	if (query.length == 0)
	{
		$(".guest").removeClass("filtered");
	}
	else
	{
		// Check every guest to see if they match the query
		for(var i = 0; i < this.list.length; i++)
		{
			var currentGuest = this.list[i];

			if (this.fuzzySearch(currentGuest.name.toLowerCase(), query)
				|| this.fuzzySearch(currentGuest.addedByName.toLowerCase(), query))
			{
				$(".guest#" + currentGuest.id).removeClass("filtered");
			}
			else
			{
				$(".guest#" + currentGuest.id).addClass("filtered");
			}
		}
	}

	this.currentFilter = query;
};

PartyModule.GuestList.prototype.fuzzySearch = function(str, pattern)
{
	pattern = pattern.split("").join(".{0,"+2+"}");

	return (new RegExp(pattern)).test(str);
};

/**
 * Get the count of total guests
 */
PartyModule.GuestList.prototype.getAllCount = function()
{
	return this.list.length;
};

/**
 * Get the count of guests for this user
 */
PartyModule.GuestList.prototype.getUserCount = function()
{

	return this.userGuestCount;
};

/**
 * Shows all of the guests in the list
 */
PartyModule.GuestList.prototype.showAllGuests = function()
{
	this.viewAllGuests = true;

	for (var i = 0; i < this.list.length; i++)
	{
		var currentGuest = this.list[i];
		$(".guest#"+currentGuest.id).removeClass("filtered-2");
	}

};

/**
 * Shows only the guests in the list added by the current user
 */
PartyModule.GuestList.prototype.showMyGuests = function()
{
	this.viewAllGuests = false;

	for (var i = 0; i < this.list.length; i++)
	{
		var currentGuest = this.list[i];
		if (currentGuest.addedByID != this.userID)
		{
			$(".guest#"+currentGuest.id).addClass("filtered-2");
		}
		else
		{
			$(".guest#"+currentGuest.id).removeClass("filtered-2");
		}
	}
};

/*
 * Party List Class Definition
 */

PartyModule.PartyList = function()
{
	this.lastTimePollTried = 0;
	this.lastTimePollSucceeded = 0;
}

/**
 * Initialize the party list, starting network connections to the Party API
 */
PartyModule.PartyList.prototype.initialize = function()
{
	var thisOuter = this;

	// Send initial "heartbeat" to the server to discover the status of the party.
	$.ajax({
		type: "GET",
	    url: "init/",
	}).done(function( data ) {

		thisOuter.userID = data.userID;
		thisOuter.partyMode = data.partymode;

		thisOuter.finishInitialization();

	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});
};

PartyModule.PartyList.prototype.finishInitialization = function()
{
	var outerThis = this;

	// Initialize guest lists
	this.maleList = new PartyModule.GuestList(this.userID, this.partyMode, "M",
		function() { outerThis.updateCount("M", 1); },
		function() { outerThis.updateCount("M", -1); },
		function() { outerThis.updateListCounts() });

	this.femaleList = new PartyModule.GuestList(this.userID, this.partyMode, "F",
		function() { outerThis.updateCount("F", 1); },
		function() { outerThis.updateCount("F", -1); },
		function() { outerThis.updateListCounts() });

	// Poll server continuously for more information.
	this.maleList.pollServer();
	this.femaleList.pollServer();

	// Setup count listeners if in party mode
	if (this.partyMode)
	{
		$(".add-count").click(function(){
			outerThis.updateCount($(this).attr("id"), 1);
		});

		$(".sub-count").click(function(){
			outerThis.updateCount($(this).attr("id"), -1);
		});

		// Continuously poll for updates to the signed in count
		this.pollCount();
	}
	else
	{
		$("#all-guests").click(function()
		{
			outerThis.maleList.showAllGuests();
			outerThis.femaleList.showAllGuests();

			$(this).parent().addClass("active");
			$("#my-guests").parent().removeClass("active");
		});

		$("#my-guests").click(function()
		{
			outerThis.maleList.showMyGuests();
			outerThis.femaleList.showMyGuests();

			$(this).parent().addClass("active");
			$("#all-guests").parent().removeClass("active");
		});
	}

	// Add guest listeners
	$("#add-male-btn").click(function() {
		var name = $("#add-male-name").val().trim();
		$("#add-male-name").val("");

		if (name.length > 0)
		{
			outerThis.addGuest(name, "M");
		}
	});

	$("#add-male-name").keyup(function(event) {
		if (event.keyCode == 13)
		{
			$("#add-male-btn").click();
		}
	});

	$("#add-female-btn").click(function() {
		var name = $("#add-female-name").val().trim();
		$("#add-female-name").val("");

		if (name.length > 0)
		{
			outerThis.addGuest(name, "F");
		}
	});

	$("#add-female-name").keyup(function(event) {
		if (event.keyCode == 13)
		{
			$("#add-female-btn").click();
		}
	});

	$("#search-btn").click(function() {
		outerThis.filterList($("#search-box").val());
	});

	$("#search-box").keyup(function(event) {
		if (event.keyCode == 13)
		{
			$("#search-btn").click();
		}
	});
};

/**
 * Add a guest to the party list
 */
PartyModule.PartyList.prototype.addGuest = function(guestName, gender)
{
	var thisOuter = this;

	$.ajax({
		type: "POST",
	    url: "create/",
	    data: {
	    	"name": guestName,
	    	"gender": gender,
	    }
	}).done(function( data ) {

		var addedGuest = new PartyModule.Guest(data.id, data.name,
			data.addedByName, data.addedByID, data.signedIn);

		if (gender === "M")
		{
			thisOuter.maleList.addGuest(addedGuest);
			PartyModule.displayMessage("Guest added.");
		}
		else if (gender === "F")
		{
			thisOuter.femaleList.addGuest(addedGuest);
			PartyModule.displayMessage("Guest added.");
		}


	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});
};

/**
 * Polls the server for updates to the party guest count
 */
PartyModule.PartyList.prototype.pollCount = function()
{
	var thisOuter = this;

	$.ajax({
		type: "GET",
	    url: "count/poll/",
	}).done(function( data ) {
		thisOuter.lastTimePollSucceeded = thisOuter.lastTimePollTried;

		$(".count#M").html(data.guycount);
		$(".count#F").html(data.girlcount);
		$(".count#total").html(data.guycount + data.girlcount);

		setTimeout(
			function(){
				thisOuter.pollCount();
			}
			, PartyModule.POLLING_TIMEOUT);
	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});

	this.lastTimePollTried = new Date().getTime();
}

/**
 * Update the guest counts
 */
PartyModule.PartyList.prototype.updateCount = function(gender, delta)
{
	var thisOuter = this;

	$.ajax({
		type: "POST",
	    url: "count/",
	    data: {
	    	"delta": delta,
	    	"gender": gender,
	    }
	}).done(function( data ) {

		// Update counts
		$(".count#M").html(data.guycount);
		$(".count#F").html(data.girlcount);
		$(".count#total").html(data.guycount + data.girlcount);

	}).fail(function( jqXHR, textStatus, errorThrown ) {
		// If failed, we alert the user
		PartyModule.displayError(jqXHR.responseText);
	});
}

PartyModule.PartyList.prototype.updateListCounts = function()
{
	var maleAll = this.maleList.getAllCount();
	var maleMy = this.maleList.getUserCount();

	var femaleAll = this.femaleList.getAllCount();
	var femaleMy = this.femaleList.getUserCount();

	var totalCounts = maleAll + femaleAll;
	var userCounts = maleMy + femaleMy;

	$("#all-guests-count").html(totalCounts);
	$("#my-guests-count").html(userCounts);

	$("#all-male-count").html(maleAll);
	$("#my-male-count").html(maleMy);

	$("#all-female-count").html(femaleAll);
	$("#my-female-count").html(femaleMy);
};

/**
 * Filter the list with the given query
 */
PartyModule.PartyList.prototype.filterList = function(query)
{
	this.maleList.filterList(query);
	this.femaleList.filterList(query);

	$("#search-box").val("");

	if(query.trim().length == 0)
	{
		$("#search-box").attr("placeholder", "Search by Guest or Brother Name");
		$("#search-btn").html("Search");
	}
	else
	{
		$("#search-box").attr("placeholder", "Current Query: " + query);
		$("#search-btn").html("Clear");
	}
};

/**
 * Start the application when the document is ready...
 */
$(document).ready(function(){
	PartyModule.partyList = new PartyModule.PartyList();

	PartyModule.partyList.initialize();
});
