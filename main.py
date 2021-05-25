import sys
import os
from MainWindow import MainWindow
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

#=========================================================================
# Descripción    : Crear ventana de la aplicación y llamar la clase MainWindow
# Source         : https://github.com/Wanderson-Magalhaes/System_Info_With_Python
#=========================================================================

if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get Context
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load QML File
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

