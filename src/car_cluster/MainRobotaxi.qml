import QtQuick 2.15
import QtQuick.Controls 2.15
import "components"

ApplicationWindow {

    id: root
    width: 1280
    height: 400
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint
    title: "Sea:Me Robotaxi Cluster"

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

    property real currentSpeed: Number(vehicle.speed)
    property string currentGear: vehicle.gear
    property int batteryLevel: Math.round(Number(vehicle.battery))
    property int temperature: Math.round(Number(vehicle.temperature))
    property int odometer: Math.round(Number(vehicle.odometer))
    property int liveRobotaxiState: Number(vehicle.robotaxiState)
    property real range: batteryLevel * 0.0806
    property bool isDm_H: false
    property real displaySpeed: isDm_H ? (currentSpeed * 10) : currentSpeed
    property string unitText: isDm_H ? "dm/h" : "km/h"
    property bool isDark: true
    property bool previewMode: robotaxiPreviewEnabled === true
    property int previewRobotaxiState: 0
    property int robotaxiState: previewMode ? previewRobotaxiState : liveRobotaxiState

    readonly property var previewStates: [0, 1, 2, 3, 4, 5, 6]

    Timer {
        id: previewTimer
        interval: 1600
        running: root.previewMode
        repeat: true
        onTriggered: {
            const index = root.previewStates.indexOf(root.previewRobotaxiState)
            root.previewRobotaxiState = root.previewStates[(index + 1) % root.previewStates.length]
        }
    }

    Image {
        id: clusterImage
        anchors.fill: parent
        source: isDark ? "assets/cluster/cluster_dark.png" : "assets/cluster/cluster_light.png"
        fillMode: Image.PreserveAspectFit
        smooth: true
        antialiasing: true

        onStatusChanged: {
            if (status === Image.Error) {
                console.log("Erro ao carregar a imagem: " + source)
            }
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
        id: gearDisplay
        currentGear: root.currentGear
        isDark: root.isDark

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
    }

    RobotaxiStatePanel {
        id: robotaxiStatePanel
        robotaxiState: root.robotaxiState
        isDark: root.isDark
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -100
    }

    Warning {
        id: warning
        temperature: root.temperature
        batteryLevel: root.batteryLevel
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    Rectangle {
        visible: root.previewMode
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
}