

from time import sleep

import win32con
import win32api
from win32api import keybd_event, mouse_event

from key_map import KEYS

class MyWinApi():
	def __init__(self, screen_x, screen_y, delay):
		self._screen_x = screen_x
		self._screen_y = screen_y
		self._delay = delay

	def key_down(self, key):
		sleep(self._delay)
		keybd_event(KEYS[key], 0, 1, 0)

	def key_up(self, key):
		sleep(self._delay)
		keybd_event(KEYS[key], 0, win32con.KEYEVENTF_EXTENDEDKEY  | 
		win32con.KEYEVENTF_KEYUP, 0)

	def press_key(self, key: str):
		sleep(self._delay)
		keybd_event(KEYS[key],0,1,0)
		sleep(self._delay) # Why? its slower...
		keybd_event(KEYS[key],0 ,win32con.KEYEVENTF_KEYUP ,0)
		
	def left_click_down(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
		
	def right_click_down(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
		
	def left_click_up(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
		
	def right_click_up(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
		
	def left_click(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
		
	def right_click(self):
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
		sleep(self._delay)
		mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

	def center_mouse(self):
		win32api.SetCursorPos([int(screen_x / 2), int(screen_y / 2)])

	def set_cursor_pos(self, x, y):
		win32api.SetCursorPos([int(x), int(y)])


	def mouse_top_left(self):
		win32api.SetCursorPos([0,0])
