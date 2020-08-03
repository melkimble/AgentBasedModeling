#################################################################
# The simplest possible Spatially-Explicit-Individually Based Model (SEIBM)
# This file and its associated modules (Animal.py and Veg.py) implement
# a three trophic level spatial model.  "Veg" is the vegetation or grass.
# Animals are Sheep and Wolves where the sheep feed on the grass and 
# the wolves feed on the sheep.
#
# The model beings with:
# - Certain percent cover of grass
# - Specified number of sheep
# - Specified number of wolves
#
# The model repeats in an infinite number of "cycles".  Each cycle 
# repesents about a month for the default setup but this is really 
# arbitrary and can have different meanings.  On each cycle the
# model is updated as follows:
# - If a patch of grass is empty and enough cycles has passed, the
#   grass will reappear and be available for eating
# - If a sheep is close enough to grass, it will eat it
# - If a sheep has gone a specified number of cycles without eating,
#   it will die
# - if a sheep has gone a specified number of cycles from their last
#   birth, they will birth another sheep
# - If a wolf is within a specified distance from a sheep, it will eat it
# - If a wolf has gone a specified number of cycles from their last
#   birth, they will birth another wolf
#
# This model technically models just the female sheep (or other herbivore)
# and wolves (predator).  It could also be interpreted as modeling
# flocks of sheep and packs of wolves.  The model could be modified in 
# a variety of ways to model other species and in different ways.
#
# Author: Jim Graham
# Date: 4/2/2015
#################################################################

# Import standard Python libraries
from Tkinter import * # import the GUI library (windows and UI controls)
import time # bring in the time library so we can "wait" between drawing
import random # import functions to create random numbers

# Import our custom modules
import Animal # module with the class to create prey and predators
import Veg # module for stuff for prey to eat (herbs for herbivores)

#################################################################
# Model constants (modify these to see different model effects)
#################################################################

PERCENT_GRASS_COVER=50 # Starting cover of grass (50) 
GRASS_REGROW_CYCLES=10 # Number of cycles to regrow one patch of grass (100)

NUM_SHEEP=100 # number of sheep to start with
SHEEP_BIRTH_CYCLES=20 # number of cycles before each sheep repoduces
SHEEP_LIFE_CYCLES=20 # number of cycles until sheep dies if they cannot find food
SHEEP_DISTANCE_TO_MOVE=5 # distance sheep can move in each cycle, in pixels.

NUM_WOLVES=5 # starting number of wolves
WOLF_BIRTH_CYCLES=20 # number of cycles before each wolf repoduces
WOLF_LIFE_CYCLES=20 # number of cycles before each wolf dies if they cannot find a sheep to eat
DISTANCE_TO_EAT=25 # how close a predator needs to be to a prey item to consume it, in pixels
WOLF_DISTANCE_TO_MOVE=20 # distance wolf can move in each cycle, in pixels

#################################################################
# Initialize the model
#################################################################

# Setup the GUI with a modeless window 
MasterWindow = Tk()
MasterWindow.title("SEIBM")
MasterWindow.resizable(0, 0)

# Create the TheCanvas widget for the blobs to move in
TheCanvas = Canvas(MasterWindow, width=500, height=500, bd=0, highlightthickness=0)
TheCanvas.pack() # fit the window to its contents

#Create the grid of grass
TheGrass=Veg.Veg(TheCanvas,PERCENT_GRASS_COVER,GRASS_REGROW_CYCLES)

# Setup the array with the living animals (prey and predators)
TheAnimals = []

# Add the prey
Count=0;
while Count<NUM_SHEEP:
	# Create a random location for the animal within the canvas
	CenterX=random.uniform(0,500)
	CenterY=random.uniform(0,500)
	
	# Randomize the life cycles for more realizm
	#LifeCycles=int(SHEEP_LIFE_CYCLES*random.uniform(0,1))
	#BirthCycles=int(SHEEP_BIRTH_CYCLES*random.uniform(0,1))
	
	# Create the new animal and add it to the list of animals
	NewSheep=Animal.AnimalClass(TheCanvas, CenterX, CenterY,Animal.TYPE_PREY,"Orange",
	    SHEEP_BIRTH_CYCLES,SHEEP_LIFE_CYCLES,0,SHEEP_DISTANCE_TO_MOVE)
	TheAnimals.append(NewSheep)
	
	Count=Count+1

# Add the predators
Count=0;
while Count<NUM_WOLVES:
	# Create a random location for the animal within the canvas
	CenterX=random.uniform(0,500)
	CenterY=random.uniform(0,500)
	
	# Randomize the life cycles for more realizm
	#LifeCycles=int(WOLF_LIFE_CYCLES*random.uniform(0,1))
	#BirthCycles=int(WOLF_BIRTH_CYCLES*random.uniform(0,1))
	
	# Create the new animal and add it to the list of animals
	NewSheep=Animal.AnimalClass(TheCanvas, CenterX, CenterY,Animal.TYPE_PREDATOR,"Red",
	    WOLF_BIRTH_CYCLES,WOLF_LIFE_CYCLES,DISTANCE_TO_EAT,WOLF_DISTANCE_TO_MOVE)
	TheAnimals.append(NewSheep)
	
	Count=Count+1

# This is required to have the objects be correctly positioned in the window
MasterWindow.update() # fix geometry

#################################################################
# Main Loop
#################################################################

# loop forever updating the grass and animals

try:
	while True: # udpate forever
		
		# Update the grass (grows back)
		TheGrass.Update()
		
		# Update the animals (repoduce, feed, die)
		for TheAnimal in TheAnimals:
			TheAnimal.Update(TheAnimals,TheGrass)
		
		# find the statistics
		NumSheep=0
		NumWolves=0
		for TheAnimal in TheAnimals:
			if TheAnimal.Type==Animal.TYPE_PREY: NumSheep=NumSheep+1
			else: NumWolves=NumWolves+1
		print(format(NumSheep)+","+format(NumWolves))

		# Update the window and give time to other processes
		MasterWindow.update_idletasks() # redraw
		MasterWindow.update() # process events
		time.sleep(.01)

except TclError:
	pass # to avoid errors when the window is closed