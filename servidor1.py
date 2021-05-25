from ObjLoader import ObjLoader
from opengl_camera import Camera
import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from screeninfo import get_monitors

# Inicializar variables
monitors = []

# Obtener el tamaño del monitor
for m in get_monitors():
    monitors.append(str(m))
monitor = monitors[0]
f_width = monitor.find('width')
f_height = monitor.find('height')
f_comas = []
for c, le in enumerate(monitor):
    if le == ',':
        f_comas.append(c)
WIDTH = int(monitor[f_width+6:f_comas[2]])
HEIGHT = int(monitor[f_height+7:f_comas[3]])
lastX, lastY = WIDTH / 2, HEIGHT / 2
lastD = 100
first_mouse = True
p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y = -0.72, -0.4, 0.72, 0.4, 0.72, 0.4, -0.72, -0.4

p11_x, p11_y, p12_x, p12_y, p13_x, p13_y, p14_x, p14_y = -0.24, -0.2, 0.24, 0.2, -0.24, -0.2, 0.24, 0.2

p21_x, p22_x, p23_x, p24_x = -0.48, 0.48, -0.48, 0.48

p31_x, p31_y, p32_x, p32_y = 0.0, 0.0, 0.0, 0.0

c1_x, c1_y, c2_x, c2_y, c3_x, c3_y, c4_x, c4_y, c5_x, c5_y = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
profundidad = 0.0
prof_ant = 0.0
doffset = 0.0
max_prof = 0.0

#=========================================================================
# Nombre         : loader()
# Descripción    : Cargar modelo a partir con la clase ObjLoader
# Parametros     : Path del archivo
#=========================================================================
def loader(filePath):
    global cubo, cubo2, cubo3, max_prof
    indices, cubo = ObjLoader.load_model(filePath)
    distancia = []
    j = []
    for i, ltr in enumerate(filePath):
        if ltr == '/':
            j.append(i)
    j = max(j)
    if filePath[j + 1:len(filePath)] == 'cubo.obj':
        for i in range(3, 49, 9):
            cubo[i] = 235 / 255
            cubo[i + 1] = 149 / 255
            cubo[i + 2] = 245 / 255

        for i in range(57, 103, 9):
            cubo[i] = 185 / 255
            cubo[i + 1] = 118 / 255
            cubo[i + 2] = 193 / 255

        for i in range(111, 157, 9):
            cubo[i] = 106 / 255
            cubo[i + 1] = 0 / 255
            cubo[i + 2] = 117 / 255
    elif filePath[j + 1:len(filePath)] == 'piramide.obj':
        for i in range(3, 22, 9):
            cubo[i] = 235 / 255
            cubo[i + 1] = 149 / 255
            cubo[i + 2] = 245 / 255

        for i in range(30, 103, 9):
            cubo[i] = 185 / 255
            cubo[i + 1] = 118 / 255
            cubo[i + 2] = 193 / 255

        for i in range(111, 157, 9):
            cubo[i] = 106 / 255
            cubo[i + 1] = 0 / 255
            cubo[i + 2] = 117 / 255

    cubo2 = cubo.copy()
    cubo3 = [0] * len(cubo)
    for j in range(2, len(cubo)-6, 9):
        cubo3[j] = cubo[j]
        distancia.append(cubo[j])
    max_prof = -1.2 - min(distancia)

#=========================================================================
# Nombre         : mouse_look_clb()
# Descripción    : Carlcular la vista del modelo a partir de la posición del usuario
# Parametros     : xpos   - Posición en x del punto medio de los ojos del usuario
#                  ypos   - Posición en y del punto medio de los ojos del usuairo
#                  width  - Ancho del frame tomado por la cámra
#                  height - Alto del frame tomado por la cámra
#                  dpos   - Distancia entre el usuario y la cámara
# Salida         : Vectores del modelo y cuadrícula con la vista actualizada
#=========================================================================
def mouse_look_clb(window, xpos, ypos, width, height, dpos):
    global first_mouse, lastX, lastY, lastD, profundidad, doffset, prof_ant, cubo, max_prof
    global p1_x, p1_y, p4_x, p4_y, p2_x, p2_y, p3_x, p3_y, p5_x, p5_y, p6_x, p6_y, p7_x, p7_y, p8_x, p8_y, p9_x, p9_y, p10_x, p10_y
    global p11_x, p11_y, p14_x, p14_y, p12_x, p12_y, p13_x, p13_y, p15_x, p15_y, p16_x, p16_y, p17_x, p17_y, p18_x, p18_y, p19_x, p19_y, p20_x, p20_y
    global p21_x, p22_x, p23_x, p24_x, p25_x, p26_x, p27_x, p28_x, p29_x, p30_x, p31_x, p31_y, p32_x, p32_y, p33_x, p33_y, p34_x, p34_y, p35_x, p35_y
    global c1_x, c1_y, c2_x, c2_y, c3_x, c3_y, c4_x, c4_y, c5_x, c5_y
    if first_mouse:
        lastX = xpos
        lastY = ypos
        lastD = dpos
        first_mouse = False

    xoffset = lastX - xpos
    yoffset = lastY - ypos
    if abs(lastD - dpos) > 0:
        profundidad = (100 - dpos) / 200
        if profundidad < max_prof:
            profundidad = prof_ant
    else:
        profundidad = profundidad

    lastX = xpos
    lastY = ypos
    lastD = dpos

    # Sumar offset del movimiento de la cuadrícula
    p1_x += xoffset * ((1.44 / width) / 5)
    p2_x += xoffset * ((1.44 / width) / 5)
    p3_x += xoffset * (((1.44 / width) / 5) * 2)
    p4_x += xoffset * (((1.44 / width) / 5) * 2)

    p11_x += xoffset * ((1.44 / width) / 5)
    p12_x += xoffset * ((1.44 / width) / 5)
    p13_x += xoffset * (((1.44 / width) / 5) * 2)
    p14_x += xoffset * (((1.44 / width) / 5) * 2)

    p21_x += xoffset * ((1.44 / width) / 5)
    p22_x += xoffset * ((1.44 / width) / 5)
    p23_x += xoffset * (((1.44 / width) / 5) * 2)
    p24_x += xoffset * (((1.44 / width) / 5) * 2)

    p31_x += xoffset * ((1.44 / width) / 5)
    p32_x += xoffset * (((1.44 / width) / 5) * 2)

    p1_y += yoffset * ((0.8 / height) / 5)
    p2_y += yoffset * ((0.8 / height) / 5)
    p3_y += yoffset * (((0.8 / height) / 5) * 2)
    p4_y += yoffset * (((0.8 / height) / 5) * 2)

    p11_y += yoffset * ((0.8 / height) / 5)
    p12_y += yoffset * ((0.8 / height) / 5)
    p13_y += yoffset * (((0.8 / height) / 5) * 2)
    p14_y += yoffset * (((0.8 / height) / 5) * 2)

    p31_y += yoffset * ((0.8 / height) / 5)
    p32_y += yoffset * (((0.8 / height) / 5) * 2)

    # Sumar offset del movimiento del modelo
    for j in range(2, len(cubo) - 6, 9):
        pro = cubo[j] + profundidad
        if pro > cubo3[j]:
            prof = pro - cubo3[j]
            cubo3[j - 2] -= ((prof / 0.1) * (p2_x - 0.72))
            cubo3[j - 1] -= ((prof / 0.1) * (p2_y - 0.4))
        elif pro < cubo3[j]:
            prof = cubo3[j] - pro
            cubo3[j - 2] += ((prof / 0.1) * (p1_x + 0.72))
            cubo3[j - 1] += ((prof / 0.1) * (p1_y + 0.4))

        dif = 1 + pro
        cubo3[j - 2] -= xoffset * ((((1.44 / width) / 5) * dif) / 0.1)
        cubo3[j - 1] -= yoffset * ((((0.8 / height) / 5) * dif) / 0.1)
        cubo3[j] = pro
    prof_ant = profundidad

    # Verificar si se llegó al limite de movimiento hacia la derecha
    if p2_x > 0.79:
        # Establecer valores máximos de la cuadrícula
        p2_x = 0.79
        p1_x = -0.72 + (p2_x - 0.72)
        p3_x = p2_x + (p2_x - 0.72)
        p4_x = p1_x + (p2_x - 0.72)

        p11_x = -0.24 + (p2_x - 0.72)
        p12_x = 0.24 + (p2_x - 0.72)
        p13_x = p11_x + (p12_x - 0.24)
        p14_x = p12_x + (p12_x - 0.24)

        p21_x = -0.48 + (p2_x - 0.72)
        p22_x = 0.48 + (p2_x - 0.72)
        p23_x = p21_x + (p22_x - 0.48)
        p24_x = p22_x + (p22_x - 0.48)

        p31_x = (p2_x - 0.72)
        p32_x = p31_x + p31_x

        # Establecer valores máximos del modelo
        for i in range(2, len(cubo) - 6, 9):
            dif = 1 + cubo[i]
            cubo3[i - 2] = -(p2_x - 0.72) * ((profundidad * 10) + (dif / 0.1))

    # Verificar si se llegó al limite de movimiento hacia la izquierda
    if p1_x < -0.79:
        # Establecer valores mínimos de la cuadrícula
        p1_x = -0.79
        p2_x = 0.72 + (p1_x + 0.72)
        p3_x = p2_x + (p1_x + 0.72)
        p4_x = p1_x + (p1_x + 0.72)

        p11_x = -0.24 + (p1_x + 0.72)
        p12_x = 0.24 + (p1_x + 0.72)
        p13_x = p11_x + (p11_x + 0.24)
        p14_x = p12_x + (p11_x + 0.24)

        p21_x = -0.48 + (p1_x + 0.72)
        p22_x = 0.48 + (p1_x + 0.72)
        p23_x = p21_x + (p21_x + 0.48)
        p24_x = p22_x + (p21_x + 0.48)

        p31_x = (p1_x + 0.72)
        p32_x = p31_x + p31_x

        # Establecer valores mínimos del modelo
        for i in range(2, len(cubo) - 6, 9):
            dif = 1 + cubo[i]
            cubo3[i - 2] = -(p1_x + 0.72) * ((profundidad * 10) + (dif / 0.1))

    # Verificar si se llegó al limite de movimiento hacia arriba
    if p2_y > 0.44:
        # Establecer valores máximos de la cuadrícula
        p2_y = 0.44
        p1_y = -0.40 + (p2_y - 0.40)
        p3_y = p2_y + (p2_y - 0.40)
        p4_y = p1_y + (p2_y - 0.40)

        p11_y = -0.20 + (p2_y - 0.40)
        p12_y = 0.20 + (p2_y - 0.40)
        p13_y = p11_y + (p12_y - 0.20)
        p14_y = p12_y + (p12_y - 0.20)

        p31_y = (p2_y - 0.40)
        p32_y = p31_y + p31_y

        # Establecer valores máximos del modelo
        for i in range(2, len(cubo) - 6, 9):
            dif = 1 + cubo[i]
            cubo3[i - 1] = -(p2_y - 0.40) * ((profundidad * 10) + (dif / 0.1))

    # Verificar si se llegó al limite de movimiento hacia la abajo
    if p1_y < -0.44:
        # Establecer valores mínimos de la cuadrícula
        p1_y = -0.44
        p2_y = 0.40 + (p1_y + 0.40)
        p3_y = p2_y + (p1_y + 0.40)
        p4_y = p1_y + (p1_y + 0.40)

        p11_y = -0.20 + (p1_y + 0.40)
        p12_y = 0.20 + (p1_y + 0.40)
        p13_y = p11_y + (p11_y + 0.2)
        p14_y = p12_y + (p11_y + 0.2)

        p31_y = (p1_y + 0.40)
        p32_y = p31_y + p31_y

        # Establecer valores mínimos del modelo
        for i in range(2, len(cubo) - 6, 9):
            dif = 1 + cubo[i]
            cubo3[i - 1] = -(p1_y + 0.40) * ((profundidad * 10) + (dif / 0.1))

    # Actualizar valores del modelo
    for i in range(2, len(cubo) - 6, 9):
        cubo2[i - 2] = round(cubo[i - 2] + cubo3[i - 2], 3)
        cubo2[i - 1] = round(cubo[i - 1] + cubo3[i - 1], 3)
        cubo2[i] = cubo[i] + profundidad

    # Actualizar valores de la cuadrícula
    vertices = [-0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                -0.72, -0.4, -1.0, 1.0, 1.0, 1.0,

                p1_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p1_y, -1.1, 1.0, 1.0, 1.0,

                p4_x, p4_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p4_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p4_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p4_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p4_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p4_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                -0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                p1_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                0.72, -0.4, -1.0, 1.0, 1.0, 1.0,
                p2_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                p2_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                -0.72, 0.4, -1.0, 1.0, 1.0, 1.0,
                p1_x, p2_y, -1.1, 1.0, 1.0, 1.0,

                p1_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p4_x, p4_y, -1.2, 1.0, 1.0, 1.0,
                p2_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p3_x, p4_y, -1.2, 1.0, 1.0, 1.0,
                p2_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p3_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p1_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p4_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                -0.72, 0.2, -1.0, 1.0, 1.0, 1.0,
                p1_x, p12_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p12_y, -1.1, 1.0, 1.0, 1.0,
                p4_x, p14_y, -1.2, 1.0, 1.0, 1.0,

                p4_x, p14_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p14_y, -1.2, 1.0, 1.0, 1.0,

                0.72, 0.2, -1.0, 1.0, 1.0, 1.0,
                p2_x, p12_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p12_y, -1.1, 1.0, 1.0, 1.0,
                p3_x, p14_y, -1.2, 1.0, 1.0, 1.0,

                -0.72, 0.0, -1.0, 1.0, 1.0, 1.0,
                p1_x, p31_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p31_y, -1.1, 1.0, 1.0, 1.0,
                p4_x, p32_y, -1.2, 1.0, 1.0, 1.0,

                p4_x, p32_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p32_y, -1.2, 1.0, 1.0, 1.0,

                0.72, 0.0, -1.0, 1.0, 1.0, 1.0,
                p2_x, p31_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p31_y, -1.1, 1.0, 1.0, 1.0,
                p3_x, p32_y, -1.2, 1.0, 1.0, 1.0,

                -0.72, -0.2, -1.0, 1.0, 1.0, 1.0,
                p1_x, p11_y, -1.1, 1.0, 1.0, 1.0,
                p1_x, p11_y, -1.1, 1.0, 1.0, 1.0,
                p4_x, p13_y, -1.2, 1.0, 1.0, 1.0,

                p4_x, p13_y, -1.2, 1.0, 1.0, 1.0,
                p3_x, p13_y, -1.2, 1.0, 1.0, 1.0,

                0.72, -0.2, -1.0, 1.0, 1.0, 1.0,
                p2_x, p11_y, -1.1, 1.0, 1.0, 1.0,
                p2_x, p11_y, -1.1, 1.0, 1.0, 1.0,
                p3_x, p13_y, -1.2, 1.0, 1.0, 1.0,

                -0.48, 0.4, -1.0, 1.0, 1.0, 1.0,
                p21_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p21_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p23_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                p23_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p23_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                -0.48, -0.4, -1.0, 1.0, 1.0, 1.0,
                p21_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p21_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p23_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                -0.24, 0.4, -1.0, 1.0, 1.0, 1.0,
                p11_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p11_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p13_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                p13_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p13_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                -0.24, -0.4, -1.0, 1.0, 1.0, 1.0,
                p11_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p11_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p13_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.0, 0.4, -1.0, 1.0, 1.0, 1.0,
                p31_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p31_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p32_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                p32_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p32_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.0, -0.4, -1.0, 1.0, 1.0, 1.0,
                p31_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p31_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p32_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.24, 0.4, -1.0, 1.0, 1.0, 1.0,
                p12_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p12_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p14_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                p14_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p14_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.24, -0.4, -1.0, 1.0, 1.0, 1.0,
                p12_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p12_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p14_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.48, 0.4, -1.0, 1.0, 1.0, 1.0,
                p22_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p22_x, p2_y, -1.1, 1.0, 1.0, 1.0,
                p24_x, p3_y, -1.2, 1.0, 1.0, 1.0,

                p24_x, p3_y, -1.2, 1.0, 1.0, 1.0,
                p24_x, p4_y, -1.2, 1.0, 1.0, 1.0,

                0.48, -0.4, -1.0, 1.0, 1.0, 1.0,
                p22_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p22_x, p1_y, -1.1, 1.0, 1.0, 1.0,
                p24_x, p4_y, -1.2, 1.0, 1.0, 1.0
                ]
    return vertices, cubo2

#=========================================================================
# Nombre         : acceptConnection()
# Descripción    : -Aceptar conexión con el cliente
#                  -Recibir posición de ojos al servidor
#                  -Calcular y desplegar vista del modelo
# Parametros     : filePath - Path del archivo escogido
#                  sock     - servidor creado
#=========================================================================
def acceptConnection(filepath, sock):
    # Inicializar variables
    FORMAT = 'utf-8'
    cam = Camera()

    vertex_scr = """
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
    fragment_scr = """
    # version 330 core
    in vec3 v_color;

    out vec4 out_color;
    void main()
    {
        out_color = vec4(v_color, 1.0);
    }
    """
    # -------------------------------------------------------------------------
    # socket.accept()
    #   Accept a connection. The socket must be bound to an address and listening for connections.
    # source: https://docs.python.org/3/library/socket.html#socket.socket.accept
    # -------------------------------------------------------------------------
    connection, client_address = sock.accept()

    try:
        # =========================================================================
        # Nombre         : key_input_clb()
        # Descripción    : Cerrar ventana del modelo cuando el usuario oprima la tecla ESC
        # Parametros     : key - Valor de la tecla oprimida
        # =========================================================================
        def key_input_clb(window, key, scancode, action, mode):
            global profundidad
            if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
                # -------------------------------------------------------------------------
                # glfw.set_window_should_close(GLFWwindow *window)
                #   This function returns the value of the close flag of the specified window.
                # source: https://www.glfw.org/docs/latest/group__window.html#ga24e02fbfefbb81fc45320989f8140ab5
                # -------------------------------------------------------------------------
                glfw.set_window_should_close(window, True)

                # -------------------------------------------------------------------------
                # socket.close(fd)
                #   Close a socket file descriptor.
                # source: https://docs.python.org/3/library/socket.html#socket.close
                # -------------------------------------------------------------------------
                connection.close()

        # =========================================================================
        # Nombre         : window_resize()
        # Descripción    : Cambia el tamaño de la proyección al cambiar el tamaño de
        #                  la ventana
        # Parametros     : width  - Ancho actual de la ventana
        #                  height - Alto actual de la ventana
        # =========================================================================
        def window_resize(window, width, height):
            glViewport(0, 0, width, height)
            try:
                # -------------------------------------------------------------------------
                # pyrr.matrix44.create_perspective_projection(fovy, aspect, near, far, dtype=None)
                #   Creates a Matrix44 for use as a perspective projection matrix.
                # source: https://pyrr.readthedocs.io/en/latest/oo_api_matrix.html#pyrr.objects.matrix44.Matrix44.perspective_projection
                # -------------------------------------------------------------------------
                projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
            except ZeroDivisionError:
                projection = pyrr.matrix44.create_perspective_projection_matrix(45, 0, 0.1, 100)

            # -------------------------------------------------------------------------
            # glUniformMatrix4fv(GLint(location), GLsizei(count), GLboolean(transpose), const GLfloat *(value))
            #   Specifies the location of the uniform variable to be modified.
            # source: http://pyopengl.sourceforge.net/documentation/manual-3.0/glUniform.html
            # -------------------------------------------------------------------------
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        # -------------------------------------------------------------------------
        # glfw.init()
        #   This function initializes the GLFW library.
        # source: https://www.glfw.org/docs/latest/group__init.html#ga317aac130a235ab08c6db0834907d85e
        # -------------------------------------------------------------------------
        if not glfw.init():
            raise Exception("glfw can not be initialized:")

        # -------------------------------------------------------------------------
        # window = glfw.create_window(640, 480, "My Title", glfwGetPrimaryMonitor(), NULL)
        #   Full screen windows cover the entire display area of a monitor, have no border or decorations.
        # source: https://www.glfw.org/docs/latest/window_guide.html#window_creation
        # -------------------------------------------------------------------------
        window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", glfw.get_primary_monitor(), None)

        if not window:
            # -------------------------------------------------------------------------
            # glfw.terminate()
            #   This function destroys all remaining windows and cursors, restores any
            #   modified gamma ramps and frees any other allocated resources.
            # source: https://www.glfw.org/docs/latest/group__init.html#gaaae48c0a18607ea4a4ba951d939f0901
            # -------------------------------------------------------------------------
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # -------------------------------------------------------------------------
        # glfw.set_window_pos(GLFWwindow *window, int xpos, int ypos)
        #   This function sets the position, in screen coordinates, of the upper-left corner of the
        #   content area of the specified windowed mode window. If the window is a full screen window,
        #   this function does nothing.
        # source: https://www.glfw.org/docs/latest/group__window.html#ga1abb6d690e8c88e0c8cd1751356dbca8
        # -------------------------------------------------------------------------
        glfw.set_window_pos(window, 0, 0)

        # -------------------------------------------------------------------------
        # glfw.set_window_size_callback(GLFWwindow *window, GLFWwindowsizefun callback)
        #   This function sets the size callback of the specified window, which is called when the window
        #   is resized. The callback is provided with the size, in screen coordinates, of the content area
        #   of the window.
        # source: https://www.glfw.org/docs/latest/group__window.html#gad91b8b047a0c4c6033c38853864c34f8
        # -------------------------------------------------------------------------
        glfw.set_window_size_callback(window, window_resize)

        # -------------------------------------------------------------------------
        # glfw.set_key_callback(GLFWwindow *window, GLFWwindowsizefun callback)
        #   This function sets the size callback of the specified window, which is called when a key is pressed
        # source: https://www.glfw.org/docs/latest/group__window.html#gad91b8b047a0c4c6033c38853864c34f8
        # -------------------------------------------------------------------------
        glfw.set_key_callback(window, key_input_clb)

        # -------------------------------------------------------------------------
        # glfw.make_context_current(GLFWwindow *window)
        #   Full screen windows cover the entire display area of a monitor, have no border or decorations.
        # source: https://www.glfw.org/docs/latest/group__context.html#ga1c04dc242268f827290fe40aa1c91157
        # -------------------------------------------------------------------------
        glfw.make_context_current(window)

        shader = compileProgram(compileShader(vertex_scr, GL_VERTEX_SHADER),
                                    compileShader(fragment_scr, GL_FRAGMENT_SHADER))
        VAO = glGenVertexArrays(3)
        VBO = glGenBuffers(3)

        glUseProgram(shader)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)

        proj_loc = glGetUniformLocation(shader, 'projection')
        view_loc = glGetUniformLocation(shader, 'view')

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        view = cam.get_view_matrix()
        loader(filepath)
        while not glfw.window_should_close(window):
            # -------------------------------------------------------------------------
            # socket.recv(bufsize[, flags])
            #   Receive data from the socket. The return value is a bytes object representing the data received.
            # source: https://docs.python.org/3/library/socket.html#socket.socket.recv
            # -------------------------------------------------------------------------
            data_pos = connection.recv(256).decode(FORMAT)
            if data_pos:
                # print(f"Received data: {data_pos} ")
                if data_pos == 'FIN':
                    break
                i = data_pos.find('[')
                j = data_pos.find(']')
                if i == -1 or j == -1:
                    continue
                data_pos = data_pos[i:i + j]
                data_pos = data_pos.replace('[', '')
                data_pos = data_pos.replace(']', '')
                data_pos = data_pos.replace(" ", "")
                data_pos = list(data_pos.split(","))
                data_pos = [float(x) for x in data_pos]
            data = data_pos
            xpos = data[2] - data[0]
            xpos /= 2
            xpos = xpos + data[0]
            ypos = data[3]

            # -------------------------------------------------------------------------
            # glfw.poll_events()
            #   This function processes only those events that are already in the event
            #   queue and then returns immediately. Processing events will cause the window
            #   and input callbacks associated with those events to be called.
            # source: https://www.glfw.org/docs/latest/group__window.html#ga37bd57223967b4211d60ca1a0bf3c832
            # -------------------------------------------------------------------------
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Cargar vectores de cuadrícula y modelo con la respectiva perspectiva
            vertices, cubo = mouse_look_clb(window, xpos, ypos, data[5], data[6], data[4])

            indices = range(len(vertices) // 6)
            vertices = np.array(vertices, dtype=np.float32)
            indices = np.array(indices, dtype=np.uint32)

            # Actualizar vectores de cuadrícula con la vista nueva
            glBindVertexArray(VAO[0])
            glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 6, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 6, ctypes.c_void_p(12))

            # Dibujar cuadrícula
            glLineWidth(2)
            glBindVertexArray(VAO[0])
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
            glDrawArrays(GL_LINES, 0, len(indices))

            indices2 = range(len(cubo) // 6)
            cubo = np.array(cubo, dtype=np.float32)
            indices2 = np.array(indices2, dtype=np.uint32)

            # Actualizar vectores del modelo con la vista nueva
            glBindVertexArray(VAO[1])
            glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
            glBufferData(GL_ARRAY_BUFFER, cubo.nbytes, cubo, GL_STATIC_DRAW)

            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cubo.itemsize * 9, ctypes.c_void_p(0))

            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, cubo.itemsize * 9, ctypes.c_void_p(12))

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cubo.itemsize * 9, ctypes.c_void_p(24))

            # Dibujar Modelo
            # glPointSize(2)
            glBindVertexArray(VAO[1])
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
            glDrawArrays(GL_TRIANGLES, 0, len(indices2)) #Cambiar a GL_POINTS en caso de querer dibujar puntos

            # -------------------------------------------------------------------------
            # glfw.swap_buffers(GLFWwindow *window)
            #   This function swaps the front and back buffers of the specified window when rendering with
            #   OpenGL or OpenGL ES. If the swap interval is greater than zero, the GPU driver waits the
            #   specified number of screen updates before swapping the buffers.
            # source: https://www.glfw.org/docs/latest/group__window.html#ga15a5a1ee5b3c2ca6b15ca209a12efd14
            # -------------------------------------------------------------------------
            glfw.swap_buffers(window)

        else:
            # -------------------------------------------------------------------------
            # socket.close(fd)
            #   Close a socket file descriptor.
            # source: https://docs.python.org/3/library/socket.html#socket.close
            # -------------------------------------------------------------------------
            connection.close()
            glfw.terminate()

    finally:
        connection.close()
        glfw.terminate()
        exit()