#include <gtest/gtest.h>
#include "../../src/car_cluster/vehicleData.hpp"

class vehicleTest : public testing::Test {

    public: 
        vehicleData *car;
        
        vehicleTest() { car = vehicleData::instance(); }

    void SetUp() override {
        car->setBattery(100); 
        car->setSpeed(4);
        car->setTemperature(50); 
        car->setCharging(false);
    }
};

// - - - - INIT STRUCT TEST - - - - 
TEST_F(vehicleTest, StructInitialization) {
    EXPECT_EQ(car->getSpeed(), 4);
    EXPECT_EQ(car->getBattery(), 100);
    EXPECT_EQ(car->getTemperature(), 50);
    EXPECT_EQ(car->getIsCharging(), false);
}

// - - - - SPEED TESTS - - - - 
TEST_F(vehicleTest, NegativeSpeedInput) {
    EXPECT_THROW(car->setSpeed(-4), std::invalid_argument);
}

TEST_F(vehicleTest, SpeedChanging) {
    car->setSpeed(10);
    EXPECT_EQ(car->getSpeed(), 10);
    car->setSpeed(23);
    EXPECT_EQ(car->getSpeed(), 23);
}

TEST_F(vehicleTest, SpeedBoundaries) { //definir max speed
    car->setSpeed(0);
    EXPECT_EQ(car->getSpeed(), 0);
    car->setSpeed(100);
    EXPECT_EQ(car->getSpeed(), 100);
}

// - - - - BATTERY TESTS - - - - 
TEST_F(vehicleTest, BatteryChanging) {
    car->setBattery(70);
    EXPECT_EQ(car->getBattery(), 70);
    car->setBattery(42);
    EXPECT_EQ(car->getBattery(), 42);
}

TEST_F(vehicleTest, OutOfRangeBatteryInputs) {
    EXPECT_THROW(car->setBattery(-3), std::out_of_range);
    EXPECT_THROW(car->setBattery(-980), std::out_of_range);
    EXPECT_THROW(car->setBattery(101), std::out_of_range);
    EXPECT_THROW(car->setBattery(645), std::out_of_range);
}

TEST_F(vehicleTest, BatteryBoundaries) {
    car->setBattery(0);
    EXPECT_EQ(car->getBattery(), 0);
    car->setBattery(100);
    EXPECT_EQ(car->getBattery(), 100);
}

TEST_F(vehicleTest, DischargingTest) {
    for (int i = 100; i >= 0; i--)
        car->setBattery(i);
    EXPECT_EQ(car->getBattery(), 0);
}

// - - - - TEMPERATURE TESTS - - - - 
TEST_F(vehicleTest, TemperatureChanging) {
    car->setTemperature(40);
    EXPECT_EQ(car->getTemperature(), 40);
    car->setTemperature(53);
    EXPECT_EQ(car->getTemperature(), 53);
}

TEST_F(vehicleTest, OutOfRangeTemperatureInputs) {
    EXPECT_THROW(car->setTemperature(-2), std::out_of_range);
    EXPECT_THROW(car->setTemperature(-28), std::out_of_range);
    EXPECT_THROW(car->setTemperature(81), std::out_of_range);
    EXPECT_THROW(car->setTemperature(127), std::out_of_range);
}

TEST_F(vehicleTest, TemperatureBoundaries) {
    car->setTemperature(0);
    EXPECT_EQ(car->getTemperature(), 0);
    car->setTemperature(80);
    EXPECT_EQ(car->getTemperature(), 80);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
