import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    
    // Signals
    signal speedUnitToggled()
    signal darkModeToggled()
        
    property bool isDark: false
    property bool isM_S: false

    Item {
        id: switchUnit
        width: 100
        height: 36
        anchors.top: parent.top
        anchors.left: parent.left

        MouseArea {
            anchors.fill: parent
            onClicked: speedUnitToggled()
        }

        Rectangle {
            anchors.fill: parent
            color: "transparent"
            radius: parent.height / 2
            border.color: root.isDark ? '#ddeff8' : '#0b4659'
            border.width: 1
        }

        Rectangle {
            id: speedCircle
            width: parent.height - 8
            height: parent.height - 8
            radius: (parent.height - 8) / 2
            color: root.isDark ? '#ddeff8' : '#0b4659'
            y: 4

            x: root.isM_S ? 6 : parent.width - speedCircle.width - 6
            Behavior on x { NumberAnimation { duration: 220; easing.type: Easing.InOutQuad } }
        }
        Text {
            id: unitLabel
            anchors.verticalCenter: parent.verticalCenter
            text: root.isM_S ? "km/h" : "m/s"  
            color: root.isDark ? '#ddeff8' : '#0b4659' 
            font.family: rajdhani.name
            font.pixelSize: 22
            font.bold: true

            // Use posições fixas relativas ao botão (não à propriedade animada knob.x)
            x: root.isM_S ? (6 + speedCircle.width + 8) : (parent.width - speedCircle.width - 6 - implicitWidth - 8)
        }
    }
    Item {
        id: modeButton
        width: 80
        height: 36
        anchors.right: parent.right 
        anchors.top: parent.top

        MouseArea {
            anchors.fill: parent
            onClicked: darkModeToggled()
        }

        Rectangle {
            anchors.fill: parent
            color: "transparent"
            radius: parent.height / 2
            border.color: root.isDark ? '#ddeff8' : '#0b4659'
            border.width: 1
        }

        Rectangle {
            id: modeCircle
            width: parent.height - 8
            height: parent.height - 8
            radius: (parent.height - 8) / 2
            color: root.isDark ? '#ddeff8' : '#0b4659'
            y: 4

            x: root.isDark ? 6 : parent.width - modeCircle.width - 6
            Behavior on x { NumberAnimation { duration: 220; easing.type: Easing.InOutQuad } }
        }

        Text {
            id: modeType
            anchors.verticalCenter: parent.verticalCenter
            text: root.isDark ?  "\uf185" : "\uf186"  // Sun/Moon em Font Awesome
            color: root.isDark ? '#ddeff8' : '#0b4659' 
            font.family: awesomeSolid.name
            font.pixelSize: 22
            font.bold: true

            x: root.isDark ? (6 + modeCircle.width + 8) : (parent.width - modeCircle.width - 6 - implicitWidth - 8)
        }
    }
}