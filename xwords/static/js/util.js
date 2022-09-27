function initInteractive(){
    set_key_down(check_alt_down);
    set_key_up(check_alt_up);
}

function check_alt_down(e){
    if (e.keyCode == 18)
        for(let i = 0; i < 4; i++)
            $("#u" + i).removeClass().addClass("alt");
}

function check_alt_up(e){
    if (e.keyCode == 18)
        for(let i = 0; i < 4; i++)
            $("#u" + i).removeClass("alt");
}

function get_shift_language_dict(language){
    let dict = {};
    switch(language){
        case 'de':
            dict = {};
            return dict;
        case 'fr':
            dict = {};
            return dict;
        case 'es':
            dict = {'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú', 'N': 'Ñ'};
            return dict;
        case 'hu':
            dict = {};
            return dict;
    }
    return {};
}

function get_allowed(language){
    switch(language){
        case 'de':
            return /[a-zA-Z]/;
        case 'fr':
            return /[a-zA-Z]/;
        case 'es':
            return /[a-zA-ZÁÉÍÓÚÑ]/;
        case 'hu':
            return /[a-zA-Z]/;
    }
    return /[a-zA-Z]/;
}
