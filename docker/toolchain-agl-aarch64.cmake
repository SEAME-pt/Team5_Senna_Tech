# Toolchain para cross-compile ARM64 (AGL)
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# Sysroot do SDK
set(CMAKE_SYSROOT "$ENV{SDKTARGETSYSROOT}")

# Compiladores ARM do SDK
# Caminhos absolutos para os compiladores (somente executável)
set(CMAKE_C_COMPILER   "/opt/agl-sdk/sysroots/x86_64-aglsdk-linux/usr/bin/aarch64-agl-linux/aarch64-agl-linux-gcc")
set(CMAKE_CXX_COMPILER "/opt/agl-sdk/sysroots/x86_64-aglsdk-linux/usr/bin/aarch64-agl-linux/aarch64-agl-linux-g++")

# Se quiser passar flags, faça separadamente:
set(CMAKE_C_FLAGS   "-O2 -fstack-protector-strong -mbranch-protection=standard -D_FORTIFY_SOURCE=2 --sysroot=${CMAKE_SYSROOT}")
set(CMAKE_CXX_FLAGS "-O2 -fstack-protector-strong -mbranch-protection=standard -D_FORTIFY_SOURCE=2 --sysroot=${CMAKE_SYSROOT}")

# Caminhos do sysroot
set(CMAKE_FIND_ROOT_PATH "$ENV{SDKTARGETSYSROOT}")

# Como o CMake encontra libs/includes
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)