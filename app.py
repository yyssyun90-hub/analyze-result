import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from supabase import create_client
import io
import re

# ========== 页面配置 ==========
st.set_page_config(
    page_title="SJKHK Academic Analytics System | 成绩分析系统",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 校领导账号 ==========
PRINCIPAL_PASSWORD = "SJKHK000"

# ========== 多语言配置 ==========
TEXTS = {
    "zh": {
        "app_title": "SJKHK 成绩分析系统",
        "subtitle": "智能学业分析平台",
        "login": "登录",
        "password": "密码",
        "login_btn": "登录",
        "logout": "退出登录",
        "select_class": "选择班级",
        "principal_mode": "校领导登录",
        "teacher_mode": "班主任登录",
        "wrong_password": "密码错误！",
        "student_performance": "📊 学生个人成绩",
        "class_performance": "📈 班级成绩分析",
        "data_management": "📁 成绩管理",
        "class_settings": "🏫 班级设置",
        "settings": "⚙️ 系统设置",
        "help": "ℹ️ 帮助",
        "core_only": "核心科目",
        "all_subjects": "全部科目",
        "subject_display": "科目显示",
        "select_student": "选择学生",
        "select_exams": "选择考试",
        "chart_type": "图表类型",
        "line_chart": "趋势图",
        "bar_chart": "对比图",
        "radar_chart": "雷达图",
        "box_plot": "分布图",
        "generate_report": "生成报告",
        "download_report": "下载报告",
        "no_students": "暂无学生数据，请先导入学生名单",
        "no_exams": "暂无考试成绩，请先导入成绩",
        "import_students": "导入学生名单",
        "import_grades": "导入考试成绩",
        "exam_name": "考试名称",
        "exam_date": "考试日期",
        "success": "导入成功！",
        "error": "导入失败",
        "student_no": "学号",
        "student_name": "姓名",
        "rank": "排名",
        "total_score": "总分",
        "average": "平均分",
        "history_exams": "历史考试",
        "delete": "删除",
        "student_count": "学生人数",
        "class_avg": "班级平均分",
        "highest_total": "最高总分",
        "pass_rate": "及格率",
        "ranking_table": "成绩排名表",
        "teacher_name_zh": "班主任 (中文)",
        "teacher_name_ms": "Guru Kelas (BM)",
        "edit_teacher": "编辑班主任信息",
        "save_teacher": "保存信息",
        "teacher_updated": "班主任信息已更新",
        "switch_class": "切换班级",
        "school_name": "学校名称",
        "academic_year": "学年",
        "save_settings": "保存设置",
        "settings_saved": "设置已保存",
        "download_template": "下载模板",
        "template_help": "点击下载 Excel 模板，按格式填写后上传",
        "core_subjects_only": "仅显示核心科目",
        "all_subjects_include": "显示全部科目",
        "no_data_radar": "暂无雷达图数据",
        "no_data_box": "暂无分布图数据"
    },
    "ms": {
        "app_title": "Sistem Analisis Akademik SJKHK",
        "subtitle": "Platform Analisis Akademik Pintar",
        "login": "Log Masuk",
        "password": "Kata Laluan",
        "login_btn": "Log Masuk",
        "logout": "Log Keluar",
        "select_class": "Pilih Kelas",
        "principal_mode": "Log Masuk Pentadbir",
        "teacher_mode": "Log Masuk Guru",
        "wrong_password": "Kata laluan salah!",
        "student_performance": "📊 Analisis Pelajar Individu",
        "class_performance": "📈 Analisis Prestasi Kelas",
        "data_management": "📁 Pengurusan Data",
        "class_settings": "🏫 Tetapan Kelas",
        "settings": "⚙️ Tetapan Sistem",
        "help": "ℹ️ Bantuan",
        "core_only": "Subjek Teras",
        "all_subjects": "Semua Subjek",
        "subject_display": "Paparan Subjek",
        "select_student": "Pilih Pelajar",
        "select_exams": "Pilih Peperiksaan",
        "chart_type": "Jenis Carta",
        "line_chart": "Carta Garisan",
        "bar_chart": "Carta Palang",
        "radar_chart": "Carta Radar",
        "box_plot": "Carta Kotak",
        "generate_report": "Hasilkan Laporan",
        "download_report": "Muat Turun Laporan",
        "no_students": "Tiada data pelajar, sila import senarai pelajar",
        "no_exams": "Tiada data peperiksaan, sila import markah",
        "import_students": "Import Senarai Pelajar",
        "import_grades": "Import Markah Peperiksaan",
        "exam_name": "Nama Peperiksaan",
        "exam_date": "Tarikh Peperiksaan",
        "success": "Import berjaya!",
        "error": "Import gagal",
        "student_no": "No. Pelajar",
        "student_name": "Nama",
        "rank": "Kedudukan",
        "total_score": "Jumlah Markah",
        "average": "Purata",
        "history_exams": "Peperiksaan Lepas",
        "delete": "Padam",
        "student_count": "Bilangan Pelajar",
        "class_avg": "Purata Kelas",
        "highest_total": "Jumlah Tertinggi",
        "pass_rate": "Kadar Lulus",
        "ranking_table": "Jadual Kedudukan",
        "teacher_name_zh": "Guru Kelas (Cina)",
        "teacher_name_ms": "Guru Kelas (BM)",
        "edit_teacher": "Edit Maklumat Guru",
        "save_teacher": "Simpan",
        "teacher_updated": "Maklumat guru dikemas kini",
        "switch_class": "Tukar Kelas",
        "school_name": "Nama Sekolah",
        "academic_year": "Tahun Akademik",
        "save_settings": "Simpan Tetapan",
        "settings_saved": "Tetapan disimpan",
        "download_template": "Muat Turun Templat",
        "template_help": "Klik untuk muat turun templat Excel",
        "core_subjects_only": "Paparan Subjek Teras",
        "all_subjects_include": "Paparan Semua Subjek",
        "no_data_radar": "Tiada data untuk carta radar",
        "no_data_box": "Tiada data untuk carta kotak"
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

# ========== 生成 Excel 模板 ==========
def generate_student_template():
    """生成学生名单模板"""
    df = pd.DataFrame({
        "学号": ["S001", "S002"],
        "姓名": ["陈小明", "李小华"],
        "姓名_马来文": ["Tan Xiao Ming", "Lee Xiao Hua"]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="学生名单", index=False)
    return output.getvalue()

def generate_grade_template(level):
    """生成成绩模板（根据年级动态生成科目）"""
    config = SUBJECTS_CONFIG.get(level, SUBJECTS_CONFIG["low_primary"])
    all_subjects = config["core"] + config["elective"]
    
    columns = ["学号", "姓名"]
    for s in all_subjects:
        columns.append(s["code"])
    
    sample_data = ["S001", "陈小明"]
    for s in all_subjects:
        sample_data.append(85)
    
    df = pd.DataFrame([sample_data], columns=columns)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="成绩表", index=False)
    return output.getvalue()

# ========== 初始化 Session State ==========
def init_session_state():
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
    if "is_principal" not in st.session_state:
        st.session_state.is_principal = False

# ========== Supabase 连接 ==========
@st.cache_resource
def init_supabase():
    try:
        supabase_url = st.secrets.get("SUPABASE_URL", "")
        supabase_key = st.secrets.get("SUPABASE_KEY", "")
        
        if not supabase_url or not supabase_key:
            return None
        
        return create_client(supabase_url, supabase_key)
    except Exception:
        return None

# ========== 数据操作函数 ==========
def get_classes(supabase):
    try:
        response = supabase.table("classes").select("*").order("grade").execute()
        return response.data if response.data else []
    except Exception:
        return []

def update_class_teacher(supabase, class_id, teacher_zh, teacher_ms):
    try:
        supabase.table("classes").update({
            "teacher_zh": teacher_zh,
            "teacher_ms": teacher_ms
        }).eq("id", class_id).execute()
        return True
    except Exception:
        return False

def get_students(supabase, class_id):
    try:
        response = supabase.table("students").select("*").eq("class_id", class_id).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def add_students(supabase, class_id, students_df):
    try:
        records = []
        for _, row in students_df.iterrows():
            records.append({
                "class_id": class_id,
                "student_no": str(row["学号"]),
                "name_zh": row["姓名"],
                "name_ms": row.get("姓名_马来文", row["姓名"])
            })
        supabase.table("students").insert(records).execute()
        return True
    except Exception:
        return False

def get_exams(supabase, class_id):
    try:
        response = supabase.table("exams").select("*").eq("class_id", class_id).order("exam_date").execute()
        return response.data if response.data else []
    except Exception:
        return []

def add_exam(supabase, class_id, exam_name, exam_date, academic_year):
    try:
        response = supabase.table("exams").insert({
            "class_id": class_id,
            "exam_name": exam_name,
            "exam_date": exam_date.isoformat(),
            "academic_year": academic_year
        }).execute()
        return response.data[0]["id"] if response.data else None
    except Exception:
        return None

def get_grades(supabase, exam_id):
    try:
        response = supabase.table("grades").select("*, students(*)").eq("exam_id", exam_id).execute()
        return response.data if response.data else []
    except Exception:
        return []

def save_grades(supabase, exam_id, grades_df):
    try:
        supabase.table("grades").delete().eq("exam_id", exam_id).execute()
        
        records = []
        for _, row in grades_df.iterrows():
            scores = {}
            for col in grades_df.columns:
                if col not in ["学号", "姓名", "student_id"]:
                    try:
                        val = float(row[col]) if pd.notna(row[col]) else None
                        if val is not None:
                            scores[col] = val
                    except:
                        pass
            if scores:
                records.append({
                    "exam_id": exam_id,
                    "student_id": row["student_id"],
                    "scores": scores
                })
        
        if records:
            supabase.table("grades").insert(records).execute()
        return True
    except Exception:
        return False

def delete_exam(supabase, exam_id):
    try:
        supabase.table("grades").delete().eq("exam_id", exam_id).execute()
        supabase.table("exams").delete().eq("id", exam_id).execute()
        return True
    except Exception:
        return False

# ========== 图表生成函数 ==========
def create_line_chart(student_data, exams, subjects, lang):
    fig = go.Figure()
    for subject in subjects:
        code = subject["code"]
        if code in student_data.columns:
            scores = student_data[code].tolist()
            name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
            fig.add_trace(go.Scatter(
                x=exams, y=scores, mode='lines+markers', name=name,
                line=dict(width=3), marker=dict(size=10, symbol='circle')
            ))
    fig.update_layout(
        title="📈 成绩趋势分析" if lang == "zh" else "📈 Analisis Trend Prestasi",
        xaxis_title="考试" if lang == "zh" else "Peperiksaan",
        yaxis_title="分数" if lang == "zh" else "Markah",
        hovermode='x unified',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    return fig

def create_bar_chart(student_data, exams, subjects, lang):
    fig = go.Figure()
    for exam in exams:
        exam_data = student_data[student_data["考试"] == exam]
        if not exam_data.empty:
            scores = []
            names = []
            for subject in subjects:
                code = subject["code"]
                if code in exam_data.columns:
                    val = exam_data[code].iloc[0]
                    if pd.notna(val):
                        scores.append(val)
                        names.append(subject["name_zh"] if lang == "zh" else subject["name_ms"])
            if scores:
                fig.add_trace(go.Bar(
                    name=exam, x=names, y=scores, text=scores, textposition='auto',
                    marker=dict(pattern_shape='solid')
                ))
    fig.update_layout(
        title="📊 各科成绩对比" if lang == "zh" else "📊 Perbandingan Markah Subjek",
        xaxis_title="科目" if lang == "zh" else "Subjek",
        yaxis_title="分数" if lang == "zh" else "Markah",
        barmode='group',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_radar_chart(student_scores, class_avg, subjects, lang):
    student_values = []
    class_values = []
    labels = []
    for subject in subjects:
        code = subject["code"]
        if code in student_scores and student_scores[code]:
            try:
                student_values.append(float(student_scores[code]))
                class_avg_val = class_avg.get(code, 0) if class_avg else 0
                class_values.append(float(class_avg_val))
                labels.append(subject["name_zh"] if lang == "zh" else subject["name_ms"])
            except:
                pass
    if not student_values or len(student_values) < 2:
        return None
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=student_values, theta=labels, fill='toself',
        name='学生成绩' if lang == "zh" else 'Markah Pelajar',
        line=dict(color='#FF6B6B', width=2),
        fillcolor='rgba(255,107,107,0.3)'
    ))
    if class_values and any(v > 0 for v in class_values):
        fig.add_trace(go.Scatterpolar(
            r=class_values, theta=labels, fill='toself',
            name='班级平均' if lang == "zh" else 'Purata Kelas',
            line=dict(color='#4ECDC4', width=2, dash='dash'),
            fillcolor='rgba(78,205,196,0.2)'
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], tickfont=dict(size=10))),
        title="🎯 能力雷达图" if lang == "zh" else "🎯 Carta Radar Kemampuan",
        height=550,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    return fig

def create_box_plot(class_df, subjects, exam_name, lang):
    if class_df.empty:
        return None
    fig = go.Figure()
    for subject in subjects:
        code = subject["code"]
        if code in class_df.columns:
            values = class_df[code].dropna()
            if len(values) > 0:
                name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
                fig.add_trace(go.Box(
                    y=values, name=name, boxmean='sd',
                    marker=dict(color='#FF6B6B'),
                    line=dict(color='#FF6B6B', width=2)
                ))
    if len(fig.data) == 0:
        return None
    fig.update_layout(
        title=f"📦 {exam_name} - 成绩分布" if lang == "zh" else f"📦 {exam_name} - Taburan Markah",
        yaxis_title="分数" if lang == "zh" else "Markah",
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def generate_simple_report(student_name, student_data, exams, subjects, class_avg_data, lang):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{student_name} - Academic Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; text-align: center; margin-bottom: 10px; }}
        h2 {{ color: #764ba2; margin-top: 30px; border-left: 4px solid #667eea; padding-left: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px; }}
        td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: center; }}
        .advice {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px; border-left: 4px solid #667eea; }}
        .date {{ text-align: center; color: #666; margin-bottom: 30px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📊 {student_name} - 成绩分析报告</h1>
    <div class="date">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
"""
    for exam in exams:
        exam_data = student_data[student_data["考试"] == exam]
        if not exam_data.empty:
            html_content += f"<h2>📚 {exam}</h2>"
            html_content += "广播电台\n"
            html_content += "    <thead>\n        <tr><th>科目</th><th>成绩</th><th>班级平均</th><th>差距</th></tr>\n    </thead>\n    <tbody>\n"
            for subject in subjects:
                code = subject["code"]
                if code in exam_data.columns:
                    try:
                        score = float(exam_data[code].iloc[0])
                        avg_data = class_avg_data.get(exam, {}) if class_avg_data else {}
                        avg = float(avg_data.get(code, 0))
                        diff = score - avg
                        diff_color = "#10b981" if diff >= 0 else "#ef4444"
                        name = subject["name_zh"] if lang == "zh" else subject["name_ms"]
                        html_content += f"         <tr><td>{name}</td><td><strong>{score:.1f}</strong></td><td>{avg:.1f}</td><td style='color:{diff_color}'>{diff:+.1f}</td></tr>\n"
                    except:
                        pass
            html_content += "    </tbody>\n</table>\n"
    if exams:
        advice = generate_rule_based_advice(student_data, subjects, exams[-1], lang)
    else:
        advice = "暂无数据生成建议。" if lang == "zh" else "Tiada data untuk cadangan."
    html_content += f"""
    <div class="advice">
        <h3>💡 学习建议</h3>
        {advice.replace(chr(10), '<br>')}
    </div>
</div>
</body>
</html>"""
    return html_content

def generate_rule_based_advice(student_data, subjects, latest_exam, lang):
    if student_data.empty:
        return "暂无数据生成建议。" if lang == "zh" else "Tiada data untuk cadangan."
    latest_data = student_data[student_data["考试"] == latest_exam]
    if latest_data.empty:
        return "暂无数据生成建议。" if lang == "zh" else "Tiada data untuk cadangan."
    latest_data = latest_data.iloc[0]
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
        return f"""
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
        return f"""
📊 **Penilaian Keseluruhan**: Purata markah {avg_score:.1f}, {'cemerlang' if avg_score >= 80 else 'baik' if avg_score >= 70 else 'perlu penambahbaikan'}.

🌟 **Subjek Kekuatan**: {', '.join([get_subject_name(c) for c in strengths]) if strengths else 'Tiada subjek kekuatan yang ketara'}.

📚 **Perlu Diperbaiki**: {', '.join([get_subject_name(c) for c in weaknesses]) if weaknesses else 'Semua subjek seimbang'}.

💡 **Cadangan Pembelajaran**:
• Luangkan 30 minit setiap hari untuk subjek lemah
• Bina buku catatan kesilapan
• Bentuk kumpulan belajar
• Kekalkan rutin tidur yang baik
"""

def get_subject_list(level, filter_type, lang):
    config = SUBJECTS_CONFIG.get(level, SUBJECTS_CONFIG["low_primary"])
    if filter_type == "core_only":
        subjects = config["core"].copy()
    else:
        subjects = config["core"].copy() + config["elective"].copy()
    for s in subjects:
        s["display"] = s["name_zh"] if lang == "zh" else s["name_ms"]
    return subjects

def parse_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file, engine='openpyxl')

def normalize_column_name(col):
    """标准化列名，去除空格并转为大写"""
    if isinstance(col, str):
        return col.strip().upper()
    return col

# ========== 班级设置页面 ==========
def show_class_settings_page(supabase, lang, t, classes):
    st.header(t["class_settings"])
    class_options = {c["name_zh"] if lang == "zh" else c["name_ms"]: c for c in classes}
    selected_name = st.selectbox(t["select_class"], list(class_options.keys()))
    selected_class = class_options[selected_name]
    if selected_class:
        st.markdown("### ✏️ " + t["edit_teacher"])
        col1, col2 = st.columns(2)
        with col1:
            teacher_zh = st.text_input(t["teacher_name_zh"], value=selected_class["teacher_zh"])
        with col2:
            teacher_ms = st.text_input(t["teacher_name_ms"], value=selected_class["teacher_ms"])
        if st.button(t["save_teacher"], type="primary"):
            if update_class_teacher(supabase, selected_class["id"], teacher_zh, teacher_ms):
                st.success(t["teacher_updated"])
                st.rerun()
        st.markdown("---")
        st.markdown("### 📋 班级信息")
        st.write(f"**班级**: {selected_class['name_zh']} / {selected_class['name_ms']}")
        st.write(f"**年级**: {selected_class['grade']}")
        st.write(f"**班主任**: {selected_class['teacher_zh']} / {selected_class['teacher_ms']}")

# ========== 系统设置页面 ==========
def show_settings_page(supabase, lang, t):
    st.header(t["settings"])
    class_id = st.session_state.class_id
    try:
        response = supabase.table("school_settings").select("*").eq("class_id", class_id).execute()
        settings = response.data[0] if response.data else {}
    except:
        settings = {}
    st.markdown("### 🏫 " + t["school_name"])
    col1, col2 = st.columns(2)
    with col1:
        school_name_zh = st.text_input("学校名称 (中文)", value=settings.get("school_name_zh", "SJKHK"))
        academic_year = st.text_input(t["academic_year"], value=settings.get("current_academic_year", "2026"))
    with col2:
        school_name_ms = st.text_input("Nama Sekolah (BM)", value=settings.get("school_name_ms", "SJKHK"))
        school_logo_url = st.text_input("校徽图片URL (可选)", value=settings.get("school_logo_url", ""))
    st.markdown("### 📝 考试设置")
    col1, col2 = st.columns(2)
    with col1:
        exam_name_prefix = st.text_input("考试名称前缀", value=settings.get("exam_name_prefix", ""))
    with col2:
        exam_name_suffix = st.text_input("考试名称后缀", value=settings.get("exam_name_suffix", academic_year))
    if st.button(t["save_settings"], type="primary", use_container_width=True):
        try:
            data = {
                "class_id": class_id, "school_name_zh": school_name_zh, "school_name_ms": school_name_ms,
                "school_logo_url": school_logo_url, "current_academic_year": academic_year,
                "exam_name_prefix": exam_name_prefix, "exam_name_suffix": exam_name_suffix,
                "updated_at": datetime.now().isoformat()
            }
            if settings:
                supabase.table("school_settings").update(data).eq("class_id", class_id).execute()
            else:
                supabase.table("school_settings").insert(data).execute()
            st.success(t["settings_saved"])
            st.rerun()
        except:
            st.error("保存失败")

# ========== 登录页面 ==========
def login_page(supabase):
    lang = st.session_state.get("language", "zh")
    t = TEXTS[lang]
    st.markdown("""
    <style>
    .login-title { text-align: center; margin-bottom: 2rem; }
    .login-title h1 { font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .login-title p { color: #666; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="login-title"><h1>🎓 {t["app_title"]}</h1><p>{t["subtitle"]}</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            if st.button("🇨🇳 中文", use_container_width=True):
                st.session_state.language = "zh"
                st.rerun()
        with col_lang2:
            if st.button("🇲🇾 BM", use_container_width=True):
                st.session_state.language = "ms"
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        classes = get_classes(supabase)
        if not classes:
            st.warning("⚠️ 暂无班级数据\n\n请在 Supabase 数据库中创建班级记录。")
            return
        with st.form("login_form"):
            login_mode = st.radio("登录模式", [t["teacher_mode"], t["principal_mode"]], horizontal=True)
            if login_mode == t["teacher_mode"]:
                class_options = {c["name_zh"] if lang == "zh" else c["name_ms"]: c for c in classes}
                selected_name = st.selectbox(t["select_class"], list(class_options.keys()))
                password = st.text_input(t["password"], type="password")
                if st.form_submit_button(t["login_btn"], type="primary", use_container_width=True):
                    class_data = class_options[selected_name]
                    if class_data["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.is_principal = False
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
            else:
                password = st.text_input(t["password"], type="password")
                if st.form_submit_button(t["login_btn"], type="primary", use_container_width=True):
                    if password == PRINCIPAL_PASSWORD:
                        st.session_state.authenticated = True
                        st.session_state.is_principal = True
                        st.session_state.class_id = classes[0]["id"]
                        st.session_state.class_name_zh = "校领导模式"
                        st.session_state.class_name_ms = "Mod Pentadbir"
                        st.session_state.teacher_zh = "校领导"
                        st.session_state.teacher_ms = "Pentadbir"
                        st.session_state.level = classes[0]["level"]
                        st.session_state.grade = classes[0]["grade"]
                        st.rerun()
                    else:
                        st.error(t["wrong_password"])

# ========== 主应用 ==========
def main_app(supabase):
    lang = st.session_state.get("language", "zh")
    t = TEXTS[lang]
    all_classes = get_classes(supabase)
    
    if st.session_state.is_principal:
        st.sidebar.markdown("""
        <style>
        .sidebar-title { text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; margin-bottom: 1rem; }
        .sidebar-title h3 { color: white; margin: 0; }
        </style>
        """, unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-title"><h3>👨‍💼 ' + t["principal_mode"] + '</h3></div>', unsafe_allow_html=True)
        class_options = {c["name_zh"] if lang == "zh" else c["name_ms"]: c for c in all_classes}
        selected_class_name = st.sidebar.selectbox(t["switch_class"], list(class_options.keys()))
        selected_class = class_options[selected_class_name]
        st.session_state.class_id = selected_class["id"]
        st.session_state.class_name_zh = selected_class["name_zh"]
        st.session_state.class_name_ms = selected_class["name_ms"]
        st.session_state.teacher_zh = selected_class["teacher_zh"]
        st.session_state.teacher_ms = selected_class["teacher_ms"]
        st.session_state.level = selected_class["level"]
        st.session_state.grade = selected_class["grade"]
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**📚 {selected_class['name_zh']}**")
        st.sidebar.markdown(f"**👩‍🏫 {selected_class['teacher_zh']}**")
    else:
        st.sidebar.markdown(f'<div class="sidebar-title"><h3>👩‍🏫 {st.session_state.class_name_zh}</h3></div>', unsafe_allow_html=True)
        st.sidebar.markdown(f"**👩‍🏫 {st.session_state.teacher_zh}**")
        st.sidebar.markdown(f"**📖 年级：{st.session_state.grade}**")
    
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
    
    subject_filter = st.sidebar.radio(t["subject_display"], [t["core_only"], t["all_subjects"]], horizontal=True)
    filter_type = "core_only" if subject_filter == t["core_only"] else "all_subjects"
    
    if st.session_state.is_principal:
        menu_options = [t["student_performance"], t["class_performance"], t["data_management"], t["class_settings"], t["settings"], t["help"]]
    else:
        menu_options = [t["student_performance"], t["class_performance"], t["data_management"], t["settings"], t["help"]]
    menu = st.sidebar.radio("", menu_options)
    
    if st.sidebar.button(t["logout"], use_container_width=True):
        keys = ["authenticated", "class_id", "class_name_zh", "class_name_ms", "teacher_zh", "teacher_ms", "level", "grade", "is_principal"]
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    students_df = get_students(supabase, st.session_state.class_id)
    exams = get_exams(supabase, st.session_state.class_id)
    subjects = get_subject_list(st.session_state.level, filter_type, lang)
    
    # ========== 学生个人成绩 ==========
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
                chart_type = st.selectbox(t["chart_type"], [t["line_chart"], t["bar_chart"]])
                tab1, tab2, tab3 = st.tabs(["📈 成绩图表", "🎯 雷达对比", "📄 报告导出"])
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
                    if class_avg:
                        class_avg = {k: np.mean(v) for k, v in class_avg.items()}
                    else:
                        class_avg = {}
                    fig = create_radar_chart(latest_data.to_dict(), class_avg, subjects, lang)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info(t.get("no_data_radar", "暂无雷达图数据"))
                    st.subheader("📝 学习建议")
                    advice = generate_rule_based_advice(df_student, subjects, latest_exam, lang)
                    st.markdown(advice)
                with tab3:
                    if st.button(t["generate_report"], type="primary"):
                        with st.spinner("生成报告中..."):
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
                                if class_avg:
                                    class_avg_data[exam_name] = {k: np.mean(v) for k, v in class_avg.items()}
                                else:
                                    class_avg_data[exam_name] = {}
                            html_report = generate_simple_report(student_name, df_student, selected_exams, subjects, class_avg_data, lang)
                            st.download_button(label=t["download_report"], data=html_report, file_name=f"{student_name}_成绩报告_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html")
    
    # ========== 班级成绩分析 ==========
    elif menu == t["class_performance"]:
        st.header(t["class_performance"])
        if not exams:
            st.info(t["no_exams"])
            return
        exam_options = [e["exam_name"] for e in exams]
        selected_exam = st.selectbox("选择考试", exam_options)
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
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(t.get("no_data_box", "暂无分布图数据"))
                st.subheader(t["ranking_table"])
                if subject_codes:
                    class_df["总分"] = class_df[subject_codes].sum(axis=1)
                    class_df["排名"] = class_df["总分"].rank(ascending=False, method='min').astype(int)
                    display_cols = ["学生"] + subject_codes + ["总分", "排名"]
                    st.dataframe(class_df[display_cols].sort_values("排名"), use_container_width=True)
    
    # ========== 成绩管理 ==========
    elif menu == t["data_management"]:
        st.header(t["data_management"])
        tab1, tab2, tab3 = st.tabs([t["import_students"], t["import_grades"], t["history_exams"]])
        with tab1:
            if not students_df.empty:
                st.dataframe(students_df[["student_no", "name_zh"]], use_container_width=True)
            st.markdown("---")
            st.markdown("### 📥 " + t["download_template"])
            col1, col2 = st.columns([1, 2])
            with col1:
                template_bytes = generate_student_template()
                st.download_button(label="📄 " + t["download_template"], data=template_bytes, file_name="学生名单模板.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            with col2:
                st.caption(t["template_help"])
            st.markdown("---")
            uploaded_file = st.file_uploader(t["import_students"], type=['csv', 'xlsx'])
            if uploaded_file:
                df = parse_uploaded_file(uploaded_file)
                if '学号' in df.columns and '姓名' in df.columns:
                    if add_students(supabase, st.session_state.class_id, df):
                        st.success(t["success"])
                        st.rerun()
                else:
                    st.error("文件必须包含「学号」和「姓名」列")
        with tab2:
            try:
                settings_response = supabase.table("school_settings").select("*").eq("class_id", st.session_state.class_id).execute()
                settings = settings_response.data[0] if settings_response.data else {}
            except:
                settings = {}
            exam_name_prefix = settings.get("exam_name_prefix", "")
            exam_name_suffix = settings.get("exam_name_suffix", settings.get("current_academic_year", "2026"))
            default_exam_name = f"{exam_name_prefix}{exam_name_suffix}" if exam_name_prefix else ""
            st.markdown("### 📥 " + t["download_template"])
            grade_template = generate_grade_template(st.session_state.level)
            st.download_button(label="📄 " + t["download_template"], data=grade_template, file_name=f"成绩模板_{st.session_state.class_name_zh}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.caption("📌 注意：副科成绩可以留空或不填写，系统会自动处理")
            st.markdown("---")
            exam_name = st.text_input(t["exam_name"], value=default_exam_name)
            exam_date = st.date_input(t["exam_date"], datetime.now())
            current_year = settings.get("current_academic_year", "2026")
            st.caption(f"当前学年: {current_year}")
            uploaded_file = st.file_uploader(t["import_grades"], type=['csv', 'xlsx'], key="grade_upload")
            if exam_name and uploaded_file:
                df = parse_uploaded_file(uploaded_file)
                if '学号' in df.columns and '姓名' in df.columns:
                    # 标准化列名
                    df.columns = [normalize_column_name(col) for col in df.columns]
                    students = get_students(supabase, st.session_state.class_id)
                    student_map = {str(row["student_no"]): row["id"] for _, row in students.iterrows()}
                    df["student_id"] = df["学号"].astype(str).map(student_map)
                    if df["student_id"].isna().any():
                        missing = df[df["student_id"].isna()]["学号"].tolist()
                        st.error(f"以下学号未在学生名单中找到: {missing}")
                    else:
                        exam_id = add_exam(supabase, st.session_state.class_id, exam_name, exam_date, current_year)
                        if exam_id:
                            if save_grades(supabase, exam_id, df):
                                st.success(t["success"])
                                st.rerun()
                else:
                    st.error("文件必须包含「学号」和「姓名」列")
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
    
    # ========== 班级设置 ==========
    elif menu == t["class_settings"] and st.session_state.is_principal:
        show_class_settings_page(supabase, lang, t, all_classes)
    
    # ========== 系统设置 ==========
    elif menu == t["settings"]:
        show_settings_page(supabase, lang, t)
    
    # ========== 帮助页面 ==========
    else:
        st.header(t["help"])
        if lang == "zh":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4 style="color: #667eea;">📌 快速入门</h4>
            <p><strong>1. 导入学生名单</strong><br>点击「下载模板」，填写后上传（需包含学号、姓名）</p>
            <p><strong>2. 导入考试成绩</strong><br>下载成绩模板，填写各科成绩后上传（副科可留空）</p>
            <p><strong>3. 查看分析</strong><br>选择学生查看成绩趋势图、雷达图，可下载报告</p>
            <p><strong>4. 班主任管理</strong><br>校领导可在「班级设置」中修改班主任姓名</p>
            </div>
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4 style="color: #667eea;">📊 科目说明</h4>
            <p><strong>核心科目：</strong>华文(BC)、国文(BM)、英文(BI)、数学(MT)、科学(SN)、历史(SEJ)</p>
            <p><strong>副科：</strong>体育(PJPK)、美术(PSV)、音乐(MUZIK)、道德(MORAL)、技术与工艺(RBT)</p>
            <p>💡 没有考的副科可以不填写，不影响系统使用</p>
            </div>
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4 style="color: #667eea;">🔐 权限说明</h4>
            <p><strong>班主任</strong> - 只能查看和操作本班数据</p>
            <p><strong>校领导</strong> - 可查看所有班级，管理班主任信息</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4 style="color: #667eea;">📌 Panduan Pantas</h4>
            <p><strong>1. Import Senarai Pelajar</strong><br>Klik 'Muat Turun Templat', isi dan muat naik</p>
            <p><strong>2. Import Markah</strong><br>Muat turun templat markah, isi markah (subjek elektif boleh dikosongkan)</p>
            <p><strong>3. Analisis</strong><br>Pilih pelajar untuk lihat carta trend dan radar</p>
            <p><strong>4. Pengurusan Guru</strong><br>Pentadbir boleh ubah nama guru di 'Tetapan Kelas'</p>
            </div>
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4 style="color: #667eea;">📊 Penerangan Subjek</h4>
            <p><strong>Subjek Teras:</strong> BC, BM, BI, MT, SN, SEJ</p>
            <p><strong>Subjek Elektif:</strong> PJPK, PSV, Muzik, Moral, RBT</p>
            <p>💡 Subjek yang tidak diambil boleh dikosongkan</p>
            </div>
            """, unsafe_allow_html=True)

# ========== 运行入口 ==========
if __name__ == "__main__":
    init_session_state()
    supabase = init_supabase()
    if not supabase:
        st.warning("⚠️ Supabase 连接失败，请检查 Secrets 配置")
        st.stop()
    if not st.session_state.authenticated:
        login_page(supabase)
    else:
        main_app(supabase)
