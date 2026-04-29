import QtQuick 2.15

Item {
    id: root
    width: 100
    height: 100
    
    property bool showSign: true
    property var currentTrafficSign: ""  
    
    function getTrafficSignImage() {
        if (currentTrafficSign == 1)
            return "../assets/traffic/stop.png"
        else if (currentTrafficSign == 11)
            return "../assets/traffic/50.png"
        else if (currentTrafficSign == 12)
            return "../assets/traffic/80.png"
        else if (currentTrafficSign == 3)
            return "../assets/traffic/crosswalk.png"
        else if (currentTrafficSign == 2)
            return "../assets/traffic/danger.png"
        else if (currentTrafficSign == 4)
            return "../assets/traffic/yield.png"
        else if (currentTrafficSign == 5)
            return "../assets/traffic/red.png"
        else if (currentTrafficSign == 6)
            return "../assets/traffic/yellow.png"
        else if (currentTrafficSign == 7)
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
