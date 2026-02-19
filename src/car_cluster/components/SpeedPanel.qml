import QtQuick 2.15

Item {
    id: root
    width: 250
    height: 250

    // Propriedades configuráveis
    property real speed: 0
    property string unitText: "km/h"
    property string odometerNumber: "2041"
    property int odometer: 0
    property string odometerUnit: "m"
    property bool isDark: false

    // Texto Centralizado
    Column {
        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -10
        spacing: -35

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: 20
            text: Math.round(root.speed)
            color: root.isDark ? '#ddeff8' : '#0b4659'
            font.family: rajdhani.name
            font.pixelSize: 150
            font.bold: true
        }

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 160

            Row {
                spacing: 5

                Rectangle {
                    width: 70
                    height: 30
                    color: "transparent"
                    border.color: root.isDark ? '#ddeff8' : '#0b4659'
                    border.width: 1
                    radius: 1

                    Text {
                        anchors.centerIn: parent
                        text: Math.round(root.odometer)
                        color: root.isDark ? '#ddeff8' : '#0b4659'
                        font.family: rajdhani.name
                        font.pixelSize: 25
                        font.bold: true
                    }
                }

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    text: root.odometerUnit
                    color: root.isDark ? '#ddeff8' : '#0b4659'
                    font.family: rajdhani.name
                    font.pixelSize: 25
                }
            }

            Text {
                text: unitText
                color: root.isDark ? '#ddeff8' : '#0b4659'
                font.family: rajdhani.name
                font.pixelSize: 25
            }
        }
    }
}