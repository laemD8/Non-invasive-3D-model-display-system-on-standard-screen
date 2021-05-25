import cv2
import numpy as np
import math
import dlib
import os

# -------------------------------------------------------------------------
# dlib.get_frontal_face_detector()
#   Modelo entrenado detector de rostros
# source: http://dlib.net/python/index.html#dlib.get_frontal_face_detector
# -------------------------------------------------------------------------
face_detector = dlib.get_frontal_face_detector()
cwd = os.path.abspath(os.path.dirname(__file__))

# -------------------------------------------------------------------------
# dlib.shape_predictor()
#   Modelo entrenado detector de puntos de referencia
# source: http://dlib.net/python/index.html#dlib.shape_predictor
# -------------------------------------------------------------------------
model_path = os.path.abspath(os.path.join(cwd, "model_eyes.dat")) # Modelo detector puntos de referencia
predictor = dlib.shape_predictor(model_path)

# Parámetros Flujo Óptico método de Lukas-Kanade
lk_params = dict(winSize=(30, 30),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Coeficientes del filtro FIR
B = [-0.088666387456937112432342473766766488552, 0.240883157846937479007465299218893051147, 0.677332774913873780775475097470916807652, 0.240883157846937479007465299218893051147, -0.088666387456937112432342473766766488552]

# Inicializar variables
x1 = [0, 480, 480, 480, 480]
x2 = [0, 640, 640, 640, 640]
x3 = [0, 480, 480, 480, 480]
x4 = [0, 640, 640, 640, 640]
x5 = [0, 80, 80, 80, 80]

th_left = []
th_right= []
global threshold, origen_eye_left, center_left, origen_eye_right, center_right, ratio_left, ratio_right, eye_left, eye_right
eye_left = [0,0]
eye_right = [0,0]
center = [0,0,0,0]
global k
k=4


#=========================================================================
# Nombre         : prom()
# Descripción    : Promedia los puntos de referencia de cada ojo
# Parametros     : Lista de valores
# Salida         : La posición x y y del centro de cada ojo
#=========================================================================
def prom(lista):
    prom_left_x = 0
    prom_right_x = 0
    prom_left_y = 0
    prom_right_y = 0
    for i in range(0,6):
        x, y = lista[i].ravel()
        prom_left_x += x
        prom_left_y += y
    for j in range(6,12):
        x, y = lista[j].ravel()
        prom_right_x += x
        prom_right_y += y
    return prom_left_x//6, prom_left_y//6, prom_right_x//6, prom_right_y//6

#=========================================================================
# Nombre         : pupils_located()
# Descripción    : Determina si las pupilas han sido ubicadas
# Salida         : Valor booleano
# Source         : https://github.com/antoinelame/GazeTracking
#=========================================================================
def pupils_located():
    try:
        int(eye_left[0])
        int(eye_left[1])
        int(eye_right[0])
        int(eye_right[1])
        return True
    except Exception:
        return False

#=========================================================================
# Nombre         : processing()
# Descripción    : Efectuar procesamiento de imágen para detectar el iris
# Parametros     : eye_frame (numpy.ndarray)
#                  threshold (int)
# Salida         : Bounding box del iris
# Source         : https://github.com/antoinelame/GazeTracking
#=========================================================================
def processing(eye_frame, threshold):
    kernel = np.ones((3, 3), np.uint8)
    # -------------------------------------------------------------------------
    # bilateralFilter(src, dst, d, sigmaColor, sigmaSpace, borderType)
    #   d          − Diameter of each pixel neighborhood that is used during filtering.
    #   sigmaColor − Filter sigma in the color space.
    #   sigmaSpace − Filter sigma in the coordinate space
    # source: https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html
    # -------------------------------------------------------------------------
    iris_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
    # -------------------------------------------------------------------------
    # This operation computes a local minimum over the area of given kernel.
    #   erosion = cv2.erode(img,kernel,iterations = 1)
    # source: https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
    # -------------------------------------------------------------------------
    iris_frame = cv2.erode(iris_frame, kernel, iterations=3)
    # -------------------------------------------------------------------------
    # retval, dst =	cv.threshold(src, thresh, maxval, type[, dst])
    #   src	   - input array (multiple-channel, 8-bit or 32-bit floating point).
    #   dst	   - output array of the same size and type and the same number of channels as src.
    #   thresh - threshold value.
    #   type   - thresholding type (see ThresholdTypes).
    # source: https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html
    # -------------------------------------------------------------------------
    iris_frame = cv2.threshold(iris_frame, threshold, 255, cv2.THRESH_BINARY)[1]
    return iris_frame


#-------------------------------------------------------------------------
# Nombre         : pupil()
# Descripción    : Detecta el iris y estima su posición con el cálculo del centroide
# Parametros     : eye_frame (numpy.ndarray)
#                  threshold (int)
# Salida         : Cáculo de centroides del iris
# Source         : https://github.com/antoinelame/GazeTracking
#-------------------------------------------------------------------------
def pupil(eye_frame, threshold):
    cx = 0
    cy = 0
    iris_frame = processing(eye_frame, threshold)
    # -------------------------------------------------------------------------
    # contours, hierarchy = cv.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
    #   mode   - Retrieves all of the contours and reconstructs a full hierarchy of nested contours.
    #   method - Stores absolutely all the contour points.
    # source: https://docs.opencv.org/master/d4/d86/group__imgproc__shape.html
    # -------------------------------------------------------------------------
    contours, _ = cv2.findContours(iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    contours = sorted(contours, key=cv2.contourArea)
    try:
        moments = cv2.moments(contours[-2])
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
    except (IndexError, ZeroDivisionError):
        pass
    return cx, cy


#-------------------------------------------------------------------------
# Nombre         : optimous_threshold()
# Descripción    : Mejora la calibración teniendo en cuenta el valor de threshold
#                  adecuado, según la imagen dada
# Parametros     : eye_frame (numpy.ndarray)
#                  side (int)
# Salida         : None
# Source         : https://github.com/antoinelame/GazeTracking
#-------------------------------------------------------------------------
def optimous_threshold(eye_frame, side):
    nb_frames = 20
    global threshold
    average_iris = 0.48
    trials = {}
    for threshold in range(5, 100, 5):
        iris_frame = processing(eye_frame, threshold)
        iris_frame = iris_frame[5:-5, 5:-5]
        height, width = iris_frame.shape[:2]
        num_pixels = height * width
        num_blacks = num_pixels - cv2.countNonZero(iris_frame)
        try:
            trials[threshold] = num_blacks / num_pixels
        except ZeroDivisionError:
            trials[threshold] = 0
    threshold, iris_size = min(trials.items(), key=(lambda p: abs(p[1] - average_iris)))
    if (len(th_left) <= nb_frames and len(th_right) <= nb_frames):
        if side == 0:
            th_left.append(threshold)
        elif side == 1:
            th_right.append(threshold)
    else:
        if side == 0:
            for i in range(0, nb_frames-1):
                th_left[i] = th_left[i + 1]
            th_left[nb_frames-1] = threshold
        elif side == 1:
            for i in range(0, nb_frames-1):
                th_right[i] = th_right[i + 1]
            th_right[nb_frames-1] = threshold

#-------------------------------------------------------------------------
# Nombre         : middle_point()
# Descripción    : Calculo distancia media entre dos puntos
# Parametros     : eye_frame (numpy.ndarray)
#                  side (int)
# Salida         : Punto medio
# Notas          : p1 (dlib.point) primer punto, p2 (dlib.point) segundo punto
# Source         : https://github.com/antoinelame/GazeTracking
#-------------------------------------------------------------------------
def middle_point(p1, p2):
    x = int((p1[0] + p2[0]) / 2)
    y = int((p1[1] + p2[1]) / 2)
    return (x, y)

#-------------------------------------------------------------------------
# Nombre         : bounding_eye()
# Descripción    : Enmarca el ojo sin ninguna otra parte del rostro
# Parametros     : frame (numpy.ndarray)
#                  landmarks (dlib.full_object_detection)
#                  points (list)
# Salida         : Frame del ojo, punto de origen, altura, ancho, centro recuadro
# Notas          : Frame contiene el rostro, landmarks representa los 68 puntos
#                  faciales, points se compone de los puntos de los ojos
# Source         : https://github.com/antoinelame/GazeTracking
#-------------------------------------------------------------------------
def bounding_eye(frame, new_points, points, side):
    #region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
    region = np.zeros((6, 2), dtype=np.int32)
    for i in range(0, 6, 1):
        region[i] = (new_points[points[i],0], new_points[points[i],1])
    # Mascara para obtener solamente los ojos
    height, width = frame.shape[:2]
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    # -------------------------------------------------------------------------
    # img = cv.fillPoly(img, pts, color[, lineType[, shift[, offset]]])
    #   pts   - Array of polygons where each polygon is represented as an array of points.
    #   color -	Polygon color.
    # source: https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html
    # -------------------------------------------------------------------------
    cv2.fillPoly(mask, [region], (0, 0, 0))
    eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)
    # Recorte del ojo
    margin = 5
    min_x = np.min(region[:, 0]) - margin
    max_x = np.max(region[:, 0]) + margin
    min_y = np.min(region[:, 1]) - margin
    max_y = np.max(region[:, 1]) + margin
    frame_eye = eye[min_y:max_y, min_x:max_x]
    origin = (min_x, min_y)
    height, width = frame_eye.shape[:2]
    center = (width / 2, height / 2)
    return frame_eye, origin, height, width, center


# -------------------------------------------------------------------------
# Nombre         : blinking()
# Descripción    : Determina si el ojo se encuentra cerrado o no
# Parametros     : landmarks (dlib.full_object_detection)
#                  points (list)
# Salida         : Proporción que indica la apertura del ojo
# Source         : https://github.com/antoinelame/GazeTracking
# -------------------------------------------------------------------------
def blinking(new_points, points):
    left = (new_points[points[0],0], new_points[points[0],1])
    right = (new_points[points[3],0], new_points[points[3],1])
    top = middle_point(new_points[points[1]], new_points[points[2]])
    bottom = middle_point(new_points[points[5]], new_points[points[4]])
    # Cálculo de la hipotenusa
    eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
    eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))
    if eye_height == 0:
        ratio = 0
    else:
        ratio = eye_width / eye_height
    return ratio


# -------------------------------------------------------------------------
# Nombre         : eyes()
# Descripción    : Determina y enmarca el ojo dentro de un nuevo bouding box,
#                  envia datos de calibración e inicializa la función pupila
# Parametros     : original_frame (numpy.ndarray)
#                  landmarks (dlib.full_object_detection)
#                  side (int)
# Salida         : Cáculo de centroides del iris
# Notas          : Original_frame contiene el marco ingresado por el usuario
# Source         : https://github.com/antoinelame/GazeTracking
# -------------------------------------------------------------------------
def eyes(original_frame, landmarks, side):
    global threshold, origen_eye_right, origen_eye_left, center_eye_left, center_eye_right, ratio_left, ratio_right
    LEFT_EYE_POINTS = [0, 1, 2, 3, 4, 5]
    RIGHT_EYE_POINTS = [6, 7, 8, 9, 10, 11]
    if side == 0:
        points = LEFT_EYE_POINTS
        ratio_left = blinking(landmarks, points)
        frame_eye_left, origen_eye_left, height_eye, width_eye, center_eye_left = bounding_eye(original_frame, landmarks, points, side)
        # Retorna true si la calibración ha sido completada
        optimous_threshold(frame_eye_left, side)
        # Retorna el valor de threshold para el respectivo ojo
        threshold = int(sum(th_left) / len(th_left))

        cx_L, cy_L = pupil(frame_eye_left, threshold)

        return (cx_L, cy_L)
    elif side == 1:
        points = RIGHT_EYE_POINTS
        ratio_right = blinking(landmarks, points)
        frame_eye_right, origen_eye_right, height_eye, width_eye, center_eye_right = bounding_eye(original_frame, landmarks, points, side)
        # Retorna true si la calibración ha sido completada

        optimous_threshold(frame_eye_right, side)
        # Retorna el valor de threshold para el respectivo ojo
        threshold = int(sum(th_right) / len(th_right))
        cx_R, cy_R = pupil(frame_eye_right, threshold)

        return (cx_R, cy_R)
    else:
        points = None

# -------------------------------------------------------------------------
# Nombre         : verificador()
# Descripción    : Hace la verificación del centro de pupila con la función
#                  eyes()
# Parametros     : frame_gray (numpy.ndarray)
#                  new_points (list)
# Salida         : Si se encuentra las coordenadas de la pupila retorna True,
#                  en caso contrario retorna False
# Notas          : new_points son los puntos de referencia encontrados por la
#                  detección o seguimiento
# -------------------------------------------------------------------------
def verificador(frame_gray, new_points):
    eye_left = eyes(frame_gray, new_points, 0)
    eye_right = eyes(frame_gray, new_points, 1)
    if ((ratio_left + ratio_right) / 2) < 8 and not (eye_right == (0, 0) or eye_left == (0, 0)):
        return True
    else:
        return False

# -------------------------------------------------------------------------
# Nombre         : deteccion()
# Descripción    : Aplica los modelos de detección de rostros y puntos de
#                  referencia en los ojos
# Parametros     : frame_gray (numpy.ndarray)
# Salida         : Los puntos encontrados por los modelos
# -------------------------------------------------------------------------
def deteccion(frame_gray):
    faces = face_detector(frame_gray)
    landmarks = predictor(frame_gray, faces[0])
    new_points = np.zeros((12, 2), dtype=np.float32)
    for i in range(0, 12, 1):
        new_points[i] = (landmarks.part(i).x, landmarks.part(i).y)
    old_points = new_points
    return old_points

# -------------------------------------------------------------------------
# Nombre         : flujo_optico()
# Descripción    : Aplica la función de flujo óptico en la imagen a partir
#                  de los puntos encontrados en el frame anterior
# Parametros     : old_frame_gray (numpy.ndarray)
#                  frame_gray (numpy.ndarray)
#                  old_points (list)
#                  w (int)
#                  h (int)
# Notas          : w y h son los valores de ancho y alto de la imagen respectivamente
# Salida         : Los puntos encontrados por los modelos
# -------------------------------------------------------------------------
def flujo_optico(old_frame_gray, frame_gray, old_points, w, h):
    old_frame_resize = cv2.resize(old_frame_gray, (100, 100), interpolation=cv2.INTER_AREA)
    frame_resize = cv2.resize(frame_gray, (100, 100), interpolation=cv2.INTER_AREA)
    for i in old_points:
        i[0] = (100*i[0])/w
        i[1] = (100*i[1])/h

    # -------------------------------------------------------------------------
    # nextPts, status, err = cv2.calcOpticalFlowPyrLK(	prevImg, nextImg, prevPts, nextPts[, status[, err[,
    #                        winSize[, maxLevel[, criteria[, flags[, minEigThreshold]]]]]]]	)
    #
    #   prevImg   - first 8-bit input image or pyramid constructed by buildOpticalFlowPyramid.
    #   nextImg	  - second input image or pyramid of the same size and the same type as prevImg.
    #   prevPts	  - vector of 2D points for which the flow needs to be found; point coordinates
    #               must be single-precision floating-point numbers.
    #   nextPts	  - output vector of 2D points (with single-precision floating-point coordinates)
    #               containing the calculated new positions of input features in the second image;
    #               when OPTFLOW_USE_INITIAL_FLOW flag is passed, the vector must have the same size
    #               as in the input.
    #   status	  - output status vector (of unsigned chars); each element of the vector is set to 1
    #               if the flow for the corresponding features has been found, otherwise, it is set to 0.
    #   err	      - output vector of errors; each element of the vector is set to an error for the corresponding
    #               feature, type of the error measure can be set in flags parameter; if the flow wasn't found
    #               then the error is not defined (use the status parameter to find such cases).
    #   winSize	  - size of the search window at each pyramid level.
    #   maxLevel  - 0-based maximal pyramid level number; if set to 0, pyramids are not used (single level),
    #               if set to 1, two levels are used, and so on; if pyramids are passed to input then algorithm
    #               will use as many levels as pyramids have but no more than maxLevel.
    #   criteria  - parameter, specifying the termination criteria of the iterative search algorithm (after the
    #               specified maximum number of iterations criteria.maxCount or when the search window moves by
    #               less than criteria.epsilon.
    #   flags	  - operation flags:
    #                   - OPTFLOW_USE_INITIAL_FLOW uses initial estimations, stored in nextPts; if the flag is
    #                     not set, then prevPts is copied to nextPts and is considered the initial estimate.
    #                   - OPTFLOW_LK_GET_MIN_EIGENVALS use minimum eigen values as an error measure (see
    #                     minEigThreshold description); if the flag is not set, then L1 distance between
    #                     patches around the original and a moved point, divided by number of pixels in a window,
    #                     is used as a error measure.
    #   minEigThreshold	- the algorithm calculates the minimum eigen value of a 2x2 normal matrix of optical flow
    #                     equations (this matrix is called a spatial gradient matrix in [29]), divided by number
    #                     of pixels in a window; if this value is less than minEigThreshold, then a corresponding
    #                     feature is filtered out and its flow is not processed, so it allows to remove bad points
    #                     and get a performance boost.
    # source: https://docs.opencv.org/3.4/dc/d6b/group__video__track.html#ga473e4b886d0bcc6b65831eb88ed93323
    # -------------------------------------------------------------------------
    new_points, st, err = cv2.calcOpticalFlowPyrLK(old_frame_resize, frame_resize, old_points, None,
                                                   **lk_params)
    for i in new_points:
        i[0] = (w*i[0])/100
        i[1] = (h*i[1])/100
    old_points = new_points
    return old_points

# -------------------------------------------------------------------------
# Nombre         : filtroFIR()
# Descripción    : Filtra las señales x y y de cada ojo
# Parametros     : point (int)
#                  side (int)
# Notas          : point es la señal x o y y side es el tipo de variable
#                  x del ojo izquierdo (0), y del ojo izquierdo (1)
#                  x del ojo derecho (2), y del ojo derecho (3)
# Salida         : La señal filtrada
# -------------------------------------------------------------------------
def filtroFIR(point, side):
    y=0
    if side == 0:
        x1[4] = x1[3]
        x1[3] = x1[2]
        x1[2] = x1[1]
        x1[1] = x1[0]
        x1[0] = point
        for i in range(0,5):
            y += x1[i] * B[i]
    if side == 1:
        x2[4] = x2[3]
        x2[3] = x2[2]
        x2[2] = x2[1]
        x2[1] = x2[0]
        x2[0] = point
        for i in range(0,5):
            y += x2[i] * B[i]

    if side == 2:
        x3[4] = x3[3]
        x3[3] = x3[2]
        x3[2] = x3[1]
        x3[1] = x3[0]
        x3[0] = point
        for i in range(0,5):
            y += x3[i] * B[i]
    if side == 3:
        x4[4] = x4[3]
        x4[3] = x4[2]
        x4[2] = x4[1]
        x4[1] = x4[0]
        x4[0] = point
        for i in range(0,5):
            y += x4[i] * B[i]
    if side == 4:
        x5[4] = x5[3]
        x5[3] = x5[2]
        x5[2] = x5[1]
        x5[1] = x5[0]
        x5[0] = point
        for i in range(0,5):
            y += x5[i] * B[i]
    return y

# -------------------------------------------------------------------------
# Nombre         : parpadea()
# Descripción    : Verifica si el usuario está parpadeando
# Salida         : True en caso de no estar parpadeando
#                  False en caso de estar parpadeando
# -------------------------------------------------------------------------
def parpadea():
    if ((ratio_left + ratio_right) / 2) < 5:
        return True
    else:
        return False