# Main logic
	Initialize the robot and constants
	Get parameters of the first token and 'list_of_markers' with "find_closer_token function"
	Find the closet token, grab it and update 'list_of_markers' and 'list_of_markers_done'


    Find the farthest token and get its parameters with" find_further_token(list_of_markers)"
    Go to the center of token disposition and release the token with" go_to_pos_release(dist1/2,offset1)"

Loop:
   
    If the list of tokens is empty, break the loop

    Find the closest token, process it, and update the lists
    
    Go to a position and release the token with "go_to_pos_release2(first_token)"  
    
    
# Function to find the closest token
Function find_closer_token(list_of_markers, list_of_markers_done):
    Initialize variables: dist = 100, offset = -1
    Create an empty list: lista
    Loop indefinitely:
        Turn the robot by an angle
        For each visible marker:
            Add markers to the 'lista' list for rotation control
            If the marker's offset is not in 'lista':
                Add the marker's offset to 'lista'
            If the marker's offset is not in 'list_of_markers' and not in 'list_of_markers_done':
                Add the marker's offset to 'list_of_markers'
            Update the minimum distance and offset if the marker is in 'list_of_markers' and closer
            If the first seen marker's offset matches the first offset in 'lista' and there is more than one marker in 'lista':
                Use 'look_at_token(offset)' to align with the closest token
                Return the offset and 'list_of_markers'
                
# Function to look at a specific token
Function look_at_token(offset):
    Initialize a flag: allineato = False
    Loop indefinitely:
        Turn the robot by an angle
        For each visible marker:
            If the marker's offset matches the specified offset and its rotation angle is within the threshold:
                Set 'allineato' flag to True
		If 'allineato' is True, break the loop
		
# Function to find tokens that are further away
Function find_further_token(list_of_markers):
    Create a control list (lista_controllo) with the content of 'list_of_markers'
    Loop while 'lista_controllo' contains elements:
        Turn the robot by an angle
        For each visible marker:
            If the marker's offset is in 'lista_controllo', remove it from 'lista_controllo'
            If the marker's distance is greater than or equal to 'dist':
                Update 'dist', 'rot_y', and 'offset' with the marker's values
    Use 'look_at_token(offset)' to align with the farthest token
    Return 'dist', 'rot_y', and 'offset'
 
# Function to catch a token
Function catch_token(offset, list_of_markers, list_of_markers_done):
    Initialize variables: dist = 0, rot_y = 0
    Loop indefinitely:
        Use 'set_parameters(offset)' to get token parameters
        If 'dist' is 0, no token is found, so find a closer token
        If 'dist' is less than the threshold and the token is not in 'list_of_markers_done', grab the token
        If the robot is well-aligned with the token, drive toward it
        If the token is to the right, turn the robot to the right
        If the token is to the left, turn the robot to the left

# Function to update the lists of markers and markers that have been processed
Function setting_lists(offset, list_of_markers, list_of_markers_done):
    Add the specified offset to 'list_of_markers_done'
    Remove the offset from 'list_of_markers'
	Return the updated 'list_of_markers' and 'list_of_markers_done'

# Function to go to a position and release the token
Function go_to_pos_release2(offset):
    Use 'look_at_token(offset)' to align with the specified token
    Loop indefinitely:
        Drive the robot forward
        Use 'set_parameters(offset)' to get token parameters
        If 'dist' is less than 1.5 times the threshold, release the token
        Drive the robot backward and break the loop

# Function to go to the center of the tokens' disposition and release the token
Function go_to_pos_release(centre, offset):
    Initialize variables: dist = 0, rot_y = 0
    Loop indefinitely:
        Drive the robot forward
        Use 'set_parameters(offset)' to get token parameters
        If 'dist' is less than the center plus the threshold, release the token
        Drive the robot backward and break the loop

# Function to get parameters of a specific token
Function set_parameters(offset):
    Initialize variables: dist = 0, rot_y = 0
    If the specified offset is not -1:
        For each visible marker:
            If the marker's offset matches the specified offset:
                Update 'dist' and 'rot_y' with the marker's values
    Return 'dist' and 'rot_y'
