FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# ------------------------------
# 1. Instala dependências do SO (Host)
# ------------------------------
RUN apt update && apt install -y \
    bash sudo xz-utils cpio file git wget tar python3 \
    qemu-user-static locales build-essential cmake ninja-build \
    libgl1-mesa-dev libglu1-mesa-dev libxkbcommon-dev libxkbcommon-x11-dev \
    libwayland-dev libwayland-egl1-mesa wayland-protocols \
    libxcb1-dev libxcb-glx0-dev libxcb-icccm4-dev libxcb-image0-dev \
    libxcb-keysyms1-dev libxcb-randr0-dev libxcb-render-util0-dev \
    libxcb-shape0-dev libxcb-shm0-dev libxcb-sync-dev libxcb-util-dev \
    libxcb-xfixes0-dev libxcb-xinerama0-dev libxcb-xkb-dev libx11-xcb-dev \
    libfontconfig1-dev libfreetype6-dev libdbus-1-dev libegl1-mesa-dev \
    libinput-dev libssl-dev libgbm-dev unzip

# ------------------------------
# 2. Baixa e extrai Qt 6.7.3
# ------------------------------
WORKDIR /opt
RUN wget https://download.qt.io/archive/qt/6.7/6.7.3/single/qt-everywhere-src-6.7.3.tar.xz && \
    tar -xf qt-everywhere-src-6.7.3.tar.xz && rm qt-everywhere-src-6.7.3.tar.xz

# ------------------------------
# 3. Instala AGL SDK
# ------------------------------
WORKDIR /opt/agl-sdk
COPY docker/agl-sdk.sh /opt/agl-sdk/sdk-install.sh
RUN chmod +x sdk-install.sh && ./sdk-install.sh -y -d /opt/agl-sdk

# Script de ambiente
RUN printf '%s\n' \
    '#!/bin/bash' \
    '. /opt/agl-sdk/environment-setup-aarch64-agl-linux' \
    'exec "$@"' \
    > /opt/agl-sdk/env.sh && chmod +x /opt/agl-sdk/env.sh

# --- CORREÇÃO CRÍTICA DO SDK ---
# Removemos as configurações CMake quebradas do SDK.
# Isso obriga o Qt a usar suas bibliotecas internas (bundled) para Protobuf e gRPC.
RUN rm -rf /opt/agl-sdk/sysroots/aarch64-agl-linux/usr/lib/cmake/utf8_range && \
    rm -rf /opt/agl-sdk/sysroots/aarch64-agl-linux/usr/lib/cmake/protobuf && \
    rm -rf /opt/agl-sdk/sysroots/aarch64-agl-linux/usr/lib/cmake/grpc

# ------------------------------
# 4. Build Qt HOST 6.7.3 (x86_64)
# ------------------------------
# Compilamos o Host com protobuf interno para gerar as ferramentas (protoc, etc)
WORKDIR /opt/qt-host-build
RUN cmake /opt/qt-everywhere-src-6.7.3 -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/qt-host-build \
    -DQT_BUILD_EXAMPLES=OFF \
    -DQT_BUILD_TESTS=OFF \
    -DFEATURE_system_protobuf=OFF \
    -DFEATURE_system_grpc=OFF

RUN ninja -j 16 && ninja install

# ------------------------------
# 5. Build Qt CROSS 6.7.3 (ARM64)
# ------------------------------
COPY docker/toolchain-agl-aarch64.cmake /opt/qt-everywhere-src-6.7.3/

WORKDIR /opt/qt-cross-build
RUN /opt/agl-sdk/env.sh cmake /opt/qt-everywhere-src-6.7.3 -GNinja \
        -DCMAKE_TOOLCHAIN_FILE=/opt/qt-everywhere-src-6.7.3/toolchain-agl-aarch64.cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/qt-cross-build \
        -DQT_HOST_PATH=/opt/qt-host-build \
        -DQT_BUILD_EXAMPLES=OFF \
        -DQT_BUILD_TESTS=OFF \
        -DFEATURE_wayland=ON \
        -DFEATURE_eglfs=ON \
        -DSKIP_qtwebengine=ON \
        -DFEATURE_system_protobuf=OFF \
        -DFEATURE_system_grpc=OFF

RUN /opt/agl-sdk/env.sh ninja -j 16 && ninja install

# ---------------------------
# OBSERVAÇÃO SOBRE PROTOBUF/GRPC MANUAL
# ---------------------------
# As instalações abaixo compilam bibliotecas para x86_64 (arquitetura do Docker).
# Se o seu 'car_cluster' usa QtGrpc, ele usará o gRPC do Qt (ARM64) que compilamos acima.
# Se 'car_control' precisar dessas libs manuais, elas não funcionarão no carro a menos
# que você as compile usando /opt/agl-sdk/env.sh (Cross-compile).
# Mantive abaixo para compatibilidade com seus scripts locais, mas cuidado.

# ------------------------------------------------------------
# 1. Compilar Protobuf para o HOST (x86) - Para ter o 'protoc'
# ------------------------------------------------------------
WORKDIR /tmp
RUN git clone -b v25.1 --recurse-submodules --depth 1 https://github.com/protocolbuffers/protobuf.git \
    && cd protobuf \
    && mkdir build && cd build \
    && cmake .. \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -Dprotobuf_BUILD_TESTS=OFF \
    && make -j 16 \
    && make install \
    && ldconfig

# ------------------------------------------------------------
# 2. Compilar gRPC para o HOST (x86) - Para ter o 'grpc_cpp_plugin'
# ------------------------------------------------------------
WORKDIR /tmp
RUN git clone -b v1.62.0 --recurse-submodules --depth 1 https://github.com/grpc/grpc \
    && cd grpc \
    && mkdir build && cd build \
    && cmake .. \
       -DgRPC_INSTALL=ON \
       -DgRPC_BUILD_TESTS=OFF \
       -DCMAKE_BUILD_TYPE=Release \
       -DgRPC_ABSL_PROVIDER=package \
       -DgRPC_PROTOBUF_PROVIDER=package \
       -DgRPC_SSL_PROVIDER=package \
       -DgRPC_ZLIB_PROVIDER=package \
    && make -j 16 \
    && make install \
    && ldconfig

# ------------------------------------------------------------
# 3. [MISSING STEP] Cross-Compile Protobuf (ARM64)
# (Isso é OBRIGATÓRIO antes de compilar o gRPC ARM)
# ------------------------------------------------------------
WORKDIR /tmp/protobuf
RUN rm -rf build_arm && mkdir build_arm && cd build_arm \
    && /opt/agl-sdk/env.sh cmake .. -DCMAKE_INSTALL_PREFIX=/opt/qt-cross-build \
    -DCMAKE_BUILD_TYPE=Release \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_BUILD_PROTOC_BINARIES=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    && make -j 16 \
    && make install

# ------------------------------------------------------------
# 4. Cross-Compile gRPC (ARM64)
# (Agora sim vai funcionar, pois o Protobuf ARM já existe)
# ------------------------------------------------------------
WORKDIR /tmp/grpc
RUN mkdir -p build_arm && cd build_arm \
    && /opt/agl-sdk/env.sh cmake .. \
    -DCMAKE_INSTALL_PREFIX=/opt/qt-cross-build \
    -DCMAKE_PREFIX_PATH="/opt/qt-cross-build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DgRPC_INSTALL=ON \
    -DgRPC_BUILD_TESTS=OFF \
    -DgRPC_BUILD_GRPC_CSHARP_PLUGIN=OFF \
    -DgRPC_BUILD_GRPC_NODE_PLUGIN=OFF \
    -DgRPC_BUILD_GRPC_OBJECTIVE_C_PLUGIN=OFF \
    -DgRPC_BUILD_GRPC_PHP_PLUGIN=OFF \
    -DgRPC_BUILD_GRPC_PYTHON_PLUGIN=OFF \
    -DgRPC_BUILD_GRPC_RUBY_PLUGIN=OFF \
    -DCMAKE_CXX_FLAGS="-Wno-error=deprecated-declarations -Wno-deprecated-declarations" \
    -DCMAKE_C_FLAGS="-Wno-error=deprecated-declarations -Wno-deprecated-declarations" \
    -DProtobuf_DIR=/opt/qt-cross-build/lib/cmake/protobuf \
    -Dabsl_DIR=/opt/qt-cross-build/lib/cmake/absl \
    -Dutf8_range_DIR=/opt/qt-cross-build/lib/cmake/utf8_range \
    -DgRPC_ABSL_PROVIDER=package \
    -DgRPC_PROTOBUF_PROVIDER=package \
    -DgRPC_SSL_PROVIDER=package \
    -DgRPC_ZLIB_PROVIDER=package \
    -DgRPC_RE2_PROVIDER=module \
    -DgRPC_CPP_PLUGIN_EXECUTABLE=/usr/local/bin/grpc_cpp_plugin \
    && make -j 16 grpc++ grpc gpr address_sorting re2 upb_mem_lib upb_message_lib upb_textformat_lib upb_json_lib upb_base_lib utf8_range_lib || true \
    && mkdir -p /opt/qt-cross-build/lib \
    && mkdir -p /opt/qt-cross-build/include \
    && find . -name "*.a" -exec cp -v {} /opt/qt-cross-build/lib/ \; \
    && cp -r ../include/* /opt/qt-cross-build/include/

# Copia código fonte
COPY src/Kuksa/car_cluster_with_kuksa/ /root/car_cluster/
COPY src/car-control/piracer-cpp /root/car_control

RUN rm -rf /root/car_cluster/CMakeLists.txt
COPY docker/CMakeListsQt.txt /root/car_cluster/CMakeLists.txt

# ------------------------------
# Compilação car_cluster (Qt ARM64)
# ------------------------------
RUN rm -rf /root/car_cluster/build && mkdir /root/car_cluster/build
WORKDIR /root/car_cluster/build
RUN /opt/agl-sdk/env.sh cmake .. -GNinja -DQT_HOST_PATH=/opt/qt-host-build \
    -DCMAKE_PREFIX_PATH=/opt/qt-cross-build     -DProtobuf_DIR=/opt/qt-cross-build/lib/cmake/protobuf \
    -Dabsl_DIR=/opt/qt-cross-build/lib/cmake/absl     -Dutf8_range_DIR=/opt/qt-cross-build/lib/cmake/utf8_range \
    -DLIB_GRPC_CPP=/opt/qt-cross-build/lib/libgrpc++.a     -DLIB_GRPC=/opt/qt-cross-build/lib/libgrpc.a \
    -DLIB_GPR=/opt/qt-cross-build/lib/libgpr.a     -DLIB_ADDR_SORTING=/opt/qt-cross-build/lib/libaddress_sorting.a \
    && ninja -j $(nproc)

#Cria diretorio para os outputs
RUN mkdir /root/outputs

# Envio dos binarios para a pasta output
RUN mv /root/car_cluster/build/appcar_cluster /root/outputs
