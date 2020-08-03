#################################################################
# A tiny class to create a field of Food for HUMANS to eat.
# Author: Jim Graham
# Modified by: Melissa Kimble
# Modified Date: 4/21/2015
#
# The class simulates "Food/Ammo", or any veg/ammo that is available for
# consumption by HUMANS.  The Food/Ammo is in a grid of cells
# and can either be present or not.  Each cell contains either 
# the object id for the rectangle on the screen (a positive integer)
# or a negative number that is a count of the number of cycles
# until the Food "regrows".
#################################################################

import random
import math

#################################################################
# Global values for the class
#################################################################

WIDTH=10 # width of each cell of Food on the screen
HEIGHT=10 # height of each cell of Food on the screen

NUM_ROWS=50 # Number of cells of Food vertically
NUM_COLUMNS=50 # Number of cells of Food horizontally

TYPE_AMMO=1 # definition for  ammo item (e.g. bullets)
TYPE_FOOD=2 # definition for a vegetation (e.g. Food)

#################################################################
# The class definition
#################################################################

class Veg:
	#################################################################
	# Private function to add Food/Ammo to a cell
	#################################################################
	def AddFood(self,Row,Column):
		X=Column*WIDTH
		Y=Row*HEIGHT
		self.TheGrid[Row][Column] = self.TheCanvas.create_rectangle(X,Y,X+WIDTH, Y+HEIGHT,fill="green")
		self.TheCanvas.lower(self.TheGrid[Row][Column])
		
	def AddAmmo(self,Row,Column):
		X=Column*WIDTH
		Y=Row*HEIGHT
		self.TheGrid[Row][Column] = self.TheCanvas.create_rectangle(X,Y,X+WIDTH, Y+HEIGHT,fill="pale goldenrod")
		self.TheCanvas.lower(self.TheGrid[Row][Column])

	#################################################################
	# Initialize the new object
	# Inputs:
	#  TheCanvas - the canvas widget that the Food will appear in
	#  PercentFull - how much of the Food is initially available
	#  RegrowCycles - number of cycles until the Food is regrown after being eaten
	#  Type - vegetation type (food or ammo) 
	#################################################################
	def __init__(self, TheCanvas,PercentFull,RegrowCycles, Type):
		self.RegrowCycles=RegrowCycles;
		self.Type=Type
		# Save the values that are passed in so we can access them in the Update() function
		self.TheCanvas = TheCanvas 

		# Create the two-dimensional array to hold the number of regrow cycles 
		self.TheGrid= [[0 for i in range(NUM_COLUMNS)] for j in range(NUM_ROWS)]
		
		# Setup the initial Food state based on percent cover
		ProportionFull=PercentFull/100.0 # compute proportion based on the percent cover
		
		Row=0
		while (Row<NUM_ROWS): # For each row
			Column=0
			while (Column<NUM_COLUMNS): # For each cell in each row
				self.TheGrid[Row][Column]=int(random.uniform(-RegrowCycles,0)) # Set a random regrow duration
				if (random.uniform(0,1)<ProportionFull): # if 0 to 1 random value is greater than proportion,
					Type=random.randint(1,100)
					if (Type==1): # if the random number is 1, then Food will grow. If it is 0, then ammo will grow. 
						self.AddAmmo(Row,Column) #add ammo to this cell
						self.Type=TYPE_AMMO						
					else:
						self.AddFood(Row,Column) # add Food to this cell
						self.Type=TYPE_FOOD
				Column=Column+1
			Row=Row+1
		
	#def HasFood(self,X,Y):
		#Row=int(Y/WIDTH)
		#Column=int(X/HEIGHT)
		#Result=self.TheGrid[Row][Column]
		#if (Result<=0): Result=False
		#else: Result=True
		#return(Result)
	
	#################################################################
	# Allows the consumption of Food/Ammo at the specified location if
	# Food/Ammo is available
	# Inputs:
	#   X - Horizontal location in pixels
	#   Y - vertical location in pixels
	# Output:
	#   True if Food/Ammo was consumed
	#   False if there was no Food/Ammo available for consumption
	#################################################################
	def EatFood(self,X,Y):
		# Find the row and column the coordinate is in
		Row=int(Y/WIDTH)
		Column=int(X/HEIGHT)
		# Get the number of cycles to regrows (negative if regrowing)
		CyclesToRegrow=self.TheGrid[Row][Column]
		# Determine if there is Food (>0) or not (<=0)
		if (CyclesToRegrow<=0): 
			Result=False # Food is regrowing so there is none for consuption
		else: 
			Result=True # There is Food
			# Eat the Food
			if self.Type==TYPE_FOOD:
				self.TheCanvas.delete(self.TheGrid[Row][Column]) # Remove the Food from the canvas
				self.TheGrid[Row][Column]=-self.RegrowCycles # Set the number of cycles to regrow
		return(Result)
	

	def UseAmmo(self,X,Y):
		# Find the row and column the coordinate is in
		Row=int(Y/WIDTH)
		Column=int(X/HEIGHT)
		# Get the number of cycles to regrows (negative if regrowing)
		CyclesToRegrow=self.TheGrid[Row][Column]
		# Determine if there is Food (>0) or not (<=0)
		if (CyclesToRegrow<=0): 
			Result=False # Food is regrowing so there is none for consuption
		else: 
			Result=True # There is Food
			# Eat the Food
			if self.Type==TYPE_AMMO:
				self.TheCanvas.delete(self.TheGrid[Row][Column]) # Remove the Food from the canvas
				self.TheGrid[Row][Column]=-self.RegrowCycles # Set the number of cycles to regrow
		return(Result)
	
	#################################################################
	# Update the state of each cell.
	# If the Food is not present this means incrementing the counter
	# When the counter reaches 0, the Food is "regrow".
	# Randomly select a number between 1 and 100; if it is 1, AMMO will spawn, else = food. 
	#################################################################
	def Update(self):
		# Setup a local variable for the grid just for readability
		TheGrid=self.TheGrid
		# update the cells
		Row=0
		while (Row<50):
			Column=0
			while (Column<50):
				if (TheGrid[Row][Column]<0): # add to counter to grow Food
					TheGrid[Row][Column]=TheGrid[Row][Column]+1
				elif (TheGrid[Row][Column]==0): # add Food
					Type=random.randint(1,100)
					if (Type==1): # if the random number is 1, then Food will grow. If it is 0, then ammo will grow. 
						self.AddAmmo(Row,Column) #add ammo to this cell
						self.Type=TYPE_AMMO						
					else:
						self.AddFood(Row,Column) # add Food to this cell
						self.Type=TYPE_FOOD
				Column=Column+1
			Row=Row+1
