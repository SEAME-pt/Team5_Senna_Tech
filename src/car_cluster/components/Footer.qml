import QtQuick 2.15

Item {
    id: root
        
    property string currentTime: ""
    property int temperature: 0
    property bool isDark: false
    
    Timer {
        id: clockTimer
        interval: 1000 // Atualiza a cada 1 segundo
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            var date = new Date()
            currentTime = date.toLocaleTimeString(Qt.locale("pt_PT"), "HH:mm")
        }
    }
    Text {
        anchors.left: parent.left 
        anchors.bottom: parent.bottom
        text: root.currentTime
        color: root.isDark ? '#ddeff8' : '#0b4659'
        font.family: rajdhani.name
        font.pixelSize: 22
        font.capitalization: Font.AllUppercase
        font.letterSpacing: 2
    }
    
    Text {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        text: root.temperature + "°C"
        color: root.isDark ? '#ddeff8' : '#0b4659'
        font.family: rajdhani.name
        font.pixelSize: 22
        font.bold: true
        font.letterSpacing: 2
    }
}