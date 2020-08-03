#################################################################
# A tiny spatially-explicit individually based model class.
# Author: Jim Graham
# Modified by: Melissa Kimble
# Modification Date: 4/21/2015
#################################################################

import random
import math
import Veg

#################################################################
# Global values for the class
#################################################################
WIDTH=10 # width of the object on the screen
HEIGHT=10 # height of the object on the screen

TYPE_HUMAN=1 # definition for  HUMAN item (e.g. sheep)
TYPE_ZOMBIE=2 # definition for a ZOMBIE (e.g. wolf)

#################################################################
# The class definition
#################################################################

class AnimalClass:
	#################################################################
	# Initialize the new object
	# Inputs:
	#  TheCanvas - the canvas widget that the blob will appear in
	#  CenterX - horizontal position of the object in the canvas
	#  CenterY - vertical position of the object in the canvas
	#  FillColor - the color of the Blob
	#  MaxBirthCycles - number of cycles before recruitment
	#  MaxLifeCycles - how many cycles a HUMAN item lives or the maximum number of cycles between feeding for ZOMBIE
	#  DistanceToEat - how far a ZOMBIE needs to be from a HUMAN item to consume it
	#  DistanceToMove - std dev of the amount the object moves on each cycle
	#  DistanceToRun - how far a HUMAN needs to be from a ZOMBIE for the human to run
	#  DistanceToRun - how far a ZOMBIE needs to be from a HUMAN for the zombie to chase
	#  DistanceToShoot - how far a HUMAN needs to be from a ZOMBIE for the human to shoot it
	#  Ammo - how much ammo the HUMAN has
	#################################################################
	def __init__(self, TheCanvas, CenterX,CenterY,Type,FillColor,MaxBirthCycles,MaxLifeCycles,DistanceToEat,DistanceToMove,DistanceToRun,DistanceToChase,DistanceToShoot,Ammo):

		# Save the values that are passed in so we can access them in the Update() function
		self.TheCanvas = TheCanvas 

		self.CenterX=CenterX
		self.CenterY=CenterY
		
		self.Type=Type
		self.FillColor=FillColor
		
		self.MaxBirthCycles=MaxBirthCycles
		self.BirthCounter=MaxBirthCycles
		
		self.MaxLifeCycles=MaxLifeCycles
		self.LifeCounter=MaxLifeCycles
		
		self.DistanceToEat=DistanceToEat
		self.DistanceToMove=DistanceToMove
		
		self.DistanceToRun=DistanceToRun
		self.DistanceToChase=DistanceToChase
		
		self.Ammo=Ammo
		
		self.DistanceToShoot=DistanceToShoot
		
		
		# create the object at the specifed x and y location 
		self.id = self.TheCanvas.create_rectangle(CenterX-WIDTH/2, CenterY-HEIGHT/2,
		    CenterX+WIDTH/2, CenterY+HEIGHT/2,fill=FillColor)

	#################################################################
	# Update the state of the individual
	# This includes:
	# - Subtract 1 from the birth and life counters (HUMAN)
	# - Produce offspring if the birth counter is 0 (HUMAN)
	# - Die if the life counter is 0 (HUMAN)
	# - For ZOMBIEs, if a HUMAN item is within reach, eat it and turn it into a zombie
	# - for HUMANS, if ZOMBIE is within reach, shoot it and -1 ammo.
	# - If the individual survived, update it's movement
	#################################################################	
	def Update(self,TheAnimals,TheFood):
		# update the counters

		self.BirthCounter=self.BirthCounter-1
		self.LifeCounter=self.LifeCounter-1
		
		# check for death; zombies don't die. 
		if (self.LifeCounter<=0) and self.Type==TYPE_HUMAN: # The human died
			self.TheCanvas.delete(self.id)
			TheAnimals.remove(self)
			print("Human died")
			#if self.Type==TYPE_ZOMBIE: print("ZOMBIE died")
			#else: print("HUMAN died")
		else: # did not die, update other stuff
			
			# See if there was a birth; zombies don't give birth.
			if (self.BirthCounter<=0) and self.Type==TYPE_HUMAN:
				NewBorn=AnimalClass(self.TheCanvas, self.CenterX, self.CenterY,
				    self.Type,self.FillColor,self.MaxBirthCycles,self.MaxLifeCycles,self.DistanceToEat,self.DistanceToMove,self.DistanceToRun,self.DistanceToChase,self.DistanceToShoot,self.Ammo)
				TheAnimals.append(NewBorn)
				#if self.Type==TYPE_ZOMBIE: print("ZOMBIE born") # For debugging
				#else: print("HUMAN born")
				self.BirthCounter=self.MaxBirthCycles
		
			# look for interactions
			if (self.Ammo>0) and self.Type==TYPE_HUMAN: # self is a HUMAN and the human has at least 1 Ammo.
				for TheItem in TheAnimals: # look for ZOMBIE that is close enough to shoot
					if TheItem.Type==TYPE_ZOMBIE: # see if the Human SHOT the ZOMBIE
						DistanceX=abs(self.CenterX-TheItem.CenterX)
						DistanceY=abs(self.CenterY-TheItem.CenterY)
						if (DistanceX<self.DistanceToShoot) and (DistanceY<self.DistanceToShoot):
							TheAnimals.remove(TheItem)
							self.TheCanvas.delete(TheItem.id)
							self.Ammo=self.Ammo-1 # used ammo, so ammo is reduced by one.
							print("Zombie was shot") # For debugging
							
			if self.Type==TYPE_ZOMBIE: # self is a ZOMBIE
				for TheItem in TheAnimals: # look for HUMAN that is close enough to eat
					if TheItem.Type==TYPE_HUMAN: # see if the ZOMBIE ate the HUMAN
						DistanceX=abs(self.CenterX-TheItem.CenterX)
						DistanceY=abs(self.CenterY-TheItem.CenterY)
						if (DistanceX<self.DistanceToEat) and (DistanceY<self.DistanceToEat):
							TheAnimals.remove(TheItem)
							self.TheCanvas.delete(TheItem.id)
							self.LifeCounter=self.MaxLifeCycles
							print("Human was eaten, and a zombie was born!") # For debugging; A new zombie is born!!
							NewBorn=AnimalClass(self.TheCanvas, self.CenterX, self.CenterY,
									    self.Type,self.FillColor,self.MaxBirthCycles,self.MaxLifeCycles,self.DistanceToEat,self.DistanceToMove,self.DistanceToRun,self.DistanceToChase,self.DistanceToShoot,self.Ammo)
							TheAnimals.append(NewBorn)
							self.BirthCounter=self.MaxBirthCycles
			else: # self is HUMAN
				if (TheFood.EatFood(self.CenterX,self.CenterY)): # call function to eat food and reset life cycle.
					self.LifeCounter=self.MaxLifeCycles
				else:
					self.LifeCounter=self.LifeCounter-1
				if (TheFood.UseAmmo(self.CenterX,self.CenterY)): # call function to grab ammo and increase +1
					self.Ammo=self.Ammo+1
					#print (self.Ammo)
			
			########################################################################
		
			# the chase starts here - if a zombie is near a human, the zombie will chase the human (DistanceToChase), 
			# but the human will also run (DistanceToRun). If none are nearby, the movement is random (DistanceToMove)
		
			if self.Type==TYPE_ZOMBIE:
				for TheItem in TheAnimals:
					if TheItem.Type==TYPE_HUMAN:
						DistanceX=abs(self.CenterX-TheItem.CenterX)
						DistanceY=abs(self.CenterY-TheItem.CenterY)
						if (DistanceX<self.DistanceToChase) and (DistanceY<self.DistanceToChase):
							self.CenterX+=DistanceX/10
							self.CenterY+=DistanceY/10						
							if self.CenterX < 0:
								self.CenterX=self.TheCanvas.winfo_width()-1
							if self.CenterX>= self.TheCanvas.winfo_width():
								self.CenterX = 0
						
							if self.CenterY < 0:
								self.CenterY=self.TheCanvas.winfo_height()-1
							if self.CenterY>= self.TheCanvas.winfo_height():
								self.CenterY = 0							
							
							self.TheCanvas.coords(self.id, self.CenterX-WIDTH/2, self.CenterY-HEIGHT/2,
									      self.CenterX+WIDTH/2, self.CenterY+HEIGHT/2)
						else:
							# Move self by a random amount if there are no humans nearby
							
							self.CenterX+=random.gauss(0,self.DistanceToMove)
							self.CenterY+=random.gauss(0,self.DistanceToMove)
							
							# if self has moved off the frame, reverse the direction of movement
							if self.CenterX < 0:
								self.CenterX=self.TheCanvas.winfo_width()-1
							if self.CenterX>= self.TheCanvas.winfo_width():
								self.CenterX = 0
					
							if self.CenterY < 0:
								self.CenterY=self.TheCanvas.winfo_height()-1
							if self.CenterY>= self.TheCanvas.winfo_height():
								self.CenterY = 0
					
							# update the position
							self.TheCanvas.coords(self.id, self.CenterX-WIDTH/2, self.CenterY-HEIGHT/2,
								self.CenterX+WIDTH/2, self.CenterY+HEIGHT/2)							
			if self.Type==TYPE_HUMAN:
				for TheItem in TheAnimals:
					if TheItem.Type==TYPE_ZOMBIE:
						DistanceX=abs(self.CenterX-TheItem.CenterX)
						DistanceY=abs(self.CenterY-TheItem.CenterY)
						if (DistanceX<self.DistanceToRun) and (DistanceY<self.DistanceToRun):
							self.CenterX-=DistanceX/5
							self.CenterY-=DistanceY/5					
							if self.CenterX < 0:
								self.CenterX=self.TheCanvas.winfo_width()-1
							if self.CenterX>= self.TheCanvas.winfo_width():
								self.CenterX = 0
						
							if self.CenterY < 0:
								self.CenterY=self.TheCanvas.winfo_height()-1
							if self.CenterY>= self.TheCanvas.winfo_height():
								self.CenterY = 0							
							
							self.TheCanvas.coords(self.id, self.CenterX-WIDTH/2, self.CenterY-HEIGHT/2,
									      self.CenterX+WIDTH/2, self.CenterY+HEIGHT/2)
						else:
							# Move self by a random amount if there are zombies nearby.
							
							self.CenterX+=random.gauss(0,self.DistanceToMove)
							self.CenterY+=random.gauss(0,self.DistanceToMove)
							
							# if self has moved off the frame, reverse the direction of movement
							if self.CenterX < 0:
								self.CenterX=self.TheCanvas.winfo_width()-1
							if self.CenterX>= self.TheCanvas.winfo_width():
								self.CenterX = 0
					
							if self.CenterY < 0:
								self.CenterY=self.TheCanvas.winfo_height()-1
							if self.CenterY>= self.TheCanvas.winfo_height():
								self.CenterY = 0
					
							# update the position
							self.TheCanvas.coords(self.id, self.CenterX-WIDTH/2, self.CenterY-HEIGHT/2,
								self.CenterX+WIDTH/2, self.CenterY+HEIGHT/2)

		