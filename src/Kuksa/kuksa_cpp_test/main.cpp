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