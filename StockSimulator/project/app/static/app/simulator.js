let events = [];

document.addEventListener('DOMContentLoaded', () => {

    // Add onclick handlers to buttons
    document.getElementById("add-event-btn").onclick = () => addEvent();

    let simulation_btn = document.getElementById("start-simulation-btn");
    if (simulation_btn !== null) {
        simulation_btn.onclick = () => runSimulation();
    }
});


// Creates a row on the table that shows simulation results
function createTableRow(index, title, totalValue, tb, date) {

    // Gets the variables on the table row
    let value = totalValue[index];
    let last30 = (((value / totalValue[index - 1]) - 1) * 100).toFixed(2);
    let alltime = (((value / totalValue[0]) - 1) * 100).toFixed(2);

    // Adds the row to the table body
    tb.innerHTML += (`
    <tr class='text-center'>
        <th scope="row">${title}</th>
        <td>${date.toLocaleDateString()}</td>
        <td>${value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2, style: 'currency', currency: 'USD'})}</td>
        ${title === "Total" ? "<td>-</td>" : (last30 < 0 ? "<td class='text-danger'>" + last30.toString() + "%</td>" : "<td class='text-success'>+" + last30.toString() + "%</td>")}
        ${alltime < 0 ? "<td class='text-danger'>" + alltime.toString() + "%</td>" : "<td class='text-success'>+" + alltime.toString() + "%</td>"}
    </tr>
    `);
}


// Populates the tab with the charts and tables for events and without events
function populateTab(prefix, prices_with_events, prices_without_events, totalValueEvents, totalValue) {

    // Creates the linecharts for the stock
    createLinechart(`${prefix}-tab-events-pane-linechart`, prices_with_events, "Simulation Results with Events");
    createLinechart(`${prefix}-tab-pane-linechart`, prices_without_events, "Simulation Results without Events");

    // Get the date and the time interval for a 30 day period
    let date = Date.now();
    let interval = 30 * 24 * 3600 * 1000;

    // Populates the tables for the stock
    let tbEvents = document.getElementById(`${prefix}-tab-events-pane-table`);
    let tb = document.getElementById(`${prefix}-tab-pane-table`);

    // Loops over twelve 30 day intervals
    for (let i=1; i <= 12; i++) {
        let currentDate = new Date(date + (i * interval));
        createTableRow(i, i, totalValueEvents, tbEvents, currentDate);
        createTableRow(i, i, totalValue, tb, currentDate);
    }

    // Adds the total at the end of the table
    finalDate = new Date(date + (365 * 24 * 3600 * 1000));
    createTableRow(13, "Total", totalValueEvents, tbEvents, finalDate);
    createTableRow(13, "Total", totalValue, tb, finalDate);
}


// Runs the simulation
function runSimulation() {
    document.getElementById("start-simulation-btn").className += " disabled";
    document.getElementById("add-event-btn").className += " disabled";
    fetch('/simulation', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            events: events
        })
    })
    .then(response => response.json())
    .then(result => {
        
        // Retrieves the elements and templates for the tabs and tab panes which show results
        document.getElementById("simulation-results").hidden = false;
        let tabTemplate = document.getElementById("template-dropdown");
        let tabPaneEventsTemplate = document.getElementById("template-tab-events-pane");
        let tabPaneTemplate = document.getElementById("template-tab-pane");
        let tabsList = document.getElementById("simulation-tabs");
        let tabsContentList = document.getElementById("simulation-tabs-content");

        // Initialises variables for the portfolio tab
        let data = result.data;
        let totalPricesEvents = new Array(365).fill(0);
        let totalPrices = new Array(365).fill(0);
        let totalValueEvents = new Array(14).fill(0);
        let totalValue = new Array(14).fill(0);

        // Adds all stock data together for the portfolio tab
        Object.keys(result.data).forEach(id => {
            // Adds all the prices for different stocks together
            for (let i=0; i < 365; i++) {
                totalPricesEvents[i] += data[id].prices_with_events[i];
                totalPrices[i] += data[id].prices_without_events[i];
            }

            // Finds the total value of the portfolio at 30 day intervals
            totalValueEvents[0] += data[id].prices_with_events[0] * data[id].units_owned;
            totalValue[0] += data[id].prices_without_events[0] * data[id].units_owned;

            for (let i=1; i <= 12; i++) {
                totalValueEvents[i] += data[id].prices_with_events[i * 30] * data[id].units_owned;
                totalValue[i] += data[id].prices_without_events[i * 30] * data[id].units_owned;
            }

            totalValueEvents[13] += data[id].prices_with_events[365] * data[id].units_owned;
            totalValue[13] += data[id].prices_without_events[365] * data[id].units_owned;

        })

        // Populates the portfolio tab
        populateTab("portfolio", totalPricesEvents, totalPrices, totalValueEvents, totalValue);

        // Loops over each stock
        Object.keys(result.data).forEach(id => {
            // Clones the template node
            let newTab = tabTemplate.cloneNode(true);
            newTab.hidden = false;
            newTab.removeAttribute("id");

            // Changes the dropdown button to match the stock
            let tabBtn = newTab.querySelector("#template-tab-btn");
            tabBtn.id = `stock-${id}-tab-btn`;
            tabBtn.innerHTML = data[id].name;

            // Changes the with events tab button
            let linkBtnEvents = newTab.querySelector("#template-tab-events");
            linkBtnEvents.id = `stock-${id}-tab-events`;
            linkBtnEvents.dataset.bsTarget = `#stock-${id}-tab-events-pane`;

            // Changes the with events tab pane
            let tabPaneEvents = tabPaneEventsTemplate.cloneNode(true);
            tabPaneEvents.id = `stock-${id}-tab-events-pane`;
            tabPaneEvents.querySelector("#template-tab-events-pane-linechart").id = `stock-${id}-tab-events-pane-linechart`;
            tabPaneEvents.querySelector("#template-tab-events-pane-table").id = `stock-${id}-tab-events-pane-table`;

            // Changes the without events tab button
            let linkBtn = newTab.querySelector("#template-tab");
            linkBtn.id = `stock-${id}-tab`;
            linkBtn.dataset.bsTarget = `#stock-${id}-tab-pane`;

            // Changes the without events tab pane
            let tabPane = tabPaneTemplate.cloneNode(true);
            tabPane.id = `stock-${id}-tab-pane`;
            tabPane.querySelector("#template-tab-pane-linechart").id = `stock-${id}-tab-pane-linechart`;
            tabPane.querySelector("#template-tab-pane-table").id = `stock-${id}-tab-pane-table`;

            // Adds all the new elements to the document
            tabsContentList.appendChild(tabPaneEvents);
            tabsContentList.appendChild(tabPane);
            tabsList.appendChild(newTab);

            //  Finds the total value of the stock owned at 30 day intervals
            let totalValueEvents = new Array(14).fill(0);
            let totalValue = new Array(14).fill(0);

            totalValueEvents[0] = data[id].prices_with_events[0] * data[id].units_owned;
            totalValue[0] = data[id].prices_without_events[0] * data[id].units_owned;

            for (let i=1; i <= 12; i++) {
                totalValueEvents[i] = data[id].prices_with_events[i * 30] * data[id].units_owned;
                totalValue[i] = data[id].prices_without_events[i * 30] * data[id].units_owned;
            }

            totalValueEvents[13] += data[id].prices_with_events[365] * data[id].units_owned;
            totalValue[13] += data[id].prices_without_events[365] * data[id].units_owned;

            // Populates the stock tab panes
            populateTab(`stock-${id}`, data[id].prices_with_events, data[id].prices_without_events, totalValueEvents, totalValue);
        })

        // Moves the user to the simulation results
        document.getElementById("simulation-results").scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});

    })
}


// Removes an event from the event list
function removeEvent(li, event) {
    li.remove();
    events.splice(events.indexOf(event), 1);

    if (events.length === 0) {
        document.getElementById("no-events-text").hidden = false;
    }
}


// Adds an event to the event list
function addEvent() {
    let event = document.getElementById("id_event");
    let name = event.options[event.selectedIndex].text;
    let event_id = event.value;
    let date_value = document.getElementById("id_date").value;
    let date = new Date(date_value);

    // Adds the event to the list and creates the list item
    events.push([event_id, date_value]);
    let li = document.createElement("li");
    li.innerHTML = `${name} on ${date.toLocaleDateString()}`;
    li.className = "list-group-item";

    // Adds the delete button to the list item
    let btn = document.createElement("button");
    btn.className = "btn btn-close position-absolute end-0 me-2";
    btn.onclick = () => removeEvent(li, [event_id, date_value]);
    li.appendChild(btn);

    // Adds the list item to the document
    document.getElementById("events-list").appendChild(li);

    // Removes the no events text
    if (events.length === 1) {
        document.getElementById("no-events-text").hidden = true;
    }
};