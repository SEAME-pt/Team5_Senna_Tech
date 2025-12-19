import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: root
    width: 1480
    height: 400
    visible: true
    //flags: Qt.Window | Qt.FramelessWindowHint
    title: "Sea:Me Instrument Cluster"

    // Properties
    property real currentSpeed: Math.round(Number(vehicle.speed))
    property real maxSpeed: 20
    property string currentGear: "D"
    property int batteryLevel:Math.round(Number(vehicle.battery))
    property int temperature: 45
    property int range: 245

    Rectangle {
           anchors.fill: parent
           gradient: Gradient {
               GradientStop { position: 0.0; color: "#ff9800" }
               GradientStop { position: 1.0; color: "#e65100"  }
           }

    // Main Dashboard Layout
    Row {
        anchors.centerIn: parent
        anchors.margins: 10       // margem opcional
        spacing: 30
        // Left Panel - Speedometer
        Rectangle {
            width: 450
            height: 330
            radius: 24
            color: Qt.rgba(1, 1, 1, 0.03)
            border.color: Qt.rgba(1, 1, 1, 0.1)
            border.width: 1

            Column {
                anchors.centerIn: parent
                spacing: 20

                // Speed Circle
                Item {
                    width: 260
                    height: 260
                    anchors.horizontalCenter: parent.horizontalCenter

                    // Background circle
                    Canvas {
                        id: bgCircle
                        anchors.fill: parent
                        onPaint: {
                            var ctx = getContext("2d")
                            ctx.clearRect(0, 0, width, height)
                            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.1)
                            ctx.lineWidth = 12
                            ctx.lineCap = "round"
                            ctx.beginPath()
                            ctx.arc(width/2, height/2, 115, 0, 2 * Math.PI)
                            ctx.stroke()
                        }
                    }

                    // Speed arc
                    Canvas {
                        id: speedArc
                        anchors.fill: parent

                        property real percentage: currentSpeed / maxSpeed
                        property color startColor: getStartColor()
                        property color endColor: getEndColor()

                        function getStartColor() {
                            if (percentage < 0.33) return "#00d4ff"
                            else if (percentage < 0.66) return "#00ffff"
                            else return "#ffaa00"
                        }

                        function getEndColor() {
                            if (percentage < 0.33) return "#00ffff"
                            else if (percentage < 0.66) return "#ffaa00"
                            else return "#ff3366"
                        }

                        onPaint: {
                            var ctx = getContext("2d")
                            ctx.clearRect(0, 0, width, height)

                            var gradient = ctx.createLinearGradient(0, 0, width, height)
                            gradient.addColorStop(0, startColor)
                            gradient.addColorStop(1, endColor)

                            ctx.strokeStyle = gradient
                            ctx.lineWidth = 12
                            ctx.lineCap = "round"
                            ctx.beginPath()
                            ctx.arc(width/2, height/2, 115, -Math.PI/2, -Math.PI/2 + (percentage * 2 * Math.PI))
                            ctx.stroke()
                        }

                        Behavior on percentage {
                            enabled: currentSpeed !== 0
                            NumberAnimation { duration: 500; easing.type: Easing.OutCubic }
                        }
                    }

                    // Speed value
                    Column {
                        anchors.centerIn: parent
                        spacing: 5

                        Text {
                            id: speedText
                            text: Math.round(currentSpeed)
                            font.pixelSize: 72
                            font.bold: true
                            color: "white"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Text {
                            text: "km/h"
                            font.pixelSize: 18
                            color: Qt.rgba(1, 1, 1, 0.6)
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                Text {
                    text: "SPEED"
                    font.pixelSize: 14
                    font.letterSpacing: 2
                    color: Qt.rgba(1, 1, 1, 0.5)
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }

        // Center Panel - Car View
        Rectangle {
            width: 450
            height: 330
            radius: 24
            color: Qt.rgba(1, 1, 1, 0.03)
            border.color: Qt.rgba(1, 1, 1, 0.1)
            border.width: 1

                // Road container
                Item {
                    width: 300
                    height: 450
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    clip: true

                    // Road
                    Rectangle {
                        id: road
                        width: 250
                        height: parent.height
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter

                        transform: [
                            Rotation {
                                origin.x: road.width / 2
                                origin.y: road.height / 2
                                axis { x: 1; y: 0; z: 0 }
                                angle: 60
                            }
                        ]

                        gradient: Gradient {
                            GradientStop { position: 0.0; color: Qt.rgba(0.31, 0.31, 0.31, 0.3) }
                            GradientStop { position: 1.0; color: Qt.rgba(0.24, 0.24, 0.24, 0.5) }
                        }

                        border.color: Qt.rgba(1, 1, 1, 0.2)
                        border.width: 2

                        // Road lines
                        Repeater {
                            model: 1

                            Rectangle {
                                width: 4
                                height: 40
                                color: Qt.rgba(1, 1, 1, 0.6)
                                anchors.horizontalCenter: parent.horizontalCenter

                                property real spacing: road.height / model
                                property real startY: -height + index * spacing
                                y: startY

                                Timer {
                                    interval: 16   // ~60 FPS
                                    running: currentSpeed > 0
                                    repeat: true
                                    onTriggered: {
                                        // delta proporcional à velocidade
                                        var delta = currentSpeed / maxSpeed * 10
                                        y += delta

                                        // reset quando passar do container
                                        if (y > road.height - 40) {
                                            y = -height + 40
                                        }
                                    }
                                }
                            }
                        }



                    // Car icon
                        Item {
                            width: 180    // largura do container
                            height: 350// altura do container
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: -30

                            Image {
                                anchors.fill: parent
                                source: "mclaren.png"
                                fillMode: Image.Stretch
                                smooth: true
                            }
                        }
                        Row {
                            id: gearRow
                            spacing: 15
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.top: parent.top
                                            // Adicionada uma margem para movê-lo um pouco para baixo
                            anchors.topMargin: -100

                            Repeater {
                                model: ["P", "R", "N", "D", "S"]

                                Rectangle {
                                    width: 50
                                    height: 50
                                    radius: 12
                                    color: currentGear === modelData ? "transparent" : Qt.rgba(1, 1, 1, 0.05)
                                    border.width: 2
                                    border.color: currentGear === modelData ? "#00ff88" : Qt.rgba(1, 1, 1, 0.1)

                                    gradient: currentGear === modelData ? activeGradient : null

                                    Gradient {
                                        id: activeGradient
                                        GradientStop { position: 0.0; color: "#00ff88" }
                                        GradientStop { position: 1.0; color: "#00cc66" }
                                    }

                                     Rectangle {
                                        visible: currentGear === modelData
                                        anchors.fill: parent
                                        anchors.margins: -8
                                        radius: 20
                                        color: "transparent"
                                        border.color: Qt.rgba(0, 1, 0.53, 0.3)
                                        border.width: 8
                                        z: -1
                                    }

                                    Text {
                                        text: modelData
                                        font.pixelSize: 20
                                        font.bold: true
                                        color: currentGear === modelData ? "black" : "white"
                                        anchors.centerIn: parent
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: currentGear = modelData
                                    }

                                    scale: currentGear === modelData ? 1.1 : 1.0
                                    Behavior on scale {
                                        NumberAnimation { duration: 300; easing.type: Easing.OutBack }
                                    }
                                }
                             }
                        }
                    }
            }
        }

        // Right Panel - Stats
        Rectangle {
            width: 450
            height: 330
            radius: 24
            color: Qt.rgba(1, 1, 1, 0.03)
            border.color: Qt.rgba(1, 1, 1, 0.1)
            border.width: 1

            Column {
                anchors.centerIn: parent
                spacing: 15
                width: parent.width - 60

                // Battery
                Column {
                    width: parent.width
                    spacing: 10

                    Row {
                        spacing: 12

                        Text {
                            text: "🔋"
                            font.pixelSize: 24
                        }

                        Text {
                            text: "BATTERY"
                            font.pixelSize: 14
                            font.letterSpacing: 1
                            color: Qt.rgba(1, 1, 1, 0.6)
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 8
                        radius: 10
                        color: Qt.rgba(1, 1, 1, 0.1)

                        Rectangle {
                            id: batteryBar
                            width: parent.width * (batteryLevel / 100)
                            height: parent.height
                            radius: 10

                            // cor dinâmica conforme o nível
                            color: batteryLevel <= 15
                                   ? "#ff3b30"   // vermelho
                                   : batteryLevel <= 50
                                     ? "#ffd60a" // amarelo
                                     : "#00ff88" // verde

                            // glow suave com cor correspondente
                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: -4
                                radius: 14
                                color: "transparent"
                                border.color: batteryLevel <= 15
                                              ? Qt.rgba(1, 0, 0, 0.3)
                                              : batteryLevel <= 50
                                                ? Qt.rgba(1, 0.84, 0, 0.3)
                                                : Qt.rgba(0, 1, 0.53, 0.3)
                                border.width: 4
                                z: -1
                            }

                            // animação de transição de tamanho (e cor)
                            Behavior on width {
                                NumberAnimation { duration: 500; easing.type: Easing.OutCubic }
                            }

                            Behavior on color {
                                ColorAnimation { duration: 300; easing.type: Easing.InOutQuad }
                            }
                        }
                    }

                    Row {
                        Text {
                            text: batteryLevel
                            font.pixelSize: 24
                            font.bold: true
                            color: "white"
                        }

                        Text {
                            text: " %"
                            font.pixelSize: 14
                            color: Qt.rgba(1, 1, 1, 0.5)
                            anchors.baseline: parent.children[0].baseline
                        }
                    }
                }

                // Temperature
                Column {
                    width: parent.width
                    spacing: 10

                    Row {
                        spacing: 12

                        Text {
                            text: "🌡️"
                            font.pixelSize: 24
                        }

                        Text {
                            text: "TEMPERATURE"
                            font.pixelSize: 14
                            font.letterSpacing: 1
                            color: Qt.rgba(1, 1, 1, 0.6)
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 8
                        radius: 10
                        color: Qt.rgba(1, 1, 1, 0.1)

                        Rectangle {
                            width: parent.width * (temperature / 100)
                            height: parent.height
                            radius: 10
                            color: "#00d4ff"

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: -4
                                radius: 14
                                color: "transparent"
                                border.color: Qt.rgba(0, 0.83, 1, 0.3)
                                border.width: 4
                                z: -1
                            }

                            Behavior on width {
                                NumberAnimation { duration: 500; easing.type: Easing.OutCubic }
                            }
                        }
                    }

                    Row {
                        Text {
                            text: temperature
                            font.pixelSize: 24
                            font.bold: true
                            color: "white"
                        }

                        Text {
                            text: " °C"
                            font.pixelSize: 14
                            color: Qt.rgba(1, 1, 1, 0.5)
                            anchors.baseline: parent.children[0].baseline
                        }
                    }
                }

                // Range
                Column {
                    width: parent.width
                    spacing: 10

                    Row {
                        spacing: 12

                        Text {
                            text: "📍"
                            font.pixelSize: 24
                        }

                        Text {
                            text: "AUTONOMY"
                            font.pixelSize: 14
                            font.letterSpacing: 1
                            color: Qt.rgba(1, 1, 1, 0.6)
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 8
                        radius: 10
                        color: Qt.rgba(1, 1, 1, 0.1)

                        Rectangle {
                            width: parent.width * (range / 300)
                            height: parent.height
                            radius: 10
                            color: "#ffaa00"

                            Rectangle {
                                anchors.fill: parent
                                anchors.margins: -4
                                radius: 14
                                color: "transparent"
                                border.color: Qt.rgba(1, 0.67, 0, 0.3)
                                border.width: 4
                                z: -1
                            }

                            Behavior on width {
                                NumberAnimation { duration: 500; easing.type: Easing.OutCubic }
                            }
                        }
                    }

                    Row {
                        Text {
                            text: range
                            font.pixelSize: 24
                            font.bold: true
                            color: "white"
                        }

                        Text {
                            text: " km"
                            font.pixelSize: 14
                            color: Qt.rgba(1, 1, 1, 0.5)
                            anchors.baseline: parent.children[0].baseline
                        }
                    }
                }
            }
        }
    }

    Timer {
        id: slowDownTimer
        interval: 2000
        repeat: false

        onTriggered: {
            decelTimer.start()
        }
    }

    Timer {
        id: decelTimer
        interval: 100
        repeat: true

        onTriggered: {
            currentSpeed -= 0.5
            if (currentSpeed <= 0) {
                currentSpeed = 0
                stop()
                simulationTimer.accelerating = true
            }
        }
    }

    // Redraw speed arc when speed changes
    Connections {
        target: root
        function onCurrentSpeedChanged() {
            speedArc.requestPaint()
        }
    }
    }
}
