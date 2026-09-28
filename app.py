import matplotlib.pyplot as plt
import streamlit as st

st.title("🍽️ 외식업 손익분기점(BEP) 계산기")

# 웹 화면 입력창 만들기
store_name = st.text_input("가게 이름", "우리동네 맛집")
fixed_costs = st.number_input("월 고정비 (원)", value=2000000, step=100000)
menu_name = st.text_input("대표 메뉴명", "제육덮밥")
price = st.number_input("판매 단가 (원)", value=10000, step=500)
variable_cost = st.number_input("1그릇당 변동비 (원)", value=4000, step=500)

if st.button("손익분기점 계산하기"):
    unit_margin = price - variable_cost
    if unit_margin <= 0:
        st.error("판매 단가가 변동비보다 작거나 같습니다. 가격을 인상하세요!")
    else:
        bep_qty = fixed_costs / unit_margin
        bep_revenue = bep_qty * price
        daily_qty = bep_qty / 25

        st.success(f"[{store_name}] 분석 결과")
        st.write(f"• 1그릇당 공헌이익: **{unit_margin:,.0f}원**")
        st.write(f"• 월 손익분기점 매출: **{bep_revenue:,.0f}원**")
        st.write(f"• 월 손익분기점 판매량: **{bep_qty:,.1f}그릇**")
        st.write(
            f"• 👉 **일일 목표 판매량(25일 기준): 약 {int(daily_qty)+1}그릇/일**"
        )

        # 그래프 생성 및 웹 표시
        max_q = int(bep_qty * 2)
        q_list = list(range(0, max_q + 1, max(1, max_q // 50)))
        rev_list = [q * price for q in q_list]
        cost_list = [fixed_costs + (q * variable_cost) for q in q_list]

        fig, ax = plt.subplots()
        ax.plot(q_list, rev_list, label='Total Revenue')
        ax.plot(q_list, cost_list, label='Total Cost')
        ax.axhline(fixed_costs, color='gray', linestyle='--', label='Fixed Cost')
        ax.plot(bep_qty, bep_revenue, 'go', label='BEP')
        ax.set_xlabel('Sales Quantity')
        ax.set_ylabel('Amount (KRW)')
        ax.legend()
        st.pyplot(fig)
