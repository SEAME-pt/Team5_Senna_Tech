import QtQuick 2.15

Item {
    id: root
    width: 100
    height: 100
    
    property bool showSign: true
    property var currentTrafficSign: ""  // Aceitar QVariant
    
    function getTrafficSignImage() {
        if (currentTrafficSign == "stop")
            return "../assets/traffic/stop.png"
        else if (currentTrafficSign == "50")
            return "../assets/traffic/50.png"
        else if (currentTrafficSign == "80")
            return "../assets/traffic/80.png"
        else if (currentTrafficSign == "crosswalk")
            return "../assets/traffic/crosswalk.png"
        else if (currentTrafficSign == "danger")
            return "../assets/traffic/danger.png"
        else if (currentTrafficSign == "yield")
            return "../assets/traffic/yield.png"
        else if (currentTrafficSign == "red")
            return "../assets/traffic/red.png"
        else if (currentTrafficSign == "yellow")
            return "../assets/traffic/yellow.png"
        else if (currentTrafficSign == "green")
            return "../assets/traffic/green.png"
        return ""
    }
    // Exibir/ocultar com animação
    opacity: showSign ? 1.0 : 0.0
    Behavior on opacity { NumberAnimation { duration: 500 } }
    
    Image {
        id: trafficImage
        anchors.fill: parent
        anchors.margins: 6
        source: getTrafficSignImage()
        fillMode: Image.PreserveAspectFit
        smooth: true
        antialiasing: true

        onStatusChanged: {
            if (status === Image.Error) {
                console.log("Erro ao carregar sinal: " + source)
            }
        }
    }
}
