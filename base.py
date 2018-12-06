import socket
import sys
import queue
#import psycopg2
import datetime
import threading
import time
import random
from _thread import *
import subprocess # port scanner
import pickle # for sending lists



class base(object):

	def __init__(self, name, port, type):
	
		self.name = name
		self.port = port
		self.type = type
		self.size = 1024
		self.close_self_flag = 1
		self.sleep_timer = 10
		
		print(self.type, ':', self.port, 'is setting up.')
		
		
