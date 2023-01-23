import time
from MyWinApi import MyWinApi
import win32con
import pyHook
from Thrasher import Thrasher
from random import shuffle
import numpy as np

class Stukov():
	def __init__(self, screen_dimensions, spawn_loc, debug=True):
		self._debug = debug
		self._spawn_location = spawn_loc
		self._num_workers = 12
		self._gas1 = None
		self._gas1_loc = ()
		self._gas2 = None
		self._gas2_loc = ()
		#self._spawn_location = None

		self._initial_setup_done = False

		self.t1 = Thrasher('t1',[[153,930]])
		self.t2 = Thrasher('t2',[[116 ,849], [128,838]])
		self.t3 = Thrasher('t3',[[235,993], [257,981], [244, 958]])
		self.t4 = Thrasher('t4',[[202,900], [186,880], [206, 866], [224, 879]])
		self.thrashers = [self.t1, self.t2, self.t3, self.t4]
		self._state = None

		#self._thrasher1 = Thrasher(137, 922, 162, 940)
		self._thrasher1_active = True
		self._thrasher2_active = False
		self._thrasher3_active = False
		self._thrasher4_active = False
		self._thrasher1_rally = (152, 929)
		self._thrasher2_rally = (115, 835)
		self._thrasher3_rally = (250, 970)
		self._thrasher4_rally = (215, 870)

		self._barracks_alive = False
		self._overlord_positioned = False

		self._hotkeys = {'command_center': '4',
							'barracks': '2'}

		self._saidGG = False

		self._left_mineral = (580,772)
		self._right_mineral = (998,775)
		
		self.bunkers = [[795, 379, False],
					[981, 429, False],
					[1173, 479, False],
					[1317, 639, False],
					[1597, 689, False]]
		
		


	def get_actions(self, screen_state, game_time) -> list:
		self._game_time = game_time
		self._actions = []
		#print(game_time)
		
		'''
		self._spawn_location='R'
		#self.set_rally(screen_state)
		self.deploy_1=True
		exec("self.deploy_{} = True".format(1))
		return self._actions
		'''
		
	
		if game_time < 5:
			self.sayGG()
			self.set_spawn_location(screen_state, game_time)
			self.setup_initial_base()
		
		if game_time > 40:
			self.set_rally(screen_state)
		
		if game_time < 50:
			self.make_overlord_and_worker()
	
		if game_time < 65 and game_time > 60:
			self.build_barracks()

		if game_time < 73 and game_time > 70:
			self.rally_overlords()
			self.make_a_worker()
	
		if game_time > 80 and game_time < 124:
			self.make_a_worker()

		if game_time > 130 and game_time < 140:
			self.upgrade_compound1()
		
		if game_time > 132 and game_time < 133:
			self.make_left_gas()
			self.make_right_gas()
		
		if game_time > 135 and game_time < 210:
			self.make_overlord_and_worker()
		
		if game_time > 180:
			self.make_engi_bay()
		
		if game_time > 230:
			self.upgrade_compound_jumper()
		
		if game_time > 300:
			self.deploy_duo_1()
			
		if game_time > 300 and game_time < 310:
			self.make_overlord()
		
		if game_time > 340 and game_time < 345:
			self.make_bunkers()

		if game_time > 400:
			self.upgrade_compound_broodling()
			self.upgrade_compound2()

		if game_time > 500:
			self.upgrade_engi_bay()
			self.make_more_overlords()
			self.move_overlords()

		if game_time > 600:
			self.deploy_duo_2()

		if game_time > 610:
			self.deploy_big_bunkers(screen_state)

		if game_time > 900:
			self.deploy_duo_3()

		if game_time > 1200:
			self.deploy_duo_infinite()
	
		return list(self._actions)

	def deploy_big_bunkers(self, screen_state):
		if int(self._game_time) % 25 == 0:
			print(" Building big bunkers!")
			def build_bunker_if_doesnt_exist(screen_state, x, y):
				#if bunker already exists...:
				#print("Setting cursor at {} {}".format(x,y))
				self._actions.append('self._window.set_cursor_pos({},{})'.format(x,y))
				self._actions.append('self._window.left_click()')

			def game_alive(screen_state):
				x1 = 1536
				y1 = 790
				x2 = 1903
				y2 = 823
				#screen_state = np.array(ImageGrab.grab()).T
				#print(screen_state.shape)
				R = np.mean(screen_state[0,x1:x2, y1:y2])
				G = np.mean(screen_state[1,x1:x2, y1:y2])
				B = np.mean(screen_state[2,x1:x2, y1:y2])
				return R > 65 and R < 70 and G < 41 and G > 37 and B > 26 and B < 31
			
			num_bunk_above = 2
			x = 945 #960
			y = 516 #540
			x_diff = 188
			y_diff = 144
			# Check if game is over... we dont want to go into replay...
			if not game_alive(screen_state):
                                return
			self.select_worker(all=True)
			self._actions.append('self._window.press_key("r")')
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("u")')
			self._actions.append('self._window.key_down("SHIFT")')
			build_bunker_if_doesnt_exist(screen_state, x, y)
			# For 1 bunker above, 2 bunkers above, 3 bunkers above... etc...
			for bunk_num in range(1, num_bunk_above + 1):
				# y+
				build_bunker_if_doesnt_exist(screen_state, x, y + (bunk_num * y_diff))
				# y-
				build_bunker_if_doesnt_exist(screen_state, x, y - (bunk_num * y_diff))
				# x+
				build_bunker_if_doesnt_exist(screen_state, x + (bunk_num * x_diff), y)
				# x-
				build_bunker_if_doesnt_exist(screen_state, x - (bunk_num * x_diff), y)
				# x+y+
				build_bunker_if_doesnt_exist(screen_state, x + (bunk_num * x_diff), y + (num_bunk_above * y_diff))
				# x+y-
				build_bunker_if_doesnt_exist(screen_state, x + (bunk_num * x_diff), y - (num_bunk_above * y_diff))
				# x-y+
				build_bunker_if_doesnt_exist(screen_state, x - (bunk_num * x_diff), y + (num_bunk_above * y_diff))
				# x-y-
				build_bunker_if_doesnt_exist(screen_state, x - (bunk_num * x_diff), y - (num_bunk_above * y_diff))
			#self._actions.append('self._window.press_key("w")')
			self._actions.append('self._window.key_up("SHIFT")')

		
	def make_bunkers(self):
		if not hasattr(self, 'bunkers_built'):
			self._print("A","{} | Building bunkers...".format(self.format_game_time()))

			self.select_worker(all=True)
			self._actions.append('self._window.press_key("e")')
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("u")')
			self._actions.append('self._window.key_down("SHIFT")')
			for i in range(len(self.bunkers)):
				if not self.bunkers[i][2]:
					self._actions.append("self._window.set_cursor_pos({},{})".format(self.bunkers[i][0],self.bunkers[i][1]))
					self._actions.append('self._window.left_click()')
					self.bunkers[i][2] = True
			self._actions.append('self._window.key_up("SHIFT")')
			self.bunkers_built = True

	def make_overlord(self):
		self._actions.append('self._window.press_key("4")')
		self._actions.append('self._window.press_key("v")')

	def make_more_overlords(self):
		if not hasattr(self, 'more_overlords'):
			self._print("A","{} | Making MORE overlords...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("4")')
			for i in range(5):
				self._actions.append('self._window.press_key("v")')
			self.more_overlords = True	

	def deploy_duo_1(self):
		if not hasattr(self, 'deploy1'):
			self._print("A","{} | Deploying duo 1...".format(self.format_game_time()))

			self._actions.append('self._window.press_key("r")')
			self.apoc_calldown()
			self.infested_bc_calldown()
			self._actions.append('time.sleep(3)')
			self._actions.append('self._window.press_key("f2")')
			self._actions.append('self._window.press_key("a")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher2_rally[0],self._thrasher2_rally[1]))
			self._actions.append('self._window.left_click()')

			# We dont need this location anymore, so lets hotkey the new bunker location
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._big_bunk_loc[0], self._big_bunk_loc[1]))
			self._actions.append('self._window.left_click()')
			self.hotkey('r')

			self.deploy1 = True
			
	def deploy_duo_2(self):
		if not hasattr(self, 'deploy2'):
			self._print("A","{} | Deploying duo 2...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("t")')
			self.apoc_calldown()
			self.infested_bc_calldown()
			self._actions.append('time.sleep(3)')
			self._actions.append('self._window.press_key("f2")')
			self._actions.append('self._window.press_key("a")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher3_rally[0],self._thrasher3_rally[1]))
			self._actions.append('self._window.left_click()')
			self.deploy2 = True

	def deploy_duo_3(self):
		if not hasattr(self, 'deploy3'):
			self._print("A","{} | Deploying duo 3...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("e")')
			self.apoc_calldown()
			self.infested_bc_calldown()
			self._actions.append('time.sleep(3)')
			self._actions.append('self._window.press_key("f2")')
			self._actions.append('self._window.press_key("a")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher4_rally[0],self._thrasher4_rally[1]))
			self._actions.append('self._window.left_click()')
			self.deploy3 = True

	def deploy_duo_infinite(self):
		x = self._game_time - 900
		deploy_id = int( x / 300 )
		if not hasattr(self, 'deploy_{}'.format(deploy_id)):
			self._print("A","{} | Deploying duo id {}...".format(self.format_game_time(), deploy_id))
			self._actions.append('self._window.press_key("e")')
			self.apoc_calldown()
			self.infested_bc_calldown()
			self._actions.append('time.sleep(3)')
			self._actions.append('self._window.press_key("f2")')
			self._actions.append('self._window.press_key("a")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher4_rally[0],self._thrasher4_rally[1]))
			self._actions.append('self._window.left_click()')
			exec("self.deploy_{} = True".format(deploy_id))

	def set_rally(self, screen_state):
		coord = None
		new_state = None
		
		for thrasher in self.thrashers:
			if thrasher.is_alive(screen_state):
				new_state, coord = thrasher.get_state_and_rallypoint(screen_state)
				break
		'''
		if self.t4.is_alive(screen_state):
			new_state, coord = self.t4.get_state_and_rallypoint(screen_state)
		elif self.t3.is_alive(screen_state):
			new_state, coord = self.t3.get_state_and_rallypoint(screen_state)
		elif self.t2.is_alive(screen_state):
			new_state, coord = self.t2.get_state_and_rallypoint(screen_state)
		elif self.t1.is_alive(screen_state):
			new_state, coord = self.t1.get_state_and_rallypoint(screen_state)
		else:
			new_state = 't4'
		'''
				
		if new_state == None or new_state == self._state:
			return
		#print(" NEW STATE DETECTED: {}".format(new_state))
		self._state = new_state
		self._actions.append('self._window.press_key("3")')
		if self._state == 't4':
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher4_rally[0], self._thrasher4_rally[1]))
		else:
			self._actions.append('self._window.set_cursor_pos({},{})'.format(coord[0], coord[1]))
		self._actions.append('self._window.right_click()')
		self._actions.append('self._window.set_cursor_pos(100,100)')

	def upgrade_compound1(self):
		if not hasattr(self, 'level1compound'):
			self._print("A","{} | Upgrading compound 1...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("3")')
			self._actions.append('self._window.press_key("g")')
			self.level1compound = True
			
	def upgrade_compound2(self):
		if not hasattr(self, 'level2compound'):
			self._print("A","{} | Upgrading compound 2...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("3")')
			self._actions.append('self._window.press_key("g")')
			self.level2compound = True
			
	def upgrade_compound_broodling(self):
		if not hasattr(self, 'broodling_compound'):
			self._print("A","{} | Upgrading compound broodling...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("3")')
			self._actions.append('self._window.press_key("b")')
			self.broodling_compound = True
			
	def upgrade_compound_jumper(self):
		if not hasattr(self, 'jumper_compound'):
			self._print("A","{} | Upgrading compound jumper...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("3")')
			self._actions.append('self._window.press_key("a")')
			self.jumper_compound = True
			
			
	def make_a_worker(self):
		self._actions.append('self._window.press_key("4")')
		self._actions.append('self._window.press_key("s")')

	def build_barracks(self):
		if not hasattr(self, 'builtbarracks'):
			self._print("A","{} | Buildilng barracks...".format(self.format_game_time()))
			self.select_worker()
			 
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("b")')
			if self._spawn_location == 'R':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(221,665))
			elif self._spawn_location == 'L':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(470,54))
			self._actions.append('self._window.left_click()')
			
			# Back to mineral
			if self._spawn_location == 'L':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(self._left_mineral[0],self._left_mineral[1]))
			elif self._spawn_location == 'R':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(self._right_mineral[0],self._right_mineral[1]))
			self._actions.append('self._window.key_down("SHIFT")')
			self._actions.append('self._window.right_click()')
			self._actions.append('self._window.key_up("SHIFT")')
			self.builtbarracks = True
			
	def hotkey_barracks(self):
		self._actions.append('time.sleep(3)')
		if self._spawn_location == 'R':
			self._actions.append('self._window.set_cursor_pos({},{})'.format(221,665))
		elif self._spawn_location == 'L':
			self._actions.append('self._window.set_cursor_pos({},{})'.format(457,125))
		self._actions.append('self._window.left_click()')
		 
		self.hotkey('2')

	def make_engi_bay(self):
		if not hasattr(self, 'built_engi'):	
			self._print("A","{} | Buildilng engi bay...".format(self.format_game_time()))

			self.select_worker()
			 
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("f")')
			if self._spawn_location == 'R':
				self._engi_bay_loc = (1367, 657)
			elif self._spawn_location == 'L':
				self._engi_bay_loc = (1028, 727)
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._engi_bay_loc[0],self._engi_bay_loc[1]))
			self._actions.append('self._window.left_click()')

			
			# Back to mineral
			if self._spawn_location == 'L':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(self._left_mineral[0],self._left_mineral[1]))
			elif self._spawn_location == 'R':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(self._right_mineral[0],self._right_mineral[1]))
			self._actions.append('self._window.key_down("SHIFT")')
			self._actions.append('self._window.right_click()')
			self._actions.append('self._window.key_up("SHIFT")')
			self.built_engi = True

	def upgrade_engi_bay(self):
		if not hasattr(self, 'upgraded_engi'):	
			self._print("A","{} | Upgrading engi bay...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("w")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._engi_bay_loc[0],self._engi_bay_loc[1]))
			self._actions.append('self._window.left_click()')
			self._actions.append('self._window.press_key("s")')
			self._actions.append('self._window.press_key("a")')
			self.upgraded_engi = True

	def sayGG(self):
		if not hasattr(self, 'alreadysaidgg'):
			self._print("A","{} | Saying glhf...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("ENTER")')
			self._actions.append('self._window.press_key("g")')
			self._actions.append('self._window.press_key("l")')
			self._actions.append('self._window.press_key("h")')
			self._actions.append('self._window.press_key("f")')
			self._actions.append('self._window.press_key("ENTER")')
			self.alreadysaidgg = True
		
	def set_spawn_location(self, screen_state, game_time) -> list:
		if not hasattr(self, 'spawn_set'):

		#if self._spawn_location == None:
			'''
			left_loc = screen_state[:,85,970]
			left_spawn = left_loc[0] > 100 and left_loc[1] < 30 and left_loc[2] < 30
			right_loc = screen_state[:,110,995]
			right_spawn = right_loc[0] > 100 and right_loc[1] < 30 and right_loc[2] < 30
			'''
			'''
			left_spawn = False
			right_spawn = False
			
			x1 = 109
			y1 = 994
			x2 = 112
			y2 = 1001
			R = np.mean(screen_state[0,x1:x2, y1:y2])
			G = np.mean(screen_state[1,x1:x2, y1:y2])
			B = np.mean(screen_state[2,x1:x2, y1:y2])
			print("RIGHT: ", R,G,B)
			if R > 100:
				right_spawn = True
			x1 = 79
			y1 = 966
			x2 = 86
			y2 = 970
			R = np.mean(screen_state[0,x1:x2, y1:y2])
			G = np.mean(screen_state[1,x1:x2, y1:y2])
			B = np.mean(screen_state[2,x1:x2, y1:y2])
			print("LEFT: ", R,G,B)
			if R > 100:
				left_spawn = True	
			'''
			print(" SELF SPAWN LOC: ", self._spawn_location)
			if self._spawn_location == 'L':
				self._big_bunk_loc = (93,949)
				self._print("G","Spawned left")
				self._actions.append('self._window.set_cursor_pos(1097, 405)')
			elif self._spawn_location == 'R':
				self._big_bunk_loc = (131,989)
				self._print("G","Spawned right")
				self._actions.append('self._window.set_cursor_pos(1000, 300)')
			else:
				print(R)
				print(G)
				print(B)
				raise Exception("NO SPAWN LOCATION!!!")
				
			self._actions.append('self._window.left_click()')
			self.hotkey('4')
			
			# Hotkey colony
			if self._spawn_location == 'L':
				self.box((1388,142),(1776,481))
			elif self._spawn_location == 'R':
				self.box((1700,200),(960,20))
			self.hotkey('3')
				
			# Hotkey all meaningful locations
			#self._actions.append('time.sleep(1)')
			self._actions.append('self._window.press_key("4")')
			self._actions.append('self._window.press_key("4")')
			self._actions.append('self._window.press_key("4")')
			self._actions.append('self._window.press_key("4")')
			self.hotkey('w')
			 
			self._actions.append('self._window.set_cursor_pos({},{})'.format(115, 968))
			self._actions.append('self._window.left_click()')
			self.hotkey('e')
			 
			self._actions.append('self._window.set_cursor_pos({},{})'.format(102,901))
			self._actions.append('self._window.left_click()')
			self.hotkey('r')
			 
			self._actions.append('self._window.set_cursor_pos({},{})'.format(180,987))
			self._actions.append('self._window.left_click()')
			self.hotkey('t')
			 
			self._actions.append('self._window.press_key("w")')
			
			# Make a worker
			self.make_a_worker()

			# Set rally to thrasher1
			self._actions.append('self._window.press_key("3")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(self._thrasher1_rally[0],self._thrasher1_rally[1]))
			self._actions.append('self._window.right_click()')
			self.spawn_set = True
			
	def setup_initial_base(self):
		if not self._initial_setup_done:
			self._print("G","Running initial base setup...")
			self._actions.append('self._window.press_key("4")')
			self._actions.append('time.sleep(3)')
			self._actions.append('self._window.press_key("s")')
			self._actions.append('time.sleep(5)')
			self._actions.append('self._window.press_key("v")')
			
			self._initial_setup_done = True

	def apoc_calldown(self):
		self._actions.append('self._window.set_cursor_pos({},{})'.format(1008,38))
		self._actions.append('self._window.left_click()')
		self._actions.append('self._window.set_cursor_pos({},{})'.format(966,500))
		self._actions.append('self._window.left_click()')
		
	def infested_bc_calldown(self):
		self._actions.append('self._window.set_cursor_pos({},{})'.format(1090,44))
		self._actions.append('self._window.left_click()')
		self._actions.append('self._window.set_cursor_pos({},{})'.format(966,500))
		self._actions.append('self._window.left_click()')


	
	def make_overlord_and_worker(self):
		self._actions.append('self._window.press_key("4")')
		self._actions.append('self._window.press_key("s")')
		self._actions.append('self._window.press_key("s")')
		self._actions.append('self._window.press_key("s")')
		self._actions.append('self._window.press_key("v")')
	
	def select_worker(self, all = False):	
		self._actions.append('self._window.press_key("w")')
		if self._spawn_location == 'L':
			self.box((87,305),(838,667))
		elif self._spawn_location == 'R':
			self.box((428,548),(1056,841))
			
		self._actions.append('self._window.set_cursor_pos({},{})'.format(745,973))
		if all:
			self._actions.append('self._window.key_down("CTRL")')
		self._actions.append('self._window.left_click()')
		if all:
			self._actions.append('self._window.key_up("CTRL")')
			
	def move_overlords(self):	
		if not hasattr(self, 'moved_ovies'):
			self._actions.append('self._window.press_key("w")')
			if self._spawn_location == 'L':
				self.box((87,305),(838,667))
			elif self._spawn_location == 'R':
				self.box((428,548),(1056,841))
				
			self._actions.append('self._window.set_cursor_pos({},{})'.format(696,918))
			self._actions.append('self._window.key_down("CTRL")')
			self._actions.append('self._window.left_click()')
			self._actions.append('self._window.key_up("CTRL")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(364, 120))
			self._actions.append('self._window.right_click()')
			self.moved_ovies = True
						
			
			
			
	def box(self, x1_y1, x2_y2):
		self._actions.append('self._window.set_cursor_pos({},{})'.format(x1_y1[0],x1_y1[1]))
		self._actions.append('self._window.left_click_down()')
		self._actions.append('self._window.set_cursor_pos({},{})'.format(x2_y2[0],x2_y2[1]))
		self._actions.append('self._window.left_click_up()')
	
	def hotkey(self, hotkey):
		self._actions.append('self._window.key_down("CTRL")')
		self._actions.append('self._window.key_down("{}")'.format(hotkey))
		self._actions.append('self._window.key_up("CTRL")')
		self._actions.append('self._window.key_up("{}")'.format(hotkey))			
		
	def make_left_gas(self):
		if not hasattr(self, 'built_left_gas'):
			self._print("A","{} | Making left gas...".format(self.format_game_time()))
			left_gas_loc = (617,174)
			right_gas_loc = (520,445)
		
			self.select_worker()
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("g")')
			if self._spawn_location == 'R':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(right_gas_loc[0], right_gas_loc[1]))
			elif self._spawn_location == 'L':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(left_gas_loc[0], left_gas_loc[1]))
			self._actions.append('self._window.left_click()')
			for i in range(2):
				self._actions.append('time.sleep(3)')
				self.select_worker()
				if self._spawn_location == 'R':
					self._actions.append('self._window.set_cursor_pos({},{})'.format(right_gas_loc[0], right_gas_loc[1]))
				elif self._spawn_location == 'L':
					self._actions.append('self._window.set_cursor_pos({},{})'.format(left_gas_loc[0], left_gas_loc[1]))
				self._actions.append('self._window.right_click()')

			self.built_left_gas = True
		
	def make_right_gas(self):
		if not hasattr(self, 'built_right_gas'):
			self._print("A","{} | Making right gas...".format(self.format_game_time()))
			left_gas_loc = (818,844)
			right_gas_loc = (1312, 838)
		
			self.select_worker()
			self._actions.append('self._window.press_key("b")')
			self._actions.append('self._window.press_key("g")')
			if self._spawn_location == 'R':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(right_gas_loc[0], right_gas_loc[1]))
			elif self._spawn_location == 'L':
				self._actions.append('self._window.set_cursor_pos({},{})'.format(left_gas_loc[0], left_gas_loc[1]))
			self._actions.append('self._window.left_click()')
			for i in range(2):
				self._actions.append('time.sleep(3)')
				self.select_worker()
				if self._spawn_location == 'R':
					self._actions.append('self._window.set_cursor_pos({},{})'.format(right_gas_loc[0], right_gas_loc[1]))
				elif self._spawn_location == 'L':
					self._actions.append('self._window.set_cursor_pos({},{})'.format(left_gas_loc[0], left_gas_loc[1]))
				self._actions.append('self._window.right_click()')

			self.built_right_gas = True	
			
	def rally_overlords(self):
		if not hasattr(self, 'rallied_ovies'):
			self._print("A","{} | Rallying overlords...".format(self.format_game_time()))
			self._actions.append('self._window.press_key("w")')
			# Ovie 1
			if self._spawn_location == 'L':
				self.box((407,86),(997,863))
			elif self._spawn_location == 'R':
				self.box((379,394),(1094,809))
			 
			self._actions.append('self._window.set_cursor_pos({},{})'.format(692,916))
			 
			self._actions.append('self._window.left_click()')
			self._actions.append('self._window.key_down("SHIFT")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(90,946))
			 
			self._actions.append('self._window.right_click()')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(102,901))
			 
			self._actions.append('self._window.right_click()')
			 
			self._actions.append('self._window.key_up("SHIFT")')
			 
			
			# OV 2
			if self._spawn_location == 'L':
				self.box((407,86),(997,863))
			elif self._spawn_location == 'R':
				self.box((379,394),(1094,809))
			self._actions.append('self._window.set_cursor_pos({},{})'.format(746,913))
			 
			self._actions.append('self._window.left_click()')
			self._actions.append('self._window.key_down("SHIFT")')
			self._actions.append('self._window.set_cursor_pos({},{})'.format(150,996))
			 
			self._actions.append('self._window.right_click()')
			 
			self._actions.append('self._window.set_cursor_pos({},{})'.format(180,987))
			self._actions.append('self._window.right_click()')
			 
			self._actions.append('self._window.key_up("SHIFT")')
			
			 
			self.rallied_ovies = True
			self.hotkey_barracks()


	def _get_game_time(self) -> int:
		sc2_seconds = (time.time() - self._start_time) * self._game_speed_ratio
		return sc2_seconds

	def format_game_time(self) -> str:
		m, s = divmod(self._game_time, 60)
		return "{}:{}".format(m,s)	

	def _print(self, message_type: str, message: str) -> None:
		'''
		Print messages to the console
		'''
		# Get the threading lock
		if self._debug:
			print(message_type,":",message)
