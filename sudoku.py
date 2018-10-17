import cv2
def findNextCellToFill(grid, i, j):
	for x in range(i,9):
		for y in range(j,9):
			if grid[x][y] == 0:
				return x,y
	for x in range(0,9):
		for y in range(0,9):
			if grid[x][y] == 0:
				return x,y
	return -1,-1

def isValid(grid, i, j, e):
	rowOk = all([e != grid[i][x] for x in range(9)])
	if rowOk:
		columnOk = all([e != grid[x][j] for x in range(9)])
		if columnOk:
			secTopX, secTopY = 3 *(i//3), 3 *(j//3)
			for x in range(secTopX, secTopX+3):
				for y in range(secTopY, secTopY+3):
					if grid[x][y] == e:
						return False
			return True
	return False

def solveSudoku(grid, i=0, j=0):
	i,j = findNextCellToFill(grid, i, j)
	if i == -1:
		return True
	for e in range(1,10):
		if isValid(grid,i,j,e):
			grid[i][j] = e
			if solveSudoku(grid, i, j):
				return True
				# Undo the current cell for backtracking
			grid[i][j] = 0
	return False

list1 = []
grid1 = []
inp = []
img = cv2.imread('db/sudoku.jpg')
C,H,W = img.shape[::-1]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,220,255,0)
_,contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
	perimeter = cv2.arcLength(contours[i],True)
	if perimeter > 25 and perimeter < 50:
		list1.append(i)
		cv2.drawContours(img, contours, -1, (0,255,0), 2)
counter = -1
column = -1;
temp1 = []
for x in list1[::-1	]:
	M = cv2.moments(contours[x])
	if M['m00']!=0:
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
	else:
		cx,cy = 0,0
	cv2.rectangle(img,(cx-10,cy-10),(cx+10,cy+10),(0,255,255), 1)
	cropped = img[cy-10:cy+10,cx-10:cx+10]
	cv2.imshow("cropped",cropped)
	
	counter = counter+1
	maxval = -1
	index = -1
	for i in range(0,10):
		template = cv2.imread("db/no"+str(i)+".jpg")
		result = cv2.matchTemplate(cropped,template,cv2.TM_CCOEFF_NORMED)
		min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
		if max_val > maxval:
			maxval = max_val
			index = i;
	temp = []
	temp.append(int(counter/9))
	temp.append(int(counter-9*int(counter/9)))
	temp.append(index)
	grid1.append(temp)


for k in range(0,9):
	temp1=[]	
	for j in range(0,9):
		temp1.append(0)
	inp.append(temp1)


for l in grid1:
	if l[2]!=0:
		inp[l[0]][l[1]] = l[2]


possibility = solveSudoku(inp)
if possibility==True:
	for i in inp:
		print(i)
else:
	print("Not possible")


cv2.imshow("original",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
