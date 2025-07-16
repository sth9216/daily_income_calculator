import streamlit as st

def compute_cost(points_needed, base_cost, Y, boost_120_points, boost_50_points):
    paid_points = max(points_needed - Y, 0)
    use_120 = min(paid_points, boost_120_points)
    remaining = paid_points - use_120
    use_50 = min(remaining, boost_50_points)
    no_boost = remaining - use_50
    total_cost = (
        use_120 * (base_cost / 2.2) +
        use_50 * (base_cost / 1.5) +
        no_boost * base_cost
    )
    return paid_points, total_cost, use_120, use_50, no_boost

st.title("每日收益模式计算器（网页版）")

meirishouyi = st.number_input("每日收益（元）", value=1200.0)
meifenzhongdingjia = st.number_input("每分钟定价（元）", value=3.5)
jinpai_zhou_jifen = st.number_input("金牌周积分", value=4500.0)
yinpai_zhou_jifen = st.number_input("银牌周积分", value=2400.0)

use_boost_120 = st.radio("是否使用120%加成", ["Y", "N"], index=1)
boost_120_points = st.number_input("120%加成积分数 (0-198)", min_value=0, max_value=198, value=0) if use_boost_120 == 'Y' else 0

use_boost_50 = st.radio("是否使用50%加成", ["Y", "N"], index=1)
boost_50_points = st.number_input("50%加成积分数 (0-405)", min_value=0, max_value=405, value=0) if use_boost_50 == 'Y' else 0

pay_for_boost = st.radio("是否自费购买加成", ["Y", "N"], index=1)

if st.button("开始计算"):
    # 积分计算
    A_points = jinpai_zhou_jifen / 7
    B_points = yinpai_zhou_jifen / 7

    A_income = meirishouyi
    B_income = meirishouyi / 0.75 * 0.7

    A_cost_per_point = 0.25
    B_cost_per_point = 0.3

    Y = meirishouyi / (meifenzhongdingjia * 0.75)

    A_paid, A_total, A_120, A_50, A_no = compute_cost(A_points, A_cost_per_point, Y, boost_120_points, boost_50_points)
    B_paid, B_total, B_120, B_50, B_no = compute_cost(B_points, B_cost_per_point, Y, boost_120_points, boost_50_points)

    boost_cost_A = 0
    boost_cost_B = 0
    if pay_for_boost == 'Y':
        if A_120 > 0:
            boost_cost_A += 28.28
        if A_50 > 0:
            boost_cost_A += 4 if A_50 <= 135 else 8 if A_50 <= 270 else 12
        if B_120 > 0:
            boost_cost_B += 28.28
        if B_50 > 0:
            boost_cost_B += 4 if B_50 <= 135 else 8 if B_50 <= 270 else 12

    A_virtual = (A_120 / 2.2 + A_50 / 1.5 + A_no) * 0.75
    B_virtual = (B_120 / 2.2 + B_50 / 1.5 + B_no) * 0.7

    A_net = A_income - A_total - A_virtual - boost_cost_A
    B_net = B_income - B_total - B_virtual - boost_cost_B

    A_video_time = A_net / meifenzhongdingjia if meifenzhongdingjia else 0
    B_video_time = B_net / meifenzhongdingjia if meifenzhongdingjia else 0

    st.markdown(f"""
    ### 金牌：
    - 付费积分: **{A_paid:.2f}**（120%: {A_120}, 50%: {A_50}, 无加成: {A_no}）
    - 购买加成成本: **{boost_cost_A:.2f} 元**
    - 净收益: **{A_net:.2f} 元**

    ### 银牌：
    - 付费积分: **{B_paid:.2f}**（120%: {B_120}, 50%: {B_50}, 无加成: {B_no}）
    - 购买加成成本: **{boost_cost_B:.2f} 元**
    - 净收益: **{B_net:.2f} 元**
    """)

    if A_net > B_net:
        st.success("✅ 推荐金牌")
    elif B_net > A_net:
        st.success("✅ 推荐银牌")
    else:
        st.info("✅ 两种模式净收益相同")
