const DARK = "dark"
const LIGHT = "light"

var defaultTheme = LIGHT;
var body = document.getElementsByTagName("body")[0];

function setTheme(color){
    let classes = body.classList;
    if (!classes.contains(color)){
        classes.forEach(function(className){
            if (className == DARK || className == LIGHT){
                body.classList.remove(className)
            }
        });
        classes.add(color);

        setThemeInLocalStorage(color)
    }

    let domBtns = document.getElementsByClassName("theme-icon");
    for (btn of domBtns){
        btn.classList.remove("fa-sun", "fa-moon")
        btn.classList.add(color == DARK ? "fa-sun" : "fa-moon")
    }
}

function getThemeFromLocalStorage(){
    color = localStorage.getItem("theme");
    return color;
}

function setThemeInLocalStorage(color){
    localStorage.setItem("theme", color)
}

function getThemeFromPreference(){
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches) ? DARK : LIGHT;
}

function changeThemeDOM(elem){
    let theme = elem.classList.contains("fa-sun") ? LIGHT : DARK;
    setTheme(theme);
}

setTheme(getThemeFromLocalStorage() || getThemeFromPreference());