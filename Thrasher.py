
import numpy as np
class Thrasher():
	def __init__(self, name, coords):
		self.name = name
		self.coords = coords
		self.d = 8
		
	def is_alive(self, screen_state, debug=False):
		thrasher_alive = False
		for i in range(len(self.coords)):
			if self.indiv_thrasher_alive(screen_state, i, debug=debug):
				thrasher_alive = True
				#print("True")
				#break
			#else:
				#print("False")
		#print("{:5s} | {:3.2f} | {:3.2f} | {:3.2f}".format(str(alive), R,G,B))
		#print("{:5s}".format(str(thrasher_alive)))
		return thrasher_alive
				
	def get_state_and_rallypoint(self, screen_state):
		thrasher_num = None
		thrasher_rallypoint = None
		for i in range(len(self.coords)):
			if self.indiv_thrasher_alive(screen_state, i):
				thrasher_num = i
				thrasher_rallypoint = self.coords[i]
				break
		return '{}_{}'.format(self.name,thrasher_num), 	thrasher_rallypoint	
		
	def indiv_thrasher_alive(self, screen_state, thrasher_idx, debug=False):
		x1 = self.coords[thrasher_idx][0] - self.d
		y1 = self.coords[thrasher_idx][1] - self.d 
		x2 = self.coords[thrasher_idx][0] + self.d
		y2 = self.coords[thrasher_idx][1] + self.d
		
		R = np.mean(screen_state[0,x1:x2, y1:y2])
		G = np.mean(screen_state[1,x1:x2, y1:y2])
		B = np.mean(screen_state[2,x1:x2, y1:y2])
		#alive = R > 35 and R < 60 and G > 85 and G < 130# and B > 35 and B < 70
		if debug:
			print("{} {:3.2f} | {:3.2f} | {:3.2f}".format(thrasher_idx, R,G,B))
		#print(G)
		alive = G > 75
		return alive
