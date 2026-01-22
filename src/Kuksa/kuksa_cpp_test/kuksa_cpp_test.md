# KUKSA Databroker C++ Subscriber (API v2)
**Project:** SEA:ME PiRacer - Team 5 Senna Tech
**Objective:** Create a simple C++ client that subscribes to and receives speed and battery updates from the Databroker.

---

## 1. Prerequisites
Before compiling the code, the system (Linux/Raspberry Pi) must have the Google gRPC and Protobuf development libraries installed.

### Installation (Ubuntu / Debian / AGL with apt)
Run in the terminal:

```bash
sudo apt update
sudo apt install -y build-essential autoconf libtool pkg-config cmake
sudo apt install -y libgrpc++-dev libprotobuf-dev protobuf-compiler-grpc
```

## 2. Project Structure
For compilation to work, it is mandatory to respect the folder structure below, as the .proto files use relative imports.

```bash
kuksa_cpp_test/
├── CMakeLists.txt       # Build configuration
├── main.cpp             # Client source code
└── protos/              # Base folder for definition files
    └── kuksa/
        └── val/
            └── v2/      # API Version 2
                ├── types.proto
                └── val.proto
```


2.1 Downloading .proto files
Run these commands at the root of the kuksa_cpp_test folder to create the structure and download the official definitions:
```bash
# Create directories
mkdir -p protos/kuksa/val/v2

# Download types.proto (Definitions for Datapoint, Value, etc.)
wget [https://raw.githubusercontent.com/eclipse-kuksa/kuksa-proto/main/proto/kuksa/val/v2/types.proto](https://raw.githubusercontent.com/eclipse-kuksa/kuksa-proto/main/proto/kuksa/val/v2/types.proto) -P protos/kuksa/val/v2/

# Download val.proto (Services for Subscribe, Get, Set)
wget [https://raw.githubusercontent.com/eclipse-kuksa/kuksa-proto/main/proto/kuksa/val/v2/val.proto](https://raw.githubusercontent.com/eclipse-kuksa/kuksa-proto/main/proto/kuksa/val/v2/val.proto) -P protos/kuksa/val/v2/
```

## 3. C++ Code (main.cpp)
This code connects to the Databroker (localhost:55555) and subscribes to two signals using API v2.

```bash
#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>

// Headers gerados
#include "kuksa/val/v2/val.grpc.pb.h"
#include "kuksa/val/v2/types.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

// Namespaces da V2
using kuksa::val::v2::VAL;
using kuksa::val::v2::SubscribeRequest;
using kuksa::val::v2::SubscribeResponse;

class KuksaClient {
public:
    KuksaClient(std::shared_ptr<Channel> channel)
        : stub_(VAL::NewStub(channel)) {}

    void SubscribeToSignals() {
        ClientContext context;
        SubscribeRequest request;
        
        request.add_signal_paths("Vehicle.Speed");
        request.add_signal_paths("Vehicle.Powertrain.TractionBattery.StateOfCharge.Current");

        // Enviar pedido
        std::unique_ptr<grpc::ClientReader<SubscribeResponse>> reader(
            stub_->Subscribe(&context, request));

        std::cout << "Connected (API V2)! Waiting for data..." << std::endl;

        SubscribeResponse response;
        while (reader->Read(&response)) {
            // 'entries' is a map<string, Datapoint>
            for (const auto& pair : response.entries()) {
                const std::string& path = pair.first;      // The key is the path (e.g., "Vehicle.Speed")
                const auto& datapoint = pair.second;       // The value is the Datapoint
                
                // Access the value inside the Datapoint
                if (datapoint.has_value()) {
                    const auto& value = datapoint.value();
                    
                    // Check the type of the value (Float, Int, Bool, etc)
                    if (value.has_float_()) {
                        float val = value.float_();
                        
                        if (path == "Vehicle.Speed") {
                            std::cout << "Speed: " << val << " km/h" << std::endl;
                        } 
                        else if (path == "Vehicle.Powertrain.TractionBattery.StateOfCharge.Current") {
                            std::cout << "Battery: " << val << "%" << std::endl;
                        }
                        else {
                            std::cout << "Update on " << path << ": " << val << std::endl;
                        }
                    }
                    else if (value.has_int32() || value.has_uint32()) {
                        // If it comes as an integer
                         std::cout << "Update (Int) on " << path << std::endl;
                    }
                }
            }
        }
        
        Status status = reader->Finish();
        if (!status.ok()) {
            std::cerr << "Error in Subscribe: " << status.error_code() << ": " << status.error_message() << std::endl;
        }
    }

private:
    std::unique_ptr<VAL::Stub> stub_;
};

int main() {
    std::string target_str = "localhost:55555";
    KuksaClient client(grpc::CreateChannel(target_str, grpc::InsecureChannelCredentials()));
    client.SubscribeToSignals();
    return 0;
}
```

## 4. Build Configuration (CMakeLists.txt)
This file instructs CMake to find the libraries and generate C++ code from the .proto files.

```bash
cmake_minimum_required(VERSION 3.15)
project(KuksaTestClient CXX)

set(CMAKE_CXX_STANDARD 17)

# Find installed dependencies
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Protos Configuration
set(PROTO_BASE_DIR ${CMAKE_SOURCE_DIR}/protos)
set(PROTO_FILES 
    ${PROTO_BASE_DIR}/kuksa/val/v2/val.proto 
    ${PROTO_BASE_DIR}/kuksa/val/v2/types.proto
)

# Command to generate C++ code from protos
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

# Executable
add_executable(meu_cliente_cpp 
    main.cpp 
    kuksa/val/v2/val.pb.cc 
    kuksa/val/v2/val.grpc.pb.cc 
    kuksa/val/v2/types.pb.cc
)

# Includes and Links
target_include_directories(meu_cliente_cpp PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(meu_cliente_cpp protobuf::libprotobuf gRPC::grpc++)
```

## 5. How to Compile and Run

1. Create build folder and compile:
```bash
mkdir -p build
cd build
cmake ..
make
```

2. Run the client: Ensure Docker (Databroker) is running.
```bash
./meu_cliente_cpp
```
Output should be: "Connected (API V2)! Waiting for data..."

## 6. How to Test (CAN Simulation)
Open a second terminal to inject data into the virtual CAN network (vcan0). The C++ client should react instantly.

Speed (ID 0x010):
```bash
# 65.0 km/h (Hex 1964)
cansend vcan0 010#1964000000000000
```

Battery (ID 0x200):
```bash
# 50% SoC, 11.5V, 2A
cansend vcan0 200#32047E00C8000000

# 100% SoC, 12.6V, 0A
cansend vcan0 200#6404EC0000000000
```