import requests

# 버스 ID
ID = '115846'

# URL
url = 'https://map.naver.com/p/api/pubtrans/realtime/bus/arrivals?stopId='+ID

# 특정 버스만 볼 것인가?
selection = False
selected_bus = ["112"]

# 1단계 : 요청
req = requests.get(url)
data = str(req.text)

# 2단계 : 반응을 리스트로 변환
import json
data = json.loads(data)


# 3단계 : 자료를 적절하게 표시
import streamlit as st
#data

for bus in data:
    if selection and not bus["name"] in selected_bus:
        continue
    
    st.write("#### :green[" + bus["longName"] + " (" + bus["direction"] + " 방면)]")
    if bus["arrival"]["status"] == "RUNNING":
        for next_bus in bus["arrival"]["buses"]:
            sec = int(next_bus["remainingTime"])
            if sec < 300:
                text = ":orange[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + next_bus["remainingStop"] + "역 전"
            else:
                text = ":blue[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + next_bus["remainingStop"] + "역 전"
            if next_bus["remainingSeat"] != None:
                text += ", 남은 좌석 : " + next_bus["remainingSeat"]
            st.write(text)
    else:
        st.write(":red[운행 안 하는 중]")

