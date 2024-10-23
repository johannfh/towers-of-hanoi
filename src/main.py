import kivy
kivy.require('2.3.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
import typing
import towers_of_hanoi as toh

class MyApp(App):

	def build(self):
		return Label(text='Hello world')

	def solve_for(self, n: int) -> typing.List[toh.Move]:
		return []


if __name__ == '__main__':
	MyApp().run()
