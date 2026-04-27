import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="智慧理財系統", layout="wide")

# ====== 標題 ======
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>💰 智慧理財與預算管理系統</h1>
""", unsafe_allow_html=True)

# ====== 初始化 ======
if "data" not in st.session_state:
    st.session_state.data = []

if "budget" not in st.session_state:
    st.session_state.budget = 20000

# ====== 側邊欄 ======
st.sidebar.header("📥 新增收支")
amount = st.sidebar.number_input("金額", min_value=0)
category = st.sidebar.selectbox("類別", ["餐飲", "交通", "娛樂", "其他"])
type_ = st.sidebar.radio("類型", ["收入", "支出"])

if st.sidebar.button("➕ 新增紀錄"):
    st.session_state.data.append({
        "amount": amount,
        "category": category,
        "type": type_
    })

# ====== 預算設定 ======
st.sidebar.header("💡 每月預算設定")
st.session_state.budget = st.sidebar.number_input("預算金額", value=st.session_state.budget)

# ====== DataFrame ======
df = pd.DataFrame(st.session_state.data)

# ====== 主畫面 ======
col1, col2, col3 = st.columns(3)

if not df.empty:
    income = df[df["type"]=="收入"]["amount"].sum()
    expense = df[df["type"]=="支出"]["amount"].sum()
    balance = income - expense

    # ====== 指標卡 ======
    col1.metric("💵 收入", income)
    col2.metric("💸 支出", expense)
    col3.metric("💰 餘額", balance)

    st.divider()

    # ====== 表格 ======
    st.subheader("📋 收支紀錄")
    st.dataframe(df, use_container_width=True)

    # ====== 圖表 ======
    st.subheader("📊 支出分析")
    expense_df = df[df["type"]=="支出"]

    if not expense_df.empty:
        category_sum = expense_df.groupby("category")["amount"].sum()
        fig, ax = plt.subplots()
        ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
        st.pyplot(fig)

    st.divider()

    # ====== 預算分析 ======
    st.subheader("📌 預算分析")

    remaining_budget = st.session_state.budget - expense
    daily_budget = remaining_budget / 30

    st.write(f"📊 本月預算：{st.session_state.budget}")
    st.write(f"📉 剩餘預算：{remaining_budget}")
    st.write(f"📅 每日可花：約 {round(daily_budget,2)}")

    if expense > st.session_state.budget:
        st.error("🚨 已超過預算！請立即控制支出")
    elif expense > st.session_state.budget * 0.8:
        st.warning("⚠️ 已使用 80% 預算，請小心消費")
    else:
        st.success("👍 預算控制良好")

    st.info("請先新增收支資料 👈")
