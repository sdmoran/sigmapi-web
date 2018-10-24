
class PartyList
{
    constructor()
    {
        this.initHandlebarsTemplates();

        this.genderCodes = {
            "M": "male",
            "F": "female",
            "male": "M",
            "female": "F"
        };

        // Keep a reference to some commonly used elements
        this.addGuestContainers = j3(".add-guest-form");

        this.addMaleField = j3("#add-name-male");
        this.addFemaleField = j3("#add-name-female");

        this.malePrepartyCheckbox = j3("#preparty-checkbox-male");
        this.femalePrepartyCheckbox = j3("#preparty-checkbox-female");
        this.prepartyContainers = j3(".preparty-container");

        this.maleBrothersDropdown = j3("#brothers-dropdown-male");
        this.femaleBrothersDropdown = j3("#brothers-dropdown-female");
        this.brothersDropdowns = this.maleBrothersDropdown.add(this.femaleBrothersDropdown);

        this.searchButton =  j3("#search-btn");
        this.searchBox =  j3("#search-box");

        this.initListeners();
        this.refreshList()
    }

    initHandlebarsTemplates()
    {
        let source = j3("#party-list-template").html();
        let template = Handlebars.compile(source);
        let maleContext = {title: "Male", name: "male", code: "M"};
        let femaleContext = {title: "Female", name: "female", code: "F"};

        // Renders the male and female columns (including the add forms)
        j3("#guests-container > .row")
            .append(template(maleContext))
            .append(template(femaleContext));
    }

    initListeners()
    {
        // Listeners for adding new guests
        this.addMaleField.keypress(e => {if (e.which === 13) this.addMale();});
        j3("#add-btn-male").click(() => {this.addMale()});
        this.addFemaleField.keypress(e => {if (e.which === 13) this.addFemale();});
        j3("#add-btn-female").click(() => {this.addFemale()});

        this.searchBox.keypress(e => {
            if (e.which === 13)
                this.filterGuests();
            else
            {
                if(j3.trim(j3(this.searchBox).val()) !== "")
                    this.searchButton.text("Search");
                else
                    this.searchBox.attr("placeholder", "Search by Guest or Brother Name");
            }
        });
        this.searchButton.click(() => {
            this.filterGuests();
        });
    }

    filterGuests()
    {
        let rawQuery = j3.trim(this.searchBox.val());
        let query = rawQuery.toLowerCase();

        // If the search query is being cleared
        if(query === "")
        {
            this.searchButton.text("Search");
            this.searchBox.attr("placeholder", "Search by Guest or Brother Name");
            j3(".guest-list .guest").show();
        }
        else
        {
            this.searchButton.text("Clear");
            this.searchBox.val("").attr("placeholder", `Current Search: ${rawQuery}`);

            // Filter the guest list
            j3(".guest-list .guest")
                .show()
                .filter(function() //Return true if the names don't match
                {
                    let name = j3(this).children(".name").text().toLowerCase();
                    let addedBy = j3(this).children(".details").text().toLowerCase();

                    return !(PartyList.nameQueryMatches(name, query) || PartyList.nameQueryMatches(addedBy, query));

                }).hide();
        }
    }

    refreshList()
    {
        j3.ajax({
            type: "GET",
            url: "all/",
        }).done((data, textStatus, xhr) => {
            this.listLoaded(data)
        }).fail((xhr, textStatus, errorThrown) => {
            console.log(xhr.status + ": " + xhr.responseText);
        });
    }

    listLoaded(data)
    {
        console.log("Data Received", data);

        this.userID = data.user_id;
        this.partyMode = data.party_mode;
        this.prepartyMode = data.preparty_mode;
        this.canRemoveAnyGuest = data.can_remove_any_guest;
        this.restrictedGuests = data.restricted_guests;
        this.minLevenshteinDist = data.min_levenshtein_dist;
        this.doorAccess = data.you_have_door_access;

        if(data.can_add_party_guests)
            this.addGuestContainers.show();

        j3("#guest-list-M").empty();
        j3("#guest-list-F").empty();

        if((data.party_mode || data.preparty_mode))
        {
            if(data.you_have_door_access)
            {
                this.brothersDropdowns.parent().show();
            }
        }
        else if(data.has_party_invite_limits || data.has_preparty_invite_limits)
        {
            this.brothersDropdowns.parent().show();
            this.brothersDropdowns.children("option:first-child").text("(Borrow an Invite)");

            if(data.has_preparty_invite_limits)
            {
                this.prepartyContainers.show();
            }
        }

        let totalMales = 0, totalFemales = 0;
        for(let guest of data.guests)
        {
            let adding = new PartyGuest(guest, this);
            adding.setRestrictedSimilarity(this.checkRestrictedList(adding.name));
            adding.renderTemplate("#guest-list-" + guest.gender);

            if(adding.gender === "M")
                totalMales++;
            else
                totalFemales++;
        }

        ListCounterManager.refreshCounters(this.listClosed);
        ListCounterManager.updateCounts(totalMales, totalFemales,
            data.guy_count, data.girl_count,
            data.guys_ever_signed_in, data.girls_ever_signed_in);

        j3("#party-footer").slideDown();

        // Hide the loading circles
        j3(".loader").hide();
    }

    get listClosed()
    {
        return (this.partyMode || this.prepartyMode);
    }

    canRemoveGuest(addedByID)
    {
        return (this.userID === addedByID || this.canRemoveAnyGuest);
    }

    addMale()
    {
        this.addGuest(
            this.addMaleField.val(),
            "M",
            this.malePrepartyCheckbox.is(":checked"),
            this.maleBrothersDropdown.val(),
            () => {
                this.addMaleField.val("");
                this.malePrepartyCheckbox.prop("checked", false);
                this.maleBrothersDropdown.val("");
            }
        );
    }

    addFemale()
    {
        this.addGuest(
            this.addFemaleField.val(),
            "F",
            this.femalePrepartyCheckbox.is(":checked"),
            this.femaleBrothersDropdown.val(),
            () => {
                this.addFemaleField.val("");
                this.femalePrepartyCheckbox.prop("checked", false);
                this.femaleBrothersDropdown.val("");
            }
        );
    }

    addGuest(name, gender, prepartyAccess, selectedBrother, onSuccess)
    {
        // Creating a variable out of the function so we can first check if the guest
        // is on the blacklist / graylist (below)
        let actualAdd = () =>
        {
            let data = {
                "name": name,
                "gender": gender,
                "prepartyAccess": prepartyAccess,
                "selectedBrother": selectedBrother,
                "forceAdd": "false"
            };

            console.log("Sending: ", data);

            j3.ajax({
                type: "POST",
                url: "create/",
                data: data
            }).done((data, textStatus, xhr) => {

                console.log(textStatus);
                console.log(data);

                let newGuest = new PartyGuest(data, this);
                newGuest.setRestrictedSimilarity(this.checkRestrictedList(newGuest.name));

                let container = j3("#party-column-" + this.genderCodes[data.gender]);

                let added = false;
                // Add the new guest to the list in the correct alphabetical spot
                if(container.find(".guest").length)
                {
                    container.find(".guest").each(function()
                    {
                        if(j3(this).find(".name").text().toLowerCase() > data.name.toLowerCase())
                        {
                            j3(this).before(newGuest.renderTemplate());
                            added = true;
                            return false;
                        }
                    });
                }
                if(!added)
                {
                    newGuest.renderTemplate(container.children(".guest-list"));
                }

                newGuest.refreshListeners();

                onSuccess();

            }).fail((xhr, textStatus, errorThrown) => {
                modal(xhr.responseText, "Close");
                console.log(xhr.status, xhr.responseText);
            });
        };


        // Check if the guest is on one of the restricted lists
        let restrictedGuest = this.checkRestrictedList(name);
        if(restrictedGuest != null)
        {
            let phrases = ["Blacklist", "blacklisted", "Blacklisted"];
            if(restrictedGuest.graylisted)
                phrases = ["Graylist", "graylisted", "Graylisted"];
            let message = `The guest you are trying to add looks similar to this ${phrases[1]} guest:<br><br>` +
                `${phrases[2]} Guest: <strong>${restrictedGuest.name}</strong><br>` +
                `Your Guest: ${name}<br><br>` +
                `Would you still like to add this guest to the list?`;
            modal(message, "Cancel", ()=>{}, "Add Anyway", actualAdd, phrases[0] + " Warning");
        }
        else
            actualAdd();

    }

    checkRestrictedList(newName)
    {
        for(let guest of this.restrictedGuests)
        {
            let dist = Levenshtein.get(newName.toLowerCase(), guest.name.toLowerCase());
            if(dist <= this.minLevenshteinDist)
                return guest;
        }
        return null;
    }

    /**
     * Perform a word-by-word search of a query typed in the search box
     */
    static nameQueryMatches(name, query)
    {
        if(name.includes(query))
            return true;

        let split = name.split(" ");
        for(let piece of split)
        {
            if(Levenshtein.get(piece, query) <= 1)
                return true;
        }

        return false;
    }
}


class PartyGuest
{
    constructor(jsonGuest, partyList)
    {
        this.jsonGuest = jsonGuest;
        this.partyList = partyList;

        if(!jsonGuest.everSignedIn)
            jsonGuest.timeFirstSignedIn = "";
    }

    get id()
    {
        return this.jsonGuest.id;
    }

    get name()
    {
        return this.jsonGuest.name;
    }

    get gender()
    {
        return this.jsonGuest.gender;
    }

    get signedIn()
    {
        return this.jsonGuest.signedIn;
    }

    set signedIn(signedIn)
    {
        this.jsonGuest.signedIn = signedIn;
        this.refreshCheck();
    }

    refreshCheck()
    {
        if(this.signedIn)
            j3(this.containerID).find('.checked-in').removeClass('hidden');
        else
            j3(this.containerID).find('.checked-in').addClass('hidden');
    }

    toggleSignedIn()
    {
        const endpoint = this.signedIn ? 'signOut' : 'signIn';
        j3.ajax({
            type: "POST",
            url: `${endpoint}/${this.id}/`
        }).done((data, textStatus, xhr) => {
            this.signedIn = !this.signedIn;
        }).fail((xhr, textStatus, errorThrown) => {
            modal(xhr.responseText, "Close");
            console.log(xhr.status, xhr.responseText);
        });
    }

    get containerID()
    {
        return "#guest-template-" + this.jsonGuest.id;
    }

    setRestrictedSimilarity(guest)
    {
        this.restrictedSimilarity = guest;
    }

    get isSimilarToRestrictedGuest()
    {
        return typeof(this.restrictedSimilarity) !== 'undefined'
            && this.restrictedSimilarity != null;
    }

    renderTemplate(container)
    {
        PartyGuest.initHandlebars();

        let context = {
            id: this.jsonGuest.id,
            guestName: this.jsonGuest.name,
            gender: this.jsonGuest.gender,
            signedIn: this.jsonGuest.signedIn,
            timeFirstSignedIn: this.jsonGuest.timeFirstSignedIn,
            addedBy: this.jsonGuest.addedBy.name,
            inviteUsed: this.jsonGuest.inviteUsed,
            canRemove: this.partyList.canRemoveGuest(this.jsonGuest.addedBy.id),
            partyMode: this.partyList.listClosed,
            prepartyAccess: this.jsonGuest.prepartyAccess,
            restrictionWarning: this.isSimilarToRestrictedGuest
        };

        let html = PartyGuest.template(context);

        j3(container).append(html);

        this.refreshListeners();
        this.refreshCheck();

        if(this.partyList.doorAccess && this.partyList.listClosed)
        {
            j3(this.containerID).addClass('pointer');
        }

        return html;
    }

    refreshListeners()
    {
        let j3Template = j3(this.containerID);

        if(this.jsonGuest.inviteUsed !== null)
        {
            // Tooltip library is attached to the old jQuery, so have to use $ here
            $(this.containerID + ">.added-by-info").tooltip();
            j3Template.children(".added-by-info").click((e) => {
                e.stopPropagation();
            })
        }

        if(!(this.partyList.partyMode || this.partyList.prepartyMode))
        {
            j3Template.children(".remove-guest")
                .off("click").on("click", () => this.destroySelf());
        }
        else
        {
            j3Template.click(() =>
            {
                this.toggleSignedIn();
            });
        }

        if(this.isSimilarToRestrictedGuest)
        {
            j3Template.children(".restriction-warning")
                .click(() => {this.showRestrictedSimilarityModal();});
        }
    }

    showRestrictedSimilarityModal()
    {
        let phrases = ["Blacklist", "blacklisted", "Blacklisted"];
        if(this.restrictedSimilarity.graylisted)
            phrases = ["Graylist", "graylisted", "Graylisted"];

        let message = `This guest looks similar to this ${phrases[1]} guest:<br><br>` +
            `${phrases[2]} Guest: <strong>${this.restrictedSimilarity.name}</strong><br>` +
            `This Guest: ${this.name}<br>`;

        modal(message, "Close", null, null, null, `${phrases[0]} Warning`)
    }

    destroySelf()
    {
        j3.ajax({
            type: "DELETE",
            url: "destroy/" + this.jsonGuest.id,
        }).done((data, textStatus, xhr) => {

            console.log(textStatus);
            console.log(data);

            j3("#guest-template-" + this.jsonGuest.id + ">.remove-guest").off();
            j3("#guest-template-" + this.jsonGuest.id).remove();

        }).fail((xhr, textStatus, errorThrown) => {
            modal(xhr.responseText, "Close");
            console.log(xhr.status, xhr.responseText);
        });
    }

    static initHandlebars()
    {
        if(typeof PartyGuest.template === 'undefined')
        {
            console.log("Compiling PartyGuest Template");
            let source = j3("#party-guest-template").html();
            PartyGuest.template = Handlebars.compile(source);
        }
    }
}


// Helper class that creates the list counters and
// manages their AJAX updates
class ListCounterManager
{
    /**
     * Call this to initialize the party counters, or when the party
     * changes modes in order to show the extra counters
     * @param listClosed True if the list is closed (party mode)
     */
    static refreshCounters(listClosed)
    {
        this.listClosed = listClosed;

        // If the list is closed, we can show the extra counters
        if(listClosed)
        {
            if(this.checkedIn === undefined)
            {
                this.checkedIn = new ListCounter("checked-in-counter", "In the Party");
                this.checkedIn.render("#footer-counters");
            }
            if(this.everCheckedIn === undefined)
            {
                this.everCheckedIn = new ListCounter("ever-checked-in-counter", "Ever Checked In");
                this.everCheckedIn.render("#footer-counters");
            }
        }
        else
        {
            // This would only happen in rare cases where the party is edited
            // after it started to be a later date, and someone still had
            // the page open

            if(this.checkedIn !== undefined)
                this.checkedIn.remove();
            if(this.everCheckedIn !== undefined)
                this.everCheckedIn.remove();
        }

        if(this.allGuests === undefined)
        {
            this.allGuests = new ListCounter("all-guests-counter", "On the List");
            this.allGuests.render("#footer-counters");
        }
    }

    static updateCounts(maleTotal, femaleTotal, maleCheckedIn=0, femaleCheckedIn=0,
                        malesEverCheckedIn=0, femalesEverCheckedIn=0)
    {
        if(this.listClosed)
        {
            this.checkedIn.updateCounts(maleCheckedIn, femaleCheckedIn);
            this.everCheckedIn.updateCounts(malesEverCheckedIn, femalesEverCheckedIn);
        }

        this.allGuests.updateCounts(maleTotal, femaleTotal);
    }
}

// Class representing a single list counter widget, found
// in the bottom navigation (ex. Total in party, Total on list, etc)
class ListCounter
{
    constructor(id, title)
    {
        this.id = id;
        this.title = title;
        this.maleCount = 0;
        this.femaleCount = 0;
    }

    render(containerSelector)
    {
        let source = j3("#party-counter-template").html();
        let template = Handlebars.compile(source);
        let listContext = {
            id: this.id,
            title: this.title,
        };
        let html = template(listContext);

        if(containerSelector !== null)
            j3(containerSelector).append(html);

        return html;
    }

    updateCounts(maleCount, femaleCount)
    {
        this.updateMaleCont(maleCount);
        this.updateFemaleCount(femaleCount);
    }

    updateMaleCont(count)
    {
        this.maleCount = count;
        j3(`#${this.id}`).find(".counter-male").text(this.maleCount);
        this.animateCounter("bubble-male");
        this._updateTotalCount();
    }

    updateFemaleCount(count)
    {
        this.femaleCount = count;
        j3(`#${this.id}`).find(".counter-female").text(this.femaleCount);
        this.animateCounter("bubble-female");
        this._updateTotalCount();
    }

    _updateTotalCount()
    {
        let total = this.femaleCount + this.maleCount;
        j3(`#${this.id}`).find(".counter-total").text(total);
        this.animateCounter("bubble-total");
    }

    animateCounter(bubbleClass)
    {
        let bubble = j3(`#${this.id}`)
            .find(`.${bubbleClass}`)
            .addClass("highlight");
        setTimeout(() => {bubble.removeClass("highlight")}, 250);
    }

    remove()
    {
        j3(`#${this.id}`).remove();
    }
}

function modal(message, primaryButtonText, primaryButtonListener=null,
               secondaryButtonText=null, secondaryButtonListener=null, title=null)
{
    let modal = $("#message-modal");

    if(title == null)
        modal.find(".modal-header").hide();
    else
    {
        modal.find(".modal-header")
            .show()
            .find("h4")
            .text(title);
    }

    j3("#modal-message").html(message);

    j3("#modal-btn-primary")
        .text(primaryButtonText)
        .show()
        .off('click').on('click', () =>
    {
        if(primaryButtonListener !== null)
            primaryButtonListener();
        modal.modal("hide");
    });

    if(secondaryButtonText !== null)
    {
        j3("#modal-btn-secondary")
            .text(secondaryButtonText)
            .show()
            .off('click').on('click', () =>
        {
            if(secondaryButtonListener !== null)
                secondaryButtonListener();
            modal.modal("hide");
        });
    }
    else
    {
        j3("#modal-btn-secondary").hide().off('click');
    }

    modal.modal();
}

function sortByName(a, b) {
    var strA = a.name.toUpperCase(); // ignore upper and lowercase
    var strB = b.name.toUpperCase(); // ignore upper and lowercase
    if (strA < strB) {
        return -1;
    }
    if (strA > strB) {
        return 1;
    }
    // names must be equal
    return 0;
}

function checkRestricted(name, party)
{
    for(let guest of party.restrictedGuests)
    {
        let dist = Levenshtein.get(name.toLowerCase(), guest.name.toLowerCase());
        if(dist <= party.minLevenshteinDist)
            return guest;
    }
    return null;
}

let _disablePollingFlag = false;
const disablePolling = () => {_disablePollingFlag = true};
const enablePolling = () => {_disablePollingFlag = false};

j3(document).ready(() =>
{
    //partyId is a global set in the template by django
    Vue.http.options.root = `/secure/parties/api/${partyId}`;
    Vue.http.interceptors.push(request => {
        if(!csrfSafeMethod(request.method)) {
            request.headers.set('X-CSRFToken', getCookie('csrftoken'))
        }
    });

    const guestResource = Vue.resource('guests{/id}/', {}, {
        signIn: {method: 'POST', url: 'guests/signIn{/id}/'},
        signOut: {method: 'POST', url: 'guests/signOut{/id}/'},
        add: {method: 'POST', url: 'guests/create/', emulateJSON: true},
        destroy: {method: 'DELETE', url: 'guests/destroy{/id}/'}
    });

    const partyResource = Vue.resource('', {}, {
        details: {method: 'GET', url: 'details/'},
        pulse: {method: 'GET', url: 'pulse/'},
        guests: {method: 'GET', url: 'guests/'},
        deltaGuests: {method: 'GET', url: 'guests/delta{/updateCounter}/'},
        permissions: {method: 'GET', url: 'permissions/'},
        restrictedGuests: {method: 'GET', url: 'restricted/'},
        updateListCount: {method: 'POST', url: 'partyCount/', emulateJSON: true}
    });

    const modalErrorFunc = function(response) {
        this.$root.$emit('modal', {
            title: response.statusText,
            message: response.bodyText,
            primaryText: "Ok",
            primaryAction: null
        });
    };
    const guestUpdateFunc = function(response){
        this.$root.$emit('guest-update', response.body);
    };

    Vue.component('party-guest', {
        props: ['guest', 'party'],
        template: "#party-guest-template",
        data: () => ({ modal: null }),
        computed: {
            canRemove: function() {
                return !this.party.listClosed && (this.guest.addedBy.id === userId ||
                    this.party.permissions.canRemoveAnyGuest);
            },
            doorAccess: function() {
                return this.party.permissions.youHaveDoorAccess;
            },
            canCheckIn: function() {
                return this.doorAccess && this.party.listClosed;
            },
            restrictedSimilarity: function() {
                return checkRestricted(this.guest.name, this.party);
            }
        },
        methods: {
            toggleSignedIn: function() {
                if(this.canCheckIn) {
                    const resourceFunc = this.guest.signedIn? guestResource.signOut : guestResource.signIn;
                    resourceFunc({id: this.guest.id}, {})
                        .then(guestUpdateFunc.bind(this))
                        .catch(modalErrorFunc.bind(this));
                }
            },
            destroy: function() {
                if(this.canRemove) {
                    guestResource.destroy({id: this.guest.id}, {}).then(response => {
                        this.$root.$emit('guest-destroy', this.guest);
                    }).catch(modalErrorFunc.bind(this));
                }
            },
            showRestrictedModal: function(event) {
                event.stopPropagation();

                let phrases = ["Blacklist", "blacklisted", "Blacklisted"];
                if(this.restrictedSimilarity.graylisted)
                    phrases = ["Graylist", "graylisted", "Graylisted"];

                let message = `This guest looks similar to this ${phrases[1]} guest:<br><br>` +
                    `${phrases[2]} Guest: <strong>${this.restrictedSimilarity.name}</strong><br>` +
                    `This Guest: ${this.guest.name}<br>`;

                this.$root.$emit('modal', {
                    title: `${phrases[0]} Warning`,
                    message,
                    primaryText: "Ok"
                });
            }
        }
    });

    Vue.component('party-counter', {
        props: ['maleCount', 'femaleCount'],
        template: "#party-counter-template",
        computed: {
            totalCount: function() {
                return this.maleCount + this.femaleCount;
            }
        }
    });

    Vue.component('party-column', {
        props: ['guests', 'party', 'title', 'name', 'code'],
        template: "#party-column-template",
        data: function() {
            return {
                newGuestName: "",
                selectedBrother: "",
                allowPreparty: false,
                modal: null,
                riskApproval: false,
            };
        },
        computed: {
            showAddBox: function() {
                return (this.party.permissions.canAddPartyGuests && !this.party.listClosed) ||
                    this.party.permissions.youHaveDoorAccess;
            },
            showPrepartyCheckbox: function() {
                return this.party.hasPrepartyInviteLimits && !this.party.listClosed;
            },
            showBrothers: function() {
                return (this.party.listClosed && this.party.permissions.youHaveDoorAccess) ||
                    (!this.party.listClosed && (this.party.hasPartyInviteLimits || this.party.hasPrepartyInviteLimits));
            },
            dropdownTitle: function() {
                return this.party.listClosed ? "(Select Voucher)" : "(Borrow an invite)";
            }
        },
        methods: {
            clear: function() {
                this.newGuestName = "";
                this.selectedBrother = "";
                this.riskApproval = false;
                this.prepartyAccess = false;
            },
            addGuest: function() {

                let actualAdd = function()
                {
                    let data = {
                        "name": this.newGuestName,
                        "gender": this.code,
                        "prepartyAccess": this.allowPreparty,
                        "selectedBrother": this.selectedBrother,
                        "riskApproval": this.riskApproval
                    };

                    guestResource.add(data).then((response) => {
                        this.$root.$emit('guest-update', response.body);

                        const signThemIn = () => {
                            guestResource.signIn({id: response.body.id}, {})
                                .then(guestUpdateFunc.bind(this))
                                .catch(modalErrorFunc.bind(this));
                        };

                        if(this.party.listClosed) {
                            this.$root.$emit('modal', {
                                title: `Sign them in?`,
                                message: `Would you like to sign in ${this.newGuestName} now?`,
                                primaryText: "Yes",
                                primaryAction: signThemIn,
                                secondaryText: "No"
                            });
                        }

                        this.clear();

                    }).catch(modalErrorFunc.bind(this));
                };
                actualAdd = actualAdd.bind(this);


                // Check if the guest is on one of the restricted lists
                let restrictedGuest = checkRestricted(this.newGuestName, this.party);
                if(restrictedGuest != null)
                {
                    this.showRestrictedModal(restrictedGuest, actualAdd);
                }
                else
                    actualAdd();
            },
            showRestrictedModal: function(restrictedGuest, addAnyway) {
                let phrases = restrictedGuest.graylisted ?["Graylist", "graylisted", "Graylisted"] :
                    ["Blacklist", "blacklisted", "Blacklisted"];

                let message = `The guest you are trying to add looks similar to this ${phrases[1]} guest:<br><br>` +
                    `${phrases[2]} Guest: <strong>${restrictedGuest.name}</strong><br>` +
                    `Your Guest: ${name}<br><br>` +
                    `Would you still like to add this guest to the list?`;

                this.$root.$emit('modal', {
                    title: `${phrases[0]} Warning`,
                    message,
                    primaryText: "Cancel",
                    primaryAction: () => {
                        this.clear();
                    },
                    secondaryText: "Add Anyway",
                    secondaryAction: addAnyway
                })
            }
        }
    });

    Vue.component('party-modal', {
        props: ['data'],
        template: "#party-modal-template"
    });

    Vue.component('party-checkbox', {
        props: ['value', 'name'],
        template: '#party-checkbox-template'
    });

    Vue.component('party-searchbox', {
        props: ['appliedFilter'],
        template: '#party-searchbox-template',
        data: () => ({ filterText: ""}),
        methods: {
            applyFilter: function() {
                if(!this.searchDisabled) {
                    if(this.clearMode)
                        this.$emit('clear-filter');
                    else {
                        this.$emit('apply-filter', this.filterText);
                        this.filterText = "";
                    }
                }
            },
            clearFilter: function() {
                this.appliedFilter = null;
                this.filterText = "";
            },
        },
        computed: {
            searchButtonText: function() {
                return this.clearMode? "Clear" : "Search";
            },
            searchDisabled: function() {
                return (this.appliedFilter == null && this.filterText === "") ||
                    this.appliedFilter === this.filterText;
            },
            placeholderText: function() {
                if(this.appliedFilter == null)
                    return "Search by Guest or Brother Name";
                else
                    return `Current Search: '${this.appliedFilter}'`;
            },
            clearMode: function() {
                if(this.searchDisabled)
                    return false;
                return !(this.appliedFilder == null &&
                    this.filterText !== "" &&
                    this.filterText !== this.appliedFilter);
            }
        }
    });



    const app = new Vue({
        el: '#party-app',
        data: {
            party: {
                permissions: [],
                restrictedGuests: [],
                loadingGuests: true,
                listClosed: null,
                partyMode: null,
                perpartyMode: null,
                girlCount: 0,
                guyCount: 0,
                girlsEverSignedIn: 0,
                guysEverSignedIn: 0,
                hasPrepartyInviteLimits: null,
                hasPartyInviteLimits: null,
            },
            guests: [],
            modal: null,
            guestFilter: null,
            restrictedFilter: false,
        },
        methods: {
            applyFilter: function(value) {
                this.restrictedFilter = false;
                this.guestFilter = value;
            },
            clearFilter: function() {
                this.guestFilter = null;
            },
            wordMatch: function(text, query, tolerance) {
                if(typeof(text) !== 'string') return false;
                text = text.toLowerCase();
                query = query.toLowerCase();

                if(text.includes(query)) return true;

                let split = text.split(" ");
                const querySplit = query.split(" ");
                for(let textPiece of split)
                {
                    if(Levenshtein.get(textPiece, query) <= tolerance)
                        return true;
                    for(let queryPiece of querySplit) {
                        if(Levenshtein.get(textPiece, queryPiece) <= tolerance)
                            return true;
                    }
                }
                return false;
            },
            refreshGuestFilters: function() {
                let amountShowing = 0;
                if(this.restrictedFilter) {
                    for(let guest of this.guests) {
                        if(checkRestricted(guest.name, this.party))
                            this.$set(guest, 'hide', false);
                        else
                            this.$set(guest, 'hide', true);
                    }
                    this.guestFilter = null;
                }
                else {
                    for(let i = 1; i < 8; i++) {
                        for(let guest of this.guests) {
                            if(this.guestFilter == null ||
                                this.wordMatch(guest.name, this.guestFilter, i) ||
                                this.wordMatch(guest.addedBy.name, this.guestFilter, i) ||
                                this.wordMatch(guest.inviteUsed, this.guestFilter, i))
                            {
                                this.$set(guest, 'hide', false);
                                amountShowing++;
                            }
                            else
                            {
                                this.$set(guest, 'hide', true);
                            }
                        }

                        if(amountShowing > 0)
                            break;
                    }
                }
            },
            modListCount: function(gender, sign) {
                const data = { gender, sign };
                partyResource.updateListCount(data).then(response => {
                    Object.assign(app.party, response.body.party);
                }).catch(modalErrorFunc.bind(this));
            },
            toggleRestrictedOnly: function() {
                this.restrictedFilter = !this.restrictedFilter;
            }
        },
        computed: {
            maleGuests: function() {
                return this.guests
                    .filter(guest => guest.gender === "M")
                    .sort(sortByName);
            },
            femaleGuests: function() {
                return this.guests
                    .filter(guest => guest.gender === "F")
                    .sort(sortByName);
            }
        },
        mounted: function() {
            this.$root.$on('guest-update', function(updated) {
                const index = this.guests.findIndex((guest) => {
                    return guest.id === updated.id;
                });
                if(index !== -1)
                    this.$set(this.guests, index, updated);
                else
                    this.guests.push(updated);
            });
            this.$root.$on('guest-destroy', function(destroyed) {
                this.guests = this.guests.filter(guest => {
                    return guest.id !== destroyed.id;
                });
            });
            this.$root.$on('modal', function(data) {
                this.modal = data;
            });
        },
        watch: {
            restrictedFilter() {
                this.refreshGuestFilters();
            },
            guestFilter() {
                this.refreshGuestFilters();
            },
            guests() {
                this.refreshGuestFilters();
            }
        }
    });

    const loadAllData = () => {
        return Promise.all([
            partyResource.details().then(response => {
                Object.assign(app.party, response.body.party);
            }),
            partyResource.guests().then(response => {
                app.party.loadingGuests = false;
                app.guests = response.body.guests;
            }),
            partyResource.permissions().then(response => {
                app.party.permissions = response.body.permissions;
            }),
            partyResource.restrictedGuests().then(response => {
                app.party.restrictedGuests = response.body.restrictedGuests;
            }),
        ]);
    };

    const pollTime = 1000;
    const pollFunc = () => {
        if(_disablePollingFlag) {
            setTimeout(pollFunc, pollTime);
            return;
        }

        partyResource.pulse().then(response => {
            // If timestamp of last update is different
            if(response.body.lastUpdated !== app.party.lastUpdated ||
                response.body.listClosed !== app.party.listClosed
            ) {
                let promises = [
                    partyResource.details().then(response => {
                        Object.assign(app.party, response.body.party);
                    })
                ];

                // If a guest was modified or added, grab any new additions from the server
                // (updateCounter is an index of the last change we knew about)
                if(response.body.guestUpdateCounter !== app.party.guestUpdateCounter) {
                    promises.push(
                        partyResource.deltaGuests({updateCounter: app.party.guestUpdateCounter}, {}).then(response => {
                            // Add and update guests that have changed
                            for(const updateGuest of response.body.guests) {
                                const index = app.guests.findIndex(g => g.id === updateGuest.id);
                                if(index === -1)
                                    app.guests.push(updateGuest);
                                else
                                    Vue.set(app.guests, index, updateGuest);
                            }

                            // Filter any guest that have been removed
                            app.guests = app.guests.filter(guest => {
                                return response.body.guestIds.includes(guest.id)
                            });
                        })
                    );
                }
                Promise.all(promises).then(() => {
                    setTimeout(pollFunc, pollTime);
                });
            }
            else
                setTimeout(pollFunc, pollTime)
        });
    };

    loadAllData().then(() => {
        console.log("Begin Polling");
        setTimeout(pollFunc, pollTime);
    });
});
