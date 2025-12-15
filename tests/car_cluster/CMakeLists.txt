cmake_minimum_required(VERSION 3.16)
project(Tests VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# -----------------------------------
# Qt
# -----------------------------------
find_package(Qt6 REQUIRED COMPONENTS Core)

# -----------------------------------
# GoogleTest via FetchContent
# -----------------------------------
include(FetchContent)

FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)

FetchContent_MakeAvailable(googletest)

enable_testing()

# -----------------------------------
# Biblioteca do projeto (Qt)
# -----------------------------------
add_library(car_cluster_lib
    ../../src/car_cluster/vehicleData.cpp
)

target_include_directories(car_cluster_lib
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/..
)

target_link_libraries(car_cluster_lib
    PUBLIC
        Qt6::Core
)

set_target_properties(car_cluster_lib PROPERTIES
    AUTOMOC ON
)

# -----------------------------------
# Executável de testes
# -----------------------------------
add_executable(test_car_cluster
    test_car_cluster.cpp
)

target_link_libraries(test_car_cluster
    PRIVATE
        car_cluster_lib
        Qt6::Core
        gtest
        gtest_main
)

set_target_properties(test_car_cluster PROPERTIES
    AUTOMOC ON
)

include(GoogleTest)
gtest_discover_tests(test_car_cluster)
