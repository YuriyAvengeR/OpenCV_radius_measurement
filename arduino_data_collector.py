import serial
import time

#n = 6

def com_connect(n):
    try:
        data = serial.Serial(port = f'COM{n}', baudrate = 9600)
        if not data.is_open:
            data.open()
        else:
            return data
    except(ValueError):
        print("[i] Невірно вказані вхідні дані.")
    except(SyntaxError):
        print("[i] Помилка в коді.")
    except (serial.serialutil.SerialException):
        print('[i] Помилка підключення до порту, вказаний неправильний порт або баудрейт. Або неможливо відкрити порт.')

def com_data(n):
    data = com_connect(n)
    if data is not None:
        try:
            port_data = data.read(10) #БУФЕР
            return port_data
        except(ValueError):
            print("[i] Невірно вказані вхідні дані.")
        except(SyntaxError):
            print("[i] Помилка виконання коду.")
        except(UnboundLocalError):
            print("[i] Помилка змінної, код не виконаний.")
        except(serial.serialutil.PortNotOpenError):
            print("COM port не був відкритий.")
    else:
        pass


#port is a device name: depending on operating system. e.g. /dev/ttyUSB0 on GNU/Linux or COM3 on Windows.