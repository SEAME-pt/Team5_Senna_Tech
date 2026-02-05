#ifndef VEHICLEDATA_H
#define VEHICLEDATA_H

#include <QObject>
#include <QTimer>
#include <QDebug>
#include <iostream>
#include <unistd.h>
//#include <sys/socket.h>
//#include <linux/can.h>
//#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <cstring>
#include <QSocketNotifier>
#include <fcntl.h>

//add na troca pelo kuksa
#include <thread> // Necessário para rodar o gRPC sem travar a UI
#include <memory> // Necessário para std::shared_ptr
//#include <grpcpp/grpcpp.h>
//#include "kuksa/val/v2/val.grpc.pb.h"

//using grpc::Channel;
//using kuksa::val::v2::VAL;


class vehicleData : public QObject
{
    Q_OBJECT
    Q_PROPERTY(double speed READ getSpeed NOTIFY speedChanged)
    Q_PROPERTY(int battery READ getBattery NOTIFY batteryChanged)
    Q_PROPERTY(int temperature READ getTemperature NOTIFY temperatureChanged)
    Q_PROPERTY(bool isCharging READ getIsCharging NOTIFY chargingChanged)


    public:
        static vehicleData* instance(); //Singleton definition

        //GETTERS
        double  getSpeed() const;
        int     getBattery() const;
        int     getTemperature() const;
        bool    getIsCharging() const;

    signals:
        void    speedChanged();
        void    batteryChanged();
        void    temperatureChanged();
        void    chargingChanged();

    public slots: // mudam os atributos e chamam os respectivos sinais
        void    setSpeed(double newSpeed);
        void    setBattery(int newBattery);
        void    setTemperature(int newTemperature);
        void    setCharging(bool newCharging);

        //SIMULATION
        void startSpeedSimulation();
        void startBatterySimulation();
        //void startKuksaSubscriber();



    private:
        vehicleData(QObject *parent = nullptr);

        //void kuksaLoop();

        double  speed;
        int     battery;
        int     temperature;
        bool    isCharging;

        // Thread para o gRPC
        //std::thread kuksaThread;

};

#endif // VEHICLEDATA_H
