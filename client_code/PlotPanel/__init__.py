from ._anvil_designer import PlotPanelTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class PlotPanel(PlotPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    
