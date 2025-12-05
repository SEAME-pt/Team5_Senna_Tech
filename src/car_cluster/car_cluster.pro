# car_cluster.pro

QT       += core quick quickcontrols2
CONFIG   += c++17 console
TEMPLATE = app

# Nome do executável
TARGET = appcar_cluster

# Arquivos fonte e headers
SOURCES += main.cpp \
           vehicleData.cpp

HEADERS += vehicleData.hpp

# Arquivos QML
QML_FILES += Main.qml

# Recursos
RESOURCES += resources.qrc

# Outras propriedades (como bundle no macOS, opcional)
#macx {    Você pode precisar adicionar o populate_sdk_qt6 ou garantir que o pacote de desenvolvimento do módulo Qt QmlBuiltins esteja na sua imagem ou no seu SDK.

#Verifique a Existência de Outras Bibliotecas: Confirme se existem outras bibliotecas Qt6 dinâmicas (libQt6Core.so, libQt6Qml.so) no mesmo diretório. Se não existirem, o problema é o SDK inteiro e ele precisa ser refeito.


 #   QMAKE_BUNDLE_NAME = $$TARGET
  #  QMAKE_INFO_PLIST = Info.plist
#}

# Deployment de imagens, se necessário
DISTFILES += mclaren.png

# Opcional: otimizações e flags adicionais
QMAKE_CXXFLAGS_RELEASE += -O2

