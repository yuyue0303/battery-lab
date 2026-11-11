import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 1. 頁面標題與說明
st.title("⚡ 未知電池內部特徵解密實驗室")
st.write("歡迎來到互動實驗室！請於左側側邊欄調整實驗參數，設定完成後點擊 **「開始執行實驗」** 按鈕來輸出分析圖表。")

# 2. 側邊欄控制項（統一控制兩部分的參數）
st.sidebar.header("🎛️ 實驗參數設定")
battery_type = st.sidebar.selectbox("電池選擇", ["A", "B"])
start = st.sidebar.number_input("外接電阻起始值 start (Ω)", value=1.0)
end = st.sidebar.number_input("外接電阻結束值 end (Ω)", value=800.0)
sample_size = st.sidebar.slider("取樣數 (個)", min_value=20, max_value=400, value=230, step=10)

st.sidebar.markdown("---")
run_button = st.sidebar.button("🚀 開始執行實驗", type="primary")

# 3. 只有當學生點擊按鈕後，才會進行計算並顯示兩個圖表
if run_button:
    with st.spinner('正在進行物理量測與分析中...'):
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

        # ==================== 第一部分：V-I 圖 ====================
        st.subheader("🔍 第一部分：V-I 測量與內部特徵解密")
        st.write("透過改變外接電阻，觀察端電壓與電流的線性關係，並從中推算電動勢與內電阻。")

        # 線性擬合
        p_fit = np.polyfit(I_values, VR_values, 1)
        slope_w = p_fit[0]
        intercept_b = p_fit[1]
        trendline = slope_w * I_values + intercept_b

        # 畫 V-I 圖
        fig1, ax1 = plt.subplots(figsize=(10, 4.5))
        ax1.scatter(I_values, VR_values, label='Measured Data (I,V)', color='dodgerblue', s=20)
        trend_label = f'Trendline: y = {slope_w:.1f}x + {intercept_b:.1f}'
        ax1.plot(I_values, trendline, label=trend_label, color='darkorange', linewidth=1)

        ax1.set_title(f"V-I Analysis: battery {battery_type}", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Current I (A)", fontsize=10)
        ax1.set_ylabel("Voltage V (V)", fontsize=10)
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(True, linestyle='--', alpha=0.6)

        st.pyplot(fig1)

        st.markdown("---")

        # ==================== 第二部分：P-R 功率曲線圖 ====================
        st.subheader("⚡ 第二部分：功率曲線與阻抗匹配")
        st.write("尋找當外接電阻多大時該電池有最大功率，探討阻抗匹配現象。")

        # 找出最大功率點
        max_idx = np.argmax(P_values)
        max_P = P_values[max_idx]
        max_R = R_values[max_idx]

        # 畫 P-R 圖
        fig2, ax2 = plt.subplots(figsize=(10, 4.5))
        ax2.set_ylim(0, max_P * 1.15)  # 讓 Y 軸頂端自動多留 15% 的空間
        ax2.scatter(R_values, P_values, label='Data (R,P)', color='dodgerblue', s=20)
        ax2.scatter(max_R, max_P, color='crimson', s=20, zorder=5, label=f'Max Power')
        
        # 標註點（已調整偏移量避免撞框）
        ax2.annotate(f"({max_R:.1f}, {max_P:.1f})",
                     xy=(max_R, max_P),
                     xytext=(-35, 10),
                     textcoords='offset points',
                     fontsize=10, color='crimson')
                     
        ax2.set_title(f"P-R Analysis: battery {battery_type}", fontsize=11, fontweight='bold')
        ax2.set_xlabel("External Resistance R (Ω)", fontsize=10)
        ax2.set_ylabel("Power P (W)", fontsize=10)
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)

        st.pyplot(fig2)
        st.success("🎉 實驗分析完成！請結合上下兩張圖表回答學習單上的問題吧！")

else:
    st.info("👈 請在左側調整好參數後，點擊 **「🚀 開始執行實驗」** 按鈕來同時展開 V-I 與 P-R 分析！")
