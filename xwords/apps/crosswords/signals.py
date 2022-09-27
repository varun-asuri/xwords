from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Word


@receiver(post_save, sender=Word)
def update_characters(sender, **kwargs):
    word_obj = kwargs['instance']
    d = word_obj.dictionary
    for ch in word_obj.word:
        if ch not in d.characters:
            d.characters.append(ch)
    d.save(update_fields=["characters"])
