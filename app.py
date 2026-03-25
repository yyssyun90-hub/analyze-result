import sys
import traceback

# 调试信息
print("=== Starting app ===")
print(f"Python version: {sys.version}")

# 尝试导入并捕获错误
try:
    import streamlit as st
    print("✓ streamlit imported")
except Exception as e:
    print(f"✗ streamlit import failed: {e}")
    raise

try:
    import pandas as pd
    print("✓ pandas imported")
except Exception as e:
    print(f"✗ pandas import failed: {e}")
    raise

try:
    import plotly.express as px
    import plotly.graph_objects as go
    print("✓ plotly imported")
except Exception as e:
    print(f"✗ plotly import failed: {e}")
    traceback.print_exc()
    st.error(f"plotly 导入失败: {e}")
    st.stop()

try:
    from supabase import create_client
    print("✓ supabase imported")
except Exception as e:
    print(f"✗ supabase import failed: {e}")
    # supabase 不是必需的，如果没有就设为 None
    create_client = None

import numpy as np
from datetime import datetime
import io
import os

print("=== All imports successful ===")

# ========== 页面配置 ==========
st.set_page_config(
    page_title="Sistem Analisis Akademik | 成绩分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 多语言配置 ==========
TEXTS = {
    "zh": {
        "app_title": "班级成绩分析系统",
        "login": "班主任登录",
        "password": "密码",
        "login_btn": "登录",
        "logout": "退出登录",
        "select_class": "选择班级",
        "wrong_password": "密码错误！",
        "student_performance": "📊 学生个人成绩",
        "class_performance": "📈 班级成绩分析",
        "data_management": "📁 成绩管理",
        "help": "ℹ️ 帮助",
        "core_only": "仅主科",
        "all_subjects": "全部科目",
        "subject_display": "科目显示",
        "select_student": "选择学生",
        "select_exams": "选择要对比的考试",
        "chart_type": "选择图表类型",
        "line_chart": "折线图",
        "bar_chart": "柱状图",
        "heatmap": "热力图",
        "stacked_bar": "堆叠图",
        "radar_chart": "雷达图",
        "box_plot": "箱线图",
        "generate_report": "生成报告",
        "download_report": "下载报告",
        "no_data": "暂无数据",
        "no_students": "请先在「成绩管理」中导入学生名单",
        "no_exams": "暂无考试成绩数据，请先在「成绩管理」中导入成绩",
        "import_students": "导入学生名单",
        "import_grades": "导入考试成绩",
        "exam_name": "考试名称",
        "exam_date": "考试日期",
        "file_upload": "上传文件",
        "success": "成功！",
        "error": "错误",
        "student_no": "学号",
        "student_name": "姓名",
        "rank": "排名",
        "total_score": "总分",
        "average": "平均分",
        "strength": "优势科目",
        "weakness": "需要加强",
        "suggestions": "学习建议",
        "history_exams": "历史考试",
        "delete": "删除",
        "view": "查看",
        "class_overview": "班级概况",
        "student_count": "学生人数",
        "class_avg": "全科平均分",
        "highest_total": "最高总分",
        "pass_rate": "及格率",
        "score_distribution": "成绩分布",
        "ranking_table": "成绩排名",
        "generate_advice": "生成学习建议",
        "export_report": "导出报告"
    },
    "ms": {
        "app_title": "Sistem Analisis Prestasi Kelas",
        "login": "Log Masuk Guru Kelas",
        "password": "Kata Laluan",
        "login_btn": "Log Masuk",
        "logout": "Log Keluar",
        "select_class": "Pilih Kelas",
        "wrong_password": "Kata laluan salah!",
        "student_performance": "📊 Analisis Pelajar Individu",
        "class_performance": "📈 Analisis Prestasi Kelas",
        "data_management": "📁 Pengurusan Data",
        "help": "ℹ️ Bantuan",
        "core_only": "Subjek Teras Sahaja",
        "all_subjects": "Semua Subjek",
        "subject_display": "Paparan Subjek",
        "select_student": "Pilih Pelajar",
        "select_exams": "Pilih Peperiksaan",
        "chart_type": "Pilih Jenis Carta",
        "line_chart": "Carta Garisan",
        "bar_chart": "Carta Palang",
        "heatmap": "Peta Haba",
        "stacked_bar": "Carta Bertindan",
        "radar_chart": "Carta Radar",
        "box_plot": "Carta Kotak",
        "generate_report": "Hasilkan Laporan",
        "download_report": "Muat Turun Laporan",
        "no_data": "Tiada data",
        "no_students": "Sila import senarai pelajar di 'Pengurusan Data'",
        "no_exams": "Tiada data peperiksaan, sila import di 'Pengurusan Data'",
        "import_students": "Import Senarai Pelajar",
        "import_grades": "Import Markah Peperiksaan",
        "exam_name": "Nama Peperiksaan",
        "exam_date": "Tarikh Peperiksaan",
        "file_upload": "Muat Naik Fail",
        "success": "Berjaya!",
        "error": "Ralat",
        "student_no": "No. Pelajar",
        "student_name": "Nama",
        "rank": "Kedudukan",
        "total_score": "Jumlah Markah",
        "average": "Purata",
        "strength": "Subjek Kekuatan",
        "weakness": "Perlu Diperbaiki",
        "suggestions": "Cadangan",
        "history_exams": "Peperiksaan Lepas",
        "delete": "Padam",
        "view": "Lihat",
        "class_overview": "Gambaran Kelas",
        "student_count": "Bilangan Pelajar",
        "class_avg": "Purata Keseluruhan",
        "highest_total": "Jumlah Tertinggi",
        "pass_rate": "Kadar Lulus",
        "score_distribution": "Taburan Markah",
        "ranking_table": "Kedudukan Markah",
        "generate_advice": "Hasilkan Cadangan",
        "export_report": "Eksport Laporan"
    }
}

# ========== 科目配置 ==========
SUBJECTS_CONFIG = {
    "low_primary": {
        "core": [
            {"code": "BC", "name_zh": "华文", "name_ms": "Bahasa Cina"},
            {"code": "BM", "name_zh": "国文", "name_ms": "Bahasa Melayu"},
            {"code": "BI", "name_zh": "英文", "name_ms": "Bahasa Inggeris"},
            {"code": "MT", "name_zh": "数学", "name_ms": "Matematik"},
            {"code": "SN", "name_zh": "科学", "name_ms": "Sains"}
        ],
        "elective": [
            {"code": "PJPK", "name_zh": "体育与体健", "name_ms": "PJPK"},
            {"code": "PSV", "name_zh": "美术", "name_ms": "PSV"},
            {"code": "MUZIK", "name_zh": "音乐", "name_ms": "Muzik"},
            {"code": "MORAL", "name_zh": "道德", "name_ms": "Moral"}
        ]
    },
    "high_primary": {
        "core": [
            {"code": "BC", "name_zh": "华文", "name_ms": "Bahasa Cina"},
            {"code": "BM", "name_zh": "国文", "name_ms": "Bahasa Melayu"},
            {"code": "BI", "name_zh": "英文", "name_ms": "Bahasa Inggeris"},
            {"code": "MT", "name_zh": "数学", "name_ms": "Matematik"},
            {"code": "SN", "name_zh": "科学", "name_ms": "Sains"},
            {"code": "SEJ", "name_zh": "历史", "name_ms": "Sejarah"}
        ],
        "elective": [
            {"code": "PJPK", "name_zh": "体育与体健", "name_ms": "PJPK"},
            {"code": "PSV", "name_zh": "美术", "name_ms": "PSV"},
            {"code": "MUZIK", "name_zh": "音乐", "name_ms": "Muzik"},
            {"code": "MORAL", "name_zh": "道德", "name_ms": "Moral"},
            {"code": "RBT", "name_zh": "技术与工艺", "name_ms": "RBT"}
        ]
    }
}

# ========== 初始化 Session State ==========
def init_session_state():
    """初始化 session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "language" not in st.session_state:
        st.session_state.language = "zh"
    if "class_id" not in st.session_state:
        st.session_state.class_id = None
    if "class_name_zh" not in st.session_state:
        st.session_state.class_name_zh = None
    if "class_name_ms" not in st.session_state:
        st.session_state.class_name_ms = None
    if "teacher_zh" not in st.session_state:
        st.session_state.teacher_zh = None
    if "teacher_ms" not in st.session_state:
        st.session_state.teacher_ms = None
    if "level" not in st.session_state:
        st.session_state.level = None
    if "grade" not in st.session_state:
        st.session_state.grade = None

# ========== Supabase 连接 ==========
@st.cache_resource
def init_supabase():
    """初始化 Supabase 客户端（使用缓存）"""
    try:
        supabase_url = st.secrets.get("SUPABASE_URL", "")
        supabase_key = st.secrets.get("SUPABASE_KEY", "")
        
        if not supabase_url or not supabase_key:
            st.warning("⚠️ 请配置 Supabase 连接信息\n\n在 Streamlit Cloud 的 Secrets 中添加：\nSUPABASE_URL\nSUPABASE_KEY")
            return None
        
        if create_client is None:
            st.error("supabase 包未安装")
            return None
        
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"Supabase 连接失败: {e}")
        return None

# ========== 数据操作函数 ==========
def get_classes(supabase):
    """获取所有班级"""
    try:
        response = supabase.table("classes").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"获取班级失败: {e}")
        return []

def get_students(supabase, class_id):
    """获取班级学生列表"""
    try:
        response = supabase.table("students").select("*").eq("class_id", class_id).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"获取学生失败: {e}")
        return pd.DataFrame()

def add_students(supabase, class_id, students_df):
    """批量添加学生"""
    try:
        records = []
        for _, row in students_df.iterrows():
            records.append({
                "class_id": class_id,
                "student_no": str(row["学号"]),
                "name_zh": row["姓名"],
                "name_ms": row.get("姓名_马来文", row["姓名"])
            })
        
        response = supabase.table("students").insert(records).execute()
        return True
    except Exception as e:
        st.error(f"添加学生失败: {e}")
        return False

def get_exams(supabase, class_id):
    """获取考试列表"""
    try:
        response = supabase.table("exams").select("*").eq("class_id", class_id).order("exam_date").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"获取考试列表失败: {e}")
        return []

def add_exam(supabase, class_id, exam_name, exam_date):
    """添加考试"""
    try:
        response = supabase.table("exams").insert({
            "class_id": class_id,
            "exam_name": exam_name,
            "exam_date": exam_date.isoformat(),
            "academic_year": str(datetime.now().year)
        }).execute()
        return response.data[0]["id"] if response.data else None
    except Exception as e:
        st.error(f"添加考试失败: {e}")
        return None

def get_grades(supabase, exam_id):
    """获取考试成绩"""
    try:
        response = supabase.table("grades").select("*, students(*)").eq("exam_id", exam_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"获取成绩失败: {e}")
        return []

def save_grades(supabase, exam_id, grades_df):
    """保存考试成绩"""
    try:
        supabase.table("grades").delete().eq("exam_id", exam_id).execute()
        
        records = []
        for _, row in grades_df.iterrows():
            scores = {}
            for col in grades_df.columns:
                if col not in ["学号", "姓名", "student_id"]:
                    try:
                        scores[col] = float(row[col]) if pd.notna(row[col]) else None
                    except:
                        scores[col] = None
            
            records.append({
                "exam_id": exam_id,
                "student_id": row["student_id"],
                "scores": scores
            })
        
        if records:
            supabase.table("grades").insert(records).execute()
        return True
    except Exception as e:
        st.error(f"保存成绩失败: {e}")
        return False

def delete_exam(supabase, exam_id):
    """删除考试"""
    try:
        supabase.table("grades").delete().eq("exam_id", exam_id).execute()
        supabase.table("exams").delete().eq("id", exam_id).execute()
        return True
    except Exception as e:
        st.error(f"删除考试失败: {e}")
        return False

# ========== 图表生成函数 ==========
def create_line_chart(student_data, exams, subjects, lang):
    """折线图"""
    fig = go.Figure()
    
    for subject in subjects:
        code = subject["code"]
        if code in student_data.columns:
            scores = student_data[code].tolist()
            name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
            fig.add_trace(go.Scatter(
                x=exams,
                y=scores,
                mode='lines+markers',
                name=name,
                line=dict(width=2),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title="成绩趋势图" if lang == "zh" else "Carta Trend Prestasi",
        xaxis_title="考试" if lang == "zh" else "Peperiksaan",
        yaxis_title="分数" if lang == "zh" else "Markah",
        hovermode='x unified',
        height=500
    )
    return fig

def create_bar_chart(student_data, exams, subjects, lang):
    """柱状图"""
    fig = go.Figure()
    
    for exam in exams:
        exam_data = student_data[student_data["考试"] == exam]
        if not exam_data.empty:
            scores = []
            names = []
            for subject in subjects:
                code = subject["code"]
                if code in exam_data.columns:
                    scores.append(exam_data[code].iloc[0])
                    names.append(subject["name_zh"] if lang == "zh" else subject["name_ms"])
            
            fig.add_trace(go.Bar(
                name=exam,
                x=names,
                y=scores,
                text=scores,
                textposition='auto'
            ))
    
    fig.update_layout(
        title="各科成绩对比" if lang == "zh" else "Perbandingan Markah Subjek",
        xaxis_title="科目" if lang == "zh" else "Subjek",
        yaxis_title="分数" if lang == "zh" else "Markah",
        barmode='group',
        height=500
    )
    return fig

def create_radar_chart(student_scores, class_avg, subjects, lang):
    """雷达图"""
    student_values = []
    class_values = []
    labels = []
    
    for subject in subjects:
        code = subject["code"]
        if code in student_scores and student_scores[code]:
            try:
                student_values.append(float(student_scores[code]))
                class_values.append(float(class_avg.get(code, 0)))
                labels.append(subject["name_zh"] if lang == "zh" else subject["name_ms"])
            except:
                pass
    
    if not student_values:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=student_values,
        theta=labels,
        fill='toself',
        name='学生成绩' if lang == "zh" else 'Markah Pelajar'
    ))
    fig.add_trace(go.Scatterpolar(
        r=class_values,
        theta=labels,
        fill='toself',
        name='班级平均' if lang == "zh" else 'Purata Kelas',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        title="成绩对比雷达图" if lang == "zh" else "Carta Radar Perbandingan",
        height=500
    )
    return fig

def create_box_plot(class_df, subjects, exam_name, lang):
    """箱线图"""
    fig = go.Figure()
    
    for subject in subjects:
        code = subject["code"]
        if code in class_df.columns:
            name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
            fig.add_trace(go.Box(
                y=class_df[code].dropna(),
                name=name,
                boxmean='sd'
            ))
    
    fig.update_layout(
        title=f"{exam_name} - 成绩分布" if lang == "zh" else f"{exam_name} - Taburan Markah",
        yaxis_title="分数" if lang == "zh" else "Markah",
        height=500
    )
    return fig

def generate_simple_report(student_name, student_data, exams, subjects, class_avg_data, lang):
    """生成简单的 HTML 报告"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{student_name} - 成绩报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; text-align: center; }}
            h2 {{ color: #666; margin-top: 30px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
            th {{ background-color: #4CAF50; color: white; }}
            .advice {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h1>{student_name} - 成绩分析报告</h1>
        <p style="text-align:center">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    """
    
    for exam in exams:
        exam_data = student_data[student_data["考试"] == exam]
        if not exam_data.empty:
            html_content += f"<h2>{exam}</h2>"
            html_content += "<table><tr><th>科目</th><th>成绩</th><th>班级平均</th><th>差距</th></tr>"
            
            for subject in subjects:
                code = subject["code"]
                if code in exam_data.columns:
                    try:
                        score = float(exam_data[code].iloc[0])
                        avg = float(class_avg_data[exam].get(code, 0))
                        diff = score - avg
                        diff_color = "green" if diff >= 0 else "red"
                        name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
                        html_content += f"<tr><td>{name}</td><td>{score:.1f}</td><td>{avg:.1f}</td><td style='color:{diff_color}'>{diff:+.1f}</td></tr>"
                    except:
                        pass
            
            html_content += "</table>"
    
    advice = generate_rule_based_advice(student_data, subjects, exams[-1], lang)
    html_content += f"""
        <div class="advice">
            <h3>📝 学习建议</h3>
            {advice.replace('\n', '<br>')}
        </div>
    </body>
    </html>
    """
    
    return html_content

def generate_rule_based_advice(student_data, subjects, latest_exam, lang):
    """基于规则生成学习建议"""
    latest_data = student_data[student_data["考试"] == latest_exam].iloc[0]
    
    scores = {}
    for subject in subjects:
        code = subject["code"]
        if code in latest_data and pd.notna(latest_data[code]):
            try:
                scores[code] = float(latest_data[code])
            except:
                pass
    
    if not scores:
        return "暂无足够数据生成建议。" if lang == "zh" else "Tiada data yang mencukupi untuk cadangan."
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    avg_score = sum(scores.values()) / len(scores)
    
    strengths = [s[0] for s in sorted_scores[:2] if s[1] >= 75]
    weaknesses = [s[0] for s in sorted_scores[-2:] if s[1] < 60]
    
    def get_subject_name(code):
        for s in subjects:
            if s["code"] == code:
                return s["name_zh"] if lang == "zh" else s["name_ms"]
        return code
    
    if lang == "zh":
        advice = f"""
📊 **总体评价**：本次考试平均分 {avg_score:.1f} 分，{'表现优秀' if avg_score >= 80 else '表现良好' if avg_score >= 70 else '有提升空间'}。

🌟 **优势科目**：{', '.join([get_subject_name(c) for c in strengths]) if strengths else '暂无明显优势科目'}，请继续保持！

📚 **需要加强**：{', '.join([get_subject_name(c) for c in weaknesses]) if weaknesses else '各科发展均衡'}，建议多花时间练习。

💡 **学习建议**：
• 每天安排 30 分钟复习薄弱科目
• 建立错题本，定期回顾
• 与同学组成学习小组
• 保持良好作息，提高效率
"""
    else:
        advice = f"""
📊 **Penilaian Keseluruhan**: Purata markah {avg_score:.1f}, {'cemerlang' if avg_score >= 80 else 'baik' if avg_score >= 70 else 'perlu penambahbaikan'}.

🌟 **Subjek Kekuatan**: {', '.join([get_subject_name(c) for c in strengths]) if strengths else 'Tiada subjek kekuatan yang ketara'}.

📚 **Perlu Diperbaiki**: {', '.join([get_subject_name(c) for c in weaknesses]) if weaknesses else 'Semua subjek seimbang'}.

💡 **Cadangan Pembelajaran**:
• Luangkan 30 minit setiap hari untuk subjek lemah
• Bina buku catatan kesilapan
• Bentuk kumpulan belajar
• Kekalkan rutin tidur yang baik
"""
    
    return advice

def get_subject_list(level, filter_type, lang):
    """获取科目列表"""
    config = SUBJECTS_CONFIG[level]
    
    if filter_type == "core_only":
        subjects = config["core"]
    else:
        subjects = config["core"] + config["elective"]
    
    for s in subjects:
        s["display"] = s["name_zh"] if lang == "zh" else s["name_ms"]
    
    return subjects

def parse_uploaded_file(uploaded_file):
    """解析上传的文件"""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file, engine='openpyxl')

def login_page(supabase):
    lang = st.session_state.get("language", "zh")
    t = TEXTS[lang]
    
    st.title(t["app_title"])
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🇨🇳 中文", use_container_width=True):
            st.session_state.language = "zh"
            st.rerun()
    with col2:
        if st.button("🇲🇾 Bahasa Melayu", use_container_width=True):
            st.session_state.language = "ms"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    classes = get_classes(supabase)
    
    if not classes:
        st.warning("⚠️ 暂无班级数据\n\n请在 Supabase 数据库中创建班级记录。")
        return
    
    with st.form("login_form"):
        class_options = {c["name_zh"] if lang == "zh" else c["name_ms"]: c for c in classes}
        selected_name = st.selectbox(t["select_class"], list(class_options.keys()))
        password = st.text_input(t["password"], type="password")
        
        if st.form_submit_button(t["login_btn"], type="primary", use_container_width=True):
            class_data = class_options[selected_name]
            
            if class_data["password"] == password:
                st.session_state.authenticated = True
                st.session_state.class_id = class_data["id"]
                st.session_state.class_name_zh = class_data["name_zh"]
                st.session_state.class_name_ms = class_data["name_ms"]
                st.session_state.teacher_zh = class_data["teacher_zh"]
                st.session_state.teacher_ms = class_data["teacher_ms"]
                st.session_state.level = class_data["level"]
                st.session_state.grade = class_data["grade"]
                st.rerun()
            else:
                st.error(t["wrong_password"])

def main_app(supabase):
    lang = st.session_state.get("language", "zh")
    t = TEXTS[lang]
    
    if lang == "zh":
        st.sidebar.title(f"👩‍🏫 {st.session_state.class_name_zh}")
        st.sidebar.markdown(f"**班主任**：{st.session_state.teacher_zh}")
        st.sidebar.markdown(f"**年级**：{st.session_state.grade}年级")
    else:
        st.sidebar.title(f"👩‍🏫 {st.session_state.class_name_ms}")
        st.sidebar.markdown(f"**Guru Kelas**：{st.session_state.teacher_ms}")
        st.sidebar.markdown(f"**Tahun**：{st.session_state.grade}")
    
    st.sidebar.markdown("---")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🇨🇳 中文", use_container_width=True):
            st.session_state.language = "zh"
            st.rerun()
    with col2:
        if st.button("🇲🇾 BM", use_container_width=True):
            st.session_state.language = "ms"
            st.rerun()
    
    st.sidebar.markdown("---")
    
    subject_filter = st.sidebar.radio(
        t["subject_display"],
        [t["core_only"], t["all_subjects"]],
        horizontal=True
    )
    filter_type = "core_only" if subject_filter == t["core_only"] else "all_subjects"
    
    menu = st.sidebar.radio(
        "功能菜单" if lang == "zh" else "Menu",
        [t["student_performance"], t["class_performance"], t["data_management"], t["help"]]
    )
    
    if st.sidebar.button(t["logout"], use_container_width=True):
        for key in ["authenticated", "class_id", "class_name_zh", "class_name_ms", "teacher_zh", "teacher_ms", "level", "grade"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    students_df = get_students(supabase, st.session_state.class_id)
    exams = get_exams(supabase, st.session_state.class_id)
    subjects = get_subject_list(st.session_state.level, filter_type, lang)
    
    if menu == t["student_performance"]:
        st.header(t["student_performance"])
        
        if students_df.empty:
            st.warning(t["no_students"])
            return
        
        if not exams:
            st.info(t["no_exams"])
            return
        
        student_options = {row["name_zh"]: row["id"] for _, row in students_df.iterrows()}
        student_name = st.selectbox(t["select_student"], list(student_options.keys()))
        student_id = student_options[student_name]
        
        exam_options = [e["exam_name"] for e in exams]
        selected_exams = st.multiselect(t["select_exams"], exam_options, default=exam_options[-3:] if len(exam_options) >= 3 else exam_options)
        
        if selected_exams:
            student_data = []
            for exam in exams:
                if exam["exam_name"] in selected_exams:
                    grades = get_grades(supabase, exam["id"])
                    student_grade = next((g for g in grades if g["student_id"] == student_id), None)
                    if student_grade and student_grade["scores"]:
                        record = {"考试": exam["exam_name"]}
                        for code, score in student_grade["scores"].items():
                            if score is not None:
                                record[code] = score
                        student_data.append(record)
            
            if student_data:
                df_student = pd.DataFrame(student_data)
                
                chart_options = [t["line_chart"], t["bar_chart"]]
                chart_type = st.selectbox(t["chart_type"], chart_options)
                
                tab1, tab2, tab3 = st.tabs(["📈 成绩图表", "🎯 雷达对比", "📄 报告导出"] if lang == "zh" else ["📈 Carta", "🎯 Radar", "📄 Laporan"])
                
                with tab1:
                    if chart_type == t["line_chart"]:
                        fig = create_line_chart(df_student, selected_exams, subjects, lang)
                    else:
                        fig = create_bar_chart(df_student, selected_exams, subjects, lang)
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    latest_exam = selected_exams[-1]
                    latest_data = df_student[df_student["考试"] == latest_exam].iloc[0]
                    exam_record = next(e for e in exams if e["exam_name"] == latest_exam)
                    grades = get_grades(supabase, exam_record["id"])
                    
                    class_avg = {}
                    for g in grades:
                        if g["scores"]:
                            for code, score in g["scores"].items():
                                if score is not None:
                                    if code not in class_avg:
                                        class_avg[code] = []
                                    class_avg[code].append(score)
                    class_avg = {k: np.mean(v) for k, v in class_avg.items()}
                    
                    fig = create_radar_chart(latest_data.to_dict(), class_avg, subjects, lang)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("📝 学习建议" if lang == "zh" else "📝 Cadangan")
                    advice = generate_rule_based_advice(df_student, subjects, latest_exam, lang)
                    st.markdown(advice)
                
                with tab3:
                    if st.button(t["generate_report"], type="primary"):
                        with st.spinner("生成报告中..." if lang == "zh" else "Sedang hasilkan laporan..."):
                            class_avg_data = {}
                            for exam_name in selected_exams:
                                exam_record = next(e for e in exams if e["exam_name"] == exam_name)
                                grades = get_grades(supabase, exam_record["id"])
                                class_avg = {}
                                for g in grades:
                                    if g["scores"]:
                                        for code, score in g["scores"].items():
                                            if score is not None:
                                                if code not in class_avg:
                                                    class_avg[code] = []
                                                class_avg[code].append(score)
                                class_avg_data[exam_name] = {k: np.mean(v) for k, v in class_avg.items()}
                            
                            html_report = generate_simple_report(student_name, df_student, selected_exams, subjects, class_avg_data, lang)
                            
                            st.download_button(
                                label=t["download_report"],
                                data=html_report,
                                file_name=f"{student_name}_成绩报告_{datetime.now().strftime('%Y%m%d')}.html",
                                mime="text/html"
                            )
    
    elif menu == t["class_performance"]:
        st.header(t["class_performance"])
        
        if not exams:
            st.info(t["no_exams"])
            return
        
        exam_options = [e["exam_name"] for e in exams]
        selected_exam = st.selectbox("选择考试" if lang == "zh" else "Pilih Peperiksaan", exam_options)
        
        exam_record = next(e for e in exams if e["exam_name"] == selected_exam)
        grades = get_grades(supabase, exam_record["id"])
        
        if grades:
            class_data = []
            for g in grades:
                if g["students"] and g["scores"]:
                    row = {"student_id": g["student_id"], "学生": g["students"]["name_zh"]}
                    for code, score in g["scores"].items():
                        if score is not None:
                            row[code] = score
                    class_data.append(row)
            
            if class_data:
                class_df = pd.DataFrame(class_data)
                
                col1, col2, col3, col4 = st.columns(4)
                subject_codes = [s["code"] for s in subjects if s["code"] in class_df.columns]
                
                with col1:
                    st.metric(t["student_count"], len(class_df))
                with col2:
                    if subject_codes:
                        avg = class_df[subject_codes].mean().mean()
                        st.metric(t["class_avg"], f"{avg:.1f}")
                with col3:
                    if subject_codes:
                        total = class_df[subject_codes].sum(axis=1)
                        st.metric(t["highest_total"], total.max())
                with col4:
                    if subject_codes:
                        pass_rate = (class_df[subject_codes] >= 60).all(axis=1).mean() * 100
                        st.metric(t["pass_rate"], f"{pass_rate:.1f}%")
                
                fig = create_box_plot(class_df, subjects, selected_exam, lang)
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader(t["ranking_table"])
                if subject_codes:
                    class_df["总分"] = class_df[subject_codes].sum(axis=1)
                    class_df["排名"] = class_df["总分"].rank(ascending=False, method='min').astype(int)
                    display_cols = ["学生"] + subject_codes + ["总分", "排名"]
                    st.dataframe(class_df[display_cols].sort_values("排名"), use_container_width=True)
    
    elif menu == t["data_management"]:
        st.header(t["data_management"])
        
        tab1, tab2, tab3 = st.tabs([t["import_students"], t["import_grades"], t["history_exams"]])
        
        with tab1:
            if not students_df.empty:
                st.dataframe(students_df[["student_no", "name_zh"]], use_container_width=True)
            
            uploaded_file = st.file_uploader(t["import_students"], type=['csv', 'xlsx'])
            if uploaded_file:
                df = parse_uploaded_file(uploaded_file)
                if '学号' in df.columns and '姓名' in df.columns:
                    if add_students(supabase, st.session_state.class_id, df):
                        st.success(t["success"])
                        st.rerun()
                else:
                    st.error("文件必须包含「学号」和「姓名」列" if lang == "zh" else "Fail mesti mengandungi lajur '学号' dan '姓名'")
        
        with tab2:
            exam_name = st.text_input(t["exam_name"])
            exam_date = st.date_input(t["exam_date"], datetime.now())
            uploaded_file = st.file_uploader(t["import_grades"], type=['csv', 'xlsx'], key="grade_upload")
            
            if exam_name and uploaded_file:
                df = parse_uploaded_file(uploaded_file)
                if '学号' in df.columns and '姓名' in df.columns:
                    students = get_students(supabase, st.session_state.class_id)
                    student_map = {str(row["student_no"]): row["id"] for _, row in students.iterrows()}
                    
                    df["student_id"] = df["学号"].astype(str).map(student_map)
                    
                    if df["student_id"].isna().any():
                        missing = df[df["student_id"].isna()]["学号"].tolist()
                        st.error(f"以下学号未在学生名单中找到: {missing}" if lang == "zh" else f"Nombor pelajar berikut tidak ditemui: {missing}")
                    else:
                        exam_id = add_exam(supabase, st.session_state.class_id, exam_name, exam_date)
                        if exam_id:
                            if save_grades(supabase, exam_id, df):
                                st.success(t["success"])
                                st.rerun()
                else:
                    st.error("文件必须包含「学号」和「姓名」列" if lang == "zh" else "Fail mesti mengandungi lajur '学号' dan '姓名'")
        
        with tab3:
            if exams:
                for exam in exams:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"📄 {exam['exam_name']} - {exam['exam_date']}")
                    with col2:
                        if st.button(t["delete"], key=f"del_{exam['id']}"):
                            if delete_exam(supabase, exam["id"]):
                                st.success(t["success"])
                                st.rerun()
            else:
                st.info(t["no_exams"])
    
    else:
        st.header(t["help"])
        if lang == "zh":
            st.markdown("""
            ### 📌 使用说明
            
            **1. 导入学生名单**
            - 文件需包含「学号」和「姓名」列
            - 支持 Excel (.xlsx) 和 CSV 格式
            
            **2. 导入考试成绩**
            - 文件需包含「学号」「姓名」和各科目列
            - 科目代码：BC, BM, BI, MT, SN, SEJ, PJPK, PSV, MUZIK, MORAL, RBT
            - 分数范围：0-100
            
            **3. 查看分析**
            - 选择学生后可查看成绩趋势图、雷达图
            - 可生成 HTML 报告下载
            
            **4. 数据存储**
            - 所有数据存储在 Supabase 云端数据库
            """)
        else:
            st.markdown("""
            ### 📌 Panduan Penggunaan
            
            **1. Import Senarai Pelajar**
            - Fail mesti mengandungi lajur '学号' dan '姓名'
            - Format Excel (.xlsx) atau CSV
            
            **2. Import Markah**
            - Fail mesti mengandungi '学号', '姓名' dan lajur subjek
            - Kod subjek: BC, BM, BI, MT, SN, SEJ, PJPK, PSV, MUZIK, MORAL, RBT
            
            **3. Analisis**
            - Pilih pelajar untuk lihat carta trend dan radar
            - Hasilkan laporan HTML
            
            **4. Penyimpanan Data**
            - Semua data disimpan di pangkalan data Supabase
            """)

if __name__ == "__main__":
    init_session_state()
    supabase = init_supabase()
    
    if not supabase:
        st.warning("⚠️ Supabase 连接失败，将使用演示模式")
        st.stop()
    
    if not st.session_state.authenticated:
        login_page(supabase)
    else:
        main_app(supabase)
