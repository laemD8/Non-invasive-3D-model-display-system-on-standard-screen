import glfw
from ObjLoader import ObjLoader
from opengl_camera import Camera
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from PIL import Image
import os
from screeninfo import get_monitors

#=========================================================================
# Nombre         : OpenGLwidget
# Descripción    : Calcular y crear la imagen miniatura del modelo
# Salida         : Path de la imagen creada
# Source         : https://github.com/totex/Learn-OpenGL-in-python
#                  https://docs.microsoft.com/en-us/windows/win32/opengl/opengl
#=========================================================================
class OpenGLwidget:

    # =========================================================================
    # Nombre         : __init__
    # Descripción    : Inicializar variables
    # =========================================================================
    def __init__(self, filePath):
        monitors = []
        for m in get_monitors():
            monitors.append(str(m))
        monitor = monitors[0]
        f_width = monitor.find('width')
        f_height = monitor.find('height')
        f_comas = []
        for c, le in enumerate(monitor):
            if le == ',':
               f_comas.append(c)
        self.WIDTH = int(monitor[f_width+6:f_comas[2]])
        self.HEIGHT = int(monitor[f_height+7:f_comas[3]])
        self.cam = Camera()
        self.filePath = filePath
        self.vertex_scr = """
            # version 330 core
            layout(location = 0) in vec3 a_position;
            layout(location = 1) in vec3 a_color;
            layout(location = 2) in vec3 a_normal;
            uniform mat4 projection;
            uniform mat4 view;
            out vec3 v_color;
            void main()
            {
                gl_Position = projection * view * vec4(a_position, 1.0);
                v_color = a_color;
            }
            """
        self.fragment_scr = """
            # version 330 core
            in vec3 v_color;

            out vec4 out_color;
            void main()
            {
                out_color = vec4(v_color, 1.0);
            }
            """

    # =========================================================================
    # Nombre         : CreateWindow()
    # Descripción    : Crear ventana en la pantalla
    # =========================================================================
    def CreateWindow(self):
        if not glfw.init():
            raise Exception("glfw can not be initialized:")
        glfw.window_hint(glfw.VISIBLE, False)
        # glfw.get_primary_monitor()
        self.window = glfw.create_window(self.WIDTH, self.HEIGHT, "My OpenGL window", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        glfw.set_window_pos(self.window, 0, 0)
        glfw.make_context_current(self.window)

    # =========================================================================
    # Nombre         : SetParameter()
    # Descripción    : Compilar vectores y arreglos del modelo
    # =========================================================================
    def SetParameter(self):
        shader = compileProgram(compileShader(self.vertex_scr, GL_VERTEX_SHADER),
                                compileShader(self.fragment_scr, GL_FRAGMENT_SHADER))
        self.VAO = glGenVertexArrays(3)
        self.VBO = glGenBuffers(3)

        glUseProgram(shader)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.WIDTH / self.HEIGHT, 0.1, 100)

        proj_loc = glGetUniformLocation(shader, 'projection')
        self.view_loc = glGetUniformLocation(shader, 'view')

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    # =========================================================================
    # Nombre         : LoadCuadra()
    # Descripción    : Cargar valores de los vectores de posición que componen
    #                  la cuadrícula de fondo más el color
    # =========================================================================
    def LoadCuadra(self):
        self.cuadra = [-0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.72, -0.4, -1.0, 1.0, 1.0, 1.0,

                    -0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, -0.4, -1.1, 1.0, 1.0, 1.0,

                    -0.72, -0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.72, -0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.1, 1.0, 1.0, 1.0,

                    -0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, -0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.4, -1.2, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.72, 0.2, -1.0, 1.0, 1.0, 1.0,
                    -0.72, 0.2, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.2, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.2, -1.2, 1.0, 1.0, 1.0,

                    -0.72, 0.2, -1.2, 1.0, 1.0, 1.0,
                    0.72, 0.2, -1.2, 1.0, 1.0, 1.0,

                    0.72, 0.2, -1.0, 1.0, 1.0, 1.0,
                    0.72, 0.2, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.2, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.2, -1.2, 1.0, 1.0, 1.0,

                    -0.72, 0.0, -1.0, 1.0, 1.0, 1.0,
                    -0.72, 0.0, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.0, -1.1, 1.0, 1.0, 1.0,
                    -0.72, 0.0, -1.2, 1.0, 1.0, 1.0,

                    -0.72, 0.0, -1.2, 1.0, 1.0, 1.0,
                    0.72, 0.0, -1.2, 1.0, 1.0, 1.0,

                    0.72, 0.0, -1.0, 1.0, 1.0, 1.0,
                    0.72, 0.0, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.0, -1.1, 1.0, 1.0, 1.0,
                    0.72, 0.0, -1.2, 1.0, 1.0, 1.0,

                    -0.72, -0.2, -1.0, 1.0, 1.0, 1.0,
                    -0.72, -0.2, -1.1, 1.0, 1.0, 1.0,
                    -0.72, -0.2, -1.1, 1.0, 1.0, 1.0,
                    -0.72, -0.2, -1.2, 1.0, 1.0, 1.0,

                    -0.72, -0.2, -1.2, 1.0, 1.0, 1.0,
                    0.72, -0.2, -1.2, 1.0, 1.0, 1.0,

                    0.72, -0.2, -1.0, 1.0, 1.0, 1.0,
                    0.72, -0.2, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.2, -1.1, 1.0, 1.0, 1.0,
                    0.72, -0.2, -1.2, 1.0, 1.0, 1.0,

                    -0.48, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.48, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.48, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.48, 0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.48, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.48, -0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.48, -0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.48, -0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.48, -0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.48, -0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.24, 0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.24, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.24, 0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.24, 0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.24, 0.4, -1.2, 1.0, 1.0, 1.0,
                    -0.24, -0.4, -1.2, 1.0, 1.0, 1.0,

                    -0.24, -0.4, -1.0, 1.0, 1.0, 1.0,
                    -0.24, -0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.24, -0.4, -1.1, 1.0, 1.0, 1.0,
                    -0.24, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.0, 0.4, -1.0, 1.0, 1.0, 1.0,
                    0.0, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.0, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.0, 0.4, -1.2, 1.0, 1.0, 1.0,

                    0.0, 0.4, -1.2, 1.0, 1.0, 1.0,
                    0.0, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.0, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.0, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.0, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.0, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.24, 0.4, -1.0, 1.0, 1.0, 1.0,
                    0.24, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.24, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.24, 0.4, -1.2, 1.0, 1.0, 1.0,

                    0.24, 0.4, -1.2, 1.0, 1.0, 1.0,
                    0.24, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.24, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.24, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.24, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.24, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.48, 0.4, -1.0, 1.0, 1.0, 1.0,
                    0.48, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.48, 0.4, -1.1, 1.0, 1.0, 1.0,
                    0.48, 0.4, -1.2, 1.0, 1.0, 1.0,

                    0.48, 0.4, -1.2, 1.0, 1.0, 1.0,
                    0.48, -0.4, -1.2, 1.0, 1.0, 1.0,

                    0.48, -0.4, -1.0, 1.0, 1.0, 1.0,
                    0.48, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.48, -0.4, -1.1, 1.0, 1.0, 1.0,
                    0.48, -0.4, -1.2, 1.0, 1.0, 1.0
                    ]

    # =========================================================================
    # Nombre         : LoadModel()
    # Descripción    : Cargar el modelo desde el archivo escogido
    # =========================================================================
    def LoadModel(self):
        indices, self.cubo = ObjLoader.load_model(self.filePath)
        j = []
        for i, ltr in enumerate(self.filePath):
            if ltr == '/':
                j.append(i)
        j = max(j)
        if self.filePath[j + 1:len(self.filePath)] == 'cubo.obj':
            for i in range(3, 49, 9):
                self.cubo[i] = 235 / 255
                self.cubo[i + 1] = 149 / 255
                self.cubo[i + 2] = 245 / 255

            for i in range(57, 103, 9):
                self.cubo[i] = 185 / 255
                self.cubo[i + 1] = 118 / 255
                self.cubo[i + 2] = 193 / 255

            for i in range(111, 157, 9):
                self.cubo[i] = 106 / 255
                self.cubo[i + 1] = 0 / 255
                self.cubo[i + 2] = 117 / 255
        elif self.filePath[j + 1:len(self.filePath)] == 'piramide.obj':
            for i in range(3, 22, 9):
                self.cubo[i] = 235 / 255
                self.cubo[i + 1] = 149 / 255
                self.cubo[i + 2] = 245 / 255

            for i in range(30, 103, 9):
                self.cubo[i] = 185 / 255
                self.cubo[i + 1] = 118 / 255
                self.cubo[i + 2] = 193 / 255

            for i in range(111, 157, 9):
                self.cubo[i] = 106 / 255
                self.cubo[i + 1] = 0 / 255
                self.cubo[i + 2] = 117 / 255

    # =========================================================================
    # Nombre         : Draw()
    # Descripción    : -Crar imagen del modelo y cuadricula
    #                  -Guardar imagen
    # Salida         : Path de la imagen creada
    # =========================================================================
    def Draw(self):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        indices = range(len(self.cuadra) // 6)
        self.cuadra = np.array(self.cuadra, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)
        glBindVertexArray(self.VAO[0])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.cuadra.nbytes, self.cuadra, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.cuadra.itemsize * 6, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.cuadra.itemsize * 6, ctypes.c_void_p(12))
        view = self.cam.get_view_matrix()
        glLineWidth(6)
        glBindVertexArray(self.VAO[0])
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_LINES, 0, len(indices))

        indices2 = range(len(self.cubo) // 6)
        self.cubo = np.array(self.cubo, dtype=np.float32)
        indices2 = np.array(indices2, dtype=np.uint32)

        glBindVertexArray(self.VAO[1])
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[1])
        glBufferData(GL_ARRAY_BUFFER, self.cubo.nbytes, self.cubo, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.cubo.itemsize * 9, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.cubo.itemsize * 9, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.cubo.itemsize * 9, ctypes.c_void_p(24))

        # glPointSize(2)
        glBindVertexArray(self.VAO[1])
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
        glDrawArrays(GL_TRIANGLES, 0, len(indices2))

        x, y, width, height = glGetDoublev(GL_VIEWPORT)
        width, height = int(width), int(height)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes('RGB', (width, height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        path = os.path.abspath(__file__)
        path = path.replace('\\', '/')
        i = []
        for j, ltr in enumerate(path):
            if ltr == '/':
                i.append(j)
        i = max(i)
        path = path[0:i+1]
        j = []
        for i, ltr in enumerate(self.filePath):
            if ltr == '/':
                j.append(i)
        j = max(j)
        filename = self.filePath[j:len(self.filePath)]
        point = filename.find('.')
        filename = filename[0:point+1] + 'jpg'
        path = path + 'images' + filename
        image.save(path, 'JPEG')
        glfw.swap_buffers(self.window)
        glfw.terminate()
        return filename