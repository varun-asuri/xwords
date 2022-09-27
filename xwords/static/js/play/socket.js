const PROTOCOL = window.location.protocol === "https:" ? "wss" : "ws";
const PATH = `${PROTOCOL}://${window.location.host}`;
let webSocket = new WebSocket(`${PATH}/play/${crossword_id}`);

webSocket.onopen = () => {
    console.log("socket is connected");
};
webSocket.onclose = () => {
    console.log("socket is closed");
};
webSocket.onmessage = (event) => {
    let data = JSON.parse(event.data);
    switch(data.type){
        case "game.error":
            runError(data);
            break;
        case "game.start":
            begin(data);
            break;
        default:
            console.log("Unknown game event received");
    }
}
