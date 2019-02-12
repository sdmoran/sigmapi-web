
function sortByName(a, b) {
    var strA = a.name.toUpperCase().trim(); // ignore upper and lowercase
    var strB = b.name.toUpperCase().trim(); // ignore upper and lowercase
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

$(document).ready(() =>
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
        updateListCount: {method: 'POST', url: 'partyCount/', emulateJSON: true},
        countsHistory: {method: 'GET', url: 'countHistory/'}
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
        props: ['maleCount', 'femaleCount', 'showColors', 'clickable', 'active'],
        template: "#party-counter-template",
        computed: {
            totalCount: function() {
                return this.maleCount + this.femaleCount;
            },
            totalColor: function() {
                if(this.totalCount > 275)
                    return '#F44336';
                else if(this.totalCount > 250)
                    return '#FBC02D';
                return '#43A047';
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
                this.allowPreparty = false;
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
        template: '#party-checkbox-template',
        watch: {
            value: function(val) {
                this.$emit('input', val);
            }
        }
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

    Vue.component('party-stats', {
        props: ['party', 'guests', 'countHistory'],
        template: "#party-stats-template",
        data: () => ({
            "createdChart": null,
            "countsChart": null,
            "aspectRatio": window.innerWidth < 767 ? 1 : 2
        }),
        computed: {
            createdData: function() {
                let sorted = this.guests
                    .map(g => new Date(g.createdAt))
                    .sort((a,b) => a-b)
                    .map((date, index) => {
                        let time = moment(date);
                        if(time.get('minute') >= 30)
                            time = time.add(1, 'hour');
                        time = time.startOf('hour');
                        return {
                            x: time,
                            y: index+1
                        };
                    });
                let grouped = _.map(
                    _.groupBy(sorted, point => point.x.valueOf()),
                    (counts, time) => ({
                        x: counts[counts.length-1].x,
                        y: counts[counts.length-1].y
                    })
                );
                return grouped;
            },
            ratioText: function() {
                let counts = _.countBy(this.guests, 'gender');
                return this.getRatioText(counts);
            },
            bestBrother: function() {
                let grouped = _.map(
                    _.mapValues(
                        _.groupBy(this.guests, 'addedBy.name'),
                        x => _.mapValues(_.groupBy(x, 'gender'), 'length')
                    ),
                    (counts, brother) => ({
                        ratioText: this.getRatioText(counts),
                        ratio: this.getRatioVal(counts), // Not actually used in the end, keeping just in case
                        totalCount: _.get(counts, 'M', 0) + _.get(counts, 'F', 0),
                        name: brother
                    })
                );
                return _.maxBy(grouped, 'totalCount');
            },
            countsData: function() {
                return this.countHistory.map(entry => ({
                    x: moment(entry.timeStamp),
                    y: (entry.girlCount + entry.guyCount)
                }));
            }
        },
        methods: {
            getAspectRatio: function() {
                return window.innerWidth < 767 ? 1 : 2;
            },
            getRatioText: function(counts) {
                const maleCount = _.get(counts, 'M', 0);
                const femaleCount = _.get(counts, 'F', 0);
                if(maleCount === 0 && femaleCount === 0)
                    return "0 to 0";
                if(maleCount > femaleCount) {
                    if(femaleCount === 0)
                        return "Infinitely Terrible";
                    return `1 to ${Math.floor(maleCount/femaleCount * 10)/10}`;
                } else {
                    if(maleCount === 0)
                        return "Infinitely Good";
                    return `${Math.floor(femaleCount/maleCount * 10)/10} to 1`;
                }
            },
            getRatioVal: function(counts) {
                const maleCount = _.get(counts, 'M', 0);
                const femaleCount = _.get(counts, 'F', 0);
                if(maleCount == 0 && femaleCount == 0)
                    return 0;
                if(maleCount === 0)
                    return Number.MAX_SAFE_INTEGER;
                if(femaleCount == 0)
                    return -1;

                return femaleCount / maleCount;
            },
            makeChart: function(canvasId, title, data) {
                return new Chart(document.getElementById(canvasId).getContext('2d'), {
                    type: 'line',
                    data: {
                        datasets: [{
                            data: data,
                            borderColor: '#3e95cd',
                            fill: false,
                            label: title,
                            lineTension: 0.1,
                        }]
                    },
                    options: {
                        scales: {
                            xAxes: [{
                                type: 'time',
                            }]
                        },
                        legend: {  display: false },
                        tooltips: {
                            callbacks: {
                                title: function(tooltipItem, data) {
                                    return moment(tooltipItem[0].xLabel).format('M/D/YY h:mma');
                                }
                            }
                        },
                        animation: { duration: 0 },
                        aspectRatio: this.getAspectRatio()
                    }
                })
            },
            initCharts: function() {
                if(!this.party.listClosed)
                    this.createdChart = this.makeChart("created-counter", "Guests on the List", this.createdData);
                if(this.party.listClosed)
                    this.countsChart = this.makeChart("live-counts-graph", "Guests Signed In", this.countsData);
            }
        },
        mounted: function() {
            this.initCharts();
        },
        watch: {
            guests() {
                if(!this.party.listClosed) {
                    if(this.createdChart != null) {
                        this.createdChart.data.datasets[0].data = this.createdData;
                        this.createdChart.update();
                    }
                }
            },
            countHistory() {
                if(this.party.listClosed) {
                    if(this.countsChart != null) {
                        this.countsChart.data.datasets[0].data = this.countsData;
                        this.countsChart.update();
                    }
                }
            }
        },
    });



    const app = new Vue({
        el: '#party-app',
        data: {
            party: {
                countHistory: [],
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
            exactFilterMatch: false,
            statsActive: false,
        },
        methods: {
            applyFilter: function(value) {
                this.exactFilterMatch = false;
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
                    if(this.exactFilterMatch) {
                        for(let guest of this.guests) {
                            if(this.guestFilter == null ||
                                guest.addedBy.name === this.guestFilter)
                            {
                                this.$set(guest, 'hide', false);
                            }
                            else
                            {
                                this.$set(guest, 'hide', true);
                            }
                        }
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
            },
            toggleStats() {
                this.statsActive = !this.statsActive;
            },
            toggleMyFilter() {
                if(this.guestFilter === userFullName)
                    this.clearFilter();
                else {
                    this.applyFilter(userFullName);
                    this.exactFilterMatch = true;
                }
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
            },
            myMaleGuests: function() {
                return this.maleGuests
                    .filter(guest => guest.addedBy.username === userName);
            },
            myFemaleGuests: function() {
                return this.femaleGuests
                    .filter(guest => guest.addedBy.username === userName);
            },
            userFullName: function() {
                return userFullName;
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
            },
            exactFilterMatch() {
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
                setTimeout(pollFunc, pollTime);
        }, errorReason => {
            setTimeout(pollFunc, pollTime * 10);
        });
    };

    loadAllData().then(() => {
        console.log("Begin Polling");
        setTimeout(pollFunc, pollTime);
    });
});
