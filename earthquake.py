
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.title("地震マップ（USGS）")

# ✅ メッセージ用プレースホルダ
status = st.empty()
status.write("地震データ取得中...")

# データ取得
url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    "?starttime=2021-01-01"
    "&endtime=2026-12-31"
    "&minmagnitude=5"
)

response = requests.get(url)
data = response.json()

# ✅ メッセージ消す
status.empty()

# 地図作成
m = folium.Map(location=[0, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(m)

# データ描画
for eq in data["features"]:
    coords = eq["geometry"]["coordinates"]
    lon, lat = coords[0], coords[1]
    mag = eq["properties"]["mag"]

    folium.Marker(
        location=[lat, lon],
        popup=f"M {mag}"
    ).add_to(marker_cluster)

# 表示
st_folium(m)


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
