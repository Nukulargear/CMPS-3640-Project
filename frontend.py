import kivy
import random
kivy.require('1.10.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.textinput import TextInput        # TEXT INPUT
from kivy.uix.boxlayout import BoxLayout        # BOX LAYOUT
from kivy.uix.floatlayout import FloatLayout	# FLOAT LAYOUT
from kivy.uix.button import Button              # BUTTON
from kivy.uix.label import Label                # LABEL
from kivy.clock import Clock			# CLOCK


#Colors
red = [255,0,0,1]
green = [0.255,0,1]
blue = [0,0,255,1]

#Servers
ser1 = "Banana Server"
ser2 = "Apple Server"
ser3 = "Orange Server"
servers = [ser1, ser2, ser3]

# Everything important
class Hello(FloatLayout):

	# Initialize 
	def __init__(self,**kwargs):
		super(Hello,self).__init__(**kwargs)

		# LABELS
		self.name_label = Label(text = "CHAT APP", size_hint=(.1, .15), pos_hint={'x':.45, 'y':.9}) 			# App label
		self.main_label = Label(text = "Not Connected to Server", size_hint=(1, .55), pos_hint={'x':0, 'y':.35})	# Server connection label
		
		t = TextInput(font_size=30, multiline=False, size_hint=(.6,.1), pos_hint={'x':.05, 'y':.1}, height=20)		# Text Input

		def on_enter(instance):												# Enter Key (find method to store textinput)
			print('User said: ', instance.text)
			t.text = ''
		t.bind(on_text_validate=on_enter)

	# Main Buttons
		self.connect_button = Button(	text = "Connect", 
						size_hint=(.3,.1), 
						pos_hint={'x':.65, 'y':.1}, 
						on_press = self.update, 
						background_color=red)

		self.add_widget(self.main_label)
		self.add_widget(self.connect_button)
		self.add_widget(self.name_label)
		self.current_text = "Not Connected to Servers"

		self.add_widget(t)												# Text Input

	# Server "Connect" Button functionality (doesn't actually work, just looks pretty)
	def update(self,event):
		self.main_label.text = random.choice(servers)									# replace with actual server names
		self.connect_button.text = "Connected"
		self.connect_button.background_color=green

# Builds the app
class app(App):
	def build(self):
		return Hello()

# Runs the app
if __name__=="__main__":
	app().run()
