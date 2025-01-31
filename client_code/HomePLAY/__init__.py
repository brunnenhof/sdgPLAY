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
    self.role_taken.visible = False
    regions_npbh = anvil.server.call('get_regions_for_players', game_id_entered)
    reg_short, reg_long = anvil.server.call('get_reg_long_names')
    for i in range(len(regions_npbh)):
      jj = regions_npbh[i]['region']
      self.set_not_played_regions_to_invisible(jj)
    
    """This method is called when the button is clicked"""
    self.take_role_card.visible = True

  def set_ministries_visible(self, game_id_entered, reg):
    self.label_radio_ministry.visible = True
    ministries = anvil.server.call('get_roles_for_a_region', game_id_entered, reg)
    for key in ministries:
      if key == 'empowerment':
        self.rb_empowerment.visible = ministries[key]
      elif key == 'poverty':
        self.rb_poverty.visible = ministries[key]
      elif key == 'inequality':
        self.rb_inequality.visible = ministries[key]
      elif key == 'food':
        self.rb_food.visible = ministries[key]
      elif key == 'energy':
        self.rb_energy.visible = ministries[key]
      elif key == 'future':
        self.rb_future.visible = ministries[key]
    self.role_taken.visible = True
        
  def radio_button_af_clicked(self, **event_args):
    global game_id_entered
    print ('in af btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'af')
  
  def radio_button_se_clicked(self, **event_args):
    global game_id_entered
    print ('in se btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'se')
  
  def radio_button_us_clicked(self, **event_args):
    global game_id_entered
    print ('in us btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'us')
  
  def radio_button_cn_clicked(self, **event_args):
    global game_id_entered
    print ('in cn btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'cn')
  
  def radio_button_me_clicked(self, **event_args):
    global game_id_entered
    print ('in me btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'me')
  
  def radio_button_sa_clicked(self, **event_args):
    global game_id_entered
    print ('in sa btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'sa')
  
  def radio_button_la_clicked(self, **event_args):
    global game_id_entered
    print ('in la btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'la')
  
  def radio_button_pa_clicked(self, **event_args):
    global game_id_entered
    print ('in pa btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'pa')
  
  def radio_button_ec_clicked(self, **event_args):
    global game_id_entered
    print ('in ec btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'ec')
  
  def radio_button_eu_clicked(self, **event_args):
    global game_id_entered
    print ('in eu btn ' + game_id_entered)
    # set all available ministries for af visible
    self.set_ministries_visible(game_id_entered, 'eu')

  def btn_continue_game_click(self, **event_args):
    alert(content = "Ask for the ID of a previous game and go to the state of the game when last played.", 
          title='ToDo', large=True)

  def minstry_clicked(self):
    if self.rb_poverty.selected:
      return 'poverty'
    if self.rb_inequality.selected:
      return 'inequality'
    if self.rb_empowerment.selected:
      return 'empowerment'
    if self.rb_food.selected:
      return 'food'
    if self.rb_energy.selected:
      return 'energy'
    if self.rb_future.selected:
      return 'future'
    return None  
    
  def role_taken_click(self, **event_args):
    """This method is called when the button is clicked"""
    # check if a role has been taken
    # if not ALERT
    which_ministy = self.minstry_clicked()
    if which_ministy == None:
      alert("You must select one Ministry", role='outlined-error')
    else:
      # save the choices
      which_region = self.region_click()
      anvil.server.call('save_player_choice', which_ministy, which_region)
      
    pass
