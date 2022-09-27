import datetime
import textwrap

from reportlab.pdfgen import canvas as cv
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth

BOLD_FONT = 'Times-Bold'
NORMAL_FONT = 'Times-Roman'
CLUE_FONT_SIZE = 10
CLUE_HEADER_FONT_SIZE = 15

def count_words_on_board(rows, cols, board):
    total_choices = set()
    for i in range(rows):
        row = board[i * cols: i * cols + cols]
        j = 0
        while j < len(row):
            if row[j] == '#':
                j += 1
                continue
            idx = row.find('#', j)
            if idx != -1:
                total_choices.add(j + cols * i)
                j = idx
            else:
                total_choices.add(j + cols * i)
                break
    for i in range(cols):
        col = board[i: cols * rows + cols - i: cols]
        j = 0
        while j < len(col):
            if col[j] == '#':
                j += 1
                continue
            idx = col.find('#', j)
            if idx != -1:
                total_choices.add(i + cols * j)
                j = idx
            else:
                total_choices.add(i + cols * j)
                break
            j += 1
    dct_choices = {}
    c = 1
    for i in sorted(list(total_choices)):
        dct_choices.update({i: c})
        c += 1
    return dct_choices


def make_template(canvas, date, spacing, rows, cols, xword_box=True):
    c_width, c_height = letter
    canvas.setLineWidth(.3)
    canvas.setFont(BOLD_FONT, 12)
    canvas.drawString(50, 730, 'By TJ Crosswords')
    canvas.drawRightString(c_width - 50, 730,
                           date.strftime('%A') + ", " + date.strftime('%B') + " " + date.strftime('%d') + ", "
                           + date.strftime('%Y'))
    canvas.setLineWidth(2)
    canvas.setFillColor('Black')
    canvas.setFont(NORMAL_FONT, spacing * 0.8)
    canvas.setFont(NORMAL_FONT, 11)


def add_clues(canvas, all_clues, vert, horiz):
    orig_vert = vert
    offset = None
    while vert > 30 and all_clues:
        clue, offset = all_clues.pop(0)
        if clue == 'DOWN':
            if vert < 70:
                all_clues.insert(0, 'DOWN')
                return
            canvas.setFont(BOLD_FONT, CLUE_HEADER_FONT_SIZE)
            if vert != orig_vert:
                vert -= 10
            canvas.drawString(horiz, vert, "DOWN")
            vert -= 15
            continue
        canvas.setFont(NORMAL_FONT, CLUE_FONT_SIZE)
        canvas.drawString(horiz + offset, vert, clue)
#        print(offset)
#        print("CLUE", clue)
        vert -= 12


def get_clue_chunks(clues, indices):
    chunks = []
    for key in sorted(clues, key=int):
        initial = str(indices.index(int(key)) + 1) + '. '
        for i, partText in enumerate(textwrap.wrap(clues[key], width=35)):
            if i == 0:
                chunks.append((initial + partText, 0))
            else:
                chunks.append((partText, stringWidth(initial, NORMAL_FONT, CLUE_FONT_SIZE)))
    return chunks


def create_pdf(buffer, partial, solved, rows, across_clues, down_clues, indices, title, solution):
    partial = partial.upper()
    solved = solved.upper()
    date = datetime.datetime.now()
    c_width, c_height = letter
    cols = int(len(solved) / rows)
    spacing = 0.85 * c_width / max(rows, cols) / 1.5
    word_starts = count_words_on_board(rows, cols, partial)
    print(word_starts)
    canvas = cv.Canvas(buffer, pagesize=letter)
    horiz_offset = 80
    vert_offset = 155

    # User's Progress Crossword Creation

    make_template(canvas, date, spacing, rows, cols)
    canvas.setFont(BOLD_FONT, 18)
    if title:
        canvas.setFont(BOLD_FONT, 20)
        canvas.drawCentredString(c_width / 2, 700, title)
        canvas.setFont(NORMAL_FONT, 18)
        canvas.drawCentredString(c_width / 2, 670, 'User\'s Progress')
    else:
        canvas.drawCentredString(c_width / 2, 670, 'User\'s Progress')
    canvas.setFont(BOLD_FONT, 18)
    for i in range(rows):
        for j in range(cols):
            value = partial[j + (rows - 1 - i) * cols]
            if (j + (rows - 1 - i) * cols) in word_starts:
                canvas.setFont(BOLD_FONT, spacing * 0.25)
                canvas.drawString(c_width / 2 - cols * spacing / 2 + j * spacing + spacing * 0.1 - horiz_offset,
                                  c_height / 2.4 - rows * spacing / 2 + i * spacing + spacing * 0.78 + vert_offset - 1,
                                  str(word_starts[(j + (rows - 1 - i) * cols)]))
                canvas.setFont(BOLD_FONT, spacing * 0.8)
            if value == '#':
                canvas.rect(c_width / 2 - cols * spacing / 2 + j * spacing - horiz_offset,
                            c_height / 2.4 - rows * spacing / 2 + i * spacing + vert_offset,
                            spacing, spacing,
                            stroke=1, fill=1)
            elif value != '-':
                canvas.drawCentredString(c_width / 2 - cols * spacing / 2 + j * spacing + spacing * 0.5 - horiz_offset,
                                         c_height / 2.4 - rows * spacing / 2 + i * spacing + spacing * 0.2 + vert_offset,
                                         value)
            canvas.rect(c_width / 2 - cols * spacing / 2 + j * spacing - horiz_offset,
                        c_height / 2.4 - rows * spacing / 2 + i * spacing + vert_offset,
                        spacing, spacing,
                        stroke=1, fill=0)

#    across_full = [str(indices.index(int(key)) + 1) + '. ' + across_clues[key] for key in sorted(across_clues, key=int)]
#    down_full = [str(indices.index(int(key)) + 1) + '. ' + down_clues[key] for key in sorted(down_clues, key=int)]
    across = get_clue_chunks(across_clues, indices)
    down = get_clue_chunks(down_clues, indices)

#    across = [(str(indices.index(int(key)) + 1) + '. ' + partText if i == 0 else partText) for key in sorted(across_clues, key=int) for
#              i, partText in
#              enumerate(textwrap.wrap(across_clues[key], width=35))]
#    down = [str(indices.index(int(key)) + 1) + '. ' + partText if i == 0 else partText for key in sorted(down_clues, key=int) for
#            i, partText in
#            enumerate(textwrap.wrap(down_clues[key], width=35))]

#    across, down = [], []
#    for clue in across_full:
#        indent = clue.index(" ") + 3
#        for i, partText in enumerate(textwrap.wrap(clue, width=35, subsequent_indent=" " * indent)):
#            across.append(partText)
#    for clue in down_full:
#        indent = clue.index(" ") + 3
#        for i, partText in enumerate(textwrap.wrap(clue, width=35, subsequent_indent=" " * indent)):
#            down.append(partText)


    all_clues = across + [("DOWN", 0)] + down
    canvas.setFont(BOLD_FONT, CLUE_HEADER_FONT_SIZE)
    canvas.drawString(50, 285, "ACROSS")

    canvas.setFont(NORMAL_FONT, CLUE_FONT_SIZE)
    add_clues(canvas, all_clues, 270, 50)
    add_clues(canvas, all_clues, 285, 230)
    add_clues(canvas, all_clues, 650, 415)

    canvas.showPage()
    while all_clues:
        make_template(canvas, date, spacing, rows, cols, xword_box=False)
        canvas.setFont(BOLD_FONT, 20)
        canvas.drawCentredString(c_width / 2, 700, 'Clues Continued')
        canvas.setFont(NORMAL_FONT, 12)

        add_clues(canvas, all_clues, 670, 50)
        add_clues(canvas, all_clues, 670, 230)
        add_clues(canvas, all_clues, 670, 415)

        canvas.showPage()

    # Solution Crossword Page
    if not solution:
        return canvas
    spacing = 0.85 * c_width / max(rows, cols)
    make_template(canvas, date, spacing, rows, cols)
    canvas.setFont(BOLD_FONT, 18)
    if title:
        canvas.setFont(BOLD_FONT, 20)
        canvas.drawCentredString(c_width / 2, 700, title)
        canvas.setFont(NORMAL_FONT, 18)
        canvas.drawCentredString(c_width / 2, 670, 'Solved Crossword Puzzle')
    else:
        canvas.drawCentredString(c_width / 2, 670, 'Solved Crossword Puzzle')
    canvas.setFont(BOLD_FONT, 18)
    for i in range(rows):
        for j in range(cols):
            value = solved[j + (rows - 1 - i) * cols]
            if (j + (rows - 1 - i) * cols) in word_starts:
                canvas.setFont(BOLD_FONT, spacing * 0.25)
                canvas.drawString(c_width / 2 - cols * spacing / 2 + j * spacing + spacing * 0.1,
                                  c_height / 2.4 - rows * spacing / 2 + i * spacing + spacing * 0.78,
                                  str(word_starts[(j + (rows - 1 - i) * cols)]))
                canvas.setFont(BOLD_FONT, spacing * 0.8)
            if value == '#':
                canvas.rect(c_width / 2 - cols * spacing / 2 + j * spacing,
                            c_height / 2.4 - rows * spacing / 2 + i * spacing,
                            spacing, spacing,
                            stroke=1, fill=1)
            elif value != '-':
                canvas.drawCentredString(c_width / 2 - cols * spacing / 2 + j * spacing + spacing * 0.5,
                                         c_height / 2.4 - rows * spacing / 2 + i * spacing + spacing * 0.2,
                                         value)
            canvas.rect(c_width / 2 - cols * spacing / 2 + j * spacing,
                        c_height / 2.4 - rows * spacing / 2 + i * spacing,
                        spacing, spacing,
                        stroke=1, fill=0)
    return canvas

