FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# ------------------------------
# Instala dependências do SDK e build
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
    libinput-dev libssl-dev libgbm-dev

# ------------------------------
# Baixa e extrai Qt 6.8.3
# ------------------------------
WORKDIR /opt
RUN wget https://download.qt.io/archive/qt/6.7/6.7.3/single/qt-everywhere-src-6.7.3.tar.xz && \
    tar -xf qt-everywhere-src-6.7.3.tar.xz && rm qt-everywhere-src-6.7.3.tar.xz
    
# 3. Instala AGL SDK
WORKDIR /opt/agl-sdk
COPY docker/agl-sdk.sh /opt/agl-sdk/sdk-install.sh
RUN chmod +x sdk-install.sh && ./sdk-install.sh -y -d /opt/agl-sdk

RUN printf '%s\n' \
    '#!/bin/bash' \
    '. /opt/agl-sdk/environment-setup-aarch64-agl-linux' \
    'exec "$@"' \
    > /opt/agl-sdk/env.sh && chmod +x /opt/agl-sdk/env.sh

# 4. Build Qt HOST 6.7.3
WORKDIR /opt/qt-host-build
RUN cmake /opt/qt-everywhere-src-6.7.3 -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/qt-host-build \
    -DQT_BUILD_EXAMPLES=OFF \
    -DQT_BUILD_TESTS=OFF

RUN ninja -j $(nproc) && ninja install

# 5. Build Qt CROSS 6.7.3
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
    -DFEATURE_eglfs=ON

RUN /opt/agl-sdk/env.sh ninja -j $(nproc) && ninja install

# Fonte do ambiente do SDK AGL
RUN echo "source /opt/agl-sdk/environment-setup-aarch64-agl-linux" >> /etc/bash.bashrc

# Alias para usar qemu facilmente
RUN echo "alias qemu='qemu-aarch64-static -L /opt/agl-sdk/sysroots/aarch64-agl-linux'" >> /etc/bash.bashrc

# Copia car_cluster e car_control para dentro do container
COPY src/car_cluster/ /root/car_cluster/
COPY src/car-control/piracer-cpp /root/car_control

# Compilaçao car_cluster
RUN rm -rf /root/car_cluster/build
RUN mkdir /root/car_cluster/build && cd /root/car_cluster/build && cmake .. -GNinja  -DQT_HOST_PATH=/opt/qt-host-build/ && ninja

# Compilacao car_control
RUN rm -rf /root/car_control/build
RUN mkdir /root/car_control/build && cd /root/car_control/build/ && cmake .. && make

#Cria diretorio para os outputs
RUN mkdir /root/outputs

# Envio dos binarios para a pasta output
RUN mv /root/car_cluster/build/appcar_cluster /root/outputs

WORKDIR /root/car_control/build/
RUN mv forward_backward_left_right gamepad_control read_battery /root/outputs

CMD ["/bin/bash"]


