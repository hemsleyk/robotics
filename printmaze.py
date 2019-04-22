# This code provides a very simple implementation of the maze and how the maze's walls can be printed visually.
# You may use this as a starting point or develop your own maze implementation.

import time, math
from statistics import mean
from collections import deque
from lib import servos, ThreadedWebcam, blob, distance, encoders

heading = "N" #important global that tracks robot heading as NESW
position = 1  #important global that tracks active maze cell
maze = [] #live data maze

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
	#needs to change: global heading, global position, cell data
	global heading
	global position
	global maze

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
	cellMove() #next cell
	heading = newHeading #always

	#update the position
	if(newHeading is "N"): position-=4
	elif(newHeading is "E"): position+=1
	elif(newHeading is "S"): position+=4
	elif(newHeading is "W"): position-=1

	#gather data on the new cell
	senseWalls(maze[position-1])

	#printing
	printLocalization()
	#detectMazeInconsistencies(maze)
	printMaze(maze)

def cellMove(): #move forwards some number of inches
	encoders.resetCounts()
	Kp = 0.75 #PID controller corrective strength
	YtdL = 5.0 #measured distance of left sensor
	YtdR = 5.0 #measured distance of right sensor
	inches = 18.0 #distance between cells
	while(encoders.getCounts()[0] < inches/IN_PER_TICK and encoders.getCounts()[1] < inches/IN_PER_TICK):
		YtdR = distance.rSensor.get_distance()
		YtdL = distance.lSensor.get_distance()
		servos.setSpeedsVW(1.5,-Kp*(0-(YtdR-YtdL))*math.pi/2) #try to make left / right sensor discrepancy zero
		time.sleep(0.05)
	setSpeeds(0,0) #stop
	return 0

def senseWalls(cell, NotFirst = True):
	#stop for 1 second, measure all sensors, take average to rule out errors.
	print("Sensing walls")
	wallDistThreshold = 256 #10in to mm
	frontData = []
	rightData = []
	leftData = []
	start = time.monotonic()
	while(start + 1.5 > time.monotonic()): #take a mean to kill sensor noise
		frontData.append(distance.fSensor.get_distance())
		rightData.append(distance.rSensor.get_distance())
		leftData.append(distance.lSensor.get_distance())
		time.sleep(0.05) #measure data
	
	print("Front Distance: ", mean(frontData))
	print("Left Distance: ", mean(leftData))
	print("Right Distance", mean(rightData))
	cell.visited = True
	if(heading is "N"):
		if(mean(frontData) < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		if(mean(leftData) < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(mean(rightData) < wallDistThreshold): cell.east = "W"
		else: cell.east = "O"
		if(NotFirst): cell.south = "O"
	elif(heading is "E"):
		if(mean(frontData) < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(mean(leftData) < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		if(mean(rightData) < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		if(NotFirst): cell.west = "O"
	elif(heading is "S"):
		if(mean(frontData) < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		if(mean(leftData) < wallDistThreshold): cell.east = "W"
		else: cell.east = "O"
		if(mean(rightData) < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(NotFirst): cell.north = "O"
	elif(heading is "W"):
		if(mean(frontData) < wallDistThreshold): cell.west = "W"
		else: cell.west = "O"
		if(mean(leftData) < wallDistThreshold): cell.south = "W"
		else: cell.south = "O"
		if(mean(rightData) < wallDistThreshold): cell.north = "W"
		else: cell.north = "O"
		if(NotFirst): cell.east = "O"

#menu functions
def calibrationMenu():
	print("Current inches/tick: ",servos.IN_PER_TICK)
	choice = float(input("Enter IN_PER_TICK, 0 to cancel: "))
	if(servos.FloatEq(choice, 0.0)):
		#user chose to cancel
		print("Calibraton unchanged")
		return 0
	elif(choice > 0 and choice < 0.5):
		#reasonable input
		servos.IN_PER_TICK = choice
		return 0
	else: #weird input
		print("Calibraton unchanged")
		return 1
def localizationMenu():
	global position
	global heading

	choice = input("Change active cell? Y/N: ")
	if(choice is 'Y'):
		position = int(input("Enter new active cell: "))
	
	choice = input("Change heading? Y/N: ")
	if(choice is 'Y'):
		heading = input("Enter new heading (N, E, S, W): ")
	
	senseWalls(maze[position-1]) #need to sense the local cell

def mappingMenu():
	global maze
	choice = input("Reload map? Y/N")
	if(choice is 'Y'):
		print("(0)\tEmpty map")
		print("(1)\tSample map")
		
		choice = int(input("Choose: "))
		if(choice is 1):
			maze = blankMaze
		else:
			maze = exampleMaze

def manualMovementMenu():
	while(True):
		choice = input("Enter cardinal direction to move, X for main menu: ")
		if(choice is 'N' or choice is 'E' or choice is 'S' or choice is 'W'):
			changeCell(choice)
			senseWalls(maze[position-1])
		elif(choice is 'X'):
			break
		else: continue
	return 0

def pathPlanningMenu():
	#You have been assigned:
	#Starting Cell: 1
	#Ending Cell: 15
	startCell = int(input("Enter starting cell number, 0 for current, -1 to cancel: "))
	if(startCell is -1):
		return 0
	elif(startCell is 0):
		startCell = position
	
	#implicit else, proceed
	endCell = int(input("Enter ending cell number: "))
	pathPlan(startCell,endCell)

	return 0
def pathPlanUtil(currentCell,endCell,visited,path):
	visited[currentCell] = True
	
	if(currentCell is endCell): return 0
	
	print(currentCell)
	if(maze[currentCell]).north is "O":
		if(visited[currentCell-4] is False):
			path.append("N")
			pathPlanUtil(currentCell-4,endCell,visited)
	if(maze[currentCell]).east is "O":
		if(visited[currentCell+4] is False):
			path.append("E")
			pathPlanUtil(currentCell+1,endCell,visited)
	if(maze[currentCell]).south is "O":
		if(visited[currentCell+4] is False):
			path.append("S")
			pathPlanUtil(currentCell+4,endCell,visited)
	if(maze[currentCell]).west is "O":
		if(visited[currentCell-1] is False):
			path.append("W")
			pathPlanUtil(currentCell-1,endCell,visited)

def pathPlan(startCell,endCell):
	#perform a depth first search
	visited = []
	path = deque([]) #empty deque that stores final path as cardinals
	for(cell in maze):
		visited.append(False) #copy in FALSEs
	pathPlanUtil(startCell,endCell,visited,path)
	print(path)


def mainMenu():
	while(True):
		print("(1)\tCalibration Menu")
		print("(2)\tLocalization Menu")
		print("(3)\tMapping Menu")
		print("(4)\tPath Planning Menu")
		print("(5)\tManual Movement")
		print("(0)\tQuit")
		choice = int(input("Select choice: "))
		if(choice is 1):
			calibrationMenu()
		elif(choice is 2):
			localizationMenu()
		elif(choice is 3):
			mappingMenu()
		elif(choice is 4):
			pathPlanningMenu()
		elif(choice is 5):
			manualMovementMenu()
		elif(choice is 0):
			break
		else: continue
def printLocalization():
	print("************")
	print("Cell:\t",position,"Heading:\t",heading)
	for i in range(4):
		for j in range(4):
			if(maze[i * 4 + j].visited):
				print("X", end='')
			else:
				print(".", end='')
		print('\n')
	print("************")

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
exampleMaze = [
	Cell('W','W','O','O', True), Cell('O','W','O','O', True), Cell('O','W','O','O', True), Cell('O','W','W','O', True),
	Cell('W','O','W','O', True), Cell('W','O','W','W', True), Cell('W','O','W','O', True), Cell('W','O','W','O', True),
	Cell('W','O','W','O', True), Cell('W','W','W','O', True), Cell('W','O','W','O', True), Cell('W','O','W','?', True),
	Cell('W','O','O','W', True), Cell('O','O','O','W', True), Cell('O','O','?','W', True), Cell('?','?','W','W', False)
] #not necessarily restricted to grid maze
blankMaze = [
	Cell('W','W','?','?', False), Cell('?','W','?','?', False), Cell('?','W','?','?', False), Cell('?','W','W','?', False),
	Cell('W','?','?','?', False), Cell('?','?','?','?', False), Cell('?','?','?','?', False), Cell('?','?','W','?', False),
	Cell('W','?','?','?', False), Cell('?','?','?','?', False), Cell('?','?','?','?', False), Cell('?','?','W','?', False),
	Cell('W','?','?','W', False), Cell('?','?','?','W', False), Cell('?','?','?','W', False), Cell('?','?','W','W', False)
]
maze = blankMaze
# How to modify a cell
#maze[0].east = 'W'
#maze[0].visited = False

#bootup
position = int(input("Cell number: "))
heading = input("Heading: ")
senseWalls(maze[position-1], False)
mainMenu()