import minimalmodbus
import time

class YieryiSensor:

    def __init__(self, port="COM4", slave_id=1):
        self.instrument = minimalmodbus.Instrument(port, slave_id)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 1
        self.instrument.mode = minimalmodbus.MODE_RTU

    def read_sample(self):
        time.sleep(30)  # estabilización confirmada experimentalmente

        regs = self.instrument.read_registers(0, 9, functioncode=3)

        return {
            "humidity": regs[0] / 10,
            "temperature": regs[1] / 50,
            "ec": regs[2],
            "ph": regs[3] / 10,
            "n": regs[4],
            "p": regs[5],
            "k": regs[6],
            "salinity": regs[7]
        }