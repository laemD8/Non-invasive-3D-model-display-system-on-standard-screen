from PySide2.QtCore import QObject, Slot, Signal, QTimer, QUrl
from subprocess import Popen, PIPE
import sys
from openglwidget import OpenGLwidget


class MainWindow(QObject):
    def init(self):
        QObject.init(self)

    # Señal para establecer el path de la imagen
    # minuatura que se calcula del modelo
    imagePath = Signal(str)

    # Señal para establecer el nombre del archivo escogido
    nameFile = Signal(str)

    # Señal para establecer el nombre del usuario
    setName = Signal(str)

    # Señal para establecer el tamaño de la ventana maximizada
    setAreaB = Signal(int)

    # Señal para establecer el tamaño de la ventana minimizada
    setAreaS = Signal(int)

    # Señal para establecer el tamaño de la letra maximizada
    setTitleB = Signal(int)

    # Señal para establecer el tamaño de la letra minimizada
    setTitleS = Signal(int)

    # Señal para dar visibilidad al recuadro del nombre
    isVisible = Signal(bool)

    # Señal para dar visibilidad al recuadro de la información
    # en la página de inicio
    isHide = Signal(bool)

    # Señal para dar paso a la ejecución de cliente.py
    isPress = Signal(int)

    # Variables para guardar datos del usuario
    name = ''
    Visible = True
    Hide = False
    WindowsStatus = False

    # -------------------------------------------------------------------------
    # Nombre         : openFile()
    # Descripción    : Escoger archivo, generar y guardar imagen miniatura del modelo
    # Parametros     : filepath (String)
    # Salida         : -Path del archivo seleccionado
    #                  -Ejecutar script servidor.py
    # -------------------------------------------------------------------------
    @Slot(str)
    def openFile(self, filePath):
        self.filePath = str(filePath[8:])

        # Funciones tomadas del script openglwidget
        opengl = OpenGLwidget(self.filePath)
        opengl.CreateWindow()
        opengl.SetParameter()
        opengl.LoadCuadra()
        opengl.LoadModel()
        self.Path_image = opengl.Draw()
        self.filePath = bytes(self.filePath, 'utf-8')

        # -------------------------------------------------------------------------
        # Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None,
        #       preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None,
        #       universal_newlines=None, startupinfo=None, creationflags=0,
        #       restore_signals=True, start_new_session=False, pass_fds=(), *, group=None,
        #       extra_groups=None, user=None, umask=-1, encoding=None, errors=None, text=None)
        #   Execute a child program in a new process.
        # source: https://docs.python.org/3/library/subprocess.html#popen-constructor
        # -------------------------------------------------------------------------
        process = Popen([sys.executable,'servidor.py'], stdout=PIPE, stdin=PIPE)

        # -------------------------------------------------------------------------
        # stdin()
        #   If the stdin argument was PIPE, this attribute is a writeable stream
        #   object as returned by open().
        # source: https://docs.python.org/3/library/subprocess.html#subprocess.Popen.stdin
        # -------------------------------------------------------------------------
        process.stdin.write(self.filePath)
        process.stdin.close()

    # -------------------------------------------------------------------------
    # Nombre         : SourceImage()
    # Descripción    : Envía al qml el path de la imagen miniatura y del nombre del archivo
    # -------------------------------------------------------------------------
    @Slot(str)
    def SourceImage(self, image):
        self.nameFile.emit(self.Path_image[1:len(self.Path_image)-4] + '.obj')
        self.imagePath.emit('../../images' + self.Path_image)

    # -------------------------------------------------------------------------
    # Nombre         : areaSizeBig()
    # Descripción    : -Actualiza el estado de la ventana a maximizado
    #                  -Envía al qml el tamaño del área de la ventana
    # -------------------------------------------------------------------------
    @Slot(int)
    def areaSizeBig(self, size):
        self.WindowsStatus = True
        self.setAreaB.emit(12)

    # -------------------------------------------------------------------------
    # Nombre         : areaSizeSmall()
    # Descripción    : -Actualiza el estado de la ventana a minimizado
    #                  -Envía al qml el tamaño del área de la ventana
    # -------------------------------------------------------------------------
    @Slot(int)
    def areaSizeSmall(self, size):
        self.WindowsStatus = False
        self.setAreaS.emit(10)

    # -------------------------------------------------------------------------
    # Nombre         : titleSizeSmall()
    # Descripción    : -Actualiza el estado de la ventana a minimizado
    #                  -Envía al qml el tamaño de la letra del contenido
    # -------------------------------------------------------------------------
    @Slot(int)
    def titleSizeSmall(self, size):
        self.WindowsStatus = False
        self.setTitleS.emit(16)

    # -------------------------------------------------------------------------
    # Nombre         : titleSizeSmall()
    # Descripción    : -Actualiza el estado de la ventana a maximizado
    #                  -Envía al qml el tamaño de la letra del contenido
    # -------------------------------------------------------------------------
    @Slot(int)
    def titleSizeBig(self, size):
        self.WindowsStatus = True
        self.setTitleB.emit(24)

    # -------------------------------------------------------------------------
    # Nombre         : showNameConfig()
    # Descripción    : -Actualiza el estado de la visibilidad del recuadro de
    #                   configuración de nombre
    #                  -Envía al qml el valor de la visibilidad a falso para que
    #                   se oculte una vez el usuario ingrese el nombre
    # -------------------------------------------------------------------------
    @Slot(bool)
    def showNameConfig(self, isChecked):
        self.Visible = False
        self.isVisible.emit(False)

    # -------------------------------------------------------------------------
    # Nombre         : showHideRectangle()
    # Descripción    : -Actualiza el estado de la visibilidad del recuadro de
    #                   contenido en la página de inicio
    #                  -Envía al qml el valor de la visibilidad a verdadero para que
    #                   se muestre una vez el usuario ingrese el nombre
    # -------------------------------------------------------------------------
    @Slot(bool)
    def showHideRectangle(self, isHide):
        self.Hide = True
        self.isHide.emit(True)

    # -------------------------------------------------------------------------
    # Nombre         : welcomeText()
    # Descripción    : -Actualiza el nombre del usuario
    #                  -Envía al qml el nombre del usuario una vez lo ingrese
    # -------------------------------------------------------------------------
    @Slot(str)
    def welcomeText(self, name):
        self.name = name
        self.setName.emit("Hola " + name)

    # -------------------------------------------------------------------------
    # Nombre         : verifyNameHomePage()
    # Descripción    : -Envía al qml el nombre del usuario cada vez que se oprime
    #                   la página inicio
    # -------------------------------------------------------------------------
    @Slot(str)
    def verifyNameHomePage(self, name):
        self.setName.emit("Hola " + self.name)

    # -------------------------------------------------------------------------
    # Nombre         : verifyVisibleHomePage()
    # Descripción    : -Envía al qml la visibilidad del rectangulo de configuración
    #                   de nombre y contenido cada vez que se oprime la página inicio
    # -------------------------------------------------------------------------
    @Slot(bool)
    def verifyVisibleHomePage(self, name):
        self.isHide.emit(self.Hide)
        self.isVisible.emit(self.Visible)

    # -------------------------------------------------------------------------
    # Nombre         : verifySizeText()
    # Descripción    : -Envía al qml el tamaño de la ventana y la letra cada
    #                   vez que se oprime la página inicio
    # -------------------------------------------------------------------------
    @Slot(int)
    def verifySizeText(self, name):
        if self.WindowsStatus:
            self.setAreaB.emit(12)
            self.setTitleB.emit(24)
        else:
            self.setAreaS.emit(10)
            self.setTitleS.emit(16)

    # -------------------------------------------------------------------------
    # Nombre         : openGL()
    # Descripción    : -Ejecuta el script cliente.py una vez el usuario oprima
    #                   el botón de comenzar
    # -------------------------------------------------------------------------
    @Slot(int)
    def openGL(self, isPress):
        if isPress == 0:
            Popen([sys.executable, 'cliente.py'], shell= True)

    