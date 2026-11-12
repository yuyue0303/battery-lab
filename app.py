import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 設定頁面標題與寬度
st.set_page_config(page_title="電池物理與系統最佳化實驗室", layout="wide")

# ==================== 側邊欄導覽：頁面切換 ====================
st.sidebar.markdown("### 🧭 實驗室導覽")
page = st.sidebar.radio(
    "選擇實驗頁面", 
    ["🔬 第一頁：V-I 與 P-R 基礎探究", "⚡ 第二頁：電池串並聯與系統最佳化"]
)

st.sidebar.markdown("---")

# ==================== 第一頁：V-I 與 P-R 基礎探究 ====================
if page == "🔬 第一頁：V-I 與 P-R 基礎探究":
    st.title("🔋⚡ 單顆電池特性與阻抗匹配實驗室")

    # 🤖 量測幫手
    col_m1, col_m2 = st.columns([1, 18])
    with col_m1:
        st.markdown("### 🤖")
    with col_m2:
        st.markdown("**【量測小幫手】** 歡迎來到第一頁！請在左側設定好單顆電池的參數與外接電阻範圍，點擊執行來探索 V-I 線性關係與功率極值。")

    # 第一頁的側邊欄控制項
    st.sidebar.header("🎛️ 第一頁實驗參數")
    battery_type = st.sidebar.selectbox("電池型號選擇", ["A", "B"])

    st.sidebar.markdown("### 🔌 外接電阻選用範圍")
    start = st.sidebar.number_input("起始值 (Ω)", value=1.0, key="p1_start")
    end = st.sidebar.number_input("結束值 (Ω)", value=800.0, key="p1_end")
    sample_size = st.sidebar.slider("取樣數 (個)", min_value=20, max_value=500, value=200, step=10, key="p1_sample")

    run_p1 = st.sidebar.button("🚀 執行第一頁實驗", type="primary")

    if run_p1:
        with st.spinner('正在進行單顆電池測量與分析...'):
            if battery_type == "A":
                global_emf, global_r = 618, 565
            else:
                global_emf, global_r = 70, 37

            R_values = np.linspace(start, end, int(sample_size))
            I_values = global_emf / (global_r + R_values)
            VR_values = global_emf - I_values * global_r
            P_values = I_values * VR_values

            # 第一部分：V-I 圖
            st.subheader("🔍 第一部分：V-I 測量與內部特徵解密")
            p_fit = np.polyfit(I_values, VR_values, 1)
            trendline = p_fit[0] * I_values + p_fit[1]

            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.scatter(I_values, VR_values, label='Measured Data', color='dodgerblue', s=20)
            ax1.plot(I_values, trendline, label=f'Trendline: y = {p_fit[0]:.1f}x + {p_fit[1]:.1f}', color='darkorange', linewidth=1.5)
            ax1.set_xlabel("Current I (A)")
            ax1.set_ylabel("Voltage V (V)")
            ax1.legend(loc='upper right')
            ax1.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig1)

            st.markdown("---")

            # 第二部分：P-R 圖
            st.subheader("⚡ 第二部分：功率曲線與阻抗匹配 (R = r)")
            max_idx = np.argmax(P_values)
            max_P = P_values[max_idx]
            max_R = R_values[max_idx]

            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.set_ylim(0, max_P * 1.15)
            ax2.scatter(R_values, P_values, label='Data (R,P)', color='dodgerblue', s=20)
            ax2.scatter(max_R, max_P, color='crimson', s=30, zorder=5, label='Max Power')
            ax2.annotate(f"({max_R:.1f}Ω, {max_P:.1f}W)", xy=(max_R, max_P), xytext=(-35, 15), textcoords='offset points', fontsize=10, color='crimson', fontweight='bold')
            ax2.set_xlabel("External Resistance R (Ω)")
            ax2.set_ylabel("Power P (W)")
            ax2.legend()
            ax2.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig2)

            # 🔬 分析小幫手
            col_a1, col_a2 = st.columns([1, 18])
            with col_a1:
                st.markdown("### 📊")
            with col_a2:
                st.markdown(f"**【分析小幫手】** 分析完成！當外接電阻 $R = {max_R:.1f}\,\Omega$ 時達到最大功率。這剛好等於電池的內電阻 $r$ 喔！準備好時，可以切換到**第二頁**挑戰串並聯架構設計。")
    else:
        st.info("👈 請在左側設定好參數，並點擊 **「🚀 執行第一頁實驗」** 來檢視圖表。")


# ==================== 第二頁：電池串並聯與系統最佳化 ====================
elif page == "⚡ 第二頁：電池串並聯與系統最佳化":
    st.title("🔋⚡ 電池陣列架構與系統最佳化實驗室")

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
                * 計算得出的等效內電阻 $r_{eq} = $ **{eq_r:.2f} Ω**。
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
