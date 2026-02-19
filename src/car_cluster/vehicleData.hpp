#ifndef VEHICLEDATA_H
#define VEHICLEDATA_H

#include <QObject>
#include <QTimer>
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <cstring>
#include <QSocketNotifier>
#include <fcntl.h>

#include <thread> // Necessário para rodar o gRPC sem travar a UI
#include <memory> // Necessário para std::shared_ptr
#include <grpcpp/grpcpp.h>
#include "kuksa/val/v2/val.grpc.pb.h"

using grpc::Channel;
using kuksa::val::v2::VAL;


class vehicleData : public QObject
{
    Q_OBJECT
    Q_PROPERTY(double speed READ getSpeed NOTIFY speedChanged)
    Q_PROPERTY(int battery READ getBattery NOTIFY batteryChanged)
    Q_PROPERTY(int temperature READ getTemperature NOTIFY temperatureChanged)
    Q_PROPERTY(unsigned int odometer READ getOdometer NOTIFY odometerChanged)
    Q_PROPERTY(QString trafficSign READ getTrafficSign NOTIFY trafficSignChanged)
    Q_PROPERTY(QString gear READ getGear NOTIFY gearChanged)

    public:
        static vehicleData* instance(); //Singleton definition

        //GETTERS
        double          getSpeed() const;
        int             getBattery() const;
        int             getTemperature() const;
        unsigned int    getOdometer() const;
        QString         getTrafficSign() const;
        QString         getGear() const;

    signals:
        void    speedChanged();
        void    batteryChanged();
        void    temperatureChanged();
        void    odometerChanged();
        void    trafficSignChanged();
        void    gearChanged();

    public slots: // mudam os atributos e chamam os respectivos sinais
        void    setSpeed(double newSpeed);
        void    setBattery(int newBattery);
        void    setTemperature(int newTemperature);
        void    setOdometer(int newOdometer);
        void    setTrafficSign(QString newTrafficSign);
        void    setGear(QString newGear);

        //SIMULATION
        void startSpeedSimulation();
        void startBatterySimulation();
        void startTrafficSignSimulation();
        
        void startKuksaSubscriber();
        void updateTemperature();
        void updateOdometer();

    private:
        vehicleData(QObject *parent = nullptr);

        void kuksaLoop();

        double      speed;
        int         battery;
        int         temperature;
        QString     trafficSign;
        QString     gear;

        // Thread para o gRPC
        std::thread kuksaThread;

};

#endif // VEHICLEDATA_H
