from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import Crossword
from .tasks import create_crossword
from .utils import serialize_crossword_info, serialize_crossword_error


class CrosswordConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crossword = None
        self.connected = False

    def connect(self):
        try:
            self.crossword = Crossword.objects.get(id=self.scope["url_route"]["kwargs"]["crossword_id"])
        except Crossword.DoesNotExist:
            return self.close()

        async_to_sync(self.channel_layer.group_add)(self.crossword.channels_group_name, self.channel_name)
        self.accept()

        self.connected = True
        create_crossword.delay(self.crossword.id)

    def disconnect(self, code):
        self.connected = False
        async_to_sync(self.channel_layer.group_discard)(
            self.crossword.channels_group_name,
            self.channel_name
        )

    def game_start(self, event):
        self.start_game()

    def game_error(self, event):
        self.send_error()

    def start_game(self):
        if self.connected:
            self.crossword.refresh_from_db()
            self.send_json(serialize_crossword_info(self.crossword))

    def send_error(self):
        if self.connected:
            self.send_json(serialize_crossword_error(self.crossword.errors.latest()))
