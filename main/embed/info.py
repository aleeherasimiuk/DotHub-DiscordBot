from .embed import Embed
from .embed import Field

class Info(Embed):

    def __init__(self, notebook, titles, model, iterations, seed, author_id):

        fields = [
            Field("Autor", f"<@{author_id}>", inline=True),
            Field("Notebook", notebook, inline=True),
            Field("Título(s)", titles, inline=True),
            Field("Modelo", model, inline=True),
            Field("Iteraciones", iterations, inline=True),
            Field("Seed", seed, inline=True)
        ]

        super().__init__("", "", "", None, None, 16122, None, None, None, fields=fields)
