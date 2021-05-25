import QtQuick 2.0
import QtQuick.Controls 2.15

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
                    anchors.rightMargin: 232
                    anchors.leftMargin: 228
                    anchors.bottomMargin: 120
                    anchors.topMargin: 80
                    fillMode: Image.PreserveAspectFit
                    horizontalAlignment: Image.AlignHCenter
                    verticalAlignment: Image.AlignVCenter
                    source: "../../images/svg_images/cad.png"
                }


                Text {
                    id: text1
                    y: 252
                    color: "#ffffff"
                    text: qsTr("¡Cuéntanos tu experiencia!")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    font.pixelSize: 16
                    anchors.top: image.bottom
                    anchors.bottom: parent.bottom
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 236
                    anchors.leftMargin: 236
                    anchors.bottomMargin: 84
                    anchors.topMargin: 44
                }

    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.5;height:480;width:800}D{i:3}D{i:4}
}
##^##*/
