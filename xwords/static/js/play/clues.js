function clue_click(e) {
    let label = e.target;
    selected = label.id.indexOf("Across") != -1 ? true : false;
    console.log(selected);
    let clue_idx = parseInt(label.id.split("-")[2]);
    console.log(clue_idx + " HIIII");
    let idx = starting_positions[clue_idx];
    let [row, col] = idx_to_row_col(idx);
    let target = get_element(row, col);
    target.select();
    target.click();
    cursorMoved(false);
    window.scrollTo(0, 150);
}

function addWordList(wordList, name) {
    console.log("Adding word list!");
    let wordlist_div = $("<div />").css("margin", "4vw 2vw 0vw").css("height", "500px").css("overflow", "scroll").addClass("small");
    wordlist_div.append($("<h3 />").text(name));
    for (let key in wordList) {
        let clue_idx = starting_positions_inv[key];
        let clue_box = $("<label />").attr("id", "label-" + name + "-" + clue_idx);
        console.log(clue_box.attr("id"));
        clue_box.text(clue_idx + ". " + wordList[key]).addClass("hoverTool");
        clue_box.click(clue_click);
        wordlist_div.append(clue_box, $("<br>"));
    }
    $("#clues_total").append(wordlist_div);
}

function addWordLists(wordListA, wordListD, starting){
    addWordList(wordListA, "Across");
    addWordList(wordListD, "Down");
}
