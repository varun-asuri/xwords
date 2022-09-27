from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.generic.websocket import WebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

from .apps.crosswords.consumers import CrosswordConsumer


class WebsocketCloseConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        pass

    def disconnect(self, code):
        pass


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("play/<int:crossword_id>", CrosswordConsumer),
                    path("<path:path>", WebsocketCloseConsumer),
                ]
            )
        )
    }
)