switch(window.location.pathname){
    case '/design/':
        $("#url-design")
            .addClass("active")
            .click(function (e) {e.preventDefault()});
        break
    case '/about/':
        $("#url-about")
            .addClass("active")
            .click(function (e) {e.preventDefault()});
        break
    case '/rules/':
        $("#url-rules")
            .addClass("active")
            .click(function (e) {e.preventDefault()});
        break
    default:
        break
}