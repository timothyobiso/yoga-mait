var queries = [
    "yoga poses to help improve balance",
    "frog",
    "poses to stretch my hamstring",
    "poses to alleviate back pain",
    "child's",
    "sage gheranda",
    "stretch my lower back",
    "arm and leg binding"
];

let i = 0;
let placeholder = "";
let index = 0;
const speed = 120;
let direction = true;
function type(){
    txt = queries[index];
    if (direction) {
        placeholder += txt.charAt(i);
        document.getElementById("query").setAttribute("placeholder", placeholder);
        i++;
        setTimeout(type, speed);
    } else {
        placeholder = placeholder.substring(0, placeholder.length-2);
        document.getElementById("query").setAttribute("placeholder", placeholder);
        setTimeout(type, speed);
    }
    if ((i == txt.length) || (!direction && (placeholder.length == 0))) {
        direction = !direction;
        if (i == txt.length) {
            index++;
            i = 0;
        }
        if (index == queries.length) {
            index = 0;
        }
    }
}

type();
