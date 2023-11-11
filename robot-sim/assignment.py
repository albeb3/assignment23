import time
from sr.robot import *

a_th = 2.0 # Threshold for angle comparison
d_th = 0.4 # Threshold for distance comparison

R = Robot()

list_of_markers = [] # List to store marker offsets
list_of_markers_done = [] # List to store markers that have been processed

# Function to control robot motor movement
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
# Function to make the robot move in a circular path
def circle(speed, seconds):
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = speed * 2
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to make the robot turn
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


# Function to find the closest token
def find_closer_token(list_of_markers,list_of_marker_done):
	dist=100
	offset=-1
	lista=[]
	while 1:
		turn(20,0.5)
		for m in R.see():
			# Insert tokens into the list to check rotation
			if m.info.offset not in lista:
				lista.append(m.info.offset)		
				if m.info.offset  not in list_of_markers and m.info.offset not in list_of_markers_done:					
					list_of_markers.append(m.info.offset)
				# Check the shortest distance between tokens in list_of_markers
				if m.dist<dist and m.info.offset in list_of_markers:
					dist=m.dist
					offset=m.info.offset
			elif m.info.offset == lista[0] and len(lista)>1:
				look_at_token(offset)
				return offset,list_of_markers


# Function to look at a specific token    
def look_at_token(offset):
	# Initialize a variable with False, which becomes True once the robot aligns with the desired token
	allineato=False
	while 1:
		turn(20,0.5)
		for r in R.see():
			if r.info.offset == offset and -a_th<r.rot_y<+a_th :
				allineato=True
				break
		if allineato:
			break
				
# Function to find tokens that are further away			
def find_farthest_token(list_of_markers):
	dist=0
	rot_y=0
	offset=-1
	# Initialize the control list with the content of list_of_markers
	lista_controllo=list(list_of_markers)
	# Execute a loop as long as the control_list contains elements
	while lista_controllo:
		turn(30,0.5)
		for token in R.see():
            # If the seen token is in the control_list, remove it
			if token.info.offset in lista_controllo:
				lista_controllo.remove(token.info.offset)
            # Iteratively check for the farthest distance between the elements in the list
			if token.dist >= dist:
				dist = token.dist
				rot_y = token.rot_y
				offset = token.info.offset
				# After finding the farthest token, the robot aligns with it through the look_at_token(offset) function
	look_at_token(offset)
	return dist, rot_y, offset
	

# Function to get parameters of a specific token
def set_parameters(offset):
	dist=0
	rot_y=0
	if offset!=-1:
		for m in R.see():
			if m.info.offset == offset:
				dist = m.dist
				rot_y = m.rot_y 
				offset1=m.info.offset
	return dist, rot_y

# Function to catch a token	
def catch_token(offset,list_of_markers,list_of_markers_done):
	dist=0
	rot_y=0
	while 1:
        # Set token parameters using set_parameters
		dist,rot_y =set_parameters(offset)
		# If the distance is 0, no token has been found, so check for the presence of other tokens and then exit the loop
		if dist==0 : 
			find_closer_token(list_of_markers)	
			break
 		# If the distance is less than the threshold value and the token is not in the list list_of_markers_done,
        # the token is captured using the grab method of the Robot class.
		elif dist < d_th and offset not in list_of_markers_done:
			if R.grab():
 				print("Gotcha!")
                # Loop to ensure that the moved token is actually removed from the list list_of_markers and placed in the list list_of_markers_done
 				while 1:
 					list_of_markers, list_of_markers_done = setting_lists(offset,list_of_markers, list_of_markers_done)
 					# list_of_markers, list_of_markers_done = setting_lists(list_of_markers, list_of_markers_done)
                    # Another check to make sure that the token has not already been captured despite the outer check
 					if offset in list_of_markers_done :
 						return list_of_markers,list_of_markers_done
 						break
		elif -a_th <= rot_y <= a_th:
			print("Ah, that'll do.")
			drive(30, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(2, 0.05)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-2, 0.05)
		
					
				
# Function to go to a centre of the tokens disposition and release the token			
def go_to_pos_release(centre,offset):
	dist=0
	rot_y=0
	while 1:
		drive(30,0.05)
		dist,rot_y=set_parameters(offset)
		if dist < centre +d_th  :
			if R.release():
				print("left token")
				drive(-20,1)
 				#turn(29.5,1)
 				break

# Function to go to a position and release the token 				
def go_to_pos_release2(offset):
	look_at_token(offset)
	while 1:
		drive(20,1)
		dist,rot_y=set_parameters(offset)
		if dist< 1.5*d_th  :
			if R.release():
 				print("left token")
 				drive(-10,1)
 				#turn(29.5,2)
 				break 				

# Function to update the lists of markers and markers that have been processed					

def setting_lists(offset,list_of_markers ,list_of_markers_done ):
	list_of_markers_done.append(offset)
	list_of_markers.remove(offset)
	return list_of_markers , list_of_markers_done
	
# Function to look at a specific token    
def look_at_token(offset):
	allineato=1
	while allineato:
		turn(20,0.05)
		for r in R.see():
			if r.info.offset == offset and -a_th<r.rot_y<+a_th :
				allineato= 0
				
				



# Get parameters of the first token
first_token,list_of_markers=find_closer_token(list_of_markers,list_of_markers_done)

# Process the first token
list_of_markers ,list_of_markers_done = catch_token(first_token,list_of_markers,list_of_markers_done)

# Loop for farthest token scanning
dist1,rot_y1,offset1=find_farthest_token(list_of_markers)

go_to_pos_release(dist1/2,offset1)


while 1:
	print("list of removed : {0}".format(list_of_markers_done))
	print("list of token to move: {0}".format(list_of_markers))
	
	if len(list_of_markers)==0:
		break
		
	closer_token,list_of_markers = find_closer_token(list_of_markers,list_of_markers_done)
	list_of_markers, list_of_markers_done = catch_token(closer_token, list_of_markers, list_of_markers_done)
	go_to_pos_release2(first_token)
	
	
		
	
	
	










