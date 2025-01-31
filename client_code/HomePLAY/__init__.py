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

  def set_not_played_regions_to_invisible(self, reg):
    if reg == 'us':
      self.radio_button_us.visible = False
    elif reg == 'af':
      self.radio_button_af.visible = False
    elif reg == 'cn':
      self.radio_button_cn.visible = False
    elif reg == 'me':
      self.radio_button_me.visible = False
    elif reg == 'sa':
      self.radio_button_sa.visible = False
    elif reg == 'la':
      self.radio_button_la.visible = False
    elif reg == 'pa':
      self.radio_button_pa.visible = False
    elif reg == 'ec':
      self.radio_button_ec.visible = False
    elif reg == 'eu':
      self.radio_button_eu.visible = False
    elif reg == 'se':
      self.radio_button_se.visible = False
      
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
    regions_npbh = anvil.server.call('get_regions_for_players', game_id_entered)
    reg_short, reg_long = anvil.server.call('get_reg_long_names')
    for i in range(len(regions_npbh)):
      jj = regions_npbh[i]['region']
      self.set_not_played_regions_to_invisible(jj)
    
    """This method is called when the button is clicked"""
    self.take_role_card.visible = True

  def set_ministries_visible(self, game_id_entered, reg):
    self.take_role_card.radio_label_ministries.visible = True
    ministries = anvil.server.call('get_roles_for_a_region', game_id_entered, 'cn')
    for key in ministries:
      if key == 'empowerment':
        self.radio_button_emp.visible = ministries[key]
      elif key == 'poverty':
        self.radio_button_pov.visible = ministries[key]
      elif key == 'inequality':
        self.radio_button_ineq.visible = ministries[key]
      elif key == 'food':
        self.radio_button_ineq.visible = ministries[key]
      elif key == 'energy':
        self.radio_button_ineq.visible = ministries[key]
      elif key == 'future':
        self.radio_button_ineq.visible = ministries[key]
    
  def radio_button_af_clicked(self, **event_args):
    global game_id_entered
    print ('in af btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'af')
  
  def radio_button_cn_clicked(self, **event_args):
    global game_id_entered
    print ('in cn btn ' + game_id_entered)
    """This method is called when this radio button is selected"""
    ministries = anvil.server.call('get_roles_for_a_region', game_id_entered, 'cn')
    for key in ministries:
      if key == 'empowerment':
        if ministries[key] == 0:
          self.radio_button_emp.visible = False
        else:
          self.radio_button_emp.visible = True
      elif key == 'poverty':
        if ministries[key] == 0:
          self.radio_button_pov.visible = False
        else:
          self.radio_button_pov.visible = True
      elif key == 'inequality':
        if ministries[key] == 0:
          self.radio_button_ineq.visible = False
        else:
          self.radio_button_ineq.visible = True
      elif key == 'food':
        if ministries[key] == 0:
          self.radio_button_ineq.visible = False
        else:
          self.radio_button_ineq.visible = True
      elif key == 'energy':
        if ministries[key] == 0:
          self.radio_button_ineq.visible = False
        else:
          self.radio_button_ineq.visible = True
      elif key == 'future':
        if ministries[key] == 0:
          self.radio_button_ineq.visible = False
        else:
          self.radio_button_ineq.visible = True
    print (ministries)

  def radio_button_me_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in me btn ' + game_id_entered)
    pass

  def radio_button_us_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in us btn ' + game_id_entered)
    pass

  def radio_button_sa_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in sa btn ' + game_id_entered)
    pass

  def radio_button_la_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in la btn ' + game_id_entered)
    pass

  def radio_button_pa_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in pa btn ' + game_id_entered)
    pass

  def radio_button_ec_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in ec btn ' + game_id_entered)
    pass

  def radio_button_eu_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in eu btn ' + game_id_entered)
    pass

  def radio_button_se_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print ('in se btn ' + game_id_entered)
    pass

  def btn_continue_game_click(self, **event_args):
    alert(content = "Ask for the ID of a previous game and go to the state of the game when last played.", 
          title='ToDo', large=True)
