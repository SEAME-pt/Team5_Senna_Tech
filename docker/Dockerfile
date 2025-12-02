FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# install sdk dependencies
RUN apt update && apt install -y \
    bash \
    sudo \
    xz-utils \
    cpio \
    file \
    git \
    wget \
    tar \
    python3 \
    qemu-user-static \ 
    locales \
    build-essential \
    cmake \
    ninja-build \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    libwayland-dev \
    libwayland-egl1-mesa \
    wayland-protocols \
    libxcb1-dev \
    libxcb-glx0-dev \
    libxcb-icccm4-dev \
    libxcb-image0-dev \
    libxcb-keysyms1-dev \
    libxcb-randr0-dev \
    libxcb-render-util0-dev \
    libxcb-shape0-dev \
    libxcb-shm0-dev \
    libxcb-sync-dev \
    libxcb-util-dev \
    libxcb-xfixes0-dev \
    libxcb-xinerama0-dev \
    libxcb-xkb-dev \
    libx11-xcb-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libdbus-1-dev \
    libegl1-mesa-dev \
    libinput-dev \
    libssl-dev \
    libgbm-dev\
    && locale-gen en_US.UTF-8 


    
#install qt 6.8.3 and its depedencies
WORKDIR /opt
RUN wget https://download.qt.io/archive/qt/6.8/6.8.3/single/qt-everywhere-src-6.8.3.tar.xz 
RUN tar -xf qt-everywhere-src-6.8.3.tar.xz
RUN rm qt-everywhere-src-6.8.3.tar.xz && cd qt-everywhere-src-6.8.3
COPY docker/toolchain-agl-aarch64.cmake qt-everywhere-src-6.8.3

#create directory to Qt-host-build
RUN cd /opt && mkdir qt-host-build && cd qt-host-build
#create build files to compile Qt through ninja build system
RUN cmake qt-everywhere-src-6.8.3 -G Ninja -DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX=/opt/qt-host-build -DQT_BUILD_EXAMPLES=OFF -DQT_BUILD_TESTS=OFF 
#compile and install Qt to host architecture(X86_64)
RUN ninja -j $(nproc)
RUN ninja install
    
# create sdk directory
RUN mkdir -p /opt/agl-sdk
WORKDIR /opt/agl-sdk
# Copy sdk scrip to the docker
COPY docker/agl-sdk.sh /opt/agl-sdk/sdk-install.sh
# make script executable
RUN chmod +x sdk-install.sh
# run sdk
RUN ./sdk-install.sh -y -d /opt/agl-sdk

# create wrapper script
RUN printf '%s\n' \
    '#!/bin/bash' \
    '. /opt/agl-sdk/environment-setup-aarch64-agl-linux' \
    'exec "$@"' \
    > /opt/agl-sdk/env.sh \
    && chmod +x /opt/agl-sdk/env.sh

#create directory to Qt-cross-build
RUN cd /opt && mkdir qt-cross-build && cd qt-cross-build
#create build files to compile Qt through ninja build system
RUN  /opt/agl-sdk/env.sh cmake ../qt-everywhere-src-6.8.3 -GNinja -DCMAKE_TOOLCHAIN_FILE=../qt-everywhere-src-6.8.3/toolchain-agl-aarch64.cmake \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DQT_HOST_PATH=/opt/qt-host-build -DQT_BUILD_EXAMPLES=OFF \
    -DQT_BUILD_TESTS=OFF -DFEATURE_wayland=ON -DFEATURE_wayland_client=ON -DFEATURE_eglfs=ON -DFEATURE_opengl=ON \
    -DFEATURE_kms=ON -DFEATURE_gbm=ON 
#compile and install Qt to target architecture (ARM64)
RUN /opt/agl-sdk/env.sh ninja -j $(nproc)
RUN /opt/agl-sdk/env.sh ninja install

#Copies the Qt project to the docker
RUN mkdir -p /root/car_cluster
COPY src/car_cluster /root/car_cluster/

RUN echo "source /opt/agl-sdk/environment-setup-*" >> /etc/bash.bashrc
RUN echo "alias qemu=\"qemu-aarch64-static -L /opt/agl-sdk/sysroots/aarch64-agl-linux\"" >> /etc/bash.bashrc

CMD ["/bin/bash"]