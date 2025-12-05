#include "vehicleData.hpp"

// Singleton implementation
vehicleData *vehicleData::instance() {
    static vehicleData data;
    return &data;
}

//Private constructor
vehicleData::vehicleData(QObject *parent) : speed(0), battery(0), temperature(50), isCharging(false) {(void) parent;}

// Getters
double vehicleData::getSpeed() const{ return speed;}

int vehicleData::getBattery() const { return battery;}

int vehicleData::getTemperature() const{ return temperature;}

bool vehicleData::getIsCharging() const{ return isCharging;}

//Slots
void    vehicleData::setSpeed(double newSpeed) {
    if (this->speed == newSpeed)
        return ;
    this->speed = newSpeed;
    emit speedChanged();
}

void    vehicleData::setBattery(int newBattery){
    if (this->battery == newBattery)
        return ;
    this->battery = newBattery;
    emit batteryChanged();
}

void    vehicleData::setTemperature(int newTemperature){
    if (this->temperature == newTemperature)
        return ;
    this->temperature = newTemperature;
    emit temperatureChanged();
}

void    vehicleData::setCharging(bool newCharging){
    if (this->isCharging == newCharging)
        return ;
    this->isCharging = newCharging;
    emit chargingChanged();
}

//SIMULATION TESTS
void vehicleData::startSpeedSimulation() {
    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        speed += 0.2;                 // aumenta 0.2 km/h por tick
        if (speed > 20.0) speed = 0.0; // reinicia se passar de 20
        emit speedChanged();
    });
    timer->start(100); // 100 ms por tick -> 10 Hz
}

void vehicleData::startBatterySimulation() {
    this->battery = 100;
    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        battery -= 0.1;
        if (battery <= 0) battery = 100;
        emit batteryChanged();
    });
    timer->start(1000); // 1000 ms por tick -> 1 Hz
}



