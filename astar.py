import sys
import re
import linecache as lc
import math

mydict = {"color":"v1", "parentnode":"v2", "direction":"v3", "x":"v4", "y":"v5", "f":"v6", "g":"v7", "node":"v8"}

# To get number of rows and columns
rc = lc.getline("maze.txt",1)
y = rc.split()
r = int(y[0])
c = int(y[1])
print("Size of the maze is ", r, " x ", c)

# To create graph from the text file
with open("maze.txt") as file:
	next(file)
	graph = [line for line in file]
open("maze-sol.txt", 'w').close()

ajm = []
openlst = []
clsdlst = []
successor = []
path = []
goal = (r-1, c-1)

# To create an adjacency matrix
for j in range(len(graph)):
	lst = graph[j]
	i = 0
	x = []
	lst2 = lst.split(' ')
	del lst2[-1]
	for i in range(len(lst2)):
		k = lst2[i].split('-')
		if(k[0][0] == 'R' or k[0][0] == 'B'):
				mydict["color"] = k[0][0]
		elif(k[0][0] == 'O'):
			mydict["color"] = k[0][0]
		mydict["node"] = k[0]
		mydict["direction"] = k[1]
		mydict["x"] = int(k[2])
		mydict["y"] = int(k[3])
		mydict["parentnode"] = (0,0)
		mydict["f"] = 0
		mydict["g"] = 0
		x.append(mydict.copy())
	ajm.append(x)

print(ajm)

#To calculate 
def dist(x1, y1, x2, y2):
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def addnodes(indx):
	nodeclr = ajm[indx[0]][indx[1]]["color"]
	nodecol = indx[1]
	noderow = indx[0]
	nodedir = ajm[indx[0]][indx[1]]["direction"]
	i = 0
	j = 0

	if (nodedir == "N"):
		i = noderow
		while (i >= 0):
			if (ajm[i][nodecol]["color"] != nodeclr):
				successor.append((i,nodecol))
			i = i-1
	
	elif (nodedir == "NE"):
		i = noderow
		j = nodecol
		while  (i >= 0 and j < c):
			if (ajm[i][j]["color"] != nodeclr):
				successor.append((i,j))
			i = i-1
			j = j+1

	elif (nodedir == "E"):
		i = nodecol
		while  (i < c):
			if (ajm[noderow][i]["color"] != nodeclr):
				successor.append((noderow,i))
			i = i+1

	elif (nodedir == "SE"):
		i = noderow
		j = nodecol
		while  (i < r and j < c):
			if (ajm[i][j]["color"] != nodeclr):
				successor.append((i,j))
			i = i+1
			j = j+1

	elif (nodedir == "S"):
		i = noderow
		while  (i < r):
			if (ajm[i][nodecol]["color"] != nodeclr):
				successor.append((i,nodecol))
			i = i+1

	elif (nodedir == "SW"):
		i = noderow
		j = nodecol
		while  (i < r and j >= 0):
			if (ajm[i][j]["color"] != nodeclr):
				successor.append((i,j))
			i = i+1
			j = j-1

	elif (nodedir == "W"):
		i = nodecol
		while  (i >= 0):
			if (ajm[noderow][i]["color"] != nodeclr):
				successor.append((noderow,i))
			i = i-1

	elif (nodedir == "NW"):
		i = noderow
		j = nodecol
		while  (i >= 0 and j >= 0):
			if (ajm[i][j]["color"] != nodeclr):
				successor.append((i,j))
			i = i-1
			j = j-1
	return successor

def shortestdistance(startnode, step):
	global successor
	if step == 'y':
		file = open("maze-sol.txt", "a")
		file.write("STEP BY STEP: \n")
		file.write("*****************************************************************************************\n")

	openlst.append(startnode)
	while(openlst != []):
		min1 = ajm[openlst[0][0]][openlst[0][1]]["f"]
		for i in range(len(openlst)):
			if ajm[openlst[i][0]][openlst[i][1]]["f"] < min1:
				min1 = ajm[openlst[i][0]][openlst[i][1]]["f"]

		for ind in openlst:
			if(ajm[ind[0]][ind[1]]["f"] == min1):
				q = ind
		
		if step == 'y':
			file.write("node selected: ")
			file.write(str(ajm[q[0]][q[1]]["node"]))
		
		addnodes(q)
		
		if step == 'y':
			file.write("\nPossible node to travel: ")
			for s in successor:
				file.write(str(ajm[s[0]][s[1]]["node"]))
				file.write(" ")

		openlst.remove(q)

		for item in successor:
			g1 = ajm[q[0]][q[1]]["g"] + dist(ajm[item[0]][item[1]]["x"], ajm[item[0]][item[1]]["y"], ajm[q[0]][q[1]]["x"], ajm[q[0]][q[1]]["y"])
			h1 = dist(ajm[item[0]][item[1]]["x"], ajm[item[0]][item[1]]["y"], ajm[r-1][c-1]["x"], ajm[r-1][c-1]["y"])
			f1 = g1 + h1

			if item in openlst:
				for o in openlst:
					if(item == o and f1 >= ajm[o[0]][o[1]]["f"]):
						continue
					elif(item == o and f1 <= ajm[o[0]][o[1]]["f"]):
						ajm[item[0]][item[1]]["g"] = g1
						ajm[item[0]][item[1]]["f"] = f1
						ajm[item[0]][item[1]]["parentnode"] = q
						#print(ajm[item[0]][item[1]]["parentnode"])
						openlst.remove(o)
						openlst.append(item)

			elif(item not in openlst and item not in clsdlst):
				ajm[item[0]][item[1]]["g"] = g1
				ajm[item[0]][item[1]]["f"] = f1
				ajm[item[0]][item[1]]["parentnode"] = q
				#print(ajm[item[0]][item[1]]["parentnode"])
				openlst.append(item)
			
		successor = []
		clsdlst.append(q)
		
		#print("Open list: ", openlst, "Closed list: ", clsdlst)
		
		if step == 'y':
			file.write("\nnode at the end of possible path: ")
			for ol in openlst:
				file.write(str(ajm[ol[0]][ol[1]]["node"]))
				file.write("(")
				file.write(str(round(ajm[ol[0]][ol[1]]["f"],3)))
				file.write(") ")
			file.write("\n*****************************************************************************************\n")

		if goal in clsdlst:
			print("Bullseye!")
			break

def fewestnodes(startnode, step):
	global successor
	if step == 'y':
		file = open("maze-sol.txt", "a")
		file.write("STEP BY STEP: \n")
		file.write("*****************************************************************************************\n")

	openlst.append(startnode)
	while(openlst != []):
		min1 = ajm[openlst[0][0]][openlst[0][1]]["f"]
		for i in range(len(openlst)):
			if ajm[openlst[i][0]][openlst[i][1]]["f"] < min1:
				min1 = ajm[openlst[i][0]][openlst[i][1]]["f"]

		for ind in openlst:
			if(ajm[ind[0]][ind[1]]["f"] == min1):
				q = ind
		
		if step == 'y':
			file.write("node selected: ")
			file.write(str(ajm[q[0]][q[1]]["node"]))
		
		addnodes(q)
		
		if step == 'y':
			file.write("\nPossible node to travel: ")
			for s in successor:
				file.write(str(ajm[s[0]][s[1]]["node"]))
				file.write(" ")

		openlst.remove(q)

		for item in successor:
			g1 = ajm[q[0]][q[1]]["g"] + 1
			h1 = 0
			f1 = g1 + h1

			if item in openlst:
				for o in openlst:
					if(item == o and ajm[item[0]][item[1]]["f"] >= ajm[o[0]][o[1]]["f"]):
						continue
					elif(item == o and ajm[item[0]][item[1]]["f"] <= ajm[o[0]][o[1]]["f"]):
						ajm[item[0]][item[1]]["g"] = g1
						ajm[item[0]][item[1]]["f"] = f1
						ajm[item[0]][item[1]]["parentnode"] = q
						#print(ajm[item[0]][item[1]]["parentnode"])
						openlst.remove(o)
						openlst.append(item)
			elif(item not in openlst and item not in clsdlst):
				ajm[item[0]][item[1]]["g"] = g1
				ajm[item[0]][item[1]]["f"] = f1
				ajm[item[0]][item[1]]["parentnode"] = q
				#print(ajm[item[0]][item[1]]["parentnode"])
				openlst.append(item)
		successor = []
		clsdlst.append(q)

		if step == 'y':
			file.write("\nnode at the end of possible path: ")
			for ol in openlst:
				file.write(str(ajm[ol[0]][ol[1]]["node"]))
				file.write("(")
				file.write(str(round(ajm[ol[0]][ol[1]]["f"],3)))
				file.write(") ")
			file.write("\n*****************************************************************************************\n")

		if goal in clsdlst:
			print("Bullseye!")
			break
		#("Open list: ", openlst, "Closed list: ", clsdlst)

def printPath(startnode, heuristic):
        i = r-1
        j = c-1
        global path
        path.append((i,j))
        while True:
        	parentRow = ajm[i][j]["parentnode"][0]
        	parentColumn = ajm[i][j]["parentnode"][1]
        	path.append((parentRow, parentColumn))
        	i = parentRow
        	j = parentColumn

        	if(i == startnode[0] and j == startnode[1]):
        		break
        	else:
        		continue
        #print("Number of nodes traversed is ", len(path))
        path.reverse()
        #print("The path is :",path)
        with open("maze-sol.txt", "a") as file:
        	file.write("The final solution is: \n")

        	if heuristic == "f":
        		for p in range(len(path)-1):
        			file.write(str(ajm[path[p][0]][path[p][1]]["node"]))
        			file.write(" to ")
        			file.write(str(ajm[path[p+1][0]][path[p+1][1]]["node"]))
        			file.write(" distance: ")
        			file.write("1")
        			file.write(",\n")
        	if heuristic == "s":
        		for p in range(len(path)-1):
        			file.write(str(ajm[path[p][0]][path[p][1]]["node"]))
        			file.write(" to ")
        			file.write(str(ajm[path[p+1][0]][path[p+1][1]]["node"]))
        			file.write(" distance: ")
        			distance = dist(ajm[path[p][0]][path[p][1]]["x"], ajm[path[p][0]][path[p][1]]["y"], ajm[path[p+1][0]][path[p+1][1]]["x"], ajm[path[p+1][0]][path[p+1][1]]["y"])
        			file.write(str(round(distance,3)))
        			file.write(",\n")
        	file.write("****************************************\n")
        	file.write("Total path distance: ")
        	file.write(str(round(ajm[r-1][c-1]["f"],3)))


if __name__ == '__main__':

	heuristic = input("Choose heuristic\nFor Straight-line distance press 's'.\nFor Fewest Nodes press 'f'.\nEnter your input: ")
	step = input("To print the path step-by-step enter 'y' or else 'n': ")
	snode = input("Enter the starting node: ")

	count = 0
	for a in ajm:
		res = next((x for x, y in enumerate(a) if y["node"] == snode), None)
		if res != None:
			startnode = (count, res)
		count += 1

	with open("maze-sol.txt", "w") as file:
		if heuristic == 's':
			file.write("A* algorithm heuristics: straight-line\n")
		elif heuristic == 'f':
			file.write("A* algorithm heuristics: fewest-nodes\n")
		if step == 'n':
			file.write("Step-by-Step: No\n")
		elif step == 'y':
			file.write("Step-by-Step: Yes\n")
		file.write("Starting node: ")
		file.write(snode)
		file.write("\n\n\n")
	try:
		if heuristic == 's':
			shortestdistance(startnode, step)
			printPath(startnode, heuristic)
		elif heuristic == 'f':
			fewestnodes(startnode, step)
			printPath(startnode, heuristic)
		else:
			sys.exit()
	except:
		print("Wrong input.")
		sys.exit()