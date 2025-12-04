set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_SYSROOT /opt/agl-sdk/sysroots/aarch64-agl-linux)
set(CMAKE_C_COMPILER /opt/agl-sdk/sysroots/x86_64-aglsdk-linux/usr/bin/aarch64-agl-linux/aarch64-agl-linux-gcc)
set(CMAKE_CXX_COMPILER /opt/agl-sdk/sysroots/x86_64-aglsdk-linux/usr/bin/aarch64-agl-linux/aarch64-agl-linux-g++)

set(QT_HOST_PATH /opt/qt-host-build)
set(Qt6_DIR /opt/qt-cross-build/lib/cmake/Qt6)

set(CMAKE_FIND_ROOT_PATH 
    /opt/qt-cross-build
    /opt/agl-sdk/sysroots/aarch64-agl-linux
)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)