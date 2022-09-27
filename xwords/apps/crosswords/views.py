import io
import json

from django.contrib import messages
from django.shortcuts import render
from django.http import FileResponse
from django.views.decorators.http import require_POST

from .models import Crossword
from .utils.pdf import create_pdf
from .forms import CrosswordForm, PDFForm


def play(request):
    if request.method == 'POST':
        form = CrosswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            c = Crossword.objects.create(
                language=cd['language'],
                width=cd['width'],
                height=cd['height'],
                board=cd['board'],
                total_blocks=cd['total_blocks'],
                optional_words=cd['optional_words'],
            )
            cd["language"] = cd["language"].id
            cd["clues_language"] = cd["clues_language"].id
            cd["optional_words"] = []
            request.session["form-data"] = json.dumps(cd)
            return render(request, "crosswords/play.html", {'id': c.id, 'form': PDFForm()})
        else:
            errors, more_errs = form.errors.get_json_data(), False
            for key, error in errors.items():
                if key == "__all__":
                    more_errs = True
                    continue
                for err in error:
                    messages.error(request, err['message'], extra_tags="danger")
            if more_errs:
                for err in form.errors.get_json_data()["__all__"]:
                    messages.error(request, err['message'], extra_tags="danger")

    initial = json.loads(request.session.get("form-data", "{}"))
    return render(request, "crosswords/design.html", {'form': CrosswordForm(initial=initial)})


@require_POST
def pdf(request):
    form = PDFForm(request.POST)
    if form.is_valid():
        buffer = io.BytesIO()
        cd = form.cleaned_data
        c = cd["crossword"]
        create_pdf(buffer, c.board, c.solved, c.height, c.clues['across'], c.clues['down'], c.indices, cd['title'], cd['solution']).save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="{}.pdf".format(str(c)))
    else:
        for err in form.errors.as_data()["__all__"]:
            messages.error(request, err.message, extra_tags="danger")
