cmake_minimum_required(VERSION 3.16)

project(car_cluster VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#set(CMAKE_PREFIX_PATH "/opt/qt-host-build")
# para compilar no pc do seame, utilizar: "cmake.. -DCMAKE_PREFIX_PATH=/home/team5/qt-everywhere-src-6.8.3/qt-host-build/qtbase/lib/cmake/Qt6/"

find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2)
find_package(Qt6 REQUIRED COMPONENTS Core)


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
    RESOURCES
        resources.qrc
        mclaren.png
)


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
)
target_link_libraries(appcar_cluster PRIVATE Qt6::Core)

include(GNUInstallDirs)
install(TARGETS appcar_cluster
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)