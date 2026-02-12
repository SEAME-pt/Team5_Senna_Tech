import QtQuick 2.15

Item {
    id: root
    width: 90
    height: 90
    
    property bool showSign: true
    property var currentTrafficSign: ""  // Aceitar QVariant
    
    
    function getTrafficSignImage() {
        if (currentTrafficSign == "stop")
            return "../assets/traffic/stop.png"
        else if (currentTrafficSign == "50")
            return "../assets/traffic/50.png"
        else if (currentTrafficSign == "80")
            return "../assets/traffic/80.png"
        else if (currentTrafficSign == "pedestrian")
            return "../assets/traffic/pedestrian.png"
        else if (currentTrafficSign == "danger")
            return "../assets/traffic/danger.png"
        else if (currentTrafficSign == "yield")
            return "../assets/traffic/yield.png"
        else if (currentTrafficSign == "red")
            return "../assets/traffic/traffic-light-red.png"
        else if (currentTrafficSign == "yellow")
            return "../assets/traffic/traffic-light-yellow.png"
        else if (currentTrafficSign == "green")
            return "../assets/traffic/traffic-light-green.png"
        else 
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
