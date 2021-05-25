import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: btnToggle
    // CUSTOM PROPERTIES
    property url btnIconSource: "../../images/svg_images/menu_icon.svg"
    property color btnColorDefault: "#000000"
    property color btnColorMouseOver: "#21201f"
    property color btnColorClicked: "#7a2e4b"

    QtObject{
        id: internal

        // MOUSE OVER AND CLICK CHANGE COLOR
        property var dynamicColor: if(btnToggle.down){
                                       btnToggle.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       btnToggle.hovered ? btnColorMouseOver : btnColorDefault
                                   }

    }

    implicitWidth: 70
    implicitHeight: 60

    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Image {
            id: iconBtn
            source: btnIconSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 25
            width: 25
            fillMode: Image.PreserveAspectFit
            visible: false
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            antialiasing: false
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:4}
}
##^##*/
