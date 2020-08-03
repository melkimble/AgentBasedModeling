#################################################################
# The simplest possible Spatially-Explicit-Individually Based Model (SEIBM)
# This file and its associated modules (Animal.py and Veg.py) implement
# a three trophic level spatial model.  "Veg" is the vegetation (food) and ammo.
# Animals are humans and if there is a zombie where the human feeds on the food (green),
# the ZOMBIES feed on the HUMAN and turns it into a zombie. 
# 
# The human starts out with 0 Ammo, but there is a 1/100 chance that Ammo will spawn (light grey)
# if the human picks up the Ammo, they can use it to shoot the Zombie, but each time they shoot they 
# reduce their Ammo by 1. They cannot shoot if they have no ammo. 
#
# The model beings with:
# - Certain percent cover of grass
# - Specified number of HUMAN
# - Specified number of ZOMBIES
# - Specified amount of AMMO
#
# The model repeats in an infinite number of "cycles".  Each cycle 
# repesents about a month for the default setup but this is really 
# arbitrary and can have different meanings.  On each cycle the
# model is updated as follows:
# - If a patch of grass is empty and enough cycles has passed, the
#   grass will reappear and be available for eating
# - If a HUMAN is close enough to food or ammo, it will eat it
# - If a HUMAN has gone a specified number of cycles without eating,
#   it will die
# - if a HUMAN has gone a specified number of cycles from their last
#   birth, they will birth another HUMAN
# - if a HUMAN is within a specified distance from a ZOMBIE, it will shoot it if it has ammo
# - If a ZOMBIE is within a specified distance from a HUMAN, it will eat it and turn the human into a ZOMBIE
# - ZOMBIES do not die unless a human shoots it, and ZOMBIES do not give birth
#
# This model technically models just the female HUMAN (or other herbivore)
# and ZOMBIES (ZOMBIE).  It could also be interpreted as modeling
# flocks of HUMAN and packs of ZOMBIES.  The model could be modified in 
# a variety of ways to model other species and in different ways.
#
# Author: Jim Graham
# Modified by: Melissa Kimble
# Modification Date: 4/21/2015
#################################################################

# Import standard Python libraries
from Tkinter import * # import the GUI library (windows and UI controls)
import time # bring in the time library so we can "wait" between drawing
import random # import functions to create random numbers

# Import our custom modules
import Animal # module with the class to create HUMAN and ZOMBIEs
import Veg # module for stuff for HUMAN to eat (herbs for herbivores)

#################################################################
# Model constants (modify these to see different model effects)
#################################################################

PERCENT_GRASS_COVER=100 # Starting cover of grass (50) 
GRASS_REGROW_CYCLES=25 # Number of cycles to regrow one patch of grass (100)

NUM_HUMAN=5 # number of HUMAN to start with
HUMAN_BIRTH_CYCLES=50 # number of cycles before each HUMAN repoduces
HUMAN_LIFE_CYCLES=20 # number of cycles until HUMAN dies if they cannot find food
HUMAN_DISTANCE_TO_MOVE=5 # distance HUMAN can move in each cycle, in pixels.
DistanceToRun=7
Ammo=0
DistanceToShoot=10

NUM_ZOMBIES=10 # starting number of ZOMBIES
ZOMBIE_BIRTH_CYCLES=1 # number of cycles before each ZOMBIE repoduces
ZOMBIE_LIFE_CYCLES=1 # number of cycles before each ZOMBIE dies if they cannot find a HUMAN to eat
DISTANCE_TO_EAT=5 # how close a ZOMBIE needs to be to a HUMAN item to consume it, in pixels
ZOMBIE_DISTANCE_TO_MOVE=3 # distance ZOMBIE can move in each cycle, in pixels
DistanceToChase=20

Type=""

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
TheGrass=Veg.Veg(TheCanvas,PERCENT_GRASS_COVER,GRASS_REGROW_CYCLES,Type)

# Setup the array with the living animals (HUMAN and ZOMBIEs)
TheAnimals = []

# Add the HUMAN
Count=0;
while Count<NUM_HUMAN:
	# Create a random location for the animal within the canvas
	CenterX=random.uniform(0,500)
	CenterY=random.uniform(0,500)
	
	# Randomize the life cycles for more realizm
	#LifeCycles=int(HUMAN_LIFE_CYCLES*random.uniform(0,1))
	#BirthCycles=int(HUMAN_BIRTH_CYCLES*random.uniform(0,1))
	
	# Create the new animal and add it to the list of animals
	NewHUMAN=Animal.AnimalClass(TheCanvas, CenterX, CenterY,Animal.TYPE_HUMAN,"Red",
	    HUMAN_BIRTH_CYCLES,HUMAN_LIFE_CYCLES,0,HUMAN_DISTANCE_TO_MOVE,DistanceToRun,0,DistanceToShoot,Ammo)
	TheAnimals.append(NewHUMAN)
	
	Count=Count+1

# Add the ZOMBIEs
Count=0;
while Count<NUM_ZOMBIES:
	# Create a random location for the animal within the canvas
	CenterX=random.uniform(0,500)
	CenterY=random.uniform(0,500)
	
	# Randomize the life cycles for more realizm
	#LifeCycles=int(ZOMBIE_LIFE_CYCLES*random.uniform(0,1))
	#BirthCycles=int(ZOMBIE_BIRTH_CYCLES*random.uniform(0,1))
	
	# Create the new animal and add it to the list of animals
	NewHUMAN=Animal.AnimalClass(TheCanvas, CenterX, CenterY,Animal.TYPE_ZOMBIE,"Black",
	    ZOMBIE_BIRTH_CYCLES,ZOMBIE_LIFE_CYCLES,DISTANCE_TO_EAT,ZOMBIE_DISTANCE_TO_MOVE,0,DistanceToChase,0,0)
	TheAnimals.append(NewHUMAN)
	
	Count=Count+1

# This is required to have the objects be correctly positioned in the window
MasterWindow.update() # fix geometry

#################################################################
# Main Loop
#################################################################

# loop forever updating the grass and animals

try:
	while True: # update forever
		
		# Update the grass (grows back)
		TheGrass.Update()
		
		# Update the animals (repoduce, feed, die)
		for TheAnimal in TheAnimals:
			TheAnimal.Update(TheAnimals,TheGrass)
		
		# find the statistics
		NumHUMAN=0
		NumZOMBIES=0
		for TheAnimal in TheAnimals:
			if TheAnimal.Type==Animal.TYPE_HUMAN: NumHUMAN=NumHUMAN+1
			else: NumZOMBIES=NumZOMBIES+1
		#print(format(NumHUMAN)+","+format(NumZOMBIES))

		# Update the window and give time to other processes
		MasterWindow.update_idletasks() # redraw
		MasterWindow.update() # process events
		time.sleep(.01)

except TclError:
	pass # to avoid errors when the window is closed