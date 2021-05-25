import socket
import time

#=========================================================================
# Descripción    : Conectar con el servidor cuando está ocupado para
#                  cerrar el puerto
#=========================================================================

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

time.sleep(2)

# -------------------------------------------------------------------------
# socket.sendall(bytes[, flags])
#   Send data to the socket. The socket must be connected to a remote socket.
# source: https://docs.python.org/3/library/socket.html#socket.socket.sendall
# -------------------------------------------------------------------------
sock.sendall('FIN'.encode(FORMAT))

# -------------------------------------------------------------------------
# socket.close(fd)
#   Close a socket file descriptor.
# source: https://docs.python.org/3/library/socket.html#socket.close
# -------------------------------------------------------------------------
sock.close()