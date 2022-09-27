// Color definitions
const BLACK = "#000000";
const WHITE = "#FFFFFF";
const YELLOW = "#FFED1A";
const BLUE = "#a7d8ff";
const highlight_color = BLUE;

let selected = true; //true for across, false for down
let prev_row = -1;
let prev_col = -1;


function idx_to_row_col(idx) {
    return [parseInt(idx / width), idx % width];
}

function row_col_to_idx(row, col) {
    return row * width + col;
}

function get_row_col(element) {
    let id = element.attr("id");
    id = id.split("_");
    console.log(id);
    let row = parseInt(id[0].split("-")[1]);
    let col = parseInt(id[1].split("-")[1]);
    return [row, col];
}

function get_element(row, col) {
    return $("#row-" + row + "_col-" + col);
}

function is_block(element) {
    return element.hasClass("crossword-board_item--blank");
}
function is_board_item(element){
    return element.hasClass("crossword-board_item");
}

function move_to_next_input(r_diff, c_diff) {
    let arr = get_row_col($(':focus'));
    let [row, col] = arr;
    row += r_diff;
    col += c_diff;
    if (row < 0 && col <= 0 || row <= 0 && col < 0) {
        row = height-1;
        col = width-1;
    }
    else if (col < 0) {
        row--;
        col = width-1;
    }
    else if (row < 0) {
        col--;
        row = height-1;
    }
    else if (row >= height && col >= width-1 || row >= height-1 && col >= width) {
        row = 0;
        col = 0;
    }
    else if (col >= width) {
        row++;
        col = 0;
    }
    else if (row >= height) {
        col++;
        row = 0;
    }
    let target = get_element(row, col);
    while (is_block(target)) {
        row += r_diff;
        col += c_diff;
        if (row < 0 && col <= 0 || row <= 0 && col < 0) {
            row = height-1;
            col = width-1;
        }
        else if (col < 0) {
            row--;
            col = width-1;
        }
        else if (row < 0) {
            col--;
            row = height-1;
        }
        else if (row >= height && col >= width-1 || row >= height-1 && col >= width) {
            row = 0;
            col = 0;
        }
        else if (col >= width) {
            row++;
            col = 0;
        }
        else if (row >= height) {
            col++;
            row = 0;
        }
        target = get_element(row, col);
    }
    target.select();
    target.click();
}

function highlight_dir(row, col, row_diff, col_diff, color, first) {
    if (row < 0 || col < 0 || row >= height || col >= width) {
        return;
    }
    let target = get_element(row, col);
    if (is_block(target))
        return;
    if (first)
        target.css("backgroundColor", YELLOW);
    else
        target.css("backgroundColor", color);
    highlight_dir(row + row_diff, col + col_diff, row_diff, col_diff, color, false);
}

function get_max_direction(row, col, row_diff, col_diff) {
    let prev = undefined;
    let target = get_element(row, col);
    while (true) {
        if (row < 0 || col < 0 || row >= height || col >= width) {
            break;
        }
        if (is_block(target))
            break;
        prev = row_col_to_idx(row, col);
        row += row_diff;
        col += col_diff;
        target = get_element(row, col);
    }
    return prev;
}

function highlight(row, col, color, direction) {
    if (!direction) {
        highlight_dir(row, col, 1, 0, color, true);
        highlight_dir(row, col, -1, 0, color, true);
    } else {
        highlight_dir(row, col, 0, 1, color, true);
        highlight_dir(row, col, 0, -1, color, true);
    }

}

function drawLabels(board_div, starting_positions) {
    let textSize = w / 3.5;
    for (let i = 1; i < starting_positions.length; i++) {
        let idx = starting_positions[i];
        let [row, col] = idx_to_row_col(idx);
        let label = $("<label></label>").attr("id", "label-" + i);
        label.text(i + "");
        label.css("left", (w * col + 2) + "px").css("top", (h * row + 3) + "px").css("fontSize", textSize + "px");
        label.addClass("crossword-board_item-label-text");
        board_div.append(label);
    }
}

function translate(leftMin, leftMax, rightMin, rightMax, value){
    let leftSpan = leftMax - leftMin;
    let rightSpan = rightMax - rightMin;
    let valueScaled = (value - leftMin) / (leftSpan);
    return rightMin + (valueScaled * rightSpan);
}

function drawRect(row_div, row, col, color, letter, onclick_function) {
    let item = $("<input></input>").attr("type", "text").attr("id", "row-" + row + "_col-" + col);
    item.css("width", 100 / Math.max(width, height) + "%").css("height", "100%");
    item.attr("maxLength", 1);
    if (color === BLACK) {
        make_block(item);
    } else {
        make_empty(item);
    }
    item.css("margin", "0px").css("fontSize", w / 1.5 + "px");
    item.click(onclick_function);
    item.val(letter);

    let borderWidth = translate(0, 35, 1.5, 0.1, Math.max(width, height));
    item.css("borderWidth", borderWidth + "px");
    row_div.append(item);
}

function drawBoard(board_div, board, onclick_function) {
    let prevrow = -1;
    let row_div = undefined;
    for (let counter = 0; counter < board.length; counter++) {
        let letter = board[counter];
        let [row, col] = idx_to_row_col(counter);
        if(row != prevrow){
            row_div = $("<div></div>").attr("id", "row-" + row);
            row_div.css("width", "100%");
            row_div.css("height", 100 / Math.max(width, height) + "%");
            row_div.css("display", "flex"); // THIS FIXED THE WEIRD ERROR BETWEEN BLOCKS
            board_div.append(row_div);
            console.log($("#board").css("width"));
            prevrow = row;
        }
        if (letter === '#') {
            drawRect(row_div, row, col, BLACK, "", onclick_function);
        } else if(letter === '-'){
            drawRect(row_div, row, col, WHITE, "", onclick_function);
        } else{
            drawRect(row_div, row, col, WHITE, letter, onclick_function);
        }
    }
}

function finalBoard(){
    let board = getBoard();
    let words = getWords(); //getWords() comes from design_page.js
    let rows = [];
    let cols = [];
    for(let i = 0; i < width * height; i += width){
        rows.push(board.slice(i, i + width));
    }
    for(let i = 0; i < width; i++){
        let column = "";
        for(let j = 0; j < width * height; j += width){
            column += board[j + i];
        }
        cols.push(column)
    }
    for(let i = 0; i < words.length; i++){//attempt to put in the words
        let word = words[i];
        for(let j = 0; j < rows.length; j++){

        }
    }
    console.log('heh', board);
    return board;
}

function getBoard(){
    let board = "";
    for(let i = 0; i < width * height; i++){
        let [row, col] = idx_to_row_col(i);
        let element = get_element(row, col);
        let val = element.val();
        if(is_block(element)){
            val = '#'
        }else if(val == ''){
            val = '-';
        }
        board += val;
    }
    return board.toLowerCase();
}

function clear_board_highlights(){
    for (let row = 0; row < height; row++) {
        for (let col = 0; col < width; col++) {
            let element = get_element(row, col);
            if (!is_block(element)) {
                element.css("backgroundColor", "");
            }
        }
    }
}

function clear_label_highlights() {
    for (let i = 0; i < width * height; i++) {
        let across = $("#label-Across-" + i);
        let down = $("#label-Down-" + i);
        if (across.length) {
            across.removeClass("hoverTool2").addClass("hoverTool");
        }
        if (down.length) {
            down.removeClass("hoverTool").addClass("hoverTool");
        }
    }
}

function make_block(item){
    item.removeClass().addClass("crossword-board_item").addClass("crossword-board_item--blank");
    item.css("backgroundColor", BLACK);
}
function make_empty(item){
    item.removeClass().addClass("crossword-board_item").addClass("crossword-board_item--empty");
    item.css("backgroundColor", undefined);
}
function opposite(element){
    let [row, col] = get_row_col(element);
    let [opprow, oppcol] = [height - row - 1, width - col - 1];
    return get_element(opprow, oppcol);
}
function draw(board_div, board, starting_positions, onclick_function){
    drawBoard(board_div, board, onclick_function);
    console.log($("#board").css("width"));
    drawLabels(board_div, starting_positions);
}

function set_width(w1){
    width = w1;
}
function set_height(h1){
    height = h1;
}
function set_board_width(board_div, b_w, is_interactive){
    let percent = "100%";
//    if(!is_interactive){
//        let temp = Math.min(55, width * 60 / height);
//        percent = temp + "%";
//    }
    console.log("Percent: " + percent);
    board_div.css("width", percent);
    board_div.css("height", board_div.css("width"));
    console.log(board_div.css("width"));
    console.log(board_div.css("height"));
    w = parseInt(board_div.css("width")) / Math.max(width, height);
    h = w;
    console.log(w);
//    board_div.css("width", b_w + "px");
//    board_div.css("height", b_w + "px");
}
function set_key_press(func){
    document.onkeypress = func;
}
function set_key_down(func){
    document.onkeydown = func;
}
function set_key_up(func){
    document.onkeyup = func;
}
function set_on_dbl_click(func){
    document.ondblclick = func;
}
