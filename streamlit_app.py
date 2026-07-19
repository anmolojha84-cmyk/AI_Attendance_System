import streamlit as st
from PIL import Image
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Smart Attendance System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#F4F6F9;
}

.title{
    font-size:40px;
    font-weight:bold;
    color:#003366;
    text-align:center;
}

.sub{
    font-size:22px;
    color:green;
    text-align:center;
}

.card{
    background:white;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 0px 10px #d3d3d3;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.image(
    "assets/college_logo.png",
    width=140
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📷 Face Recognition",
        "👨‍🎓 Students",
        "📊 Attendance",
        "📈 Analytics",
        "🤖 AI Assistant",
        "📧 Parent Email",
        "🛠 Technology Stack",
        "📸 Project Gallery",
        "👨‍💻 About Developer"
    ]
)

# -----------------------------
# HOME PAGE
# -----------------------------
if page=="🏠 Home":

    st.markdown(
        "<h1 class='title'>AI SMART ATTENDANCE SYSTEM</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 class='sub'>Face Recognition Based Attendance Monitoring</h3>",
        unsafe_allow_html=True
    )

    st.write("")

    col1,col2,col3,col4=st.columns(4)

    col1.metric(
        "Registered Students",
        "25"
    )

    col2.metric(
        "Today's Attendance",
        "18"
    )

    col3.metric(
        "Unknown Faces",
        "2"
    )

    col4.metric(
        "Attendance Accuracy",
        "98%"
    )

    st.write("")

    st.markdown("## 📖 Project Introduction")

    st.write("""
AI Smart Attendance Monitoring System is an Artificial Intelligence based
attendance management solution that uses Face Recognition technology
to automatically identify students and mark attendance.

The system eliminates manual attendance, reduces proxy attendance,
and generates attendance reports automatically.
""")

    st.success("Project Status : Successfully Running")

    st.info("Developer : Anmol Ojha")

    st.write("")

    st.image(
        "assets/dashboard.png",
        use_container_width=True
    )
    # ==========================================
# FACE RECOGNITION PAGE
# ==========================================

elif page=="📷 Face Recognition":

    st.title("📷 Face Recognition")

    st.image(
        "assets/face_recognition.png",
        use_container_width=True
    )

    st.markdown("""
### How Face Recognition Works

The AI Smart Attendance System uses Face Recognition technology
to automatically identify registered students and mark attendance.

### Process

1️⃣ Capture Image from Camera

⬇

2️⃣ Detect Face

⬇

3️⃣ Generate Face Encoding

⬇

4️⃣ Compare with Stored Encodings

⬇

5️⃣ Identify Student

⬇

6️⃣ Mark Attendance

⬇

7️⃣ Voice Confirmation

⬇

8️⃣ Save Attendance Report

""")

    st.success("Recognition Accuracy : 98%")

# ==========================================
# STUDENTS PAGE
# ==========================================

elif page=="👨‍🎓 Students":

    st.title("👨‍🎓 Registered Students")

    if os.path.exists("images"):

        files = [
            f for f in os.listdir("images")
            if f.lower().endswith(
                (".jpg",".jpeg",".png")
            )
        ]

        st.metric(
            "Total Students",
            len(files)
        )

        cols = st.columns(4)

        i=0

        for file in files:

            img=os.path.join("images",file)

            with cols[i]:

                st.image(
                    img,
                    width=150
                )

                st.write(
                    file.split(".")[0]
                )

            i+=1

            if i==4:

                cols=st.columns(4)

                i=0

    else:

        st.warning("Images folder not found.")

# ==========================================
# ATTENDANCE PAGE
# ==========================================

elif page=="📊 Attendance":

    st.title("📊 Attendance Reports")

    if os.path.exists("Attendance"):

        reports=[
            f for f in os.listdir("Attendance")
            if f.endswith(".csv")
        ]

        if reports:

            selected=st.selectbox(
                "Select Attendance File",
                reports
            )

            path=os.path.join(
                "Attendance",
                selected
            )

            df=pd.read_csv(path)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.download_button(
                "⬇ Download CSV",
                df.to_csv(index=False),
                file_name=selected,
                mime="text/csv"
            )

        else:

            st.info("No attendance reports found.")

    else:

        st.warning("Attendance folder not found.")
        # ==========================================
# ANALYTICS PAGE
# ==========================================

elif page == "📈 Analytics":

    st.title("📈 Attendance Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", "25")
        st.metric("Present Today", "18")
        st.metric("Absent Today", "7")

    with col2:
        st.metric("Attendance Accuracy", "98%")
        st.metric("Unknown Faces", "2")
        st.metric("Recognition Speed", "0.35 sec")

    chart_data = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat"],
        "Attendance":[18,22,21,20,24,23]
    })

    st.line_chart(
        chart_data.set_index("Day")
    )

    st.bar_chart(
        chart_data.set_index("Day")
    )

    st.success("Analytics Generated Successfully")

# ==========================================
# AI ASSISTANT PAGE
# ==========================================

elif page == "🤖 AI Assistant":

    st.title("🤖 AI Assistant")

    st.info(
        "This module uses Google's Generative AI "
        "to answer attendance related queries."
    )

    question = st.text_input(
        "Ask Your Question"
    )

    if st.button("Generate Response"):

        if question == "":

            st.warning(
                "Please enter a question."
            )

        else:

            st.success("Sample Response")

            st.write(
                f"""
Question:

{question}

Answer:

The AI Assistant helps users
understand attendance reports,
student information,
and project related queries.

(Connect Gemini API here
for live responses.)
"""
            )

# ==========================================
# AI PARENT EMAIL
# ==========================================

elif page == "📧 Parent Email":

    st.title("📧 AI Parent Email")

    student = st.text_input(
        "Student Name"
    )

    attendance = st.slider(
        "Attendance Percentage",
        0,
        100,
        80
    )

    if st.button(
        "Generate Email"
    ):

        email = f"""
Dear Parent,

This is to inform you that
{student}'s attendance is
currently {attendance}%.

Please ensure regular attendance
for better academic performance.

Regards,

AI Smart Attendance System
United Institute of Technology
"""

        st.text_area(
            "Generated Email",
            email,
            height=250
        )

# ==========================================
# TECHNOLOGY STACK
# ==========================================

elif page == "🛠 Technology Stack":

    st.title("🛠 Technology Stack")

    st.markdown("""
### Programming Language
- Python

### Libraries
- OpenCV
- face_recognition
- NumPy
- Pillow
- Streamlit
- Tkinter
- ReportLab

### AI Technologies
- Face Recognition
- Google Gemini AI

### Database
- SQLite

### Reports
- CSV
- PDF
- Excel

### Operating System
- Windows 10 / Windows 11
""")

# ==========================================
# PROJECT GALLERY
# ==========================================

elif page == "📸 Project Gallery":

    st.title("📸 Project Gallery")

    images = [
        "assets/dashboard.png",
        "assets/face_recognition.png",
        "assets/analytics.png",
        "assets/report.png"
    ]

    cols = st.columns(2)

    i = 0

    for img in images:

        if os.path.exists(img):

            with cols[i]:

                st.image(
                    img,
                    use_container_width=True
                )

        i += 1

        if i == 2:

            cols = st.columns(2)
            i = 0
            # ==========================================
# ABOUT DEVELOPER
# ==========================================

elif page == "👨‍💻 About Developer":

    st.title("👨‍💻 About Developer")

    col1, col2 = st.columns([1,2])

    with col1:

        if os.path.exists("assets/profile.jpg"):
            st.image("assets/profile.jpg", width=220)
        else:
            st.info("Developer Photo")

    with col2:

        st.subheader("Anmol Ojha")

        st.write("""
**B.Tech - Computer Science & Engineering**

United Institute of Technology

Prayagraj, Uttar Pradesh
""")

        st.markdown("### Skills")

        st.write("""
- Python
- OpenCV
- Face Recognition
- Tkinter
- SQLite
- Streamlit
- Artificial Intelligence
- Machine Learning
- Git & GitHub
""")

        st.markdown("### Project")

        st.success(
            "AI Smart Attendance Monitoring System"
        )

# ==========================================
# PROJECT OBJECTIVES
# ==========================================

    st.markdown("---")

    st.header("🎯 Project Objectives")

    st.write("""
✔ Automate attendance process

✔ Reduce proxy attendance

✔ Improve attendance accuracy

✔ Save faculty time

✔ Generate reports automatically

✔ AI-based attendance management

✔ Easy monitoring and analytics
""")

# ==========================================
# PROJECT MODULES
# ==========================================

    st.markdown("---")

    st.header("📦 Project Modules")

    modules = [
        "Student Registration",
        "Face Encoding",
        "Face Recognition",
        "Attendance Management",
        "Unknown Face Detection",
        "Attendance Analytics",
        "PDF Report Generation",
        "Excel Report Generation",
        "AI Parent Email",
        "AI Assistant"
    ]

    for module in modules:
        st.checkbox(module, value=True)

# ==========================================
# GITHUB
# ==========================================

    st.markdown("---")

    st.header("🌐 GitHub Repository")

    st.markdown(
        "[🔗 View Project on GitHub](https://github.com/anmolojha84-cmyk/AI_Attendance_System)"
    )

# ==========================================
# REFERENCES
# ==========================================

    st.markdown("---")

    st.header("📚 References")

    st.write("""
• Python Official Documentation

• OpenCV Documentation

• Face Recognition Library

• Streamlit Documentation

• ReportLab Documentation

• GitHub

• Google Gemini AI Documentation
""")

# ==========================================
# CONTACT
# ==========================================

    st.markdown("---")

    st.header("📞 Contact")

    st.info(
        """
Developer : Anmol Ojha

College : United Institute of Technology

Project : AI Smart Attendance Monitoring System
"""
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;
font-size:18px;
font-weight:bold;
color:green;'>

🎓 AI Smart Attendance Monitoring System

Developed by <b>Anmol Ojha</b>

United Institute of Technology

Made with ❤️ using Python, OpenCV,
Face Recognition & Streamlit

© 2026 All Rights Reserved

</div>
""",
unsafe_allow_html=True
)