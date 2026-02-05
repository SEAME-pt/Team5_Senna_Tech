import QtQuick 2.15
import QtQuick.Controls 2.15
import "components"

ApplicationWindow {

    id: root
    width: 1280
    height: 400
    visible: true
    //flags: Qt.Window | Qt.FramelessWindowHint
    title: "Sea:Me Instrument Cluster"

    FontLoader {
        id: sonic_turbo
        source: "assets/Sonic_Turbo.otf"
    }
    // Propriedades para armazenar os textos formatados
    property string currentTime: ""
    property string currentDate: ""

    Timer {
        id: clockTimer
        interval: 1000 // Atualiza a cada 1 segundo
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            var date = new Date()
            currentTime = date.toLocaleTimeString(Qt.locale("pt_PT"), "HH:mm")
            currentDate = date.toLocaleDateString(Qt.locale("en_US"), "dd MMM yyyy")
        }
    }
    // Properties
    property real currentSpeed: Math.round(Number(vehicle.speed))
    property real maxSpeed: 20
    property string currentGear: "D"
    property int batteryLevel:Math.round(Number(vehicle.battery))
    property int temperature: 45
    property int range: 245
    // speed unit change
    property bool isM_S: false
    property real displaySpeed: isM_S ? (currentSpeed / 3.6) : currentSpeed
    property real displayMaxSpeed: isM_S ? (20 / 3.6) : 20
    property string unitText: isM_S ? "m/s" : "km/h"
    // cluster mode
    property bool isDark: false

    Image {
            id: clusterImage
            anchors.fill: parent

            // Caminho para o recurso (ajuste se estiver dentro de um prefixo no .qrc)
            source: isDark ? "assets/cluster_dark.png" : "assets/cluster_light.png" 

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
    Item {
        id: header
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 20 // Espaçamento das bordas da tela

        // DATA - Canto Superior Esquerdo
        Text {
            anchors.left: parent.left 
            anchors.top: parent.top
            anchors.leftMargin: 80
            text: root.currentDate
            color: "white"
            font.family: sonic_turbo.name
            font.pixelSize: 20
            font.capitalization: Font.AllUppercase
            font.letterSpacing: 2
        }

        // HORA - Canto Superior Direito
        Text {
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 80
            text: root.currentTime
            color: "white" // Hora em branco puro para maior destaque
            font.family: sonic_turbo.name
            font.pixelSize: 20
            font.bold: true
            font.letterSpacing: 1
        }
    }
    Button {
        id: switchUnit
        text: isM_S ? "SWITCH TO KM/H" : "SWITCH TO M/S"
        anchors.bottom: parent.bottom
        x: (parent.width / 4) - (width / 2) + 40 
        anchors.bottomMargin: 20
        
        onClicked: root.isM_S   = !root.isM_S
    
        contentItem: Text {
            text: parent.text
            font: sonic_turbo.name
            color: "white"
            horizontalAlignment: Text.AlignHCenter
        }
        background: Rectangle {
            color: Qt.rgba(1, 1, 1, 0.2)
            radius: 7
        }
    }
    Button {
        id:switchMode
        text: isDark ? "LIGHT MODE" : "DARK MODE"
        anchors.bottom: parent.bottom
        x: (parent.width / 5) - (width)
        anchors.bottomMargin: 20
        
        onClicked: root.isDark   = !root.isDark
    
        contentItem: Text {
            text: parent.text
            font: sonic_turbo.name
            color: "white"
            horizontalAlignment: Text.AlignHCenter
        }
        background: Rectangle {
            color: Qt.rgba(1, 1, 1, 0.2)
            radius: 7
        }
    }
    SpeedArc{
        anchors.verticalCenter: parent.verticalCenter 
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: - parent.width / 4
        speed: root.displaySpeed
        maxSpeed: root.displayMaxSpeed
        unitText: root.unitText
    }
    BatteryArc {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: parent.width / 4
        battery: root.batteryLevel // Sua propriedade vinculada ao C++
        accentColor: "white" // Um verde "Spring Green" para bateria
    }
}
