#################################################################
# A tiny class to create a field of grass for herbivores to eat.
# Author: Jim Graham
# Date: 3/30/2015
#
# The class simulates "grass", or any veg that is available for
# consumption by herbivores.  The grass is in a grid of cells
# and can either be present or not.  Each cell contains either 
# the object id for the rectangle on the screen (a positive integer)
# or a negative number that is a count of the number of cycles
# until the grass "regrows".
#################################################################

import random
import math

#################################################################
# Global values for the class
#################################################################

WIDTH=10 # width of each cell of grass on the screen
HEIGHT=10 # height of each cell of grass on the screen

NUM_ROWS=50 # Number of cells of grass vertically
NUM_COLUMNS=50 # Number of cells of grass horizontally

#################################################################
# The class definition
#################################################################

class Veg:
	#################################################################
	# Private function to add grass to a cell
	#################################################################
	def AddGrass(self,Row,Column):
		X=Column*WIDTH
		Y=Row*HEIGHT
		self.TheGrid[Row][Column] = self.TheCanvas.create_rectangle(X,Y,X+WIDTH, Y+HEIGHT,fill="green")
		self.TheCanvas.lower(self.TheGrid[Row][Column])

	#################################################################
	# Initialize the new object
	# Inputs:
	#  TheCanvas - the canvas widget that the grass will appear in
	#  PercentFull - how much of the grass is initially available
	#  RegrowCycles - number of cycles until the grass is regrown after being eaten
	#################################################################
	def __init__(self, TheCanvas,PercentFull,RegrowCycles):
		self.RegrowCycles=RegrowCycles;
		
		# Save the values that are passed in so we can access them in the Update() function
		self.TheCanvas = TheCanvas 

		# Create the two-dimensional array to hold the number of regrow cycles 
		self.TheGrid= [[0 for i in range(NUM_COLUMNS)] for j in range(NUM_ROWS)]
		
		# Setup the initial grass state based on percent cover
		ProportionFull=PercentFull/100.0 # compute proportion based on the percent cover
		
		Row=0
		while (Row<NUM_ROWS): # For each row
			Column=0
			while (Column<NUM_COLUMNS): # For each cell in each row
				self.TheGrid[Row][Column]=int(random.uniform(-RegrowCycles,0)) # Set a random regrow duration
				if (random.uniform(0,1)<ProportionFull): # if 0 to 1 random value is greater than proportion,
					self.AddGrass(Row,Column) # add grass to this cell
				Column=Column+1
			Row=Row+1
		
	#def HasGrass(self,X,Y):
		#Row=int(Y/WIDTH)
		#Column=int(X/HEIGHT)
		#Result=self.TheGrid[Row][Column]
		#if (Result<=0): Result=False
		#else: Result=True
		#return(Result)
	
	#################################################################
	# Allows the consuption of grass at the specified location if
	# grass is available
	# Inputs:
	#   X - Horizontal location in pixels
	#   Y - vertical location in pixels
	# Output:
	#   True if grass was consumed
	#   False if there was no grass available for consumption
	#################################################################
	def EatGrass(self,X,Y):
		# Find the row and column the coordinate is in
		Row=int(Y/WIDTH)
		Column=int(X/HEIGHT)
		# Get the number of cycles to regrows (negative if regrowing)
		CyclesToRegrow=self.TheGrid[Row][Column]
		# Determine if there is grass (>0) or not (<=0)
		if (CyclesToRegrow<=0): 
			Result=False # Grass is regrowing so there is none for consuption
		else: 
			Result=True # There is grass
			# Eat the grass
			self.TheCanvas.delete(self.TheGrid[Row][Column]) # Remove the grass from the canvas
			self.TheGrid[Row][Column]=-self.RegrowCycles # Set the number of cycles to regrow
		return(Result)
	
	#################################################################
	# Update the state of each cell.
	# If the grass is not present this means incrementing the counter
	# When the counter reaches 0, the grass is "regrow".
	#################################################################
	def Update(self):
		# Setup a local variable for the grid just for readability
		TheGrid=self.TheGrid
		
		# update the cells
		Row=0
		while (Row<50):
			Column=0
			while (Column<50):
				if (TheGrid[Row][Column]<0): # add to counter to grow grass
					TheGrid[Row][Column]=TheGrid[Row][Column]+1
				elif (TheGrid[Row][Column]==0): # add grass
					self.AddGrass(Row,Column)
				Column=Column+1
			Row=Row+1
