import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# 设置页面配置（增加页面宽度以便更好地展示表格）
st.set_page_config(page_title="导师有约活动报名系统", page_icon="📝", layout="centered")

# --- 初始化 Supabase 客户端 ---
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

# --- 管理员登录逻辑 ---
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

with st.sidebar:
    st.write("### 🔒 管理员登录")
    if not st.session_state['admin_logged_in']:
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            if username == "123" and password == "123":
                st.session_state['admin_logged_in'] = True
                st.success("登录成功！")
                st.rerun()
            else:
                st.error("用户名或密码错误！")
    else:
        st.success("已登录管理员账号")
        if st.button("退出登录"):
            st.session_state['admin_logged_in'] = False
            st.rerun()

# --- 前端展示：页面头部信息 ---
st.title("【导师有约】系列活动第十四期")
st.subheader("行业导师职场领航计划·企业直聘专场")

st.markdown("""
欢迎报名参加本次活动！
* **活动时间**：2026年3月29日 19:00 - 21:00 
* **活动地点**：西教学楼3-104 
* **特邀企业**：广东瑞丰生态环境科技股份有限公司及16家区域农资龙头企业
* **面向对象**：学院各年级有求职需求的学生
""")

st.divider()

# --- 新增：招聘岗位与企业信息展示区 ---
st.write("### 🔥 抢先看：本次直聘企业及高薪岗位")

# 1. 核心岗位高亮展示
st.info("""
**🌟 核心招聘岗位及优厚待遇：**
* 👨‍🔬 **智慧农业技术与设备研发**：年薪 15~20万
* 🌍 **农业技术推广区域经理**：年薪 15~20万
* 🧪 **产品研发经理** / **作物营养服务经理**：年薪 12~18万
* 💼 **管理培养生**：年薪 10~15万
* 📱 **新媒体运营专员**：年薪 8~12万
*(注：绝大部分岗位面向本、硕应届生；瑞丰公司新媒体等岗位接受博士应聘，薪资面谈)*
""")

# 2. 17家参会企业一览表 (使用 expander 折叠，避免页面过长)
with st.expander("点击查看完整 17 家参会企业及对应岗位分布", expanded=False):
    companies_data = [
        {"企业名称": "广东瑞丰生态环境科技股份有限公司", "招聘岗位": "管培生/区域经理/智慧农业研发/新媒体", "学历要求": "本/硕/博"},
        {"企业名称": "云南省通海红跃农资有限责任公司", "招聘岗位": "管培生/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "广西贺州市金田野农资有限公司", "招聘岗位": "管培生/区域经理/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "广西中桂农资有限公司", "招聘岗位": "产品研发/管培生", "学历要求": "本/硕"},
        {"企业名称": "广东珠海市悦之丰农业科技有限公司", "招聘岗位": "管培生/区域经理/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "广州市农家邦农业技术服务有限公司", "招聘岗位": "管培生/新媒体/作物营养/智慧农业研发", "学历要求": "本/硕"},
        {"企业名称": "广东江门市德稻农业种植专业合作社", "招聘岗位": "区域经理/管培生/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "广东茂名市绿鼎农资贸易有限公司", "招聘岗位": "管培生/区域经理", "学历要求": "本/硕"},
        {"企业名称": "山东奋泉农业科技有限公司", "招聘岗位": "管培生/区域经理/新媒体/作物营养/智慧农业研发", "学历要求": "本/硕"},
        {"企业名称": "江苏邳州市国之光农业科技有限公司", "招聘岗位": "管培生/区域经理/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "海南及时雨农业生产资料有限公司", "招聘岗位": "区域经理/产品研发", "学历要求": "本/硕"},
        {"企业名称": "河南省沃农喜肥业有限公司", "招聘岗位": "区域经理/新媒体/作物营养", "学历要求": "本/硕"},
        {"企业名称": "宁夏鼎茂源农业科技有限公司", "招聘岗位": "区域经理/新媒体/作物营养/智慧农业研发", "学历要求": "本/硕"},
        {"企业名称": "浙江台州市黄农农业科技有限公司", "招聘岗位": "管培生/区域经理", "学历要求": "本/硕"},
        {"企业名称": "浙江台州市黄岩八达农资有限公司", "招聘岗位": "区域经理/管培生", "学历要求": "本/硕"},
        {"企业名称": "福建漳州市龙鑫农资有限公司", "招聘岗位": "产品研发/区域经理/管培生", "学历要求": "本/硕"},
        {"企业名称": "四川雅安市新生泰农资有限公司", "招聘岗位": "区域经理/新媒体/作物营养", "学历要求": "本/硕"}
    ]
    st.dataframe(pd.DataFrame(companies_data), hide_index=True, use_container_width=True)

st.divider()

# --- 前端展示：构建报名表单 ---
with st.form("registration_form"):
    st.write("### 请填写您的报名信息")
    
    student_name = st.text_input("姓名 *", placeholder="请输入您的真实姓名")
    contact_info = st.text_input("联系方式（手机号） *", placeholder="请输入您的手机号码")
    student_class = st.text_input("班级 *", placeholder="例如：2023级农学1班")
    
    degree_level = st.selectbox(
        "当前学历级别 *",
        options=["请选择", "本科生", "硕士研究生", "博士研究生"]
    )
    
    research_direction = st.text_input("研究方向（硕博生必填）", placeholder="如：智慧农业、生物技术、植物保护等相关方向")
    
    # 结合上方的岗位信息，优化这里的 placeholder 提示
    interested_position = st.text_input("意向岗位 *", placeholder="请参考上方列表，如：管培生、区域经理、智慧农业研发等")
    
    submitted = st.form_submit_button("立即报名，锁定直聘名额")
    
    if submitted:
        if not student_name or not contact_info or not student_class or not interested_position or degree_level == "请选择":
            st.error("请完善所有带 * 的必填基础信息！")
        elif degree_level in ["硕士研究生", "博士研究生"] and not research_direction:
            st.error("研究生同学请务必填写您的研究方向！")
        else:
            new_entry = {
                "student_name": student_name,
                "contact_info": contact_info,
                "student_class": student_class,
                "degree_level": degree_level,
                "research_direction": research_direction if research_direction else "无",
                "interested_position": interested_position 
            }
            try:
                response = supabase.table("registrations").insert(new_entry).execute()
                st.success(f"报名成功！期待在会场见到你，{student_name}同学。")
            except Exception as e:
                st.error(f"报名失败，请稍后重试。错误信息：{e}")

# --- 后台数据管理视图 (仅管理员可见) ---
if st.session_state['admin_logged_in']:
    st.divider()
    st.write("### 🛠️ 后台数据管理 (管理员视图)")

    try:
        records = supabase.table("registrations").select("*").execute()
        data = records.data
        
        if data:
            df = pd.DataFrame(data)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('Asia/Shanghai').dt.strftime('%Y-%m-%d %H:%M:%S')
            
            df_display = df.rename(columns={
                "id": "序号",
                "created_at": "报名时间",
                "student_name": "姓名",
                "contact_info": "联系方式",
                "student_class": "班级",
                "degree_level": "学历",
                "research_direction": "研究方向",
                "interested_position": "意向岗位"
            })
            
            df_display = df_display[["序号", "报名时间", "姓名", "联系方式", "班级", "学历", "研究方向", "意向岗位"]]
            
            st.write("#### 📊 意向岗位热度统计")
            position_counts = df_display['意向岗位'].value_counts().reset_index()
            position_counts.columns = ['意向岗位', '报名人数']
            st.bar_chart(position_counts.set_index('意向岗位'))
            
            st.write("#### 📋 详细名单")
            st.dataframe(df_display, use_container_width=True)
            
            csv = df_display.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 导出名单给企业HR (CSV) ",
                data=csv,
                file_name='瑞丰公司企业直聘_报名名单.csv',
                mime='text/csv',
            )

            st.write("---")
            st.write("#### 🗑️ 删除错误信息")
            st.warning("请注意：数据删除后无法恢复，请谨慎操作。")
            
            delete_options = df.apply(lambda row: f"{row['id']} - {row['student_name']} ({row['contact_info']})", axis=1).tolist()
            selected_to_delete = st.selectbox("请选择要删除的学生记录：", ["请选择..."] + delete_options)
            
            if st.button("确认删除此记录"):
                if selected_to_delete != "请选择...":
                    target_id = int(selected_to_delete.split(" - ")[0])
                    try:
                        supabase.table("registrations").delete().eq("id", target_id).execute()
                        st.success(f"已成功删除记录：{selected_to_delete}")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"删除失败：{e}")
                else:
                    st.error("请先在下拉菜单中选择一条需要删除的记录。")
                    
        else:
            st.info("目前还没有同学报名。")
    except Exception as e:
        st.warning(f"数据拉取异常，请检查数据库配置。详情：{e}")
