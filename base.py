import socket
import sys
import queue
#import psycopg2
import datetime
import threading
import time
from _thread import *


class base(object):

	def __init__(self, name, port, type):
	
		self.name = name
		self.port = port
		self.type = type
		self.close_self_flag = 1
		
		print(self.type, ':', self.port, 'is setting up.')
