import QtQuick 2.15
import QtQuick.Effects

Item {
    id: root
    width: 250
    height: 250

    property real battery: 0
    property bool isDark: false
    property real autonomy: 74
    
    function getBatteryImage() {
        if (root.battery >= 76) {
            return root.isDark ? "../assets/battery/battery_dark_100.png" : "../assets/battery/battery_light_100.png"
        } else if (root.battery >= 51) {
            return root.isDark ? "../assets/battery/battery_dark_75.png" : "../assets/battery/battery_light_75.png"
        } else if (root.battery >= 31) {
            return root.isDark ? "../assets/battery/battery_dark_50.png" : "../assets/battery/battery_light_50.png"
        } else if (root.battery >= 16) {
            return root.isDark ? "../assets/battery/battery_dark_30.png" : "../assets/battery/battery_light_30.png"
        } else {
            return root.isDark ? "../assets/battery/battery_dark_15.png" : "../assets/battery/battery_light_15.png"
        }
    }
    
    Column {
        anchors.centerIn: parent
        anchors.horizontalCenterOffset: 10
        spacing: -35
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: -20
            text: Math.round(root.battery)
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

                Image {
                    id: autonomyImage
                    width: 28
                    height: 28
                    source: root.isDark ? "../assets/autonomy_dark.png" : "../assets/autonomy_light.png" 
                    fillMode: Image.PreserveAspectFit

                    smooth: true
                    antialiasing: true

                    onStatusChanged: {
                        if (status === Image.Error) {
                            console.log("Erro ao carregar a imagem: " + source)
                        }
                    }
                }
                
                Text {
                    text: root.autonomy + "km"
                    color:root.isDark ? '#ddeff8' : '#0b4659'
                    font.family: rajdhani.name
                    font.pixelSize: 25
                    font.bold: true
                }
            }

            Row {
                spacing: 3

                Text {
                    text: "%"
                    color:root.isDark ? '#ddeff8' : '#0b4659'
                    font.family: rajdhani.name
                    font.pixelSize: 25
                    font.bold: true
                }
                Image {
                    id: batteryImage
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: -5
                    width: 40
                    height: 40
                    source: root.getBatteryImage()

                    smooth: true
                    antialiasing: true

                    onStatusChanged: {
                        if (status === Image.Error) {
                            console.log("Erro ao carregar a imagem: " + source)
                        }
                    }
                }
            }
        }
    }
}