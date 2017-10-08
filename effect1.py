import os.path
import pygame.mixer, pygame.time
import pygame, sys, random
from pykinect2 import PyKinectRuntime
from pykinect2 import PyKinectV2
class Effect1:


	def __init__(self,pygame, main_dir, mixer, FPSCLOCK, FPS):
		self.FIRE = pygame.image.load('fire.png')
		self.PIXEL = pygame.image.load('fire_yellow.png')
		self.FIRE_YELLOW = pygame.image.load('green_yellow.png')
		self.main_dir = main_dir
		self.mixer = mixer
		self.FPSCLOCK = FPSCLOCK
		self.FPS = FPS
		file_path = os.path.join(self.main_dir,'data','Broom2.wav')
		self.sound = self.mixer.Sound(file_path)

	def prepare(self):

	
		
		particles = 1000
		particle_xysize = []
		while particles > 0:	
			particle_xysize.append([0,0,0,0,0,0,0,(0,0,0),(0,0)])
			particles -= 1
		
		for element in range(len(particle_xysize)):
			particle_xysize[element][2] = 10
			particle_xysize[element][4] = random.randint(0,1)
		velocity = []
		for particle in particle_xysize:
			velocity.append(random.randint(1, 10))
		
		mouse_x = 0
		mouse_y = 0
		mouse_x_old = 0
		mouse_y_old = 0
		random_numbers = [1, -1]
		
		# Reset Values
		for integer in velocity:
			integer *= random.sample(random_numbers, 1)[0]
						
		for direction in range(len(particle_xysize)):
			particle_xysize[direction][3] = random.sample(random_numbers, 1)[0]
			particle_xysize[direction][4] = random.sample(random_numbers, 1)[0]
			particle_xysize[direction][8] = (random.randint(1,2), random.randint(1,2))
			
		traegheit = 0

		gkinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
		hkinect = pygame.Surface((gkinect.color_frame_desc.Width, gkinect.color_frame_desc.Height), 0, 32)

		return hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old,  particle_xysize,velocity, random_numbers, gkinect

	def show(self,DISPLAYSURF, hkinect, mouse_x, mouse_y, mouse_x_old, mouse_y_old,  particle_xysize,velocity, random_numbers, gkinect):
		bodies = None
		if gkinect.has_new_body_frame(): 
			bodies = gkinect.get_last_body_frame()

		if bodies is not None:
			for i in range(0, gkinect.max_body_count):
				body = bodies.bodies[i]
				if not body.is_tracked: 
				    continue 

				joints = body.joints 
				jointPoints = gkinect.body_joints_to_color_space(joints)
		
				joint0 = PyKinectV2.JointType_SpineMid
				joint1 = PyKinectV2.JointType_SpineBase


				try:
					joint0State = joints[joint0].TrackingState;
					joint1State = joints[joint1].TrackingState;

					# both joints are not tracked
					if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
					    continue

					# both joints are not *really* tracked
					if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
					    continue

					# ok, at least one is good 
					start = (jointPoints[joint0].x, jointPoints[joint0].y)
					end = (jointPoints[joint1].x, jointPoints[joint1].y)
				except Exception as e:
					continue
				mouse_x, mouse_y = start

				try:
					pygame.draw.line(hkinect, color, start, end, 8)
				except Exception as e:
					continue

		x = int(mouse_x)
		x_old = int(mouse_x_old)

		y = int(mouse_y)
		y_old = int(mouse_y_old)

		diff  = (x - x_old) - (y - y_old)

		if diff < -200 or diff > 200:
			self.sound.play()

		mouse_x_old = mouse_x


		# Fill the Display for new objects to be drawn
		DISPLAYSURF.fill((0, 0, 0))
		# Draw Elements
		for element in range(len(particle_xysize)):
			width = particle_xysize[element][2]
			height = particle_xysize[element][2]
			particle_x = particle_xysize[element][0]
			particle_y = particle_xysize[element][1]
			addition = particle_xysize[element][6]
			influence = particle_xysize[element][8]
			color = particle_xysize[element][7]
		
			particle_x += (velocity[element] + addition * influence[0] / 4) * particle_xysize[element][4]
			particle_y += (velocity[element] + addition * influence[1] / 4) * particle_xysize[element][3]
			
			if particle_xysize[element][5] == 0:
				firesmall = pygame.transform.scale(self.FIRE, (int(width), int(height)))
				#pygame.draw.rect(DISPLAYSURF, color, (particle_x - width / 2, particle_y - height / 2, width, height))
				DISPLAYSURF.blit(firesmall,[particle_x - width / 2,particle_y - height / 2])
			elif particle_xysize[element][5] == 1:
				#pygame.draw.circle(DISPLAYSURF, color, (particle_x - int(width / 2), particle_y - int(height / 2)), int(width))		
				white = pygame.transform.scale(self.PIXEL, (int(width / 4), int(height / 4)))
				DISPLAYSURF.blit(white,[particle_x - width / 2,particle_y - height / 2])
			elif particle_xysize[element][5] == 2:
				fire_yellow = pygame.transform.scale(self.FIRE_YELLOW, (int(width * 2), int(height * 2)))
				DISPLAYSURF.blit(fire_yellow,[particle_x - width,particle_y - height])
				
			if particle_xysize[element][2] > 0:
				particle_xysize[element][2] -= 0.5
				velocity[element] += 1
				if particle_xysize[element][6] < 50:
					particle_xysize[element][6] += 1
			else:
				while True:
					particle_xysize[element][3] = random.sample(random_numbers, 1)[0]
					particle_xysize[element][4] = random.sample(random_numbers, 1)[0]
					particle_xysize[element][5] = random.randint(0,2)
					particle_xysize[element][7] = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
					particle_xysize[element][6] = 0
					particle_xysize[element][8] = (random.randint(1,40), random.randint(1,40))
					if random.randint(1, 50) > 4:
						particle_xysize[element][2] = random.randint(1, 40)
					velocity[element] = random.randint(1, 1)
					particle_xysize[element][0], particle_xysize[element][1] = mouse_x, mouse_y
					break
					
		pygame.display.update()
		self.FPSCLOCK.tick(self.FPS)