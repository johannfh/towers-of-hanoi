import kivy
kivy.require('2.3.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

import typing
import towers_of_hanoi as toh

class TowersOfHanoiAnimation(Widget):
	pass

class TohApp(App):

	def build(self):
		return Label(text='Hello world')

	def solve_for(self, n: int) -> typing.List[toh.Move]:
		return []


if __name__ == '__main__':
	TohApp().run()
