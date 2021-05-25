from pyrr import Vector3, matrix44

#=========================================================================
# Nombre         : Camera
# Descripción    : Manejo de los parámetros extrínsecos de la cámara virtual
# Salida         : Vector de parámetros extrínsecos de la cámara virtual
# Source         : https://github.com/totex/Learn-OpenGL-in-python
#=========================================================================

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0.0, 0.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0 ,1.0 ,0.0])
        self.camera_right = Vector3([0.0, 0.0, 0.0])

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)