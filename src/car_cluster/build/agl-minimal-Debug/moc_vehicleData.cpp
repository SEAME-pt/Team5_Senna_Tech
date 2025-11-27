/****************************************************************************
** Meta object code from reading C++ file 'vehicleData.hpp'
**
** Created by: The Qt Meta Object Compiler version 68 (Qt 6.7.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../vehicleData.hpp"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'vehicleData.hpp' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 68
#error "This file was generated using the moc from 6.7.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
QT_WARNING_DISABLE_GCC("-Wuseless-cast")
namespace {

#ifdef QT_MOC_HAS_STRINGDATA
struct qt_meta_stringdata_CLASSvehicleDataENDCLASS_t {};
constexpr auto qt_meta_stringdata_CLASSvehicleDataENDCLASS = QtMocHelpers::stringData(
    "vehicleData",
    "speedChanged",
    "",
    "batteryChanged",
    "temperatureChanged",
    "chargingChanged",
    "setSpeed",
    "newSpeed",
    "setBattery",
    "newBattery",
    "setTemperature",
    "newTemperature",
    "setCharging",
    "newCharging",
    "startSpeedSimulation",
    "startBatterySimulation",
    "speed",
    "battery",
    "temperature",
    "isCharging"
);
#else  // !QT_MOC_HAS_STRINGDATA
#error "qtmochelpers.h not found or too old."
#endif // !QT_MOC_HAS_STRINGDATA
} // unnamed namespace

Q_CONSTINIT static const uint qt_meta_data_CLASSvehicleDataENDCLASS[] = {

 // content:
      12,       // revision
       0,       // classname
       0,    0, // classinfo
      10,   14, // methods
       4,   92, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags, initial metatype offsets
       1,    0,   74,    2, 0x06,    5 /* Public */,
       3,    0,   75,    2, 0x06,    6 /* Public */,
       4,    0,   76,    2, 0x06,    7 /* Public */,
       5,    0,   77,    2, 0x06,    8 /* Public */,

 // slots: name, argc, parameters, tag, flags, initial metatype offsets
       6,    1,   78,    2, 0x0a,    9 /* Public */,
       8,    1,   81,    2, 0x0a,   11 /* Public */,
      10,    1,   84,    2, 0x0a,   13 /* Public */,
      12,    1,   87,    2, 0x0a,   15 /* Public */,
      14,    0,   90,    2, 0x0a,   17 /* Public */,
      15,    0,   91,    2, 0x0a,   18 /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::Double,    7,
    QMetaType::Void, QMetaType::Int,    9,
    QMetaType::Void, QMetaType::Int,   11,
    QMetaType::Void, QMetaType::Bool,   13,
    QMetaType::Void,
    QMetaType::Void,

 // properties: name, type, flags
      16, QMetaType::Double, 0x00015001, uint(0), 0,
      17, QMetaType::Int, 0x00015001, uint(1), 0,
      18, QMetaType::Int, 0x00015001, uint(2), 0,
      19, QMetaType::Bool, 0x00015001, uint(3), 0,

       0        // eod
};

Q_CONSTINIT const QMetaObject vehicleData::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_CLASSvehicleDataENDCLASS.offsetsAndSizes,
    qt_meta_data_CLASSvehicleDataENDCLASS,
    qt_static_metacall,
    nullptr,
    qt_incomplete_metaTypeArray<qt_meta_stringdata_CLASSvehicleDataENDCLASS_t,
        // property 'speed'
        QtPrivate::TypeAndForceComplete<double, std::true_type>,
        // property 'battery'
        QtPrivate::TypeAndForceComplete<int, std::true_type>,
        // property 'temperature'
        QtPrivate::TypeAndForceComplete<int, std::true_type>,
        // property 'isCharging'
        QtPrivate::TypeAndForceComplete<bool, std::true_type>,
        // Q_OBJECT / Q_GADGET
        QtPrivate::TypeAndForceComplete<vehicleData, std::true_type>,
        // method 'speedChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'batteryChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'temperatureChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'chargingChanged'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'setSpeed'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        QtPrivate::TypeAndForceComplete<double, std::false_type>,
        // method 'setBattery'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        QtPrivate::TypeAndForceComplete<int, std::false_type>,
        // method 'setTemperature'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        QtPrivate::TypeAndForceComplete<int, std::false_type>,
        // method 'setCharging'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        QtPrivate::TypeAndForceComplete<bool, std::false_type>,
        // method 'startSpeedSimulation'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'startBatterySimulation'
        QtPrivate::TypeAndForceComplete<void, std::false_type>
    >,
    nullptr
} };

void vehicleData::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<vehicleData *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->speedChanged(); break;
        case 1: _t->batteryChanged(); break;
        case 2: _t->temperatureChanged(); break;
        case 3: _t->chargingChanged(); break;
        case 4: _t->setSpeed((*reinterpret_cast< std::add_pointer_t<double>>(_a[1]))); break;
        case 5: _t->setBattery((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 6: _t->setTemperature((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 7: _t->setCharging((*reinterpret_cast< std::add_pointer_t<bool>>(_a[1]))); break;
        case 8: _t->startSpeedSimulation(); break;
        case 9: _t->startBatterySimulation(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (vehicleData::*)();
            if (_t _q_method = &vehicleData::speedChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (vehicleData::*)();
            if (_t _q_method = &vehicleData::batteryChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (vehicleData::*)();
            if (_t _q_method = &vehicleData::temperatureChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (vehicleData::*)();
            if (_t _q_method = &vehicleData::chargingChanged; *reinterpret_cast<_t *>(_a[1]) == _q_method) {
                *result = 3;
                return;
            }
        }
    } else if (_c == QMetaObject::ReadProperty) {
        auto *_t = static_cast<vehicleData *>(_o);
        (void)_t;
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< double*>(_v) = _t->getSpeed(); break;
        case 1: *reinterpret_cast< int*>(_v) = _t->getBattery(); break;
        case 2: *reinterpret_cast< int*>(_v) = _t->getTemperature(); break;
        case 3: *reinterpret_cast< bool*>(_v) = _t->getIsCharging(); break;
        default: break;
        }
    } else if (_c == QMetaObject::WriteProperty) {
    } else if (_c == QMetaObject::ResetProperty) {
    } else if (_c == QMetaObject::BindableProperty) {
    }
}

const QMetaObject *vehicleData::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *vehicleData::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_CLASSvehicleDataENDCLASS.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int vehicleData::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 10)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 10;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 10)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 10;
    }else if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    }
    return _id;
}

// SIGNAL 0
void vehicleData::speedChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void vehicleData::batteryChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void vehicleData::temperatureChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void vehicleData::chargingChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
