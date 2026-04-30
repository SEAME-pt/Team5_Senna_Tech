# PARA COMPILAR NO PC TEAM-5 UTILIZAR O COMANDO: cmake .. -DCMAKE_PREFIX_PATH=/home/team5/qt-everywhere-src-6.8.3/qt-host-build/qtbase/lib/cmake/Qt6/

cmake_minimum_required(VERSION 3.16)

project(car_cluster VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2 Core)


# ---------------------------------------------------------
# 5. EXECUTÁVEL
# ---------------------------------------------------------
qt_add_executable(appcar_cluster
    main.cpp
    vehicleData.cpp
    vehicleData.hpp
)

qt_add_qml_module(appcar_cluster
    URI car_cluster
    VERSION 1.0
    QML_FILES
        Main.qml
        components/SpeedPanel.qml
        components/BatteryPanel.qml
        components/GearSelector.qml
        components/Footer.qml
        components/Header.qml
        components/TrafficSign.qml
        components/Warning.qml
    RESOURCES
        resources.qrc
        assets/cluster/cluster_light.png
        assets/cluster/cluster_dark.png
        assets/fonts/Rajdhani.ttf
        assets/fonts/Michroma.ttf
        assets/fonts/Awesome_Solid.otf
        assets/autonomy_light.png
        assets/autonomy_dark.png
        assets/battery/battery_light_100.png
        assets/battery/battery_light_75.png
        assets/battery/battery_light_50.png
        assets/battery/battery_light_30.png
        assets/battery/battery_light_15.png
        assets/battery/battery_dark_100.png
        assets/battery/battery_dark_75.png
        assets/battery/battery_dark_50.png
        assets/battery/battery_dark_30.png
        assets/battery/battery_dark_15.png
        assets/traffic/50.png
        assets/traffic/80.png
        assets/traffic/stop.png
        assets/traffic/yield.png
        assets/traffic/danger.png
        assets/traffic/crosswalk.png
        assets/traffic/red.png
        assets/traffic/green.png
        assets/traffic/yellow.png
        assets/warnings/warning_estop.png
        assets/warnings/warning_low_battery.png
        assets/warnings/warning_temp_max.png
        assets/warnings/warning_temp_rising.png
)

# Incluir diretórios
target_include_directories(appcar_cluster PRIVATE 
    ${CMAKE_CURRENT_BINARY_DIR}
    /opt/qt-cross-build/include
)

# Propriedades
set_target_properties(appcar_cluster PROPERTIES
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

# ---------------------------------------------------------
# 6. LINKAGEM (A parte importante)
# ---------------------------------------------------------
# Pega TODAS as bibliotecas estáticas que compilamos e copiamos
file(GLOB ALL_STATIC_LIBS "/opt/qt-cross-build/lib/*.a")

target_link_libraries(appcar_cluster
    PRIVATE 
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::Core
    -Wl,--start-group
    ${ALL_STATIC_LIBS}
    -Wl,--end-group
    z
    ssl
    crypto
    #systemd
)

include(GNUInstallDirs)
install(TARGETS appcar_cluster
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
