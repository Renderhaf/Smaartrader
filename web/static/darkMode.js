const DARK = "dark"
const LIGHT = "light"

var defaultColor = LIGHT;
var body = document.getElementsByTagName("body")[0];

function setColor(color){
    let classes = body.classList;
    if (!classes.contains(color)){
        classes.forEach(function(className){
            if (className == DARK || className == LIGHT){
                body.classList.remove(className)
            }
        });
        classes.add(color);

        setColorInLocalStorage(color)
    }
}

function getColorFromLocalStorage(){
    color = localStorage.getItem("theme");
    return color;
}

function setColorInLocalStorage(color){
    localStorage.setItem("theme", color)
}

function getColorFromPreference(){
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches) ? DARK : LIGHT;
}

setColor(getColorFromLocalStorage() || getColorFromPreference());