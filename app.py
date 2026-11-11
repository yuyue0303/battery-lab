import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 頁面標題與說明
st.title("⚡ 未知電池內部特徵解密實驗室")
st.write("系統將會為您測量電壓及電流，請於下方調整實驗參數來觀察 V-I 圖表變化：")

# 侧邊欄控制項 (對應原本的 Colab 表單)
st.sidebar.header("🎛️ 實驗參數設定")
battery_type = st.sidebar.selectbox("電池選擇", ["A", "B"])
start = st.sidebar.number_input("外接電阻起始值 start (Ω)", value=1.0)
end = st.sidebar.number_input("外接電阻結束值 end (Ω)", value=800.0)
sample_size = st.sidebar.slider("取樣數 (個)", min_value=20, max_value=400, value=230, step=10)

# 內部隱藏的真實參數
if battery_type == "A":
    global_emf, global_r = 618, 565
else:
    global_emf, global_r = 70, 37

# 產生資料
R_values = np.linspace(start, end, int(sample_size))
I_values = global_emf / (global_r + R_values)
VR_values = global_emf - I_values * global_r
P_values = I_values * VR_values

# 線性擬合
p_fit = np.polyfit(I_values, VR_values, 1)
slope_w = p_fit[0]
intercept_b = p_fit[1]
trendline = slope_w * I_values + intercept_b

# 畫 V-I 圖 (Streamlit 需要透過 fig 物件渲染)
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.scatter(I_values, VR_values, label='Measured Data (I,V)', color='dodgerblue', s=20)

# 直接將擬合方程式寫進 Trendline 的圖例標籤中
trend_label = f'Trendline: y = {slope_w:.1f}x + {intercept_b:.1f}'
ax.plot(I_values, trendline, label=trend_label, color='darkorange', linewidth=1)

ax.set_title(f"V-I Analysis: battery {battery_type}", fontsize=11, fontweight='bold')
ax.set_xlabel("Current I (A)", fontsize=10)
ax.set_ylabel("Voltage V (V)", fontsize=10)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)

# 在網頁上顯示圖表
st.pyplot(fig)
