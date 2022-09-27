let starting_positions = [];

function initInteractive(){
    set_key_down(check_arrow);
    set_key_up(check_alpha);
    set_on_dbl_click(ondbl);
    let width = 10;
    let height = 10;
    drawInteractive(width, height);
    detectChange();
}

function can_delete(rowChange, colChange) { //determines how far they can backspace
    let  arr = get_row_col($(':focus'));
    let [row, col] = arr;
    row += rowChange;
    col += colChange;
    let target = get_element(row, col);
    return !(is_block(target) || row<0 || col<0 || row >= height || col >= width);
}

function drawInteractive(width, height){
    let board_div = $("#interactive_board");
    let board = '-'.repeat(width * height);
    starting_positions = [];
    set_width(width);
    set_height(height);

    set_board_width(board_div, 500, true);
    board_div.css("verticalAlign", "top");
    drawBoard(board_div, board, on_click);
}

function reset(){
    // Remove whatever's already there
    let board_div = $("#interactive_board");
    board_div.empty();
    // Create the new board here
    let width = parseInt($("#id_width").val());
    let height = parseInt($("#id_height").val());
    drawInteractive(width, height);
}

function detectChange(){
    $("#id_width").change(reset);
    $("#id_height").change(reset);
}

function on_click(){
    if(!is_block($(':focus'))){
        highlight_pos();
    }
}

function highlight_pos(){
    clear_board_highlights();
    $(':focus').css("backgroundColor", YELLOW);
}

function check_alpha(e) {
    let active = $(':focus');
    if(!is_board_item(active)){
        return;
    }
    const inp = active.val();
    console.log(inp);
    let language = $("#id_language").val();
    let allowed = get_allowed(language);
    if (!allowed.test(inp) && inp != "#") {
        active.val("");
        return;
    }
    if(e.shiftKey){
        let lang_dict = get_shift_language_dict(language);
        let shift_val = lang_dict[inp.toUpperCase()];
        if(shift_val !== undefined){
            active.val(shift_val);
        }
    }
    if (selected) {
        move_to_next_input(0, 1);
    } else {
        move_to_next_input(1, 0);
    }
}

function ondbl(){
    let active = $(':focus');
    if(!is_board_item(active)){
        return;
    }
    if(is_block(active)) {
        make_empty(active);
        make_empty(opposite(active));
        highlight_pos();
    }
    else{
        active.val("");
        make_block(active);
        make_block(opposite(active));
    }
}

function check_arrow(e){
    let active = $(':focus');
    if(!is_board_item(active)){
        return;
    }
    switch (e.keyCode) {
        case 37:
            move_to_next_input(0, -1);
            highlight_pos();
            break;
        case 9:
        case 13:
        case 39:
            move_to_next_input(0, 1);
            highlight_pos();
            break;
        case 38:
            move_to_next_input(-1, 0);
            highlight_pos();
            break;
        case 40:
            move_to_next_input(1, 0);
            highlight_pos();
            break;
        case 46:
            if (active.val() == "") {
                if (selected && can_delete(0,1)) 
                    move_to_next_input(0, 1);
                else if (can_delete(1,0))
                    move_to_next_input(1, 0);
            } else active.val("");
            break;
        case 8: //here it checks if it can be deleted
            if (active.val() == "") {
                if (selected && can_delete(0,-1))
                    move_to_next_input(0, -1);
                else if (can_delete(-1,0))
                    move_to_next_input(-1, 0);
            } else active.val("");
            break;
    }
}
