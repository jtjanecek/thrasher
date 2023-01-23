import time
from MyWinApi import MyWinApi

import numpy as np
from PIL import ImageGrab
from MyWinApi import MyWinApi
win = MyWinApi(1920,1080,0)

#win.set_cursor_pos(215, 870)
#time.sleep(1)
#win.right_click()
import win32gui
import sys
from Thrasher import Thrasher

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
        print(R, G, B)
        return R > 65 and R < 70 and G < 41 and G > 37 and B > 26 and B < 31

'''
while 1:
        print(game_alive(np.array(ImageGrab.grab()).T))
        time.sleep(.1)
'''

while(True):
	time.sleep(.5)
	flags, hcursor, (x,y) = win32gui.GetCursorInfo()
	print(x, y)


win = MyWinApi(1920,1080,0)
win.set_cursor_pos(934, 67)
#win.set_cursor_pos(892, 19)
sys.exit()



win.set_cursor_pos(341,25)
win.left_click()
sys.exit()

while True:
	screen_state = np.array(ImageGrab.grab()).T
	#print(screen_state.shape)
	x1 = 282
	y1 = 58
	x2 = 1631
	y2 = 919
	R = np.mean(screen_state[0,x1:x2, y1:y2])
	G = np.mean(screen_state[1,x1:x2, y1:y2])
	B = np.mean(screen_state[2,x1:x2, y1:y2])
	print(R,G,B)
	test = R > 1 and R < 3 and G > 13 and G < 15 and B > 32 and B < 33
	print(test)
	time.sleep(1)
	#return test


while True:
	if test():
		win.set_cursor_pos(338, 24)
		win.left_click()









