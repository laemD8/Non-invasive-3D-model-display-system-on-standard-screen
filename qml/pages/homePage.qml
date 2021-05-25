import QtQuick 2.0
import QtQuick.Controls 2.15
import "../controls"
import QtQuick.Layouts 1.0



Item {
    Rectangle {
        id: rectangle
        color: "#2B2B2B"
        border.width: 0
        anchors.fill: parent

        Rectangle {
            id: rectangleTop
            height: 69
            visible: !rectangleVisible.visible
            color: "#1F1F1F"
            radius: 0
            border.width: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 50
            anchors.leftMargin: 50
            anchors.topMargin: 40

            GridLayout {
                anchors.fill: parent
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                rows: 1
                columns: 2

                CustomTextField{
                    id: textField
                    placeholderText: "Escribe tu nombre"
                    Layout.fillWidth: true
                    Keys.onEnterPressed: {
                        backend.welcomeText(textField.text)
                    }
                    Keys.onReturnPressed: {
                        backend.welcomeText(textField.text)
                    }
                }

                CustomButton{
                    id: btnChangeName
                    text: "Cambiar nombre"
                    Layout.maximumWidth: 200
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    Layout.preferredWidth: 120
                    onClicked: {
                        backend.welcomeText(textField.text)
                        backend.showHideRectangle(btnChangeName.checked)
                        backend.showNameConfig(btnChangeName.checked)
                    }
                }
            }
        }
    }

    Connections{
        target: backend

        function onSetName(name){
            labelTextName.text = name
        }

        function onIsVisible(isVisible){
            rectangleTop.visible = isVisible
        }

        function onIsHide(isHide){
            rectangleVisible.visible= isHide
        }

        function onSetAreaB(setAreaB){
            textArea.font.pointSize = setAreaB

        }

        function onSetAreaS(setAreaS){
            textArea.font.pointSize = setAreaS

        }

        function onSetTitleB(setTitleB){
            labelTextName.font.pointSize = setTitleB

        }

        function onSetTitleS(setTitleS){
            labelTextName.font.pointSize = setTitleS

        }
    }

    Rectangle {
        id: rectangleVisible
        visible: false
        color: "#1F1F1F"
        radius: 0
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: rectangleTop.bottom
        anchors.bottom: parent.bottom
        anchors.fill: parent

        Label {
            id: labelTextName
            height: 25
            color: "#ffffff"
            text: qsTr("Hola")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.rightMargin: 10
            anchors.topMargin: 30
            font.pointSize: 16
        }

        Text {
            id: text1
            color: "#ffffff"
            text: qsTr("Esta aplicación ofrece visualizar diferentes vistas de modelos 3D de forma interactiva")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: labelTextName.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            lineHeightMode: Text.ProportionalHeight
            wrapMode: Text.Wrap
            minimumPixelSize: 10
            fontSizeMode: Text.FixedSize
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.topMargin: 30
            font.pointSize: textArea.font.pointSize
        }

        GridLayout {
            y: 102
            height: 278
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: text1.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 30
            anchors.bottomMargin: 20
            anchors.rightMargin: 20
            anchors.leftMargin: 20
            rows: 2
            columns: 2

            TextArea {
                id: textArea
                width: 250
                height: 60
                text: qsTr("Se determinará la posición de sus ojos con respecto a la pantalla por medio de la cámara, por favor ubiquese dentro del rango de captura")
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.minimumHeight: 50
                Layout.minimumWidth: 50
                Layout.preferredWidth: -1
                font.pointSize: textArea.font.pointSize
                Layout.fillHeight: true
                Layout.fillWidth: true
                color: "#ffffff"
            }
            TextArea {
                id: textArea1
                width: 250
                height: 300
                text: qsTr("Varie la posición de su cabeza de forma horizontal y vertical a diferentes distancias. Así podrá controlar la vista del modelo")
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.minimumHeight: 50
                Layout.minimumWidth: 50
                Layout.preferredWidth: -1
                font.pointSize: textArea.font.pointSize
                Layout.fillHeight: true
                Layout.fillWidth: true
                color: "#ffffff"
            }

            Image {
                id: image
                width: 206
                height: 150
                source: "../../images/svg_images/1.png"
                sourceSize.height: 600
                sourceSize.width: 600
                Layout.maximumHeight: 500
                Layout.fillHeight: true
                Layout.fillWidth: true
                fillMode: Image.PreserveAspectFit
            }

            Image {
                id: image1
                width: 206
                height: 150
                source: "../../images/svg_images/2.png"
                sourceSize.height: 600
                sourceSize.width: 600
                Layout.maximumHeight: 500
                Layout.maximumWidth: 65535
                Layout.fillHeight: true
                Layout.fillWidth: true
                fillMode: Image.PreserveAspectFit
            }
        }

        anchors.rightMargin: 50
        anchors.leftMargin: 50
        anchors.bottomMargin: 40
        anchors.topMargin: 40
    }


}




/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:480;width:640}D{i:8}
}
##^##*/
