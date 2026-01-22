cmake_minimum_required(VERSION 3.15)
project(KuksaTestClient CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Diretório base onde estão os protos
set(PROTO_BASE_DIR ${CMAKE_SOURCE_DIR}/protos)

# Lista dos arquivos (com o caminho relativo correto)
set(PROTO_FILES 
    ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto 
    ${PROTO_BASE_DIR}/kuksa/val/v2/types.proto
)

# Gera os arquivos mantendo a estrutura de pastas
add_custom_command(
    OUTPUT 
        kuksa/val/v2/val.pb.cc kuksa/val/v2/val.pb.h 
        kuksa/val/v2/val.grpc.pb.cc kuksa/val/v2/val.grpc.pb.h
        kuksa/val/v2/types.pb.cc kuksa/val/v2/types.pb.h
    COMMAND protoc
    ARGS --proto_path=${PROTO_BASE_DIR}
         --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
         --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
         --plugin=protoc-gen-grpc=`which grpc_cpp_plugin`
         ${PROTO_FILES}
    DEPENDS ${PROTO_FILES}
)

add_executable(meu_cliente_cpp 
    main.cpp 
    kuksa/val/v2/val.pb.cc 
    kuksa/val/v2/val.grpc.pb.cc 
    kuksa/val/v2/types.pb.cc
)

# Inclui o diretório de build para achar os headers gerados
target_include_directories(meu_cliente_cpp PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

target_link_libraries(meu_cliente_cpp
    protobuf::libprotobuf
    gRPC::grpc++
)