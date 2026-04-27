import streamlit as st
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

    # ====== 類別分析 ======
    if not expense_df.empty:
        total_expense = expense_df["amount"].sum()
        if "餐飲" in category_sum and category_sum["餐飲"] > total_expense * 0.4:
            st.warning("🍔 餐飲支出偏高，建議減少外食")

    st.divider()

    # ====== 購物建議 ======
    st.subheader("🛒 智慧購物建議")

    if remaining_budget > 8000:
        st.success("🎉 預算充足，可以適度犒賞自己！")
    elif remaining_budget > 3000:
        st.info("🙂 建議理性消費")
    elif remaining_budget > 0:
        st.warning("⚠️ 建議暫停非必要購物")
    else:
        st.error("❌ 不建議任何消費")

    # ====== 匯出 ======
    st.download_button(
        label="📥 下載CSV",
        data=df.to_csv(index=False),
        file_name="finance_data.csv",
        mime="text/csv"
    )

else:
    st.info("請先新增收支資料 👈")
