import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

TextField {
    id: textField

    // Custom Properties
    property color colorDefault: "#000000"
    property color colorOnFocus: "#121212"
    property color colorMouseOver: "#121212"

    QtObject{
        id: internal

        property var dynamicColor: if(textField.focus){
                                        textField.hovered ? colorOnFocus : colorDefault
                                   }else{
                                       textField.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 300
    implicitHeight: 40
    placeholderText: qsTr("Type something")
    color: "#ffffff"
    background: Rectangle {
        color: internal.dynamicColor
        radius: 10
    }

    selectByMouse: true
    selectedTextColor: "#FFFFFF"
    selectionColor: "#ff007f"
    placeholderTextColor: "#FFFFFF"
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:40;width:640}
}
##^##*/
