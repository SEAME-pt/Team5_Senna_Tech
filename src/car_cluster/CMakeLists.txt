cmake_minimum_required(VERSION 3.16)
project(CarClusterQt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Quick)

qt_add_executable(appCarClusterQt
    main.cpp
)

qt_add_resources(appCarClusterQt
    "resources"
    FILES qml.qrc
)

target_link_libraries(appCarClusterQt
    PRIVATE Qt6::Quick
)