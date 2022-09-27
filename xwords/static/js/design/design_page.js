var pageWords = [];


function getWords(){
    let all_words = "";
    let inputs = $(".optional_words");
    inputs.each(function() {
        all_words += `${$(this).val()},`;
    });
    return all_words.substring(0, all_words.length-1);
}

window.onload = () => {
    initInteractive();
    $("#addword_button").click(function () {
        $("#optional_words-wrapper").append(
            "<p><label>Word: </label><input type='text' class='optional_words'>"
        );
    });

    $("#removeword_button").click(function () {
        $("#optional_words-wrapper").children().last().remove();
    });


    $("#submit").click(() => {
        $("#id_board").val(finalBoard());
        $("#id_optional_words").val(getWords());
    });
    $("#id_language").selectize();
    $("#id_clues_language").selectize();
    $("#id_width").selectize();
    $("#id_height").selectize();
    $("#id_total_blocks").selectize();
    let msg = localStorage.getItem("error");
    if(msg){
        $("#error_display").css("display", "block");
        $("#error_content").text(msg);
        localStorage.removeItem("error");
    }
};
