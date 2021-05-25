import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id: magicButton

    // Custom Properties
    property color colorDefault: "#A63F66"
    property color colorMouseOver: "#AD637F"
    property color colorPressed: "#7a2e4b"

    QtObject{
        id: internal

        property var dynamicColor: if(magicButton.down){
                                       magicButton.down ? colorPressed : colorDefault
                                   }else{
                                       magicButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    text: qsTr("Button")
    contentItem: Item{
        Text {
            id: name
            text: magicButton.text
            font: magicButton.font
            color: "#ffffff"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    background: Rectangle{
        color: internal.dynamicColor
        radius: 10
    }
}
/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:2;height:40;width:200}
}
##^##*/
