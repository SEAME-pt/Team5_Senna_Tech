#ifndef VEHICLEDATA_H
#define VEHICLEDATA_H

#include <QObject>
#include <QTimer>
#include <QDebug>
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
        void startReadCan();



    private:
        vehicleData(QObject *parent = nullptr);

        double  speed;
        int     battery;
        int     temperature;
        bool    isCharging;

};

#endif // VEHICLEDATA_H
