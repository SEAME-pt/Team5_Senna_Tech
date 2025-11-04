#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QObject>
#include <QTimer>
#include <QtMath>
#include <QRandomGenerator>
#include <QDebug>

class ClusterBackend : public QObject {
    Q_OBJECT
    Q_PROPERTY(double speed READ speed NOTIFY speedChanged)
    Q_PROPERTY(int battery READ battery NOTIFY batteryChanged)
    Q_PROPERTY(bool charging READ charging NOTIFY chargingChanged)
public:
    ClusterBackend(QObject* parent = nullptr)
        : QObject(parent), m_speed(0.0), m_battery(85), m_charging(false)
    {
        // Simula variação de velocidade e bateria
        QTimer *t = new QTimer(this);
        connect(t, &QTimer::timeout, this, &ClusterBackend::updateValues);
        t->start(100); // 10 Hz para demo suave
    }

    double speed() const { return m_speed; }
    int battery() const { return m_battery; }
    bool charging() const { return m_charging; }

signals:
    void speedChanged();
    void batteryChanged();
    void chargingChanged();

public slots:
    void setCharging(bool c) {
        if (m_charging == c) return;
        m_charging = c;
        emit chargingChanged();
    }

private slots:
    void updateValues() {
        // Uma simulação simples: velocidade oscila senoidalmente entre 0 e 220
        static double t = 0.0;
        t += 0.03;
        m_speed = qBound(0.0, 110.0 + 110.0 * qSin(t), 240.0);

        // Simula consumo de bateria — se charging = true, sobe
        if (m_charging) {
            // bounded(a,b) retorna inteiro em [a, b-1]
            int add = QRandomGenerator::global()->bounded(1, 3); // retorna 1 ou 2
            m_battery = qMin(100, m_battery + add);
        } else {
            int sub = QRandomGenerator::global()->bounded(0, 2); // 0 ou 1
            m_battery = qMax(0, m_battery - sub);
        }

        emit speedChanged();
        emit batteryChanged();
    }

private:
    double m_speed;
    int m_battery;
    bool m_charging;
};

#include "main.moc"

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;

    ClusterBackend backend;
    engine.rootContext()->setContextProperty("clusterBackend", &backend);

    const QUrl url(QStringLiteral("qrc:/Main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
                         if (!obj && url == objUrl)
                             QCoreApplication::exit(-1);
                     }, Qt::QueuedConnection);

    engine.load(url);

    return app.exec();
}
