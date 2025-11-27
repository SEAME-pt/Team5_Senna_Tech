FROM ubuntu:22.04

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
    cmake \
    python3 \
    qemu-user-static \
    locales \
    && locale-gen en_US.UTF-8

ENV LANG=UTF-8
ENV LC_ALL=C.UTF-8
ENV QT_QPA_PLUGIN=wayland

# create sdk directory
RUN mkdir -p /opt/agl-sdk
WORKDIR /opt/agl-sdk

# Copy sdk scrip to the docker
COPY agl-sdk.sh /opt/agl-sdk/sdk-install.sh
COPY appcar_cluster /home/app

# make script executable
RUN chmod +x sdk-install.sh

# run sdk
RUN ./sdk-install.sh -y -d /opt/agl-sdk

RUN echo "source /opt/agl-sdk/environment-setup-*" >> /etc/bash.bashrc
RUN echo "alias qemu=\"qemu-aarch64-static -L /opt/agl-sdk/sysroots/aarch64-agl-linux\"" >> /etc/bash.bashrc

CMD ["/bin/bash"]