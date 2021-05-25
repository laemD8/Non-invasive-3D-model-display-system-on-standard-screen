import QtQuick 2.0
import QtQuick.Controls 2.15
import "../controls"
import QtQuick.Layouts 1.0
import QtGraphicalEffects 1.15


Item {
    Rectangle {
        id: rectangle
        color: "#2B2B2B"
        anchors.fill: parent
    }

    Rectangle {
        id: rectangleVisible
        color: "#1F1F1F"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.bottom
        anchors.bottom: parent.bottom
        anchors.fill: parent
        anchors.leftMargin: 50
        anchors.bottomMargin: 40
        anchors.rightMargin: 50
        anchors.topMargin: 40

        Image {
            id: image
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            fillMode: Image.PreserveAspectFit
            horizontalAlignment: Image.AlignHCenter
            verticalAlignment: Image.AlignVCenter
            source: image.source
            anchors.bottomMargin: 115
            anchors.topMargin: 86
            anchors.rightMargin: 201
            anchors.leftMargin: 200
        }


        Text {
            id: text1
            y: 252
            color: "#ffffff"
            text: text1.text
            anchors.bottom: image.top
            font.pixelSize: 16
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.bottomMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        CustomButton2{
            id: magicButton
            width: 150
            height: 40
            text: "Comenzar"
            anchors.top: image.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
            Layout.maximumWidth: 400
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.preferredWidth: 200

            onClicked: {
                backend.openGL(magicButton.checked)
            }
        }
    }

    Connections{
        target: backend
        function onImagePath(Path){
            image.source = Path
        }
        function onNameFile(filename){
            text1.text = filename
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.5;height:480;width:800}D{i:3}D{i:4}D{i:5}
}
##^##*/


/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.5;height:480;width:800}
}
##^##*/
