# Non invasive 3D model display system on standard screen

## Description

In this project, it is proposed to display a 3D model on a standard screen, generating anapproximation to the real object through illusion. The user must face the device and movesideways, front or back, to observe the effect. The position of the eyes is established in thecoordinates x, y, and z, using a web camera. The image varies depending on this value. Thepurpose of this is to allow the observer to feel the changes in point of view. The evaluationof the system’s operation to be developed will be carried out from the experience of severalusers. The result is expected to have four limitations:

![alt text](https://github.com/laemD8/Non-invasive-3D-model-display-system-on-standard-screen/blob/main/images/modelo.jpg)

1. It does not offer total immersion in the experience, by not having invasive devices.
2. The camera’s field of view demarcates the space in which the observer moves.
3. The capacity of multiple users at the same time is restricted.
4. Three-dimensional models are point clouds

### Functional specifications
- The application allows to select and upload files of the textit obj format.
- The software displays the name of the chosen file and an image associated with thedisplay model.
- The system will recognize and follow the position of the observer’s eyes from a webcamera, once the virtual environment display is enabled.
- The perspective of the model selected by the user is shown through a screen accordingto the position of their eyes

### Non-functional specifications
- When the system loses the user’s optical flow due to a change in the speed or angularposition of the face, the system will rerun the detection algorithm to generate eye recognition.
- If a face is not detected, the system will continue to operate, and the display willremain with the last calculation made until recognition is generated again.
- The software will work properly as long as the user is in a space with optimal lightingconditions.
- The user’s facial features must be visible, as they are necessary for the detection andsubsequent monitoring process.
- The use of glasses does not affect the system’s functionality unless the light generatesa reflection effect on the lenses, destabilizing the eye tracker.
- This development was designed to be operated by a single user.

## Test requirements
- [x] PySide2
- [x] socket
- [x] opencv-python
- [x] dlib
- [x] math
- [x] numpy
- [x] Pyopengl
- [x] glfw
- [x] pyrr
- [x] pillow
- [x] screeninfo


_#Ka&Lau4ever 🛠️_
