#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "vehicleData.hpp"
#include <QQuickStyle>
#include <QProcessEnvironment>


int main(int argc, char *argv[])
{

    QQuickStyle::setStyle("Basic");

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    vehicleData *vehicle = vehicleData::instance();

     engine.rootContext()->setContextProperty("vehicle", vehicle);

    const bool previewRobotaxi = QProcessEnvironment::systemEnvironment().value("ROBOTAXI_PREVIEW") == "1";
    engine.rootContext()->setContextProperty("robotaxiPreviewEnabled", previewRobotaxi);

    const bool useRobotaxiUi = QProcessEnvironment::systemEnvironment().value("ROBOTAXI_CLUSTER") == "1";
    const QUrl url(useRobotaxiUi
        ? QUrl(QStringLiteral("qrc:/car_cluster/MainRobotaxi.qml"))
        : QUrl(QStringLiteral("qrc:/car_cluster/Main.qml")));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
                         if (!obj && url == objUrl)
                             QCoreApplication::exit(-1);
                     }, Qt::QueuedConnection);
    engine.load(url);

    if (engine.rootObjects().isEmpty()) {
        qDebug() << "ERRO: QML não carregou!";
        return -1;
    }

    //vehicle->startReadCan();
    //vehicle->startBatterySimulation();
    //vehicle->startSpeedSimulation();
    //vehicle->startTrafficSignSimulation();

    if (!previewRobotaxi) {
        vehicle->startKuksaSubscriber();
    }

    return app.exec();
}
