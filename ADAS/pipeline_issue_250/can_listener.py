import can

def simple_listener():
    bus = None
    try:
        # filtrado o ID da FSM
        filters = [{"can_id": 0x001, "can_mask": 0x7FF, "extended": False}]

        bus = can.interface.Bus(channel='vcan0', interface='socketcan', can_filters=filters)
        
        print("A escutar APENAS ID 0x001 no vcan0... (Pressiona Ctrl+C para sair)")
        
        while True:
            msg = bus.recv(timeout=1.0) 
            if msg:
                data_str = " ".join(f"{b:02X}" for b in msg.data)
                print(f"ID: {hex(msg.arbitration_id)} | DLC: {msg.dlc} | Data: [ {data_str} ]")

    except KeyboardInterrupt:
        print("\n[INFO] Interrupção detetada. A encerrar...")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema: {e}")
    finally:
        if bus:
            bus.shutdown()
            print("[OK] SocketcanBus encerrado corretamente.")

if __name__ == "__main__":
    simple_listener()