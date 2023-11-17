# 제목 출력
import streamlit as st
def print_title(title):
    st.write("### " + title)

# 정류장 단위 출력
import requests
def print_station(Id, selection, selected_bus):
    # URL
    url = 'https://map.naver.com/p/api/pubtrans/realtime/bus/arrivals?stopId='+Id

    # 1단계 : 요청
    req = requests.get(url)
    data = str(req.text)

    # 2단계 : 반응을 리스트로 변환
    import json
    data = json.loads(data)


    # 3단계 : 자료를 적절하게 표시
    for bus in data:
        if selection and not bus["name"] in selected_bus:
            continue
    
        st.write("#### :green[" + bus["longName"] + " (" + bus["direction"] + " 방면)]")
        if bus["arrival"]["status"] == "RUNNING":
            for next_bus in bus["arrival"]["buses"]:
                sec = int(next_bus["remainingTime"])
                if sec < 300:
                    text = ":orange[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + str(next_bus["remainingStop"]) + "역전"
                else:
                    text = ":blue[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + str(next_bus["remainingStop"]) + "역전"
                if next_bus["remainingSeat"] != None:
                    text += ", 남은 좌석 : " + str(next_bus["remainingSeat"])
                st.write(text)
        else:
            st.write(":red[운행 안 하는 중]")

def main():
    # streamlit 시차 고려
    import datetime
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    
    # 학원 가는거
    if now.hour < 15:
        print_title("집 > 학원")
        print_station("115846", True, "112")
        print_title("학원 > 집")
        print_station("115065", True, "112")
    # 집 가는거
    else:
        print_title("학원 > 집")
        print_station("115065", True, "112")
        print_title("집 > 학원")
        print_station("115846", True, "112")

    st.write(str(now.hour) + ":" + str(now.minute) + " 기준")

main()
