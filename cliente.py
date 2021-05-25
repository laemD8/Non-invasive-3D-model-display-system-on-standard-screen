import socket
import time
from funciones_seguidor import *

#=========================================================================
# Nombre         : clientSideConnection()
# Descripción    : -Conectar con el servidor
#                  -Hacer seguimiento de ojos
#                  -Enviar posición de ojos al servidor
#=========================================================================

def clientSideConnection():
    # Formato de envío
    FORMAT = 'utf-8'

    # -------------------------------------------------------------------------
    # socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
    #   Create a new socket using the given address family, socket type and protocol number.
    # source: https://docs.python.org/3/library/socket.html#socket.socket
    # -------------------------------------------------------------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # -------------------------------------------------------------------------
    # socket.gethostbyname(hostname)
    #   Translate a host name to IPv4 address format.
    # source: https://docs.python.org/3/library/socket.html#socket.gethostbyname
    # -------------------------------------------------------------------------
    local_hostname = socket.gethostname()

    # -------------------------------------------------------------------------
    # socket.getfqdn([name])
    #   Return a fully qualified domain name for name. If name is omitted or empty,
    #   it is interpreted as the local host.
    # source: https://docs.python.org/3/library/socket.html#socket.getfqdn
    # -------------------------------------------------------------------------
    local_fqdn = socket.getfqdn()

    ip_address = socket.gethostbyname(local_hostname)
    port = 55468 # Puerto de conexión
    server_address = (ip_address, port)

    # -------------------------------------------------------------------------
    # socket.connect(address)
    #   Connect to a remote socket at address.
    # source: https://docs.python.org/3/library/socket.html#socket.socket.connect
    # -------------------------------------------------------------------------
    sock.connect(server_address)

    print (f"Connecting to {local_hostname} ({local_fqdn}) with {ip_address}")
    print("Connected to server-side. ")

    time.sleep(2)
    cap = cv2.VideoCapture(1) # Abrir cámara

    # Obtener parámetro ancho y alto de la imagen capturada por la cámara
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Incializar variables
    fx = 1000
    dist = 6
    lista = []
    t_prom = []
    flag = False
    distancia = 100

    while True:
        start = time.time() # Empezar contador de tiempo
        _, frame = cap.read()  # Leer imagen
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            if not flag:
                # Detección de rostro y puntos de referencia
                points = deteccion(frame_gray)
            else:
                # Seguimiento frame a frame de puntos de referencia
                points = flujo_optico(old_frame_gray, frame_gray, points, w, h)

            # Verificar si hay pupila con procesamiento de imágenes
            if verificador(frame_gray, points):
                flag = True
            else:
                flag = False

            # Promedio espacial de los puntos de referencia para encontrar el centro del ojo
            x_left, y_left, x_right, y_right = prom(points)

            # Calcular distancia entre el usuario y la cámara
            x = x_right - x_left
            y = abs(y_left - y_right)
            d = math.sqrt(np.power(x, 2) + np.power(y, 2))
            if parpadea():
                lista.append(int((dist * fx) / d))
                if len(lista) > 10:
                    lista.pop(0)
                distancia = (sum(lista)//len(lista))

            #Filtrar señales
            x_left = int(filtroFIR(x_left, 0))
            y_left = int(filtroFIR(y_left, 1))
            x_right = int(filtroFIR(x_right, 2))
            y_right = int(filtroFIR(y_right, 3))

            old_frame_gray = frame_gray

            # Enviar datos al servidor
            MEN = [x_left, y_left, x_right, y_right, abs(distancia), w, h]
            try:
                # -------------------------------------------------------------------------
                # socket.sendall(bytes[, flags])
                #   Send data to the socket. The socket must be connected to a remote socket.
                # source: https://docs.python.org/3/library/socket.html#socket.socket.sendall
                # -------------------------------------------------------------------------
                sock.sendall(str(MEN).encode(FORMAT))
            except (ConnectionAbortedError, ConnectionResetError):
                break
        except (IndexError, cv2.error):
            flag = False

        # Promediar tiempos
        end = time.time()
        t_prom.append(end-start)
        if len(t_prom) > 60:
            t = (sum(t_prom)) / len(t_prom)
            t_prom = []
            print('Tiempo:', t)
    cap.release()

    # -------------------------------------------------------------------------
    # socket.close(fd)
    #   Close a socket file descriptor.
    # source: https://docs.python.org/3/library/socket.html#socket.close
    # -------------------------------------------------------------------------
    sock.close()

clientSideConnection()
