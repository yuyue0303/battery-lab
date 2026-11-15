import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 設定頁面標題與寬度
st.set_page_config(page_title="線上虛擬實驗室", layout="wide")

# ==================== 側邊欄導覽：頁面切換 ====================
st.sidebar.markdown('<h3 style="font-size: 20px; margin-bottom: 0px;">🧭 實驗室導覽</h3>', unsafe_allow_html=True)

# 在選項最前面多加一個「請選擇」的選項
page = st.sidebar.radio(
    "選擇頁面", 
    ["🏠首頁", "➊ 探究未知電池", "➋ 串並聯與最大功率"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

if page == "🏠首頁":
    # 預設首頁畫面
    st.title("歡迎來到愉悅的線上虛擬實驗室!")
    st.markdown("---")
    
    # 你指定的提示訊息
    st.info("👋 **請於左側側邊欄選擇頁面**")
    
# ==================== 第一頁：V-I 與 P-R 基礎探究 ====================
elif page == "➊ 探究未知電池":
    st.title("探究未知電池🔋")
    st.info("🦾 **量測小幫手** 將為您測量電壓及電流！\n請於左側側邊欄設定實驗參數，設定完成後點擊「執行量測」。")

    # 側邊欄控制項（統一控制兩部分的參數）
    st.sidebar.header("🎛️ 參數設定")
    battery_type = st.sidebar.selectbox("**電池類型**", ["A", "B", "C"])
    st.sidebar.markdown('<span style="font-size: 14px;">**外接電阻選用範圍**</span>', unsafe_allow_html=True)
    start = st.sidebar.number_input("起始值(Ω)", step=10)
    end = st.sidebar.number_input("結束值(Ω)", step=10)
    sample_size = st.sidebar.slider("**取樣數**", min_value=50, max_value=600, value=300, step=5)
    st.sidebar.markdown("---")
    run_p1 = st.sidebar.button("執行量測", type="primary")


    if run_p1:
        with st.spinner('正在進行測量與分析...'):
            if battery_type == "A":
                global_emf, global_r = 105, 75
            if battery_type == "B":
                global_emf, global_r = 818, 365
            else:
                global_emf, global_r = 70, 37

            R_values = np.linspace(start, end, int(sample_size))
            I_values = global_emf / (global_r + R_values)
            VR_values = global_emf - I_values * global_r
            P_values = I_values * VR_values

            # ==================== 第一部分：V-I 圖 ====================
            st.subheader("🔍 內部解密")
            st.success("💻 **分析小幫手** 已將電壓與電流量測結果畫成圖表，輸出一張 V-I 圖，包含擬合方程式。")

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

            st.write("💡當外接電阻多大時，這顆電池有最大功率?")
        
            st.markdown("---")

             # ==================== 第二部分：P-R 功率曲線圖 ====================
            st.subheader("📈 功率曲線與阻抗匹配")
            st.success("💻 **分析小幫手** 使用了量測出的電壓與電流計算出功率，以外接電阻值為橫軸，畫出 P-R 圖，並標示出最大功率點...")
            
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
            st.success("請結合上下兩張圖表回答學習單上的問題吧！")

# ==================== 第二頁：電池串並聯與系統最佳化 ====================
elif page == "➋ 串並聯與最大功率":
    st.title("串並聯與最大功率⚡")

    # 🤖 陣列量測幫手
    col_m1, col_m2 = st.columns([1, 18])
    with col_m1:
        st.markdown("### 🦾")
    with col_m2:
        st.markdown("**【陣列量測幫手】** 歡迎來到進階工程挑戰！請在左側調整**串聯個數 ($n_s$)** 與 **並聯個數 ($n_p$)**，找出能夠完美匹配外接負載、榨出最大功率的組合！")

    # 第二頁的側邊欄控制項
    st.sidebar.header("🎛️ 第二頁陣列參數設定")
    battery_type_p2 = st.sidebar.selectbox("單顆電池型號", ["A", "B"], key="p2_bat")

    st.sidebar.markdown("### 🔗 電池陣列架構 (串並聯)")
    ns = st.sidebar.number_input("串聯個數 ($n_s$)", min_value=1, max_value=20, value=4, step=1)
    np_parallel = st.sidebar.number_input("並聯分支數 ($n_p$)", min_value=1, max_value=20, value=2, step=1)

    st.sidebar.markdown("### 🔌 外接電阻選用範圍")
    start_p2 = st.sidebar.number_input("起始值 (Ω)", value=1.0, key="p2_start")
    end_p2 = st.sidebar.number_input("結束值 (Ω)", value=500.0, key="p2_end")
    sample_size_p2 = st.sidebar.slider("取樣數 (個)", min_value=20, max_value=500, value=200, step=10, key="p2_sample")

    run_p2 = st.sidebar.button("🚀 執行陣列實驗與分析", type="primary")

    if run_p2:
        with st.spinner('正在計算陣列等效電路與功率曲線中...'):
            # 單顆基準參數
            if battery_type_p2 == "A":
                single_emf, single_r = 12.0, 5.0  
            else:
                single_emf, single_r = 9.0, 2.5   

            # 陣列等效計算：r_eq = (ns / np) * r
            eq_emf = ns * single_emf
            eq_r = (ns / np_parallel) * single_r

            R_values = np.linspace(start_p2, end_p2, int(sample_size_p2))
            I_values = eq_emf / (eq_r + R_values)
            VR_values = eq_emf - I_values * eq_r
            P_values = I_values * VR_values

            max_idx = np.argmax(P_values)
            max_P = P_values[max_idx]
            max_R = R_values[max_idx]

            # 即時摘要面板
            st.markdown("### 📊 本次陣列配置摘要")
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("總電動勢 ($\mathcal{E}_{eq}$)", f"{eq_emf:.1f} V")
            m_col2.metric("等效內電阻 ($r_{eq}$)", f"{eq_r:.2f} Ω")
            m_col3.metric("最佳外接電阻 ($R$)", f"{max_R:.1f} Ω")
            m_col4.metric("最大輸出功率 ($P_{max}$)", f"{max_P:.2f} W")

            st.markdown("---")

            # 繪製圖表
            st.subheader("⚡ 陣列功率對外接電阻曲線 (P-R)")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.set_ylim(0, max_P * 1.15)
            ax2.scatter(R_values, P_values, label='Array Power Curve', color='dodgerblue', s=15)
            ax2.scatter(max_R, max_P, color='crimson', s=30, zorder=5, label=f'Peak P: {max_P:.1f}W')
            ax2.annotate(f"({max_R:.1f}Ω, {max_P:.1f}W)", xy=(max_R, max_P), xytext=(-40, 15), textcoords='offset points', fontsize=10, color='crimson', fontweight='bold')
            ax2.set_xlabel("External Resistance R (Ω)")
            ax2.set_ylabel("Power P (W)")
            ax2.legend()
            ax2.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig2)

            # 🔬 分析小幫手回饋
            col_a1, col_a2 = st.columns([1, 18])
            with col_a1:
                st.markdown("### 📈")
            with col_a2:
                st.markdown(f"""
                **【分析小幫手報告】** 
                * 當前陣列組合：**{ns} 串 {np_parallel} 並** 
                st.markdown(f"* 計算得出的等效內電阻 $r_{eq} = $ <b>{eq_r:.2f} Ω</b>", unsafe_allow_html=True)
                * **思考點**：當前架構的 $r_{eq}$ 是否完美匹配你的外接負載？試著微調左側的 $n_s$ 和 $n_p$，看看能不能把最大功率往上推升！
                """)
    else:
        st.info("👈 請在左側設定好串並聯個數，並點擊 **「🚀 執行陣列實驗與分析」** 來展開探究！")

    # 小組討論引導區
    st.markdown("---")
    st.subheader("🗣️ 小組分享與討論指引")
    st.markdown("""
    完成數據搜尋後，各組可以準備分享以下幾個問題：
    1. **最佳組合策略**：你們組試了哪幾種 $n_s$ 與 $n_p$ 組合？哪一組的輸出功率最高？
    2. **阻抗匹配驗證**：你們找到的最高功率組合，其等效內電阻 $r_{eq}$ 是否真的等於外接電阻 $R$？
    3. **工程取捨**：當電池總數有限制時，為了達到特定負載的最大功率，串聯跟並聯該如何分配？
    """)
