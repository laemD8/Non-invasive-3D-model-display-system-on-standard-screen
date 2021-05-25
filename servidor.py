import socket
import sys
import time
from subprocess import Popen, PIPE
from servidor1 import *
#=========================================================================
# Descripción    : -Crear servidor
#                  -Aceptar conexión con cliente
#                  -Recibir posición de ojos al servidor
#                  -Calcular y desplegar vista del modelo
#=========================================================================

try:
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

    time.sleep(1)

    # -------------------------------------------------------------------------
    # socket.bind(address)
    #   Bind the socket to address.
    # source: https://docs.python.org/3/library/socket.html#socket.socket.bind
    # -------------------------------------------------------------------------
    sock.bind(server_address)
    sock.listen(1)
    time.sleep(1)
    timeout = 0
except OSError: # Si el puerto está ocupado
    # -------------------------------------------------------------------------
    # Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None,
    #       preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None,
    #       universal_newlines=None, startupinfo=None, creationflags=0,
    #       restore_signals=True, start_new_session=False, pass_fds=(), *, group=None,
    #       extra_groups=None, user=None, umask=-1, encoding=None, errors=None, text=None)
    #   Execute a child program in a new process.
    # source: https://docs.python.org/3/library/subprocess.html#popen-constructor
    # -------------------------------------------------------------------------
    process = Popen([sys.executable, 'ServiceBusy.py'], shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_hostname = socket.gethostname()
    local_fqdn = socket.getfqdn()

    ip_address = socket.gethostbyname(local_hostname)
    port = 55468

    server_address = (ip_address, port)

    time.sleep(1)
    sock.bind(server_address)
    sock.listen(1)
    time.sleep(1)
    timeout = 0

# Path escogido por el usuario
filePath = input()

#Aceptar conexión
acceptConnection(filePath, sock)
