function check_alpha(e) {
    let active = $(':focus');
    if(!is_board_item(active)){
        return;
    }
    var inp = String.fromCharCode(e.keyCode);
    console.log(e.keyCode);
    if (/[a-zA-Z]/.test(inp)) {
        $(':focus').val("");
        if (selected) {
            move_to_next_input(0, 1);
        } else {
            move_to_next_input(1, 0);
        }
    }
}

function check_arrow(e){
    let active = $(':focus');
    if(!is_board_item(active)){
        return;
    }
    let prev = selected;
    var inp = String.fromCharCode(e.keyCode);
    console.log(inp);
    switch (e.keyCode) {
        case 37: //arrow left
            selected = true;
            cursorMoved(false);
            if (prev == selected)
                move_to_next_input(0, -1);
            break;
        case 39: //arrow right
            selected = true;
            cursorMoved(false);
            if (prev == selected)
                move_to_next_input(0, 1);
            break;
        case 13: //enter
            selected = true;
            cursorMoved(false);
            if (prev == selected)
                move_to_next_input(0, 1);
            break;
        case 38: //arrow up
            selected = false;
            cursorMoved(false);
            if (prev == selected)
                move_to_next_input(-1, 0);
            break;
        case 40: //arrow down
            selected = false;
            cursorMoved(false);
            if (prev == selected)
                move_to_next_input(1, 0);
            break;
        case 46: //delete
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
        case 32: //space
            selected = !selected;
            cursorMoved(false);
            break;
    }
}

function cursorMoved(clicked = true) {
    // Clear the board
    clear_board_highlights();
    // Highlight corresponding row and column
    console.log("Active element changed: " + $(':focus'));
    let [row, col] = get_row_col($(':focus'));
    if (clicked && row == prev_row && col == prev_col)
    	selected = !selected;
    prev_row = row;
    prev_col = col;
    highlight(row, col, highlight_color, selected);
    clear_label_highlights();
    let start_idx = selected ? get_max_direction(row, col, 0, -1) : get_max_direction(row, col, -1, 0);
    let clue_idx = starting_positions_inv[start_idx];
    let name = selected ? "Across" : "Down";
    console.log(starting_positions_inv);
    console.log(start_idx + " " + clue_idx + " " + name);
    console.log("label-" + name + "-" + clue_idx);
    let label = document.getElementById("label-" + name + "-" + clue_idx);
    $("#label-" + name + "-" + clue_idx).removeClass().addClass("hoverTool2");
}
