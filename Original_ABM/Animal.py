#################################################################
# A tiny spatially-explicit individually based model class.
# Author: Jim Graham
# Date: 3/30/2015
#################################################################

import random
import math
import Veg

#################################################################
# Global values for the class
#################################################################
WIDTH=10 # width of the object on the screen
HEIGHT=10 # height of the object on the screen

TYPE_PREY=1 # definition for  prey item (e.g. sheep)
TYPE_PREDATOR=2 # definition for a predator (e.g. wolf)

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
	#  MaxLifeCycles - how many cycles a prey item lives or the maximum number of cycles between feeding for predator
	#  DistanceToEat - how far a predator needs to be from a prey item to consume it
	#  DistanceToMove - std dev of the amount the object moves on each cycle
	#################################################################
	def __init__(self, TheCanvas, CenterX,CenterY,Type,FillColor,MaxBirthCycles,MaxLifeCycles,DistanceToEat,DistanceToMove):

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
		
		# create the object at the specifed x and y location 
		self.id = self.TheCanvas.create_rectangle(CenterX-WIDTH/2, CenterY-HEIGHT/2,
		    CenterX+WIDTH/2, CenterY+HEIGHT/2,fill=FillColor)

	#################################################################
	# Update the state of the individual
	# This includes:
	# - Subtract 1 from the birth and life counters
	# - Produce offspring if the birth counter is 0
	# - Die if the life counter is 0
	# - For predators, if a prey item is within reach, eat it
	# - If the individual survived, update it's movement
	#################################################################	
	def Update(self,TheAnimals,TheGrass):
		# update the counters

		self.BirthCounter=self.BirthCounter-1
		self.LifeCounter=self.LifeCounter-1
		
		# check for death
		if (self.LifeCounter<=0): # died
			self.TheCanvas.delete(self.id)
			TheAnimals.remove(self)
			#if self.Type==TYPE_PREDATOR: print("Predator died")
			#else: print("Prey died")
		else: # did not die, update other stuff
			
			# See if there was a birth
			if (self.BirthCounter<=0):
				NewBorn=AnimalClass(self.TheCanvas, self.CenterX, self.CenterY,
				    self.Type,self.FillColor,self.MaxBirthCycles,self.MaxLifeCycles,self.DistanceToEat,self.DistanceToMove)
				TheAnimals.append(NewBorn)
				#if self.Type==TYPE_PREDATOR: print("Predator born") # For debugging
				#else: print("Prey born")
				self.BirthCounter=self.MaxBirthCycles
		
			# look for interactions
			if self.Type==TYPE_PREDATOR: # self is a predator
				for TheItem in TheAnimals: # look for prey that is close enough to eat
					if TheItem.Type==TYPE_PREY: # see if the predator ate the prey
						DistanceX=abs(self.CenterX-TheItem.CenterX)
						DistanceY=abs(self.CenterY-TheItem.CenterY)
						if (DistanceX<self.DistanceToEat) and (DistanceY<self.DistanceToEat):
							TheAnimals.remove(TheItem)
							self.TheCanvas.delete(TheItem.id)
							self.LifeCounter=self.MaxLifeCycles
							#print("Sheep was eaten") # For debugging
			else: # self is prey
				if (TheGrass.EatGrass(self.CenterX,self.CenterY)): 
					self.LifeCounter=self.MaxLifeCycles
				else:
					self.LifeCounter=self.LifeCounter-1
			
			########################################################################
			# Move self by a random amount
			
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


		