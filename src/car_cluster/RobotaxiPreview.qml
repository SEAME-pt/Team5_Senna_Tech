import QtQuick 2.15
import QtQuick.Controls 2.15
import "components"

ApplicationWindow {
    id: root
    width: 1280
    height: 400
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint
    title: "Sea:Me Robotaxi Preview"

    FontLoader {
        id: rajdhani
        source: "assets/fonts/Rajdhani.ttf"
    }
    FontLoader {
        id: michroma
        source: "assets/fonts/Michroma.ttf"
    }
    FontLoader {
        id: awesomeSolid
        source: "assets/fonts/Awesome_Solid.otf"
    }

    property bool isDark: true
    property bool isDm_H: false
    property real currentSpeed: 24.0
    property int batteryLevel: 78
    property int temperature: 49
    property int odometer: 1532
    property string currentGear: "D"
    property real displaySpeed: isDm_H ? (currentSpeed * 10) : currentSpeed
    property string unitText: isDm_H ? "dm/h" : "km/h"
    property real range: batteryLevel * 0.0806

    readonly property var previewStates: [0, 1, 2, 3, 4, 5, 6]
    property int robotaxiState: 0

    Image {
        anchors.fill: parent
        source: isDark ? "assets/cluster/cluster_dark.png" : "assets/cluster/cluster_light.png"
        fillMode: Image.PreserveAspectFit
        smooth: true
        antialiasing: true
    }

    Timer {
        interval: 1600
        running: true
        repeat: true
        onTriggered: {
            const index = root.previewStates.indexOf(root.robotaxiState)
            root.robotaxiState = root.previewStates[(index + 1) % root.previewStates.length]
        }
    }

    Rectangle {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 20
        radius: 10
        color: "#1f6f8b"
        opacity: 0.9
        border.color: "#d7f3ff"
        border.width: 1
        width: previewLabel.implicitWidth + 24
        height: previewLabel.implicitHeight + 14

        Text {
            id: previewLabel
            anchors.centerIn: parent
            text: "PREVIEW MODE"
            color: "#ffffff"
            font.pixelSize: 13
            font.bold: true
        }
    }

    Header {
        isDm_H: root.isDm_H
        isDark: root.isDark
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20

        onSpeedUnitToggled: root.isDm_H = !root.isDm_H
        onDarkModeToggled: root.isDark = !root.isDark
    }

    Footer {
        temperature: root.temperature
        isDark: root.isDark
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20
    }

    SpeedPanel {
        speed: root.displaySpeed
        odometer: root.odometer
        unitText: root.unitText
        isDark: root.isDark

        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -20
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: -parent.width / 3 - 20
    }

    BatteryPanel {
        battery: root.batteryLevel
        isDark: root.isDark
        range: root.range

        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -20
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: parent.width / 3 + 20
    }

    GearSelector {
        currentGear: root.currentGear
        isDark: root.isDark

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
    }

    RobotaxiStatePanel {
        robotaxiState: root.robotaxiState
        isDark: root.isDark
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -100
    }

    Warning {
        temperature: root.temperature
        batteryLevel: root.batteryLevel
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}