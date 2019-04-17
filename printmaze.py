# This code provides a very simple implementation of the maze and how the maze's walls can be printed visually.
# You may use this as a starting point or develop your own maze implementation.

import time, math
from lib import servos, ThreadedWebcam, blob, distance

heading #important global that tracks robot heading as NESW
position #important global that tracks active maze cell

class Cell:
	def __init__(self, west, north, east, south, visited = False):
		# There are 4 walls per cell
		# Wall values can be 'W', 'O', or '?' (wall, open, or unknown)
		self.west = west
		self.north = north
		self.east = east
		self.south = south
		
		# Store whether or not the cell has been visited before
		self.visited = visited
def changeCell(newHeading):
	#needs to know: current cell, walls, next cell
	#needs to change: global heading, global position
	global heading
	global position

	#skip over rotation
	if(heading is newHeading): #moving straight
		print("Proceeding straight")

	#rotate to new heading
	elif(heading is "N"):
		if(newHeading is "E"):
			servos.Execute90(1)
		elif(newHeading is "S"):
			servos.Execute90(1)
			servos.Execute90(1)
		elif(newHeading is "W"):
			servos.Execute90(-1)
	elif(heading is "E"):
		if(newHeading is "N"):
			servos.Execute90(-1)
		elif(newHeading is "S"):
			servos.Execute90(1)
		elif(newHeading is "W"):
			servos.Execute90(1)
			servos.Execute90(1)
	elif(heading is "S"):
		if(newHeading is "N"):
			servos.Execute90(1)
			servos.Execute90(1)
		elif(newHeading is "E"):
			servos.Execute90(-1)
		elif(newHeading is "W"):
			servos.Execute90(1)
	elif(heading is "W"):
		if(newHeading is "N"):
			servos.Execute90(1)
		elif(newHeading is "E"):
			servos.Execute90(1)
			servos.Execute90(1)
		elif(newHeading is "S"):
			servos.Execute90(-1)
	else: print("Something went horribly wrong attempting to change cells")
	
	#execute motion
	servos.executeCoast(8.0) #8 inch coast
	heading = newHeading #always

	#update the position
	if(newHeading is "N"): position-=4
	elif(newHeading is "E"): position+=1
	elif(newHeading is "S"): position+=4
	elif(newHeading is "W"): position-=1

def senseWalls(cell):
	#stop for 1 second, measure all sensors, take average to rule out errors.
	print("Sensing walls")
	wallDistThreshold = 128 #5in to mm
	frontData = []
	rightData = []
	leftData = []
	start = time.monotonic()
	while(start < time.monotonic() + 1): #take a mean to kill sensor noise
		frontData.append(distance.fSensor.get_distance())
		rightData.append(distance.rSensor.get_distance())
		leftData.append(distance.lSensor.get_distance())
	if(heading is "N"):
		if(frontData.mean() < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		if(leftData.mean() < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(rightData.mean() < wallDistThreshold): cell.east = "W"
		else: cell.east = "O"
		cell.south = "O"
	elif(heading is "E"):
		if(frontData.mean() < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(leftData.mean() < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		if(rightData.mean() < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		cell.west = "O"
	elif(heading is "S"):
		if(frontData.mean() < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		if(leftData.mean() < wallDistThreshold): cell.east = "W"
		else: cell.east = "O"
		if(rightData.mean() < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		cell.north = "O"
	elif(heading is "W"):
		if(frontData.mean() < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(leftData.mean() < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		if(rightData.mean() < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		cell.east = "O"

# Helper function that verifies all the walls of the maze
def detectMazeInconsistencies(maze):
	# Check horizontal walls
	for i in range(3):
		for j in range(4):
			pos1 = i * 4 + j
			pos2 = i * 4 + j + 4
			hWall1 = maze[pos1].south
			hWall2 = maze[pos2].north		
			assert hWall1 == hWall2, " Cell " + str(pos1) + "'s south wall doesn't equal cell " + str(pos2) + "'s north wall! ('" + str(hWall1) + "' != '" + str(hWall2) + "')"
	
	# Check vertical walls
	for i in range(4):
		for j in range(3):
			pos1 = i * 4 + j
			pos2 = i * 4 + j + 1
			vWall1 = maze[pos1].east
			vWall2 = maze[pos2].west
			assert vWall1 == vWall2, " Cell " + str(pos1) + "'s east wall doesn't equal cell " + str(pos2) + "'s west wall! ('" + str(vWall1) + "' != '" + str(vWall2) + "')"

			
# You don't have to understand how this function works
def printMaze(maze, hRes = 4, vRes = 2):
	assert hRes > 0, "Invalid horizontal resolution"
	assert vRes > 0, "Invalid vertical resolution"

	# Get the dimensions of the maze drawing
	hChars = 4 * (hRes + 1) + 2
	vChars = 4 * (vRes + 1) + 1
	
	# Store drawing into a list
	output = [" "] * (hChars * vChars - 1)
	
	# Draw top border
	for i in range(1, hChars - 2):
		output[i] = "_"
	
	# Draw bottom border
	for i in range(hChars * (vChars - 1) + 1, hChars * (vChars - 1) + hChars - 2):
		output[i] = "¯"
	
	# Draw left border
	for i in range(hChars, hChars * (vChars - 1), hChars):
		output[i] = "|"
		
	# Draw right border
	for i in range(2 * hChars - 2, hChars * (vChars - 1), hChars):
		output[i] = "|"

	# Draw newline characters
	for i in range(hChars - 1, hChars * vChars - 1, hChars):
		output[i] = "\n"
	
	# Draw dots inside maze
	for i in range((vRes + 1) * hChars, hChars * (vChars - 1), (vRes + 1) * hChars):
		for j in range(hRes + 1, hChars - 2, hRes + 1):
			output[i + j] = "·"
	
	# Draw question marks if cell is unvisited
	for i in range(4):
		for j in range(4):
			cellNum = i * 4 + j
			if maze[cellNum].visited:
				continue
			origin = (i * hChars * (vRes + 1) + hChars + 1) + (j * (hRes + 1))
			for k in range(vRes):
				for l in range(hRes):
					output[origin + k * hChars + l] = "?"
	
	# Draw horizontal walls
	for i in range(3):
		for j in range(4):
			cellNum = i * 4 + j
			origin = ((i + 1) * hChars * (vRes + 1) + 1) + (j * (hRes + 1))
			hWall = maze[cellNum].south
			for k in range(hRes):
				output[origin + k] = "-" if hWall == 'W' else " " if hWall == 'O' else "?"
	
	# Draw vertical walls
	for i in range(4):
		for j in range(3):
			cellNum = i * 4 + j
			origin = hChars + (hRes + 1) * (j + 1) + i * hChars * (vRes + 1)
			vWall = maze[cellNum].east
			for k in range(vRes):
				output[origin + k * hChars] = "|" if vWall == 'W' else " " if vWall == 'O' else "?"

	# Print drawing
	print(''.join(output))


# Initialize the maze with a set of walls and visited cells
# The bottom right cell is marked as unvisited and with unknown walls
maze = [
	Cell('W','W','O','O', True), Cell('O','W','O','O', True), Cell('O','W','O','O', True), Cell('O','W','W','O', True),
	Cell('W','O','W','O', True), Cell('W','O','W','W', True), Cell('W','O','W','O', True), Cell('W','O','W','O', True),
	Cell('W','O','W','O', True), Cell('W','W','W','O', True), Cell('W','O','W','O', True), Cell('W','O','W','?', True),
	Cell('W','O','O','W', True), Cell('O','O','O','W', True), Cell('O','O','?','W', True), Cell('?','?','W','W', False)
] #not necessarily restricted to grid maze

# How to modify a cell
#maze[0].east = 'W'
#maze[0].visited = False

detectMazeInconsistencies(maze)
printMaze(maze)

#bootup
position = input("Cell number: ")
heading = input("Heading: ")

senseWalls(maze[position-1])
printMaze(maze)

changeCell("S")
senseWalls(maze[position-1])
printMaze(maze)