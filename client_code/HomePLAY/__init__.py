from ._anvil_designer import HomePLAYTemplate
from anvil import *
import anvil.server


class HomePLAY(HomePLAYTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def join_new_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    games_info = anvil.server.call('get_latest_game')
    game_id = games_info['game_id']
    npbhp = games_info['npbhp']
    if not npbhp == '[]':
      a = npbhp.replace("['", '')
      a = a.replace("']", '')
      a = a.replace("', '", ' ')
      npbhp = a.split(' ')
    return game_id, npbhp
