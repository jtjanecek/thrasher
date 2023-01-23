from Stukov import Stukov
import time
import threading
import win32api, win32console, win32gui
import pythoncom, pyHook
import numpy as np
from PIL import ImageGrab
from MyWinApi import MyWinApi

'''
The state controller is responsible for two things:
1. Read the information of the state of the SC2 game (by sending the pixels and game time to the bot)
2. Execute the commands that the bot wants to do to the game state


General process goes like this:
StateController reads SC2 state -> StateController sends state to bot -> StateController receives commands from bot ->
	StateController executes those commands onto the state -> State controller reads SC2 state -> ...
'''

class StateController():
	def __init__(self, debug=True):
		self._debug = debug
		self._game_speed = 1.2
		self._alive = True
		self._window = MyWinApi(screen_dimensions[0], screen_dimensions[1], .1)
		self._curr_state = None


	def main_routine(self, screen_dimensions, bot_class):
		global time
		self._print("I","Starting pyhook thread...")
		# Start the 'q' exit thread
		self._lock = threading.Lock()
		self._pyhook = threading.Thread(target=self._pyhook_interrupt_thread)
		self._pyhook.start()
		
		self._print("I", "Sleeping 3 seconds before starting...")
		time.sleep(3)
		self._print("I", "Starting state controller")

		while self._am_i_alive():
			state = self.detect_state()
			if state != self._curr_state:
				self._print("S", state)
				self._curr_state = state
			if state == 'game_ready':
				time.sleep(.6)
				self.start(screen_dimensions,bot_class)
			else:
				#pass
				self.change_state(state)
	
		'''
		self._print("I","At loading screen...")
		while(self._at_loading_screen(self._get_screen_state())):
			continue
		self.start(screen_dimensions, bot_class)
		'''
		
	def start(self, screen_dimensions, bot_class):
		global time

		self._print("I","Initializing bot...")
		# We are no longer at the loading screen, start the timer, and start state cycle
		print(" SELF._LOC = ", self._loc)
		bot = bot_class(screen_dimensions, self._loc)

		self._print("I","Starting clock...")
		# Start the *game-clock*
		self._start_time = time.time()
		screen_state = self._get_screen_state()

		self._print("I","Looping perceive -> compute -> action...")
		while self._am_i_alive() and not self.is_victory(screen_state):

			screen_state = self._get_screen_state()
			game_time = self.get_time()

			actions = bot.get_actions(screen_state, game_time)

			self.execute(actions)
			
		self._print("S", "Game ended.")
		
	def detect_state(self):
		screen_state = self._get_screen_state()
		if self.is_multiplayer(screen_state):
			return 'multiplayer'
		if self.is_victory(screen_state):
			return 'victory'
		if self.is_defeat(screen_state):
			return 'defeat'
		if self.is_error_screen(screen_state):
			return 'error'
		if self.is_score_screen(screen_state):
			return 'score_screen'
		if self.is_ready_screen(screen_state):
			return 'ready'
		if self.is_searching(screen_state):
			return 'searching'
		if self.is_loading1(screen_state):
			return 'loading1'
		if self.is_game_ready(screen_state):
			return 'game_ready'
		if self.is_error(screen_state):
			return 'error'
		return "unknown"
		
	def change_state(self, state):
		if state == 'multiplayer':
			self._window.set_cursor_pos(338, 24)
			self._window.left_click()
			return
		if state == 'victory':
			self._window.set_cursor_pos(100,100)
			self._window.press_key('s')
			return
		if state == 'defeat':
			return
		if state == 'score_screen':
			self._window.set_cursor_pos(233,849)
			self._window.left_click()
			self._window.set_cursor_pos(100,100)
		if state == 'ready':
			self._window.set_cursor_pos(238,956)
			self._window.left_click()
			self._window.set_cursor_pos(100,100)
			return
		if state == 'loading1':
			return
		if state == 'error':
			self._window.set_cursor_pos(1620,58)
			self._window.left_click()
			self._window.set_cursor_pos(100,100)	
			time.sleep(.5)
			self._window.set_cursor_pos(341,25)
			self._window.left_click()
			return
			
	def is_error(self, screen_state) -> bool:
		x1 = 282
		y1 = 58
		x2 = 1631
		y2 = 919
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		test = R > 1 and R < 3 and G > 13 and G < 15 and B > 32 and B < 33
		return test
		
	def is_multiplayer(self, screen_state) -> bool:
		x1 = 96
		y1 = 238
		x2 = 816
		y2 = 432
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		test = R > 23 and R < 34 and G > 63 and G < 69 and B > 93 and B < 105
		return test
		
	def is_victory(self, screen_state) -> bool:
		x_low = 720
		x_high = 1200
		y_low = 210
		y_high = 300 # 620
		R = np.mean(screen_state[0,x_low:x_high, y_low:y_high])
		G = np.mean(screen_state[1,x_low:x_high, y_low:y_high])
		B = np.mean(screen_state[2,x_low:x_high, y_low:y_high])
		is_victory = R < 126 and R > 120 and G < 62 and G > 58 and B < 145 and B > 140
		if is_victory:
			#self._print("V","R:{},G:{},B:{}".format(R,G,B))
			return True
		return False
	
	def is_defeat(self, state):
		return False
		
	def is_score_screen(self, screen_state) -> bool:
		#orange box (LEAVE)
		x1 = 103
		y1 = 823
		x2 = 352
		y2 = 863
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		orange_box_active = R > 66 and R < 70 and G > 32 and G < 37 and B > 4 and B < 9
		
		#blue box (options)
		x1 = 637
		y1 = 827
		x2 = 876
		y2 = 862
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		blue_box_active = R > 12 and R < 16 and G > 33 and G < 37 and B > 54 and B < 58

		return orange_box_active and blue_box_active
		
	
	def is_error_screen(self, screen_state):
		return False

	def is_ready_screen(self, screen_state):
		#orange box (LEAVE)
		x1 = 105
		y1 = 929
		x2 = 323
		y2 = 969
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		orange_box_active = R > 63 and R < 68 and G > 32 and G < 36 and B > 6 and B < 10
		
		#blue box (options)
		x1 = 348
		y1 = 932
		x2 = 562
		y2 = 971
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		blue_box_active=  R > 18 and R < 21 and G > 40 and G < 43 and B > 61 and B < 64
		return orange_box_active and blue_box_active
				
	
		return False
		
	def is_searching(self, screen_state):
		x1 = 102
		y1 = 1003
		x2 = 378
		y2 = 1057

		screen_state = np.array(ImageGrab.grab()).T
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		searching = R > 22 and R < 28 and G > 48 and G < 53 and B > 81 and B < 87
		return searching
		
	def is_loading1(self, screen_state):
		x1 = 161
		y1 = 162
		x2 = 510
		y2 = 713

		screen_state = np.array(ImageGrab.grab()).T
		#print(screen_state.shape)
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		load1 = R > 33 and R < 37 and G > 24 and G < 28 and B > 26 and B < 31
		return load1	
		

	def is_game_ready(self, screen_state):
		x1 = 109
		y1 = 994
		x2 = 112
		y2 = 1001
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		if R > 100:
			self._loc = 'R'
			print(" FOUND RIGHT!")
			return True
		x1 = 79
		y1 = 966
		x2 = 86
		y2 = 970
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		if R > 100:
			self._loc = 'L'
			print(" FOUND LEFT!")
			return True
		return False
	
		left_loc = state[:,85,970]
		#print(left_loc)
		left_spawn = left_loc[0] > 100 and left_loc[1] < 30 and left_loc[2] < 30
		right_loc = state[:,110,995]
		#print(right_loc)
		right_spawn = right_loc[0] > 100 and right_loc[1] < 30 and right_loc[2] < 30
		#print(staqte[:,85,970], state[:,110,995], left_spawn,right_spawn)
		if left_spawn or right_spawn:
			return True
		return False
		#return not np.all(state == np.array([0,255,0])) ## Check if Sgt Hammers Fortress health is there
		
		
	def execute(self, actions: list) -> None:
		for action in actions:
			#self._print("A",action)
			eval(action)

	def game_started(self, state) -> bool:
		left_loc = state[:,85,970]
		left_spawn = left_loc[0] == 0 and left_loc[1] != 0 and left_loc[2] == 0
		right_loc = state[:,110,995]
		right_spawn = right_loc[0] == 0 and right_loc[1] != 0 and right_loc[2] == 0
		#print(staqte[:,85,970], state[:,110,995], left_spawn,right_spawn)
		if left_spawn or right_spawn:
			return True
		return False
		#return not np.all(state == np.array([0,255,0])) ## Check if Sgt Hammers Fortress health is there


	def _print(self, message_type: str, message: str) -> None:
		if self._debug:
			print(message_type, ":", message)

	def _get_screen_state(self):
		return np.array(ImageGrab.grab()).T

	def get_time(self):
		sc2_seconds = (time.time() - self._start_time) * self._game_speed + 3
		return sc2_seconds

	################# PyHook / Interrupt Methods #################
	def _am_i_alive(self) -> bool:
		self._lock.acquire()
		if not self._alive:
			self._lock.release()
			return False
		self._lock.release()
		return True

	def set_dead(self) -> None:
		with self._lock:
			self._alive = False
			self._print("I","END SIGNAL DETECTED")

	def _quit_signal(self, event):
		#print(event.KeyID)
		#print(type(event.KeyID))
		if event.KeyID == 81: #keycode for q
			threading.Thread(target=self.set_dead).start()
		return True

	def _pyhook_interrupt_thread(self):
		hm = pyHook.HookManager()
		hm.KeyDown = self._quit_signal
		hm.HookKeyboard()
		while True:
			self._lock.acquire()
			if not self._alive:
				self._lock.release()
				break
			self._lock.release()
			pythoncom.PumpWaitingMessages()

if __name__ == '__main__':
	screen_dimensions = (1920, 1080)
	StateController().main_routine(screen_dimensions, Stukov)
