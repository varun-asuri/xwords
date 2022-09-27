import sys
import pickle

from django.conf import settings
from django.core.management import BaseCommand
from rich.progress import track

from ...models import Crossword, Dictionary
from .....crosswords.handler import get_clues


class Command(BaseCommand):
    help = "Import crosswords from file into database"
    CHOICES = [x[1] for x in settings.LANGUAGE_CHOICES]

    def add_arguments(self, parser):
        parser.add_argument("file", help="path to crosswords file to import", type=str)
        parser.add_argument("language",
                            choices=self.CHOICES,
                            help="language of words to import"
                            )

    def handle(self, *args, **options):
        try:
            d = Dictionary.objects.get(language=options["language"])
        except Dictionary.DoesNotExist:
            sys.stderr.write("Language {} does not exist!".format(options["language"]))
            return -1

        pzls = pickle.load(open(options["file"], 'rb'))
        print("IMPORTING PUZZLES:")
        for pzl in track(pzls):
            w, h, blocks = pzl
            boards = pzls[pzl]
            default_args = {"language": d, "width": w, "height": h, "total_blocks": blocks, "is_copy": False,
                            "optional_words": list()}
            if boards[0] is None:
                Crossword.objects.create(
                    valid=False,
                    **default_args
                )
            elif boards[1] is None:
                Crossword.objects.create(
                    board=boards[0],
                    valid=False,
                    **default_args
                )
            else:
                across, down = get_clues(w, h, boards[1], d)
                Crossword.objects.create(
                    board=''.join([''.join(row) for row in boards[0]]),
                    solved=''.join([''.join(row) for row in boards[1]]),
                    clues={
                        "across": across,
                        "down": down,
                    },
                    indices=[*sorted(set([*across.keys()] + [*down.keys()]))],
                    valid=True,
                    **default_args
                )
