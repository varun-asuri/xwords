import json
import requests

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..crosswords.models import Crossword


@csrf_exempt
def create(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        if "width" not in body or "height" not in body or "blocks" not in body or "language" not in body:
            return JsonResponse({
                "error": 1,
                "message": "Missing required body parameters: width, height, blocks, language"
            })
        else:
            print(body["language"])
            url = settings.SOLVER_ENDPOINT.format(language=body["language"])
            board = body['board'] if 'board' in body else '-' * int(body["height"]) * int(body["width"])
            headers = {"Content-type": "application/json", "Access-Control-Allow-Origin": "*"}
            data = json.dumps(
                {"width": int(body["width"]), "height": int(body["height"]), "blocks": int(body["blocks"]),
                 "board": board})
            try:
                r = requests.post(url, data=data, headers=headers)
            except:
                return JsonResponse({
                    "error": 1,
                    "message": "Internal Server Error, check logs for more details"
                })
            response = json.loads(r.text)
            if not response['error']:
                Crossword.objects.create(
                    language=response["lang"],
                    board=response["empty_board"],
                    valid=True,
                    solved=response["solved_board"],
                    width=response["width"],
                    height=response["height"],
                    total_blocks=response["blocks"],
                    indices=response["indices"],
                    clues=response["clues"]
                )
            print(r.text)
            return JsonResponse(response)
    return JsonResponse({
        "error": 1,
        "message": "{method} not allowed".format(method=request.method)
    })


@csrf_exempt
def cache(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        Crossword.objects.create(
            language=body["lang"],
            board=body["empty_board"],
            valid=body["valid"],
            solved=body["solved_board"],
            width=body["width"],
            height=body["height"],
            total_blocks=body["blocks"],
            indices=body["indices"],
            clues=body["clues"]
        )
        return JsonResponse({
            "error": 0,
            "message": "Successfully created Crosswords object"
        })
    return JsonResponse({
        "error": 1,
        "message": "{method} not allowed".format(method=request.method)
    })
