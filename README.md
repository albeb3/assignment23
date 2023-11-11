Alberto Bono 3962994
====================

Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

use `python2 run.py assignment.py` in the terminal for run the script


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

Python node that controls the robot to put all the golden boxes together
------------------------------------------------------------------------

### Main Logic ###

1. Obtain parameters for the `first_token` and `list_of_markers` using the `find_closer_token` function.
2. Identify the closest token, grab it, and update `list_of_markers` and `list_of_markers_done` with the `catch_token` function.
3. Determine the farthest token and its distance using `find_farthest_token`.
4. Move to the center, considering the midpoint between the handled token and the farthest one, and release the token with `go_to_pos_release`, providing half the distance found in the previous step.

Afterward, enter an indefinite loop that continues until all tokens are centralized.
Within the loop, include a conditional block that exits when the `list of tokens` is empty. Reuse the `find_closer_token` and `catch_token` functions to relocate all remaining tokens to the center using `go_to_pos_release2`. This function differs from the previous one as the distance of the first token is specified, releasing the token near another one with a distinct logical sequence.
    
    
### Function to Find the Closest Token ###

The `find_closer_token` function takes `list_of_markers` and `list_of_markers_done` as arguments. Initialize control variables: `dist=100`, `offset=-1`, and `lista=[]`. In an indefinite loop, allow the robot to turn slightly until a complete rotation is done. Meanwhile, fill the `list_of_markers` with all visible tokens. Check if the distance seen for the token is the smallest. Break the loop when the first token seen is visible again, aligning the robot with the closest token using the `look_at_token` function. Output the token number and the updated `list_of_markers`.

### Function to Look at a Specific Token ###

The `look_at_token` function takes the token number as an argument, allowing the robot to turn slightly until the searched token is found.

### Function to Find Tokens that Are Further Away ###

The `find_farthest_token` function initializes a local variable with the content of the provided list. Use it as a condition for a while loop until the list is empty. Allow the robot to turn slightly until the farthest distance is found. Remove the seen token from the control list and align the robot with the closest token using the `look_at_token` function. Output the token number, rotation with respect to the robot, and distance.

### Function to Catch a Token ###

The `catch_token` function takes the token number and two lists (`list_of_markers` and `list_of_markers_done`). Initiate an indefinite loop, continuously updating parameters with the `set_parameters` function. These parameters help the robot reach and grab the token. After grabbing the token, update `list_of_markers` and `list_of_markers_done` using the `setting_lists` function to prevent the robot from grabbing the same token again.

### Function to Update Lists of Markers and Processed Markers ###

The `setting_lists` function switches data from one list to another.

### Function to Go to a Position and Release the Token ###

The `go_to_pos_release2` function takes the token number as an argument, utilizing `look_at_token` to align the robot with the specified token. Initiate an indefinite loop, continuously updating parameters with the `set_parameters` function. These parameters are essential to release the handled token near the specified token.

### Function to Go to the Center of the Tokens' Disposition and Release the Token ###

The `go_to_pos_release2` function takes the token number as an argument, utilizing `look_at_token` to align the robot with the specified token. Initiate an indefinite loop, continuously updating parameters with the `set_parameters` function. These parameters are essential to release the handled token near the specified token.

### Function to Get Parameters of a Specific Token ###

The `set_parameters` function takes the token number as an argument, extracting parameters from the `R.see` method through a conditional block. It checks for a match between the argument and the token seen by the robot, providing the angle of the token seen with respect to the robot and its distance.

Pseudocode
----------

### Pseudocode for Main Logic ###
 

1. **Start**
2. Initialize the robot and constants
3. Get parameters of the first token and 'list_of_markers' with "find_closer_token" function
4. Find the closest token, grab it, and update 'list_of_markers' and 'list_of_markers_done'
5. Find the farthest token and get its parameters with "find_further_token(list_of_markers)"
6. Go to the center of token disposition and release the token with "go_to_pos_release(dist1/2, offset1)"
7. **Loop:**
8. If the list of tokens is empty, **break the loop**
9. Find the closest token, process it, and update the lists
10. Go to a position and release the token with "go_to_pos_release2(first_token)"
11. **End**

### Flowchart for "find_closer_token" Function ###

1. **Start**
2. Initialize variables: `dist = 100`, `offset = -1`
3. Create an empty list: `lista`
4. **Loop indefinitely:**
   5. Turn the robot by an angle
   6. **For each visible marker:**
      7. Add markers to the `lista` list for rotation control
      8. If the marker's offset is not in `lista`, add it
      9. If the marker's offset is not in 'list_of_markers' and not in 'list_of_markers_done':
      10. Add the marker's offset to 'list_of_markers'
      11. Update the minimum distance and offset if the marker is in 'list_of_markers' and closer
      12. If the first seen marker's offset matches the first offset in 'lista' and there is more than one marker in 'lista':
      13. Use 'look_at_token(offset)' to align with the closest token
      14. **Return** the offset and 'list_of_markers'
15. **End**

### Possible improvements ###

The script is written to move all the tokens to the middle using the robot. It is possible to improve it by utilizing the timestamp object to minimize rotations. For example, adjusting the rotation direction based on elapsed time. Additionally, it is feasible to implement a function that enables the robot to avoid tokens already moved when it changes direction. I attempted to extract some lines from the `find_closer_token` function, creating a new function called `find_token` to call it only once in the main logic. However, I encountered difficulties in managing the information. I also faced challenges when attempting to populate the list with tokens towards the conditional block. Sometimes, I observed that the list was filled with the same token's information despite having a condition to fill the list only if the token's number does not already exist in the list.

