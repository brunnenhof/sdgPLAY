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
    self.start_up.visible = False
    self.check_gameID_card.visible = True
    self.check_gameID.text = game_id
    
    return game_id, npbhp

  def btn_gameID_ok_click(self, **event_args):
    global game_id_entered
    game_id_entered = self.check_gameID.text
    games_info = anvil.server.call('get_entered_game', game_id_entered)
    # TODO
    # check that game_id_entered has correct format
    # check that game_id_entered exists
    # handle both if not
    game_id = games_info['game_id']
    roles = anvil.server.call('get_roles', game_id_entered)
    self.start_up.visible = False
    self.check_gameID_card.visible = False
    #print (roles)
    # get fill_roles .....
    # self.radio_button_us.enabled = False
    
    """This method is called when the button is clicked"""
    self.take_role_card.visible = True

  def radio_button_cn_clicked(self, **event_args):
    global game_id_entered
    """This method is called when this radio button is selected"""
    ministries = anvil.server.call('get_roles_for_a_region', game_id_entered, 'cn')
    print (ministries)
