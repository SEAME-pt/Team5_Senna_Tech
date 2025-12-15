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
    car->setSpeed(0);
    EXPECT_EQ(car->getSpeed(), 0);
    car->setSpeed(10);
    EXPECT_EQ(car->getSpeed(), 10);
    car->setSpeed(23);
    EXPECT_EQ(car->getSpeed(), 23);
}

//Implementar boundaries tests, stress tests

// - - - - BATTERY TESTS - - - - 
TEST_F(vehicleTest, OutOfRangeBatteryInputs) {
    EXPECT_THROW(car->setBattery(-3), std::out_of_range);
    EXPECT_THROW(car->setBattery(-980), std::out_of_range);
    EXPECT_THROW(car->setBattery(101), std::out_of_range);
    EXPECT_THROW(car->setBattery(645), std::out_of_range);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
