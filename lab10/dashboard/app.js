const PRO_API_STATS = "http://localhost:8100/stats";
const ANA_APIS = {
    stats: "http://localhost:8110/stats",
    activity: "http://localhost:8110/lol/activity?index=",
    match: "http://localhost:8110/lol/match?index=",
};

// TIM: helper functions
const timUpdateCodeDiv = (result, elemId)  => document.getElementById(elemId).innerText = JSON.stringify(result, null, 4);
const timGetLocalDateStr = () => (new Date()).toLocaleString();
const getRandomIndex = () => Math.floor(Math.random() * 21);        // between 0 and 20

// TIM: displays error message and remove after 7 seconds 
const timUpdateErrorMessage = (message) => {
    const id = Date.now();
    console.log("Creation", id);
    const msg = document.createElement("div");
    msg.id = `error-${id}`;
    msg.innerHTML = `<p>Something happen at ${timGetLocalDateStr()}!</p><code>${message}</code>`;
    document.getElementById("message").style.display = "block";
    document.getElementById("message").prepend(msg);
    setTimeout(() => {
        const elem = document.getElementById(`error-${id}`);
        if (elem) { elem.remove() }
    }, 7000)
};

// TIM: fetches and updates the general statistics
const timMakeReq = (url, cb) => {
    fetch(url)
        .then(res => {
            console.log(`Fetching: ${url}, Status: ${res.status}`);
            return res.json();
        })
        .then((result) => {
            console.log(`Received data: ${result}`);
            cb(result);
        })
        .catch((error) => {
            console.error(`Fetch failed: ${error}`);
            timUpdateErrorMessage(error.message);
        })
};

// TIM: gets all stats in with timMakeReq()
const timGetStats = () => {
    document.getElementById("last-updated-value").innerText = timGetLocalDateStr();

    timMakeReq(PRO_API_STATS, (result) => timUpdateCodeDiv(result, "processing-value"));
    timMakeReq(ANA_APIS.stats, (result) => timUpdateCodeDiv(result, "analyzer-value"));
    timMakeReq(`${ANA_APIS.activity}${getRandomIndex()}`, (result) => timUpdateCodeDiv(result, "event-activity-value"));
    timMakeReq(`${ANA_APIS.match}${getRandomIndex()}`, (result) => timUpdateCodeDiv(result, "event-match-value"))
};

// TIM: update stats every 4 seconds
const timSetup = () => {
    getStats();
    setInterval(() => getStats(), 4000);
};

// No () when passing a function reference to run later.
document.getElementById("DOMContentLoaded", timSetup);      