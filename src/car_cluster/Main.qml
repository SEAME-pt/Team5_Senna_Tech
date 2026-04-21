import QtQuick 2.15
import QtQuick.Controls 2.15
import "components"

ApplicationWindow {

    id: root
    width: 1280
    height: 400
    visible: true
    flags: Qt.Window | Qt.FramelessWindowHint
    title: "Sea:Me Instrument Cluster"

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
    // Properties
    property real currentSpeed: Number(vehicle.speed)
    property string currentGear: vehicle.gear
    property int batteryLevel:Math.round(Number(vehicle.battery))
    property int temperature: Math.round(Number(vehicle.temperature))
    property int odometer: Math.round(Number(vehicle.odometer))
    property string currentTrafficSign: vehicle.trafficSign
    property string currentSpeedSign: vehicle.speedSign
    property real range: batteryLevel * 0.0806
    // speed unit change
    property bool isDm_H: false
    property real displaySpeed: isDm_H ? (currentSpeed * 10) : currentSpeed
    property string unitText: isDm_H ? "dm/h" : "km/h"
    // cluster mode
    property bool isDark: true

    Image {
            id: clusterImage
            anchors.fill: parent

            // Caminho para o recurso (ajuste se estiver dentro de um prefixo no .qrc)
            source: isDark ? "assets/cluster/cluster_dark.png" : "assets/cluster/cluster_light.png" 

            // Garante que a imagem preencha o espaço sem distorcer
            fillMode: Image.PreserveAspectFit

            // Melhora a qualidade ao redimensionar
            smooth: true
            antialiasing: true

            // Caso a imagem falhe ao carregar, imprime um erro no console
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
    SpeedPanel{
        speed: root.displaySpeed
        odometer: root.odometer
        unitText: root.unitText
        isDark: root.isDark

        anchors.verticalCenter: parent.verticalCenter 
        anchors.verticalCenterOffset: - 20
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: - parent.width / 3 - 20
    }
    BatteryPanel {
        battery: root.batteryLevel // Sua propriedade vinculada ao C++
        isDark: root.isDark
        range: root.range

        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: - 20
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
    TrafficSign{
        id: trafficSign
        currentTrafficSign: root.currentTrafficSign
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -100
        anchors.horizontalCenterOffset: +100
    }
    TrafficSign{
        id: speedSign
        currentTrafficSign: root.currentSpeedSign
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -100
        anchors.horizontalCenterOffset: -100

    }
    Warning{
        id: warning
        temperature: root.temperature
        batteryLevel: root.batteryLevel
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}
