from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from uix.screens import homescreen, accountscreen, settingsscreen, surveyscreen, assessscreen, createscreen


class ScreenManaga(ScreenManager):
	
	def __init__(self, **kwargs):
		super(ScreenManaga, self).__init__(**kwargs)
		self.transition = FadeTransition(duration=0.3)
		

class ImageButton(ToggleButtonBehavior, Image):
	
	def __init__(self, **kwargs):
		super(ImageButton, self).__init__(**kwargs)
		self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}


class NavigationBar(BoxLayout):
	
	def __init__(self, **kwargs):
		super(NavigationBar, self).__init__(**kwargs)
		self.orientation = 'horizontal'
		
		with self.canvas:
			Color(0.8745, 0.9019, 0.9137, 1.0)
			self.rect = Rectangle(pos=self.pos, size=self.size)
		self.bind(pos=self.update_rect, size=self.update_rect)
	
	def update_rect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size


class MainControl(BoxLayout, Screen):

	def __init__(self, **kwargs):
		self.sm = ScreenManaga()
		self.nb = NavigationBar()
		super(MainControl, self).__init__(**kwargs)
		self.orientation = "vertical"


class MainScreen(ScreenManager):

	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		self.transition = FadeTransition(duration=0.3)
