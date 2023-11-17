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
                    text = ":orange[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + next_bus["remainingStop"] + "역 전"
                else:
                    text = ":blue[" + str(sec // 60) + "분 " + str(sec % 60) + "초], " + next_bus["remainingStop"] + "역 전"
                if next_bus["remainingSeat"] != None:
                    text += ", 남은 좌석 : " + next_bus["remainingSeat"]
                st.write(text)
        else:
            st.write(":red[운행 안 하는 중]")

def main():
    # streamlit 시차 고려
    import datetime
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    weekday = now.weekday
    
    # 학원 > 집
    if weekday == 3 or weekday == 4:
        print_title("학원에서 집가기")
        print_station('101480', True, ['5712'])
        print_title("집에서 학교가기")
        print_station('101401', True, ['603', '5012', '6617'])
        
    # 집 > 학교
    else:
        print_title("집에서 학교가기")
        print_station('101401', True, ['603', '5012', '6617'])
        print_title("학원에서 집가기")
        print_station('101480', True, ['5712'])

    st.write(str(now.hour) + ":" + str(now.minute) + " 기준")

main()

print_title("후후 조티미가윰")
