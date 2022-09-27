from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField


class Dictionary(models.Model):

    language = models.CharField(max_length=200, choices=settings.LANGUAGE_CHOICES)
    characters = ArrayField(models.CharField(max_length=1), default=list, blank=True)

    def __str__(self):
        return self.get_language_display()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["language"], name="unique_dictionary")
        ]


class Word(models.Model):

    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="words")
    word = models.CharField(max_length=300)

    def __str__(self):
        return self.word

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dictionary", "word"], name="unique_word")
        ]


class DefinitionSet(models.QuerySet):

    def all_definitions(self):
        return [x.definition for x in self.all()]


class Definition(models.Model):

    objects = DefinitionSet.as_manager()

    language = models.ForeignKey(Dictionary, on_delete=models.CASCADE,)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="definitions")
    definition = models.TextField()

    def __str__(self):
        return self.definition

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["language", "word", "definition"], name="unique_definition")
        ]


class CrosswordSet(models.QuerySet):

    def valid(self):
        return self.filter(valid=True)


class Crossword(models.Model):

    objects = CrosswordSet.as_manager()

    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    language = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="crosswords")

    width = models.IntegerField(default=10)
    height = models.IntegerField(default=10)

    board = models.CharField(max_length=1225, default='')
    solved = models.CharField(max_length=1225, default='')
    optional_words = ArrayField(models.CharField(max_length=256), default=list)
    total_blocks = models.IntegerField(default=25)

    valid = models.BooleanField(default=False)
    is_copy = models.BooleanField(default=False)

    indices = ArrayField(models.IntegerField(), default=list)
    clues = JSONField(default=dict)

    @property
    def channels_group_name(self):
        return "crossword-{id}".format(id=self.id)

    def __str__(self):
        return "{lang}_{w}x{h}_{b}_{t}".format(lang=self.language, w=self.width,
                                               h=self.height, b=self.total_blocks, t=self.created_at.strftime("%m:%d:%y"))


class CrosswordError(models.Model):

    crossword = models.ForeignKey(Crossword, on_delete=models.CASCADE, related_name="errors")
    created_at = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=10240, default='')

    class Meta:
        get_latest_by = "created_at"
