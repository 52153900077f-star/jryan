import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="理財系統", layout="wide")

st.title("💰 智慧理財系統")

if "data" not in st.session_state:
    st.session_state.data = []

# 側邊欄輸入
st.sidebar.header("新增紀錄")
amount = st.sidebar.number_input("金額", min_value=0)
category = st.sidebar.selectbox("類別", ["餐飲", "交通", "娛樂", "其他"])
type_ = st.sidebar.radio("類型", ["收入", "支出"])

if st.sidebar.button("新增"):
    st.session_state.data.append({
        "amount": amount,
        "category": category,
        "type": type_
    })

df = pd.DataFrame(st.session_state.data)

col1, col2 = st.columns(2)

if not df.empty:
    with col1:
        st.subheader("📋 收支資料")
        st.dataframe(df)

    income = df[df["type"]=="收入"]["amount"].sum()
    expense = df[df["type"]=="支出"]["amount"].sum()
    balance = income - expense

    with col2:
        st.subheader("💵 財務狀況")
        st.write(f"收入：{income}")
        st.write(f"支出：{expense}")
        st.write(f"餘額：{balance}")

    st.subheader("📊 支出分析")
    expense_df = df[df["type"]=="支出"]

    if not expense_df.empty:
        category_sum = expense_df.groupby("category")["amount"].sum()
        fig, ax = plt.subplots()
        ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
        st.pyplot(fig)

    st.subheader("📌 預算建議")
    if not expense_df.empty:
        total_expense = expense_df["amount"].sum()
        if "餐飲" in category_sum and category_sum["餐飲"] > total_expense * 0.4:
            st.warning("餐飲支出過高，建議減少外食")
        if expense > income:
            st.error("已超支，請控制支出")

    st.subheader("🛒 購物建議")
    if balance > 5000:
        st.success("可適度消費")
    elif balance > 0:
        st.info("建議控制開銷")
    else:
        st.error("不建議任何額外消費")

    st.download_button(
        label="下載CSV",
        data=df.to_csv(index=False),
        file_name="finance_data.csv",
        mime="text/csv"
    )

else:
    st.info("請先新增資料")
