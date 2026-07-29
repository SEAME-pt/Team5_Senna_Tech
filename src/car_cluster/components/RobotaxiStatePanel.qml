import QtQuick 2.15

Item {
    id: root
    width: 280
    height: 72

    property int robotaxiState: 0
    property bool isDark: true

    function stateLabel() {
        switch (root.robotaxiState) {
        case 1: return "GOING TO PICKUP"
        case 2: return "WAITING AT PICKUP"
        case 3: return "GOING TO DROPOFF"
        case 4: return "WAITING AT DROPOFF"
        case 5: return "RETURNING TO PARKING"
        case 6: return "MISSION COMPLETE"
        default: return "WAITING FOR COMMAND"
        }
    }

    function stateColor() {
        switch (root.robotaxiState) {
        case 1:
        case 3:
        case 5:
            return "#4cc9f0"
        case 2:
        case 4:
            return "#ffd166"
        case 6:
            return "#5ef38c"
        case 7:
            return "#ff6b6b"
        default:
            return root.isDark ? "#ddeff8" : "#0b4659"
        }
    }

    Rectangle {
        anchors.fill: parent
        radius: 18
        color: root.isDark ? "#10212a" : "#f1f7fb"
        border.width: 2
        border.color: stateColor()
        opacity: 0.96
    }

    Column {
        anchors.centerIn: parent
        spacing: 4

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "ROBOTAXI STATE"
            color: root.isDark ? "#9ecae1" : "#2a5b73"
            font.pixelSize: 14
            font.bold: true
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: stateLabel()
            color: stateColor()
            font.pixelSize: 18
            font.bold: true
        }
    }
}