from modbus485 import*
from mqtt import*
import time
import serial as serial
import json

try:
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
except:
    print("Modbus485**","Failed to write data")
m485 = Modbus485(ser)

relay_ON=[[1, 6, 0, 0, 0, 255, 201, 138],[2, 6, 0, 0, 0, 255, 201, 185],[3, 6, 0, 0, 0, 255, 200, 104],[4, 6, 0, 0, 0, 255, 201, 223],[5, 6, 0, 0, 0, 255, 200, 14],
          [6, 6, 0, 0, 0, 255, 200, 61],[7, 6, 0, 0, 0, 255, 201, 236],[8, 6, 0, 0, 0, 255, 201, 19]]
relay_OFF=[[1, 6, 0, 0, 0, 0, 137, 202],[2, 6, 0, 0, 0, 0, 137, 249],[3, 6, 0, 0, 0, 0, 136, 40],[4, 6, 0, 0, 0, 0, 137, 159],
           [5, 6, 0, 0, 0, 0, 136, 78],[6, 6, 0, 0, 0, 0, 136, 125],[7, 6, 0, 0, 0, 0, 137, 172],[8, 6, 0, 0, 0, 0, 137, 83]]

valve_value=[0,0,0]
pump_value=[0,0,0,0,0,]

relay1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

relay4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
relay4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

relay5_ON  = [5, 6, 0, 0, 0, 255, 200, 14]
relay5_OFF = [5, 6, 0, 0, 0, 0, 136, 78]

relay6_ON  = [6, 6, 0, 0, 0, 255, 200, 61]
relay6_OFF = [6, 6, 0, 0, 0, 0, 136, 125]

relay7_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
relay7_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

relay8_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
relay8_OFF = [8, 6, 0, 0, 0, 0, 137, 83]

soil_temperature =[10, 3, 0, 6, 0, 1, 101, 112]
soil_moisture = [10, 3, 0, 21, 0, 1, 148, 181]

mqtt=MQTTHelper()
# Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
def receive_callback(message):
    json_data = json.loads(message.payload.decode("utf-8"))
    print("Received from server: ",message.topic )
    
    if message.topic=="/innovation/valvecontroller/station1":
        index=0
        for sensor in json_data["sensors"]:
            if valve_value[index] !=sensor["sensor_value"]:
                if sensor["sensor_value"]==1 :
                    print("Relay Valve ",index+1)
                    print("ON")
                    m485.modbus485_send(relay_ON[index])
                    time.sleep(1)
                    m485.modbus485_read_adc()
                else :
                    print("Relay Valve ",index+1)
                    print("OFF")
                    m485.modbus485_send(relay_OFF[index])
                    time.sleep(1)
                    m485.modbus485_read_adc()
                valve_value[index]=sensor["sensor_value"]
            index=index+1
        
    if message.topic=="/innovation/pumpcontroller/station1":
        index=3
        for sensor in json_data["sensors"]:
            if pump_value[index-3] !=sensor["sensor_value"]:
                if sensor["sensor_value"]==1 :
                    print("Relay Pump ",index-3)
                    print(" ON")
                    m485.modbus485_send(relay_ON[index])
                    time.sleep(1)
                    m485.modbus485_read_adc()
                else :
                    print("Relay Pump ",index-3)
                    print(" OFF")
                    m485.modbus485_send(relay_OFF[index])
                    time.sleep(1)
                    m485.modbus485_read_adc()
                pump_value[index-3]=sensor["sensor_value"]
            index=index+1

# Gọi phương thức setRecvCallBack để gán hàm xử lý cho việc nhận thông điệp
mqtt.setRecvCallBack(receive_callback)

while True:
    pass
    # m485.modbus485_send(soil_temperature)
    # time.sleep(1)
    # m485.modbus485_read_adc()
    # time.sleep(1)

    # m485.modbus485_send(soil_moisture)
    # time.sleep(1)
    # m485.modbus485_read_adc()
    # time.sleep(1)

    # mqtt.publish(MQTT_TOPIC_SENSOR,"hello")
    # time.sleep(5)