import kivy
import random
kivy.require('1.10.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

red = [1,0,0,1]
green = [0,1,0,1]
blue = [0,0,1,1]
purple = [1,0,1,1]

class Chat(App):
#	Horizontal Layout
	def build(self):
		"""
		Horizontal BoxLayout example
		"""
		layout = BoxLayout(padding=10)
		colors = [red, green, blue, purple]

		for i in range(5):
			btn = Button(text="Button #%s " % (i+1),
					background_color=random.choice(colors)
					)

			layout.add_widget(btn)
		return layout


if __name__== '__main__':
	app = Chat()
	app.run()
