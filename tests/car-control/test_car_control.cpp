#include <gtest/gtest.h>
#include "../../src/car-control/piracer-cpp/PiRacer/PiRacer.hpp"

TEST(InitialTest, Initialization) {
    // PiRacer racer;

    EXPECT_TRUE(1) 
        << "Tests working";
}

// Ponto de entrada do GoogleTest
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}