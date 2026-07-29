cmake_minimum_required(VERSION 3.16)

project(car_cluster VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2 Core)

# ---------------------------------------------------------
# 1. PROTOBUF (Config Mode - Esse funciona)
# ---------------------------------------------------------
find_package(Protobuf CONFIG REQUIRED)
message(STATUS "Protobuf Found: ${Protobuf_DIR}")

# ---------------------------------------------------------
# 2. GRPC (Manual Mode - "Force Brute")
# ---------------------------------------------------------
# Como o gRPCConfig.cmake não foi gerado corretamente,
# vamos pegar as bibliotecas estáticas diretamente.
set(GRPC_SEARCH_PATH "/opt/qt-cross-build/lib")

find_library(LIB_GRPC_CPP grpc++ PATHS ${GRPC_SEARCH_PATH} NO_DEFAULT_PATH REQUIRED)
find_library(LIB_GRPC grpc PATHS ${GRPC_SEARCH_PATH} NO_DEFAULT_PATH REQUIRED)
find_library(LIB_GPR gpr PATHS ${GRPC_SEARCH_PATH} NO_DEFAULT_PATH REQUIRED)
find_library(LIB_ADDR_SORTING address_sorting PATHS ${GRPC_SEARCH_PATH} NO_DEFAULT_PATH REQUIRED)
message(STATUS "gRPC Libs Found Manually: ${LIB_GRPC_CPP}")

# ---------------------------------------------------------
# 3. FERRAMENTAS DO HOST (x86)
# ---------------------------------------------------------
# Renomeamos a variável para evitar conflitos de cache
find_program(MY_PROTOC_EXEC protoc 
             PATHS /usr/local/bin /usr/bin 
             NO_DEFAULT_PATH REQUIRED)

find_program(MY_GRPC_CPP_PLUGIN grpc_cpp_plugin 
             PATHS /usr/local/bin /usr/bin 
             NO_DEFAULT_PATH REQUIRED)

message(STATUS "Using protoc: ${MY_PROTOC_EXEC}")
message(STATUS "Using grpc_plugin: ${MY_GRPC_CPP_PLUGIN}")

# ---------------------------------------------------------
# 4. GERAÇÃO DOS ARQUIVOS .PROTO
# ---------------------------------------------------------
set(PROTO_BASE_DIR ${CMAKE_SOURCE_DIR}/protos)

# Verifica se os arquivos existem para não dar erro obscuro depois
if(NOT EXISTS "${PROTO_BASE_DIR}/kuksa/val/v2/val.proto")
    message(FATAL_ERROR "ERRO: ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto não encontrado!")
endif()

set(PROTO_FILES 
    ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto 
    ${PROTO_BASE_DIR}/kuksa/val/v2/types.proto
)

# Cria pasta de output
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/kuksa/val/v2)

# Comando para gerar C++
add_custom_command(
    OUTPUT 
        kuksa/val/v2/val.pb.cc kuksa/val/v2/val.pb.h 
        kuksa/val/v2/val.grpc.pb.cc kuksa/val/v2/val.grpc.pb.h
        kuksa/val/v2/types.pb.cc kuksa/val/v2/types.pb.h
    COMMAND ${MY_PROTOC_EXEC}
    ARGS --proto_path=${PROTO_BASE_DIR}
         --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
         --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
         --plugin=protoc-gen-grpc=${MY_GRPC_CPP_PLUGIN}
         ${PROTO_FILES}
    DEPENDS ${PROTO_FILES}
    COMMENT "Compilando Protos..."
)

# ---------------------------------------------------------
# 5. EXECUTÁVEL
# ---------------------------------------------------------
qt_add_executable(appcar_cluster
    main.cpp
    vehicleData.cpp
    vehicleData.hpp
    # Arquivos Gerados
    kuksa/val/v2/val.pb.cc 
    kuksa/val/v2/val.grpc.pb.cc 
    kuksa/val/v2/types.pb.cc    
)

qt_add_qml_module(appcar_cluster
    URI car_cluster
    VERSION 1.0
    QML_FILES
        Main.qml
        MainRobotaxi.qml
        components/SpeedPanel.qml
        components/BatteryPanel.qml
        components/GearSelector.qml
        components/Footer.qml
        components/Header.qml
        components/TrafficSign.qml
        components/RobotaxiStatePanel.qml
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
    systemd
)

include(GNUInstallDirs)
install(TARGETS appcar_cluster
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
