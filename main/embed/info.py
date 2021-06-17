from .embed import Embed
from .embed import Field
from .embed import Thumbnail
from datetime import datetime

class Info(Embed):

    def __init__(self, title, model, i, seed, author_id, size = "Desconocido", input_images = False, thumbnail_url = None):

        emoji = "\u200B:white_check_mark:" if input_images else "\u200B:x:"

        thumbnail = None
        if thumbnail_url:
            thumbnail = Thumbnail(thumbnail_url)

        fields = [
            Field("Título(s)", title, inline = False),
            Field("Autor", f"<@{author_id}>", inline = True),
            Field("Modelo", model, inline = True),
            Field("Iteraciones", i, inline = True),
            Field("Resolución", size, inline = True),
            Field("Seed", seed, inline = True),
            Field("Imágenes de Input", emoji, inline = True)
        ]

        super().__init__("", "", "", None, None, 16122, None, thumbnail, datetime.utcnow().isoformat(), fields=fields)
