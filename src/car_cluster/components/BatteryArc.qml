import QtQuick 2.15
import QtQuick.Effects

Item {
    id: root
    width: 250
    height: 250

    property real battery: 0
    property color accentColor: "white"
    property real lineWidth: 25

    Behavior on battery {
        NumberAnimation { duration: 250; easing.type: Easing.OutCubic }
    }

    onBatteryChanged: canvas.requestPaint()

    // Canvas 1: Desenha apenas o trilho (SEM BRILHO)
    Canvas {
        id: backgroundCanvas
        anchors.fill: parent
        antialiasing: true
        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            var centerX = width / 2;
            var centerY = height / 2;
            var radius = (Math.min(width, height) / 2) - root.lineWidth;

            ctx.beginPath();
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.1);
            ctx.lineWidth = root.lineWidth;
            ctx.lineCap = "round";
            // IMPORTANTE: o 'true' no final força o caminho pela DIREITA (D)
            ctx.arc(centerX, centerY, radius, 0.5 * Math.PI, -0.5 * Math.PI, true);
            ctx.stroke();
        }
    }

    // Canvas 2: Desenha apenas a barra colorida (COM BRILHO)
    Canvas {
        id: canvas
        anchors.fill: parent
        antialiasing: true
        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            var centerX = width / 2;
            var centerY = height / 2;
            var radius = (Math.min(width, height) / 2) - root.lineWidth;

            var startAngle = 0.5 * Math.PI; 
            var endAngle = -0.5 * Math.PI;
            var progress = Math.min(Math.max(root.battery / 100, 0), 1);
            var currentAngle = startAngle + (progress * (endAngle - startAngle));

            ctx.beginPath();
            ctx.strokeStyle = root.accentColor;
            ctx.lineWidth = root.lineWidth;
            ctx.lineCap = "round";
            // O 'true' garante que a barra suba pela DIREITA
            ctx.arc(centerX, centerY, radius, startAngle, currentAngle, true);
            ctx.stroke();
        }
    }

    // Agora o MultiEffect só enxerga o 'canvas' (a barra), ignorando o fundo
    MultiEffect {
        anchors.fill: canvas
        source: canvas
        blurEnabled: true
        blur: 0.4
        shadowEnabled: true
        shadowColor: "#00F5FF"
        shadowBlur: 0.7
        shadowHorizontalOffset: 0
        shadowVerticalOffset: 0
    }

    Column {
        anchors.centerIn: parent
        spacing: -5
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: -20
            text: Math.round(root.battery)
            color: "white"
            font.family: sonic_turbo.name
            font.pixelSize: 82
            font.bold: true
        }
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: -20
            text: "%"
            color: "#888888"
            font.family: sonic_turbo.name
            font.pixelSize: 25
        }
    }
}