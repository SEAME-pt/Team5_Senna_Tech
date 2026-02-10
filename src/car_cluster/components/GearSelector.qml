import QtQuick 2.15

Item {
    id: root
    width: 200
    height: 40

    property string currentGear: "D"
    property bool isDark: false

    Row {
        anchors.centerIn: parent
        spacing: 15

        // Função auxiliar para criar cada letra
        Repeater {
            model: ["P", "R", "N", "D"]
            delegate: Text {
                text: modelData
                font.family: michroma.name
                font.pixelSize: 30
                font.bold: root.currentGear === modelData
                font.underline: root.currentGear === modelData
                
                // Cor: Verde se for a marcha atual, branco translúcido se não for
                color: root.currentGear === modelData ? root.isDark ? '#53c9ce' : '#0b4659' : '#86797e'
                
                // Efeito sutil de escala na marcha ativa
                scale: root.currentGear === modelData ? 1.2 : 1.0

                Behavior on scale { NumberAnimation { duration: 200 } }
                Behavior on color { ColorAnimation { duration: 200 } }
            }
        }
    }
}