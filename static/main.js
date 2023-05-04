var queries = [
    "yoga poses to help improve balance",
    "frog",
    "poses to stretch my hamstring",
    "poses to alleviate back pain",
    "child's",
    "sage gheranda",
    "stretch my lower back",
    "arm and leg binding",
    "my thigh hurts"
];

let i = 0;
let placeholder = "";
const speed = 120;
let direction = true;
let txt = queries[Math.floor(Math.random() * queries.length)];

function type(){
    if (direction) {
        placeholder += txt.charAt(i);
        document.getElementById("query").setAttribute("placeholder", placeholder + "|");
        i++;
        setTimeout(type, speed);
    } else {
        placeholder = placeholder.substring(0, placeholder.length-2);
        document.getElementById("query").setAttribute("placeholder", placeholder + "|");
        setTimeout(type, speed);
    }
    if ((i == txt.length) || (!direction && (placeholder.length == 0))) {
        direction = !direction;
        if (i == txt.length) {
            txt = queries[Math.floor(Math.random() * queries.length)];
            i = 0;
        }
    }
}

type();
