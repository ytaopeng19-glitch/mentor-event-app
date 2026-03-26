import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 设置页面配置
st.set_page_config(page_title="导师有约活动报名系统", page_icon="📝", layout="centered")

# --- 初始化 Supabase 客户端 ---
# 这里会自动读取我们在 Streamlit 部署后台 Advanced settings -> Secrets 中配置的密钥
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("数据库连接失败，请确保已经在 Streamlit 后台配置了 Secrets。")
    st.stop()

# 页面头部信息
st.title("【导师有约】系列活动第十四期")
st.subheader("行业导师职场领航计划·企业直聘专场")

st.markdown("""
欢迎报名参加本次活动！
* **活动时间**：2026年3月29日 19:00 - 21:00 
* **活动地点**：西教学楼3-104 
* **特邀企业**：广东瑞丰生态环境科技有限公司及区域农资龙头企业
* **面向对象**：学院各年级有求职需求的学生
""")

st.divider()

# 构建报名表单
with st.form("registration_form"):
    st.write("### 请填写您的报名信息")
    
    # 基础信息
    student_name = st.text_input("姓名 *", placeholder="请输入您的真实姓名")
    contact_info = st.text_input("联系方式（手机号） *", placeholder="请输入您的手机号码")
    student_class = st.text_input("班级 *", placeholder="例如：2023级农学1班")
    
    # 学历与研究方向
    degree_level = st.selectbox(
        "当前学历级别 *",
        options=["请选择", "本科生", "硕士研究生", "博士研究生"]
    )
    
    # 因为 Streamlit 的 form 不支持在内部做太复杂的动态组件显隐，
    # 我们将研究方向设为选填，但在提交逻辑中进行强校验
    research_direction = st.text_input("研究方向（硕博生必填）", placeholder="如：智慧农业、生物技术、植物保护等相关方向")
    
    # 意向岗位（新增）
    interested_position = st.text_input("意向岗位 *", placeholder="例如：产品研发、技术支持、销售管培生等")
    
    # 提交按钮
    submitted = st.form_submit_button("提交报名")
    
    if submitted:
        # 表单验证逻辑
        if not student_name or not contact_info or not student_class or not interested_position or degree_level == "请选择":
            st.error("请完善所有带 * 的必填基础信息！")
        elif degree_level in ["硕士研究生", "博士研究生"] and not research_direction:
            st.error("研究生同学请务必填写您的研究方向！")
        else:
            # 准备写入数据库的数据，字典的 Key 必须与 Supabase 表中的列名严格对应
            new_entry = {
                "student_name": student_name,
                "contact_info": contact_info,
                "student_class": student_class,
                "degree_level": degree_level,
                "research_direction": research_direction if research_direction else "无",
                "interested_position": interested_position # 新增的数据列
            }
            
            # 尝试写入 Supabase
            try:
                # .execute() 发送插入请求
                response = supabase.table("registrations").insert(new_entry).execute()
                st.success(f"报名成功！期待在会场见到你，{student_name}同学。")
            except Exception as e:
                st.error(f"报名失败，请稍后重试。错误信息：{e}")

st.divider()

# --- 后台数据展示与导出 ---
# 实际给学生用的版本中，您可以将这部分代码用 st.expander 藏起来，或者加个简单的密码校验
st.write("### 已报名学生名单及统计 (辅导员/管理员视图)")

try:
    # 从 Supabase 获取所有报名数据
    records = supabase.table("registrations").select("*").execute()
    data = records.data
    
    if data:
        # 将 JSON 数据转为 Pandas DataFrame 处理
        df = pd.DataFrame(data)
        
        # 整理列名，替换为中文
        df = df.rename(columns={
            "created_at": "报名时间",
            "student_name": "姓名",
            "contact_info": "联系方式",
            "student_class": "班级",
            "degree_level": "学历",
            "research_direction": "研究方向",
            "interested_position": "意向岗位"
        })
        
        # 挑选需要的列并排序展示
        df = df[["报名时间", "姓名", "联系方式", "班级", "学历", "研究方向", "意向岗位"]]
        
        # 格式化时间（Supabase默认返回的是UTC时间，将其转为本地格式更易读）
        df['报名时间'] = pd.to_datetime(df['报名时间']).dt.tz_convert('Asia/Shanghai').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # --- 新增：意向岗位统计图表 ---
        st.write("#### 📊 意向岗位热度统计")
        # 统计各个意向岗位的数量
        position_counts = df['意向岗位'].value_counts().reset_index()
        position_counts.columns = ['意向岗位', '报名人数']
        
        # 显示柱状图
        st.bar_chart(position_counts.set_index('意向岗位'))
        
        st.write("#### 📋 详细名单")
        st.dataframe(df, use_container_width=True)
        
        # 生成 CSV 下载按钮 
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 导出名单给企业HR (CSV) ",
            data=csv,
            file_name='瑞丰公司企业直聘_报名名单.csv',
            mime='text/csv',
        )
    else:
        st.info("目前还没有同学报名。")
except Exception as e:
    st.warning("暂无数据或数据库配置尚未完成，部署完成后将正常显示。")
