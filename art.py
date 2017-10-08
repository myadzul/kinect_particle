

import pygame

from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
import os, sys

from effect1 import Effect1
from effect2 import Effect2
from pygame.locals import *

mixer = pygame.mixer
time = pygame.time

main_dir = os.path.split(os.path.abspath(__file__))[0]


FPS = 30
WINDOWWIDTH = 1900
WINDOWHEIGHT = 1070


KINECTEVENT = pygame.USEREVENT

pygame.display.set_caption("Installation art")

# def toggle_fullscreen():
# 	screen = pygame.display.get_surface()
# 	tmp = screen.convert()
# 	caption = pygame.display.get_caption()
# 	cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
# 	w,h = screen.get_width(),screen.get_height()
# 	flags = screen.get_flags()
# 	bits = screen.get_bitsize()
    
# 	pygame.display.quit()
# 	pygame.display.init()
    
# 	screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
# 	screen.blit(tmp,(0,0))
# 	pygame.display.set_caption(*caption)

# 	pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

# 	pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

# 	return screen

def draw_text(text):
	wincolor = 40, 40, 90
	fg = 250, 240, 230
   	bg = 5, 5, 5

	#fill background
	DISPLAYSURF.fill(wincolor)

    #load font, prepare values
   	font = pygame.font.Font(None, 80)
   	size = font.size(text)

    #no AA, no transparancy, normal
   	ren = font.render(text, 0, fg, bg)
   	DISPLAYSURF.blit(ren, (10, 10))

def wait_for_keyboard_press():
	pygame.display.flip()
 	while 1:
        #use event.wait to keep from polling 100% cpu
		if pygame.event.wait().type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN): break

def main():
	global FPSCLOCK, DISPLAYSURF, gkinect
	pygame.init()
	#pygame.display.set_mode((640,480),pygame.FULLSCREEN)
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.mouse.set_visible(1)
	mixer.init(11025) #raises exception on fail

	#
	# Show intro
	#

	#toggle_fullscreen()

	fg = 250, 240, 230
	bg = 5, 5, 5
	wincolor = 118, 122, 121

	font = pygame.font.Font(None, 100)
	text = 'Welcome to the Escapism'
	size = font.size(text)

	DISPLAYSURF.fill(wincolor)

	a_sys_font = pygame.font.SysFont("Bebas Neue", 100)

	#AA, no transparancy, bold
	ren = a_sys_font.render(text, 1, fg)
	DISPLAYSURF.blit(ren, (500, 200 + size[1]))

	wait_for_keyboard_press()

	#
	# Show effects
	#

	current_effect = 0
	old_effect = -1

	ef1 = Effect1(pygame, main_dir, mixer, FPSCLOCK, FPS)
	ef2 = Effect2(pygame, main_dir, mixer, FPSCLOCK, FPS)

	while True:
	
		# Get Events of Game Loop
		for event in pygame.event.get():
			if event.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
				current_effect += 1

		bodies = None

		if current_effect != old_effect:
			if current_effect == 0:
				hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old,  particle_xysize,velocity,random_numbers,gkinect = ef1.prepare()
			elif current_effect == 1:
				hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old,  particle_xysize,velocity,random_numbers,gkinect = ef2.prepare()
			old_effect = current_effect

		if current_effect == 0:
			ef1.show(DISPLAYSURF, hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old, particle_xysize,velocity, random_numbers,gkinect)
		elif current_effect == 1:
			ef2.show(DISPLAYSURF, hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old, particle_xysize,velocity, random_numbers,gkinect)
		else:
			pygame.quit()
			sys.exit()




if __name__ == '__main__':
	main()
	
	
	
	
	
	
	
