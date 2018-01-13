#coding: utf-8

from smbus2 import SMBus
import time
import sendtemperature as send

bus_number  = 1
# SDO = GND > 0x76
# SDO = GND > 0x77
# 今回はSDOをGNDに接続している為、0x76
i2c_address = 0x76

bus = SMBus(bus_number)

digT = []

t_fine = 0.0


def writeReg(reg_address, data):
	bus.write_byte_data(i2c_address,reg_address,data)

def get_calib_param():
	calib = []

	for i in range (0x88,0x88+6):
		calib.append(bus.read_byte_data(i2c_address,i))
	digT.append((calib[1] << 8) | calib[0])
	digT.append((calib[3] << 8) | calib[2])
	digT.append((calib[5] << 8) | calib[4])
	# ２の補数で表現されているので、符合bitである最上位bitが1の時に10進数で扱えるように変換する
	for i in range(1,2):
		if digT[i] & 0x8000:
			digT[i] = (-digT[i] ^ 0xFFFF) + 1

def readData():
    data = []
    for i in range (0xFA, 0xFA+3):
        data.append(bus.read_byte_data(i2c_address,i))
    temp_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    compensate_T(temp_raw)

def compensate_T(adc_T):
    # globalな理由は気圧と湿度の制度を上げる為の計算に、気温情報を使っていた為
    global t_fine
    # ここの式は上位Bitデータと下位Bitのデータを
    v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
    v2 = (adc_T / 131072.0 - digT[0] / 8192.0) * (adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
    t_fine = v1 + v2
    temperature = t_fine / 5120.0
    print("temp : %-6.2f ℃" % (temperature))

def setup():
	osrs_t = 1			#Temperature oversampling x 1
	osrs_p = 0			#Pressure oversampling x 1
	osrs_h = 0			#Humidity oversampling x 1
	mode   = 3			#Normal mode
	t_sb   = 5			#Tstandby 1000ms
	filter = 0			#Filter off
	spi3w_en = 0			#3-wire SPI Disable

	ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
	config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
	ctrl_hum_reg  = osrs_h

	writeReg(0xF2,ctrl_hum_reg)
	writeReg(0xF4,ctrl_meas_reg)
	writeReg(0xF5,config_reg)


setup()
get_calib_param()


if __name__ == '__main__':
    while True:
        readData()
        send.post_server(t_fine)
        time.sleep(10)
