
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.title("地震マップ（USGS）")

# ✅ ローディング表示
with st.spinner("地震データ取得中..."):

    try:
        url = (
            "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
            "?starttime=2024-01-01"
            "&endtime=2024-12-31"
            "&minmagnitude=5"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

    except Exception as e:
        st.error(f"データ取得エラー: {e}")
        st.stop()

# 地図
m = folium.Map(location=[0, 0], zoom_start=2)
marker_cluster = MarkerCluster().add_to(m)

# 最大件数制限（重要）
for eq in data["features"][:500]:   # ←ここ重要（負荷制御）
    coords = eq["geometry"]["coordinates"]
    lon, lat = coords[0], coords[1]
    mag = eq["properties"]["mag"]

    folium.Marker(
        location=[lat, lon],
        popup=f"M {mag}"
    ).add_to(marker_cluster)

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
