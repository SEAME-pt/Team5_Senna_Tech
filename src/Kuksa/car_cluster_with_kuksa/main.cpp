#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "vehicleData.hpp"
#include <QQuickStyle>


int main(int argc, char *argv[])
{

    QQuickStyle::setStyle("Basic");

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    vehicleData *vehicle = vehicleData::instance();

     engine.rootContext()->setContextProperty("vehicle", vehicle);

    const QUrl url(QStringLiteral("qrc:/car_cluster/Main.qml"));
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
    vehicle->startBatterySimulation();

    vehicle->startKuksaSubscriber();

    return app.exec();
}
