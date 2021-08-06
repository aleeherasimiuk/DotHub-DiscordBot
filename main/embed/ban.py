from .embed import Embed

class Ban(Embed):

  def __init__(self, user, message):
    super().__init__(user, "", f"**Usuario Baneado**\n\nMotivo:\n```\n{message}```", None, None, 16122, None, None, None)

  