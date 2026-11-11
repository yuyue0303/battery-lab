import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 頁面標題與說明
st.title("⚡ 未知電池內部特徵解密實驗室")
st.write("歡迎來到互動實驗室！請於左側側邊欄調整實驗參數，設定完成後點擊 **「開始執行實驗」** 按鈕來輸出分析圖表。")

# 2. 側邊欄控制項
st.sidebar.header("🎛️ 實驗參數設定")
battery_type = st.sidebar.selectbox("電池選擇", ["A", "B"])
start = st.sidebar.number_input("外接電阻起始值 start (Ω)", value=1.0)
end = st.sidebar.number_input("外接電阻結束值 end (Ω)", value=800.0)
sample_size = st.sidebar.slider("取樣數 (個)", min_value=20, max_value=400, value=230, step=10)

st.sidebar.markdown("---")
# 🌟 需求 1：加入「執行按鈕」，必須點下去才會跑出圖表
run_button = st.sidebar.button("🚀 開始執行實驗", type="primary")

# 3. 只有當學生點擊按鈕後，才會進行計算與畫圖
if run_button:
    with st.spinner('正在測量電壓與電流中...'):
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

        # 畫 V-I 圖
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.scatter(I_values, VR_values, label='Measured Data (I,V)', color='dodgerblue', s=20)
        
        # 擬合方程式圖例
        trend_label = f'Trendline: y = {slope_w:.1f}x + {intercept_b:.1f}'
        ax.plot(I_values, trendline, label=trend_label, color='darkorange', linewidth=1)

        ax.set_title(f"V-I Analysis: battery {battery_type}", fontsize=11, fontweight='bold')
        ax.set_xlabel("Current I (A)", fontsize=10)
        ax.set_ylabel("Voltage V (V)", fontsize=10)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.6)

        # 顯示成功提示與圖表
        st.success("實驗測量完畢！以下是本次的 V-I 分析圖表：")
        st.pyplot(fig)
else:
    st.info("👈 請在左側調整好參數後，點擊 **「🚀 開始執行實驗」** 按鈕。")
