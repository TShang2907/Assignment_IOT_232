from modbus485 import*
from mqtt import*
import time
import serial as serial
import json
from Scheduler.scheduler import  *
from datetime import datetime,timedelta

#RS485
# try:
#     ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
# except:
#     print("Modbus485**","Failed to write data")
# m485 = Modbus485(ser)

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

############## Schedule  ######################
scheduler = Scheduler()
scheduler.SCH_Init()

##############  MQTT  #######################
mqtt=MQTTHelper()
MQTT_TOPIC_SUB_SCHEDULELIST="/innovation/valvecontroller/schedulelist1"
schedulelist = {
    "station_id": "SCHEDULE_0001",
    "station_name": "Lich tuoi",
    "gps_longitude": 106.89,
    "gps_latitude": 10.5,
    "schedule_list": [
      {
        "startTime": "16:40",
        "endTime": "16:40",
        "nitorValue": 0,
        "kaliValue": 0,
        "photphoValue": 0,
        "cycle": 0,
        "isActive": True,
        "status": "WAITING",
        "area": 1,
        "priority": 3
      }
    ]
  }


def Task_Run_Watering(index):
    print("Bắt đầu tưới")
    print("Trộn dung dịch 1")
    time.sleep(1)
    print("Trộn dung dịch 2")
    time.sleep(1)
    print("Trộn dung dịch 3")
    time.sleep(1)
    print("Máy bơm vào bật")
    time.sleep(3)
    print("Máy bơm vào tăt")
    print("Máy bơm ra bật")
    time.sleep(3)
    print("Máy bơm ra tăt")
    schedulelist["schedule_list"][index]["status"]="DONE"
    mqtt.publish(MQTT_TOPIC_SUB_SCHEDULELIST,json.dumps(schedulelist))

# Định nghĩa một hàm xử lý để nhận các thông điệp từ máy chủ MQTT
def receive_callback(message):
    global schedulelist
    json_data = json.loads(message.payload.decode("utf-8"))
    print("Received from server: ",message.topic )

    #Control Valve
    if message.topic=="/innovation/valvecontroller/station1":
        index=0
        for sensor in json_data["sensors"]:
            if valve_value[index] !=sensor["sensor_value"]:
                if sensor["sensor_value"]==1 :
                    print("Relay Valve ",index+1)
                    print("ON")
                    # m485.modbus485_send(relay_ON[index])
                    # time.sleep(1)
                    # m485.modbus485_read_adc()
                else :
                    print("Relay Valve ",index+1)
                    print("OFF")
                    # m485.modbus485_send(relay_OFF[index])
                    # time.sleep(1)
                    # m485.modbus485_read_adc()
                valve_value[index]=sensor["sensor_value"]
            index=index+1

    ## Control Pump
    if message.topic=="/innovation/pumpcontroller/station1":
        index=3
        for sensor in json_data["sensors"]:
            if pump_value[index-3] !=sensor["sensor_value"]:
                if sensor["sensor_value"]==1 :
                    print("Relay Pump ",index-3)
                    print(" ON")
                    # m485.modbus485_send(relay_ON[index])
                    # time.sleep(1)
                    # m485.modbus485_read_adc()
                else :
                    print("Relay Pump ",index-3)
                    print(" OFF")
                    # m485.modbus485_send(relay_OFF[index])
                    # time.sleep(1)
                    # m485.modbus485_read_adc()
                pump_value[index-3]=sensor["sensor_value"]
            index=index+1

    ## Schedule
    if message.topic=="/innovation/valvecontroller/schedulelist1" :
        schedulelist=json_data
        if(len(schedulelist["schedule_list"])>0):
            for schedule in schedulelist["schedule_list"]:
                if(schedule["status"]=="WAITING"):
                    #Lay thoi gian bat dau
                    str_time_start=schedule["startTime"]
                    str_time_end=schedule["endTime"]
                    # Tìm vị trí của dấu hai chấm
                    colon_index = str_time_start.index(':')
                    # Lấy phút và giây dưới dạng số nguyên
                    hour = int(str_time_start[:colon_index])
                    minute = int(str_time_start[colon_index + 1:])
                    total_minute=hour*60+minute

                   
                    #Lay thoi gian hien tai
                    current_time=datetime.now()
                    hour1=current_time.hour
                    minute1=current_time.minute
                    total_minute1=hour1*60+minute1
                    print("Lịch tưới "+str_time_start+" - "+str_time_end)
                   
                    #Delay Time
                    delay_time=total_minute-total_minute1
                   
                    #Area 
                    area=schedule["area"]
                    scheduler.SCH_Add_Task(Task_Run_Watering, delay_time,0,area)
        else :
            # scheduler.SCH_Delete()
            print("Lich tuoi trong")

# Gọi phương thức setRecvCallBack để gán hàm xử lý cho việc nhận thông điệp
mqtt.setRecvCallBack(receive_callback)
while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(1)
   
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