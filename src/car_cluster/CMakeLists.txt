cmake_minimum_required(VERSION 3.16)

project(car_cluster VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_PREFIX_PATH "/opt/qt-host-build")
# para compilar no pc do seame, utilizar: "cmake.. -DCMAKE_PREFIX_PATH=/home/team5/qt-everywhere-src-6.8.3/qt-host-build/qtbase/lib/cmake/Qt6/"

find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2)
find_package(Qt6 REQUIRED COMPONENTS Core)

# adicionado para Protobuf e gRPC
find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

find_program(PROTOC_EXEC protoc REQUIRED HINTS /usr/local/bin /usr/bin)
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin REQUIRED HINTS /usr/local/bin /usr/bin)

message(STATUS "Using protoc: ${PROTOC_EXEC}")
message(STATUS "Using grpc_cpp_plugin: ${GRPC_CPP_PLUGIN}")

# configurar onde estão os arquivos .proto (AJUSTAR O CAMINHO CONFORME SEJA NECESSARIO)
set(PROTO_BASE_DIR ${CMAKE_SOURCE_DIR}/protos)
# Verificação de segurança (opcional, mas ajuda a debugar)
if(NOT EXISTS "${PROTO_BASE_DIR}/kuksa/val/v2/val.proto")
    message(FATAL_ERROR "Arquivo Proto não encontrado em: ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto. Verifique a estrutura de pastas.")
endif()
set(PROTO_FILES 
    ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto 
    ${PROTO_BASE_DIR}/kuksa/val/v2/types.proto
)

# gerar código C++ a partir dos Protos
add_custom_command(
    OUTPUT 
        kuksa/val/v2/val.pb.cc kuksa/val/v2/val.pb.h 
        kuksa/val/v2/val.grpc.pb.cc kuksa/val/v2/val.grpc.pb.h
        kuksa/val/v2/types.pb.cc kuksa/val/v2/types.pb.h
	COMMAND /usr/local/bin/protoc
    ARGS --proto_path=${PROTO_BASE_DIR}
        --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
        --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
        --plugin=protoc-gen-grpc=`which grpc_cpp_plugin`
        ${PROTO_FILES}
    DEPENDS ${PROTO_FILES}
)

qt_add_executable(appcar_cluster
    main.cpp
    vehicleData.cpp
    vehicleData.hpp
    #adicionados
    kuksa/val/v2/val.pb.cc 
    kuksa/val/v2/val.grpc.pb.cc 
    kuksa/val/v2/types.pb.cc    
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
        assets/traffic/pedestrian.png
        assets/traffic/traffic-light-red.png
        assets/traffic/traffic-light-green.png
        assets/traffic/traffic-light-yellow.png
        assets/warnings/warning_estop.png
        assets/warnings/warning_low_battery.png
        assets/warnings/warning_temp_max.png
        assets/warnings/warning_temp_rising.png
)

# Incluir diretórios de build para achar os headers gerados
target_include_directories(appcar_cluster PRIVATE ${CMAKE_CURRENT_BINARY_DIR})


# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appcar_cluster PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appQML_study
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_link_libraries(appcar_cluster
    PRIVATE Qt6::Quick
    Qt6::QuickControls2
    #adicionado
    protobuf::libprotobuf gRPC::grpc++
    protobuf::libprotobuf
    gRPC::grpc++
)

include(GNUInstallDirs)
install(TARGETS appcar_cluster
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
