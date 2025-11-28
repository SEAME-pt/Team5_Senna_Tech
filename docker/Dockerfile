FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# install sdk dependencies
RUN apt update && apt install -y \
    bash \
    sudo \
    xz-utils \
    cpio \
    make \
    file \
    g++ \
    git \
    wget \
    tar \
    python3 \
    qemu-user-static \ 
    locales \
    && locale-gen en_US.UTF-8 

#install qt 6.8.3 and its depedencies
RUN wget https://download.qt.io/archive/qt/6.8/6.8.3/single/qt-everywhere-src-6.8.3.tar.xz 
RUN tar -xf qt-everywhere-src-6.8.3.tar.xz
RUN cd qt-everywhere-src-6.8.3
COPY docker/toolchain-agl-aarch64.cmake qt-everywhere-src-6.8.3

# create sdk directory
RUN mkdir -p /opt/agl-sdk
WORKDIR /opt/agl-sdk

# Copy sdk scrip to the docker
COPY docker/agl-sdk.sh /opt/agl-sdk/sdk-install.sh

RUN mkdir -p /root/car_cluster
COPY src/car_cluster /root/car_cluster/

# make script executable
RUN chmod +x sdk-install.sh

# run sdk
RUN ./sdk-install.sh -y -d /opt/agl-sdk

RUN echo "source /opt/agl-sdk/environment-setup-*" >> /etc/bash.bashrc
RUN echo "alias qemu=\"qemu-aarch64-static -L /opt/agl-sdk/sysroots/aarch64-agl-linux\"" >> /etc/bash.bashrc

CMD ["/bin/bash"]