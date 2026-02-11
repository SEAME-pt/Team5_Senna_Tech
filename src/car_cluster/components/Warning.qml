import QtQuick 2.15

Item {
    id: root
    width: 200
    height: 200
    
    property int temperature: 45
    property int batteryLevel: 100

    function getWarningImage() {
        if (root.temperature > 70 && root.temperature < 80)
            return "../assets/warnings/warning_temp_rising.png"
        else if (root.temperature >= 80)
            return "../assets/warnings/warning_temp_max.png"
        else if (root.batteryLevel <= 15)
            return "../assets/warnings/warning_low_battery.png"
        else
            return ""
    }
    
    Image {
        id: warningImage
        anchors.fill: parent
        anchors.margins: 6
        source: getWarningImage()
        fillMode: Image.PreserveAspectFit
        smooth: true
        antialiasing: true

        // Animação de piscar contínua
        SequentialAnimation on opacity {
            id: blinkAnimation
            running: warningImage.source !== ""  // Anima apenas se houver imagem
            loops: Animation.Infinite
            
            PropertyAnimation {
                to: 0.3
                duration: 600  // Fade out em 600ms
            }
            PropertyAnimation {
                to: 1.0
                duration: 600  // Fade in em 600ms
            }
        }

        onStatusChanged: {
            if (status === Image.Error) {
                console.log("Erro ao carregar sinal: " + source)
            }
        }
    }
}
