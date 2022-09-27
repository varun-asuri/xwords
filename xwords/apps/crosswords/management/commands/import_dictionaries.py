import pickle

from django.conf import settings
from django.core.management import BaseCommand
from rich.progress import track

from ...signals import update_characters
from ...models import Dictionary, Word, Definition


class Command(BaseCommand):
    help = "Import definitions and clues from file"
    CHOICES = [x[0] for x in settings.LANGUAGE_CHOICES]

    def add_arguments(self, parser):
        parser.add_argument("file", help="path to dictionary file to import", type=str)
        parser.add_argument("language",
                            choices=self.CHOICES,
                            help="language of words to import"
                            )

    def handle(self, *args, **options):
        d = Dictionary.objects.get_or_create(language=options["language"])[0]
        d.full_clean()

        words = pickle.load(open(options["file"], 'rb'))

        print("IMPORTING WORDS: ")
        word_objs = []
        for w in track(words):
            word_objs.append(
                Word(
                    dictionary=d,
                    word=w,
                )
            )
        d.words.bulk_create(word_objs)
        print("FINISHED WORDS\nIMPORTING DEFINITIONS: ")
        for obj in track(word_objs):
            defs = []
            for language in words[obj.word]:
                for definition in words[obj.word][language]:
                    lang = Dictionary.objects.get_or_create(language=language)[0]
                    lang.full_clean()
                    defs.append(
                        Definition(
                            language=lang,
                            word=obj,
                            definition=definition,
                        )
                    )
            obj.definitions.bulk_create(defs)
        print("FINISHED DEFINITIONS\nUPDATING DICTIONARY CHARACTERS: ")
        for word in track(d.words.all()):
            update_characters(None, instance=word)

