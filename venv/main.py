from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def get_title(url):
    try:
        html = urlopen(url)
    # 404, 500 등 예외 처리
    except HTTPError as e:
        return None
    try:
        bs_obj = BeautifulSoup(html.read(), "html.parser")
        title = bs_obj.body.h1
    except AttributeError as e:
        return None
    return title


def get_weather_info_naver():
    try:
        html = urlopen("https://search.naver.com/search.naver?query=weather")
    except HTTPError as e:
        return None
    try:
        bs_obj = BeautifulSoup(html, "html.parser")
        today_data = bs_obj.find("div", {"class": "today_area _mainTabContent"})
        tomorrow_data = bs_obj.find("div", {"class": "tomorrow_area _mainTabContent"})
        day_after_tomorrow_data = bs_obj.find("div", {"class": "tomorrow_area day_after _mainTabContent"})
        days = {
            "today": {
                "cast_txt": today_data.find("p", {"class": "cast_txt"}).get_text().replace("아요", "습니다."),
                "temp": today_data.find("span", {"class": "todaytemp"}).get_text(),
                "temp_min": today_data.find("span", {"class": "min"}).find("span").get_text(),
                "temp_max": today_data.find("span", {"class": "max"}).find("span").get_text(),
                "fine_dust": today_data.findAll("dd", {"class": "lv1"})[0].find("span", {"class": "num"}).get_text(),
                "ultra_fine_dust": today_data.findAll("dd", {"class": "lv1"})[1].find("span",
                                                                                      {"class": "num"}).get_text()
            },
            "tomorrow": {
                "temp_am": tomorrow_data.findAll("span", {"class": "todaytemp"})[0].get_text(),
                "temp_pm": tomorrow_data.findAll("span", {"class": "todaytemp"})[1].get_text(),
                "fine_dust_status": tomorrow_data.find("span", {"class": "lv3"}).get_text()
            },
            "day_after_tomorrow": {
                "temp_am": day_after_tomorrow_data.findAll("span", {"class": "todaytemp"})[0].get_text(),
                "temp_pm": day_after_tomorrow_data.findAll("span", {"class": "todaytemp"})[1].get_text(),
                "fine_dust_status": day_after_tomorrow_data.find("span", {"class": "lv3"}).get_text()
            }
        }

    except AttributeError as e:
        return None
    return days


weather_info = get_weather_info_naver()
today_weather_info = weather_info['today']
tomorrow_weather_info = weather_info['tomorrow']
day_after_tomorrow_weather_info = weather_info['day_after_tomorrow']
print(weather_info)

print("오늘 날씨입니다.")
print("오늘의 날씨는 " + today_weather_info['cast_txt'])
print("오늘의 온도는 " + today_weather_info['temp'] + "℃이며, 최저 " + today_weather_info['temp_max'] + "℃, 최고 " +
      today_weather_info['temp_min'] + "℃ 입니다.")
print("오늘의 미세먼지는 " + today_weather_info['fine_dust'] + ", 초미세먼지는 " + today_weather_info['ultra_fine_dust'] + "입니다.")

print("\n내일 날씨입니다.")
print("내일의 오전 온도는 " + tomorrow_weather_info['temp_am'] + "℃, 오후 온도는 " + tomorrow_weather_info['temp_pm'] + "℃ 입니다.")
print("내일의 미세먼지는 \"" + tomorrow_weather_info['fine_dust_status'] + "\" 입니다.")

print("\n모레 날씨입니다.")
print("모레의 오전 온도는 " + day_after_tomorrow_weather_info['temp_am'] + "℃, 오후 온도는 " + day_after_tomorrow_weather_info[
    'temp_pm'] + "℃ 입니다.")
print("모레의 미세먼지는 \"" + day_after_tomorrow_weather_info['fine_dust_status'] + "\" 입니다.")
