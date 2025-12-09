#include <gtest/gtest.h>
#include "../../src/car-control/piracer-cpp/PiRacer/PiRacer.hpp"

TEST(PiRacerTests, DutyCycleCalculation) {
    
    float duty = PiRacer::_get50HzDutyCycleFromPercent(0.5);
    EXPECT_FLOAT_EQ(duty, 0.0015 + 0.5 * 0.001);

    duty = racer._get50HzDutyCycleFromPercent(-1.0);
    EXPECT_FLOAT_EQ(duty, 0.0015 + (-1.0 * 0.001));
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

