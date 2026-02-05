import QtQuick 2.15
import QtQuick.Effects

Item {
    id: root
    width: 250
    height: 250

    // Propriedades configuráveis
    property real speed: 0
    property real maxSpeed: 20
    property color accentColor: "white" // Cor da barra
    property real lineWidth: 25
    property string unitText: "km/h"

    // Animação suave para o valor da velocidade
    Behavior on speed {
        NumberAnimation { duration: 250; easing.type: Easing.OutCubic }
    }

    // O Canvas redesenha sempre que a propriedade 'speed' mudar
    onSpeedChanged: canvas.requestPaint()

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

            // Ângulos em Radianos 
            var startAngle = 0.5 * Math.PI;
            var endAngle = 1.5 * Math.PI;
            
            // Cálculo do progresso atual baseado na velocidade (0 a 20)
            var progress = Math.min(Math.max(root.speed / root.maxSpeed, 0), 1);
            var currentAngle = startAngle + (progress * (endAngle - startAngle));

            // 1. Desenhar o Fundo do Arco (Trilha vazia)
            ctx.beginPath();
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.1); // Branco com 10% de opacidade
            ctx.lineWidth = root.lineWidth;
            ctx.lineCap = "round";
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.stroke();

            // 2. Desenhar a Barra de Velocidade (O progresso)
            ctx.beginPath();
            ctx.strokeStyle = root.accentColor;
            ctx.lineWidth = root.lineWidth;
            ctx.lineCap = "round";
            ctx.arc(centerX, centerY, radius, startAngle, currentAngle);
            ctx.stroke();
        }
    }

   MultiEffect {
        anchors.fill: canvas
        source: canvas
        
        // Configurações de Brilho (Blur/Glow)
        blurEnabled: true
        blur: 0.5            // Intensidade do borrão (0.0 a 1.0)
        
        // Para criar o efeito de cor (o brilho verde-azulado)
        // No MultiEffect, usamos o shadow para simular o glow colorido
        shadowEnabled: true
        shadowColor: "#00F5FF"
        shadowBlur: 0.8
        shadowHorizontalOffset: 0
        shadowVerticalOffset: 0
    }

    // Texto Centralizado
    Column {
        anchors.centerIn: parent
        spacing: -5

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: 20
            text: Math.round(root.speed)
            color: "white"
            font.family: sonic_turbo.name
            font.pixelSize: 82
            font.bold: true
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.horizontalCenterOffset: 20
            text: unitText
            color: "#888888"
            font.family: sonic_turbo.name
            font.pixelSize: 25
        }
    }
}