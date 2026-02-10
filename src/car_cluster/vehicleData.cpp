#include "vehicleData.hpp"
#include <vector>
#include <memory>
//#include "kuksa/val/v2/types.pb.h" // necessário para ler os tipos

//using grpc::ClientContext;
//using grpc::Status;
//using kuksa::val::v2::SubscribeRequest;
//using kuksa::val::v2::SubscribeResponse;

// Singleton implementation
vehicleData *vehicleData::instance() {
    static vehicleData data;
    return &data;
}

//Private constructor
vehicleData::vehicleData(QObject *parent) : speed(0), battery(0), temperature(50), trafficSign("") {(void) parent;}

// Getters
double vehicleData::getSpeed() const{ return speed;}

int vehicleData::getBattery() const { return battery;}

int vehicleData::getTemperature() const{ return temperature;}

std::string vehicleData::getTrafficSign() const{ return trafficSign;}

//Slots
void    vehicleData::setSpeed(double newSpeed) {
    if (newSpeed < 0) {
        throw::std::invalid_argument("Speed cannot be negative");
        return ;
    }
    if (this->speed == newSpeed)
        return ;
    this->speed = newSpeed;
    emit speedChanged();
}

void    vehicleData::setBattery(int newBattery){
    if (newBattery < 0 || newBattery > 100) {
        throw(std::out_of_range("Battery level must in a range of 0 to 100"));
    }
    if (this->battery == newBattery)
        return ;
    this->battery = newBattery;
    emit batteryChanged();
}

void    vehicleData::setTemperature(int newTemperature){
    if (newTemperature < 0 || newTemperature > 80)
        throw(std::out_of_range("Temperature level is considered risky to the system"));
    if (this->temperature == newTemperature)
        return ;
    this->temperature = newTemperature;
    emit temperatureChanged();
}

void    vehicleData::setTrafficSign(std::string newTrafficSign){
    if (this->trafficSign == newTrafficSign)
        return ;
    this->trafficSign = newTrafficSign;
    emit trafficSignChanged();
}

//SIMULATION TESTS
void vehicleData::startSpeedSimulation() {
    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        speed += 0.2;                 // aumenta 0.2 km/h por tick
        if (speed > 20.0) speed = 0.0; // reinicia se passar de 20
        emit speedChanged();
    });
    timer->start(100); // 100 ms por tick -> 10 Hz
}

void vehicleData::startBatterySimulation() {
    this->battery = 100;
    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        battery -= 0.1;
        if (battery <= 0) battery = 100;
        emit batteryChanged();
    });
    timer->start(1000); // 1000 ms por tick -> 1 Hz
}

void vehicleData::startTrafficSignSimulation() {
    // Lista de sinais que serão exibidos em loop
    std::vector<std::string> signs = {"stop", "80", "50", "danger", "pedestrian", "yield", "red", "yellow", "green"};

    if (!signs.empty())
        this->setTrafficSign(signs[0]);

    // índice compartilhado entre chamadas do lambda para permanecer válido
    auto index = std::make_shared<int>(0);

    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this, signs, index]() mutable {
        *index = (*index + 1) % static_cast<int>(signs.size());
        this->setTrafficSign(signs[*index]);
    });
    timer->start(5000); // troca a cada 5 segundos
}

/*void vehicleData::startReadCan() {
    this->speed = 0;

    QTimer* timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, [this]() {
        int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        if (sock < 0)
            qWarning() << "Socket initialization error:" << strerror(errno);
        // 2️⃣ Configura interface can0
        struct ifreq ifr;
        std::strcpy(ifr.ifr_name, "can0");
        ioctl(sock, SIOCGIFINDEX, &ifr);

        struct sockaddr_can addr{};
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;

        if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0){
            qWarning() << "Bind error:" << strerror(errno);
            close(sock);
            return;
        }

        std::cout << "Waiting messages CAN...\n";

        // 3️⃣ Loop de leitura
        struct can_frame frame;
        int nbytes = read(sock, &frame, sizeof(frame));
        if (nbytes > 0) {
            std::cout << "ID: 0x" << std::hex << frame.can_id
            << " DLC: " << std::dec << (int)frame.can_dlc
            << " DATA: ";
            for (int i = 0; i < frame.can_dlc; i++)
            std::cout << (int)frame.data[0] << " ";
            std::cout << "\n";
            setSpeed((int)frame.data[0]);
        }
        close(sock);
    });
    timer->start(1000); // 1000 ms por tick -> 1 Hz
}*/

/*void vehicleData::startKuksaSubscriber() {
    // Inicia o loop do KUKSA em uma thread separada
    // Se rodarmos direto aqui, a GUI do Qt vai congelar!
    kuksaThread = std::thread(&vehicleData::kuksaLoop, this);
    kuksaThread.detach(); // Deixa rodando em background
}

void vehicleData::kuksaLoop() {
    std::string target_str = "localhost:55555";
    auto channel = grpc::CreateChannel(target_str, grpc::InsecureChannelCredentials());
    auto stub = VAL::NewStub(channel);

    ClientContext context;
    SubscribeRequest request;

    // Adiciona os caminhos VSS que queremos ouvir
    request.add_signal_paths("Vehicle.Speed");
    request.add_signal_paths("Vehicle.Powertrain.TractionBattery.StateOfCharge.Current");
    // request.add_signal_paths("Vehicle.Powertrain.ElectricMotor.Temperature");

    std::unique_ptr<grpc::ClientReader<SubscribeResponse>> reader(
        stub->Subscribe(&context, request));

    std::cout << "Conectado ao KUKSA Databroker!" << std::endl;

    SubscribeResponse response;
    while (reader->Read(&response)) {
        for (const auto& pair : response.entries()) {
            const std::string& path = pair.first;
            const auto& datapoint = pair.second;

            if (datapoint.has_value()) {
                const auto& value = datapoint.value();
                
                // Atualiza a UI baseada no caminho recebido
                // Nota: setSpeed e setBattery emitem sinais que o Qt entende
                
                if (path == "Vehicle.Speed") {
                    if (value.has_float_()) {
                        setSpeed((double)value.float_());
                    }
                } 
                else if (path == "Vehicle.Powertrain.TractionBattery.StateOfCharge.Current") {
                    if (value.has_float_()) {
                        setBattery((int)value.float_());
                    } else if (value.has_uint32()) {
                        setBattery((int)value.uint32());
                    }
                }
            }
        }
    }
    std::cout << "Desconectado do KUKSA." << std::endl;
}

*/
