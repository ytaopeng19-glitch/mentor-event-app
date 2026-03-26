import streamlit as st
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="导师有约活动报名系统", page_icon="📝", layout="centered")

# 初始化 session_state 用于在内存中临时存储报名数据
if 'registration_data' not in st.session_state:
    st.session_state['registration_data'] = []

# 页面头部信息
st.title("【导师有约】系列活动第十四期")
st.subheader("行业导师职场领航计划·企业直聘专场")

st.markdown("""
欢迎报名参加本次活动！
* **活动时间**：2026年3月29日 19:00 - 21:00
* **活动地点**：西教学楼3-104
* **面向对象**：农学院各年级有求职需求的学生
""")

st.divider()

# 构建报名表单
with st.form("registration_form"):
    st.write("### 请填写您的报名信息")
    
    # 基础信息
    student_name = st.text_input("姓名 *", placeholder="请输入您的真实姓名")
    contact_info = st.text_input("联系方式（手机号） *", placeholder="请输入您的手机号码")
    student_class = st.text_input("班级 *", placeholder="例如：2023级农学1班")
    
    # 学历与研究方向（条件显示）
    degree_level = st.selectbox(
        "当前学历级别 *",
        options=["请选择", "本科生", "硕士研究生", "博士研究生"]
    )
    
    # 如果是硕博，则显示研究方向
    research_direction = ""
    if degree_level in ["硕士研究生", "博士研究生"]:
        research_direction = st.text_input("研究方向 *", placeholder="请输入您的具体研究方向（如：土壤磷素转化、生物炭应用等）")
    
    # 提交按钮
    submitted = st.form_submit_button("提交报名")
    
    if submitted:
        # 表单验证
        if not student_name or not contact_info or not student_class or degree_level == "请选择":
            st.error("请完善所有带 * 的必填信息！")
        elif degree_level in ["硕士研究生", "博士研究生"] and not research_direction:
            st.error("研究生请务必填写研究方向！")
        else:
            # 记录数据
            new_entry = {
                "报名时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "姓名": student_name,
                "联系方式": contact_info,
                "班级": student_class,
                "学历": degree_level,
                "研究方向": research_direction if research_direction else "无"
            }
            st.session_state['registration_data'].append(new_entry)
            st.success(f"报名成功！期待在会场见到你，{student_name}同学。")

st.divider()

# 后台数据展示与导出（在实际应用中，这部分可设为管理员可见）
if st.session_state['registration_data']:
    st.write("### 已报名学生名单 (管理员视图)")
    df = pd.DataFrame(st.session_state['registration_data'])
    st.dataframe(df, use_container_width=True)
    
    # 提供CSV下载功能
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 导出报名名单 (CSV)",
        data=csv,
        file_name='导师有约_报名名单.csv',
        mime='text/csv',
    )