import requests
import folium
import urllib3
from folium.plugins import MarkerCluster

# SSL警告OFF
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# USGS API
url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    "?starttime=2021-01-01"
    "&endtime=2026-12-31"
    "&minmagnitude=5"
)

print("地震データ取得中...")

# データ取得
response = requests.get(url, verify=False)

# JSON化
data = response.json()

print("取得完了")

# 地図作成
m = folium.Map(
    location=[20, 0],
    zoom_start=2
)

# クラスタ
marker_cluster = MarkerCluster().add_to(m)

earthquake_count = 0

# 地震処理
for feature in data["features"]:

    properties = feature["properties"]
    geometry = feature["geometry"]

    mag = properties["mag"]
    place = properties["place"]

    if mag is None:
        continue

    lon, lat, depth = geometry["coordinates"]

    earthquake_count += 1

    # 色
    if mag >= 7:
        color = "red"
    elif mag >= 6:
        color = "orange"
    else:
        color = "blue"

    popup_text = (
        f"<b>Magnitude:</b> {mag}<br>"
        f"<b>Place:</b> {place}<br>"
        f"<b>Depth:</b> {depth} km"
    )

    folium.CircleMarker(
        location=[lat, lon],
        radius=mag * 2,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
    ).add_to(marker_cluster)

# 保存
save_path = (
    r"C:\Users\T.Sugawara\OneDrive - Shell\デスクトップ\earthquake_map.html"
)

m.save(save_path)

print("================================")
print("地図保存完了")
print(save_path)
print(f"地震数: {earthquake_count}")
print("================================")