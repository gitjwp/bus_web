# 구조화
import datetime
from dataclasses import dataclass
@dataclass
class bus:
    remainingTime:int = None
    remainingStop:int = None
    remainingSeat:int = None

@dataclass
class busline:
    name:str = ""
    direction:str = ""
    status:bool = False
    next_buses:list = None

@dataclass
class station:
    title:str = ""
    Id:str = None
    selective:bool = True
    select_buslines:list = None
    least_time:int = None
    buslines:list = None

@dataclass
class struct:
    stations:list = None
    last_time:datetime.datetime = None

# 순서 조건
def reverse():
    # streamlit 시차 고려, 9시간 더하기
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    return not (now.weekday == 3 or now.weekday == 4)

# 구조 초기화
def init_struct():
    # 구조 생성
    S = struct()
    S.last_time = datetime.datetime.now() + datetime.timedelta(hours=9)
    S.stations = [station(), station()]
    
    S.stations[0].title = "학원에서 집으로"
    S.stations[0].Id = "101480"
    S.stations[0].select_buslines = ["5712"]
        
    S.stations[1].title = "집에서 학교로"
    S.stations[1].Id = "101401"
    S.stations[1].select_buslines = ["603", "5012", "6617"]

    if reverse():
        S.stations.reverse()
        
    return S

# 정거장 단위로 데이터 얻어서 적용
import requests
def station_data(station):
    # 초기화
    station.least_time = None
    
    # 1단계 : 요청
    req = requests.get('https://map.naver.com/p/api/pubtrans/realtime/bus/arrivals?stopId='+station.Id)
    data = str(req.text)

    # 2단계 : 반응을 리스트로 변환
    import json
    data = json.loads(data)

    # 3단계 : 자료 저장
    station.buslines = []
    for bus_line in data:
        if station.selective and not bus_line["name"] in station.select_buslines:
            continue

        station.buslines.append(busline())
        station.buslines[-1].name = bus_line["longName"]
        station.buslines[-1].direction = bus_line["direction"]
        station.buslines[-1].status = bus_line["arrival"]["status"] == "RUNNING"
        station.buslines[-1].next_buses = []

        for next_bus in bus_line["arrival"]["buses"]:
            station.buslines[-1].next_buses.append(bus())
            station.buslines[-1].next_buses[-1].remainingTime = next_bus["remainingTime"]
            station.buslines[-1].next_buses[-1].remainingStop = next_bus["remainingStop"]
            station.buslines[-1].next_buses[-1].remainingSeat = next_bus["remainingSeat"]

            if next_bus["remainingTime"] != None:
                if station.least_time == None:
                    station.least_time = next_bus["remainingTime"]
                elif next_bus["remainingTime"] < station.least_time:
                    station.least_time = next_bus["remainingTime"]

# 정거장 초기화
import streamlit as st
def init_stations(S):
    for station in S.stations:
        # 정거장 데이터 적용
        station_data(station)

# 실제로 전시하는 함수 (메인쓰레드) + 1초씩 깎기
import time
def display(S):
    UI = st.empty()
    while True:
        dS = UI.container()
        for i, station in enumerate(S.stations):
            # 업데이트가 필요한지 검사 & 실행
            if station.least_time != None:
                if station.least_time < 5 or station.least_time % 30 == 0:
                    station_data(station)
            
            # 헤더 표시
            dS.header(station.title, divider='rainbow')
            
            # 정보 게시            
            for busline in station.buslines:
                dS.write("#### :green[" + busline.name + " (" + busline.direction + " 방면)]")
                
                bus_content = ""
                if busline.status:
                    for next_bus in busline.next_buses:
                        sec = int(next_bus.remainingTime)
                        if sec < 300:
                            bus_content += ":orange[" + str(sec // 60) + "분 " + str(sec % 60) + "초] (" + str(next_bus.remainingStop) + "역전) "
                        else:
                            bus_content += ":blue[" + str(sec // 60) + "분 " + str(sec % 60) + "초] (" + str(next_bus.remainingStop) + "역전) "
                        #if next_bus["remainingSeat"] != None:
                        #    text += ", 남은 좌석 : " + str(next_bus.remainingSeat)
                        next_bus.remainingTime -= 1
                else:
                    bus_content = ":red[운행 안 하는 중]"
                
                dS.write(bus_content)
                
            if station.least_time != None:
                station.least_time -= 1

        time.sleep(1)

# 메인 함수
def main():
    S = init_struct()
    init_stations(S)
    display(S)

main()
