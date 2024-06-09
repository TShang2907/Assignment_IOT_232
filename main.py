from modbus485 import*
from mqtt import*
import time
import serial as serial
import json

try:
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
except:
    print("Modbus485**","Failed to write data")
MQTT_TOPIC_AI="/innovation/valvecontroller/ai"
m485 = Modbus485(ser)
relay_ON=[[1, 6, 0, 0, 0, 255, 201, 138],[2, 6, 0, 0, 0, 255, 201, 185],[3, 6, 0, 0, 0, 255, 200, 104]]
relay_OFF=[[1, 6, 0, 0, 0, 0, 137, 202],[2, 6, 0, 0, 0, 0, 137, 249],[3, 6, 0, 0, 0, 0, 136, 40]]

relay1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
relay1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

relay2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

relay3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

soil_temperature =[10, 3, 0, 6, 0, 1, 101, 112]
soil_moisture = [10, 3, 0, 21, 0, 1, 148, 181]

mqtt=MQTTHelper()
# Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
def receive_callback(message):
    json_data = json.loads(message.payload.decode("utf-8"))
    print("Received: ",json_data )
    
    if message.topic=="/innovation/valvecontroller/station1":
        index=0
        for sensor in json_data["sensors"]:
            if sensor.sensor_value==1 :
                m485.modbus485_send(relay_ON[index])
                time.sleep(1)
                m485.modbus485_read_adc()
            else :
                m485.modbus485_send(relay_OFF[index])
                time.sleep(1)
                m485.modbus485_read_adc()
            index=index+1
        
    # if message.topic=="/innovation/pumpcontroller/station1":

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
    #mqtt.publish(MQTT_TOPIC_AI,"hello")