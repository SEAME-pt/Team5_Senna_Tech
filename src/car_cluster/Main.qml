import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: root
    width: 1200
    height: 400
    visible: true
    color: "#0b0f14"
    title: "Car Cluster - Demo"


    Rectangle {
        anchors.fill: parent
        color: "transparent"
        RowLayout {
            anchors.fill: parent
            anchors.margins: 24
            spacing: 24


            Rectangle {
                id: speedPanel
                Layout.preferredWidth: parent.width * 0.62
                Layout.alignment: Qt.AlignVCenter
                Layout.fillHeight: true
                radius: 16
                color: "#0f1720"
                border.color: "#A7FF0A"
                border.width: 1
                anchors.verticalCenter: parent.verticalCenter
                Row {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 20


                    Item {
                        anchors.centerIn: parent
                        width: parent.height - 10
                        height: width

                        Canvas {
                            id: dial
                            anchors.centerIn: parent
                            width: parent.width
                            height: parent.height
                            onPaint: {
                                var ctx = getContext("2d");
                                ctx.reset();
                                var cx = width/2;
                                var cy = height/2 + 1.5;
                                var radius = Math.min(width, height) * 0.35;

                                // background ring
                                ctx.beginPath();
                                ctx.arc(cx, cy, radius+20, Math.PI*0.75, Math.PI*0.25, false);
                                ctx.lineWidth = 15;
                                ctx.strokeStyle = "#A7FF0A";
                                ctx.stroke();

                                // ticks
                                var minAngle = Math.PI*0.75;
                                var maxAngle = Math.PI*0.25 + 2*Math.PI;

                                var totalAngle = 1.5*Math.PI;
                                var maxSpeed = 240.0;
                                for (var i=0;i<=120;i++){
                                    var fraction = i/120.0;
                                    var angle = minAngle + fraction * totalAngle;
                                    var x1 = cx + (radius+10)*Math.cos(angle);
                                    var y1 = cy + (radius+10)*Math.sin(angle);
                                    var x2 = cx + (radius-10)*Math.cos(angle);
                                    var y2 = cy + (radius-10)*Math.sin(angle);
                                    ctx.beginPath();
                                    ctx.moveTo(x1,y1);
                                    ctx.lineTo(x2,y2);
                                    ctx.lineWidth = 1;
                                    ctx.strokeStyle = "#4a5560";
                                    ctx.stroke();

                                    ctx.font = "36px sans-serif";
                                    ctx.fillStyle = "#ffffff";
                                    ctx.textAlign = "center";
                                    ctx.textBaseline = "middle";
                                    var speedd = clusterBackend.speed;
                                    ctx.fillText(Math.round(speedd).toString(), cx, cy-15);

                                    ctx.font = "24px  sans-serif";
                                    ctx.fillStyle = "#ffffff";
                                    ctx.textAlign = "center";
                                    ctx.textBaseline = "middle";
                                    ctx.fillText("Km/h", cx, cy+25);
                                }

                                var speed = clusterBackend.speed;
                                var speedFraction = Math.min(1.0, Math.max(0.0, speed / maxSpeed));
                                var endAngle = minAngle + speedFraction * totalAngle;

                                var grad = ctx.createLinearGradient(cx-radius,cy, cx+radius,cy);
                                grad.addColorStop(0.0, "#487CBD");
                                grad.addColorStop(0.6, "#295791");
                                grad.addColorStop(1.0, "#133969");
                                ctx.beginPath();
                                ctx.arc(cx, cy, radius, minAngle, endAngle, false);
                                ctx.lineWidth = 20;
                                ctx.strokeStyle = grad;
                                ctx.lineCap = "square";
                                ctx.stroke();
                            }
                        }

                        Connections {
                            target: clusterBackend
                            onSpeedChanged: dial.requestPaint()
                        }
                    }

                }
            }

            Rectangle {
                Layout.preferredWidth: parent.width * 0.34
                Layout.alignment: Qt.AlignVCenter
                Layout.fillHeight: true
                radius: 16
                color: "#071421"
                border.color: "#A7FF0A"
                border.width: 1

                    Column {
                        anchors.centerIn: parent
                        spacing: 20

                        Text {
                            id: batteryText
                            text: qsTr("Battery")
                            color: "#ffffff"
                            font.pixelSize: 33
                            horizontalAlignment: Text.AlignHCenter
                            anchors.horizontalCenter: parent.horizontalCenter
                        }

                        Rectangle {
                            id: barOutline
                            width: 200
                            height: 40
                            // radius: 10
                            color: "#071c24"
                            border.color: "#102429"
                            border.width: 2
                            anchors.horizontalCenter: parent.horizontalCenter

                            Rectangle {
                                id: barFill
                                width: (barOutline.width - 4) * clusterBackend.battery / 100.0
                                height: barOutline.height - 4
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: parent.left
                                anchors.leftMargin: 2
                                // radius: 8
                                gradient: Gradient {
                                    GradientStop { position: 0.0; color: clusterBackend.battery > 50 ? "#A7FF0A" :
                                                                   clusterBackend.battery > 20 ? "#FF6403" : "#FF0303" }
                                    GradientStop { position: 1.0; color: clusterBackend.battery > 50 ? "#10b981" :
                                                                   clusterBackend.battery > 20 ? "#FFC003" : "#FF5F03" }
                                }
                            }

                            Text {
                                text: clusterBackend.battery + "%"
                                anchors.centerIn: parent
                                color: "#e6f0f8"
                                font.pixelSize: 14
                            }
                    }

                    Connections {
                        target: clusterBackend
                    }
                }
            }
        }
    }
}
