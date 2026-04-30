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

enum class TRAFFIC_SIGN {
    NONE = 0,
    STOP = 1,
    DANGER = 2,
    CROSSWALK = 3,
    YIELD = 4, 
    RED = 5,
    YELLOW = 6,
    GREEN = 7,
};

enum class SPEED_SIGN {
    NONE = 10,
    SIGNAL_50 = 11,
    SIGNAL_80 = 12,
};

class vehicleData : public QObject
{
    Q_OBJECT
    Q_PROPERTY(double speed READ getSpeed NOTIFY speedChanged)
    Q_PROPERTY(int battery READ getBattery NOTIFY batteryChanged)
    Q_PROPERTY(int temperature READ getTemperature NOTIFY temperatureChanged)
    Q_PROPERTY(uint16_t odometer READ getOdometer NOTIFY odometerChanged)
    Q_PROPERTY(TRAFFIC_SIGN trafficSign READ getTrafficSign NOTIFY trafficSignChanged)
    Q_PROPERTY(SPEED_SIGN speedSign READ getSpeedSign NOTIFY speedSignChanged)
    Q_PROPERTY(QString gear READ getGear NOTIFY gearChanged)

    public:
        static vehicleData* instance(); //Singleton definition

        //GETTERS
        double          getSpeed() const;
        int             getBattery() const;
        int             getTemperature() const;
        uint16_t        getOdometer() const;
        TRAFFIC_SIGN    getTrafficSign() const;
        SPEED_SIGN      getSpeedSign() const;
        QString         getGear() const;

    signals:
        void    speedChanged();
        void    batteryChanged();
        void    temperatureChanged();
        void    odometerChanged();
        void    trafficSignChanged();
        void    speedSignChanged();
        void    gearChanged();

    public slots: // mudam os atributos e chamam os respectivos sinais
        void    setSpeed(double newSpeed);
        void    setBattery(int newBattery);
        void    setTemperature(int newTemperature);
        void    setOdometer(uint16_t newOdometer);
        void    setTrafficSign(TRAFFIC_SIGN newTrafficSign);
        void    setSpeedSign(SPEED_SIGN newSpeedSign);
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

        double        speed;
        int           battery;
        int           temperature;
        uint16_t      odometer;
        TRAFFIC_SIGN  trafficSign = TRAFFIC_SIGN::NONE;
        SPEED_SIGN    speedSign = SPEED_SIGN::NONE;
        QString       gear;

        // Thread para o gRPC
        std::thread kuksaThread;

};

#endif // VEHICLEDATA_H
