var solution;
let across;
let down;
var emptyboard;
function initPlay(width, height, board, starting){
    starting_positions = starting;
    starting_positions_inv = {};
    starting_positions.unshift(-1);
    for(let i = 0; i < starting_positions.length; i++){
        starting_positions_inv[starting_positions[i]] = i;
    }
    set_key_down(check_arrow);
    set_key_press(check_alpha);
    let board_div = $("#board");
    board_div.css("verticalAlign", "top");
    set_width(width);
    set_height(height);
    set_board_width(board_div, 500, false);
    draw(board_div, board, starting_positions, cursorMoved);
    console.log($("#board").css("width"));
}

function runError(data){
    localStorage.setItem("error", data.message);
    location.replace(location.href);
}

function checkSolved(board){
    return board == solution;
}

function evaluate(){
    console.log("Evaluating board");
    let board = getBoard();
    let correct = 0;
    let total = 0;
    for(let i = 0; i < width * height; i++){
        let [row, col] = idx_to_row_col(i);
        let element = get_element(row, col);
        if(board.charAt(i) == '-'){
            element.css("backgroundColor", "#FFFFFF");
            continue;
        }
        if(board.charAt(i) == '#'){
            continue;
        }
        if(board.charAt(i) == solution.charAt(i)){
            element.css("backgroundColor", "#00FF00");
            total += 1;
            correct += 1;
        }
        else{
            element.css("backgroundColor", "#FF0000");
            total += 1;
        }
    }
    alert(`You attempted ${total} and got ${correct} correct`);
}

function setup_board(width, height, clues, empty, solved, indices){
    set_width(width);
    set_height(height);
    across = clues.across;
    down = clues.down;
    console.log("Setting up gameboard");
    $("#root").css("display", "block");
    $("#loading").css("display", "none");
    solution = solved;
    emptyboard = empty;
    initPlay(width, height, empty, indices);
    addWordLists(across, down);
}

function setBoard(board){
    for(let idx = 0; idx < board.length; idx++){
        let [row, col] = idx_to_row_col(idx);
        let char = board[idx];
        let element = get_element(row, col);
        if(board[idx] == "#"){
            make_block(element);
            continue;
        }
        if(board[idx] == '-'){
            char = "";
        }
        element.val(char);
    }
}

function can_delete(rowChange, colChange) { //determines how far they can backspace
    let  arr = get_row_col($(':focus'));
    let [row, col] = arr;
    row += rowChange;
    col += colChange;
    let target = get_element(row, col);
    return !(is_block(target) || row < 0 || col < 0 || row >= height || col >= width);
}

function begin(data){
    $("#evaluate").click(evaluate);

    $("#pdf").click(() => {
        $("#id_board").val(getBoard());
        $("#id_crossword").val(crossword_id);
    });

    $("#showAnswers").click(() => {
        if (window.confirm('Are you sure you want to see the answer?')) {
            setBoard(solution);
        }
    });

    $("#clearBoard").click(() => {
        if(window.confirm('Are you sure you want to clear the board?')) {
            setBoard(emptyboard);
            evaluate();
        }
    });

    $("#pdfSubmit").click(() => {
        $("#pdfForm").modal('hide');
    });

    setup_board(data.width, data.height, data.clues, data.board, data.solved, data.indices);
}
