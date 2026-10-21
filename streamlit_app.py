import os
import pandas as pd
from PIL import Image
from datetime import datetime
import streamlit as st

import ui_components as ui
import face_module as fm
import ai_assistant as ai
import auth

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Smart Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Responsive CSS
ui.apply_custom_css()

# -----------------------------
# AUTHENTICATION STATE & LOGIC
# -----------------------------
auth.init_user_db()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# If NOT authenticated, display Login & Sign Up Gate
if not st.session_state["authenticated"]:
    with st.sidebar:
        if os.path.exists("assets/college_logo.png"):
            st.image("assets/college_logo.png", width=150)
        else:
            st.markdown("### 🎓 Attendance System")

        st.markdown("""
        <div style="background: rgba(220, 38, 38, 0.1); border: 1px solid rgba(220, 38, 38, 0.2); padding: 8px 12px; border-radius: 8px; font-weight: 700; color: #DC2626; font-size: 13px; margin: 8px 0 14px 0;">
            🔒 Portal Locked
        </div>
        """, unsafe_allow_html=True)
        st.caption("Please sign in or create an account to access Attendance, Camera Recognition, and AI Assistant.")

        st.markdown("---")
        # Mobile QR Connect in Sidebar
        local_ip = ui.get_local_ip()
        phone_url = f"http://{local_ip}:8501"

        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: 12px; text-align: center;">
            <div style="font-size: 12px; font-weight: 800; color: #4338CA;">📱 PHONE ACCESS</div>
            <div style="font-size: 11px; color: #64748B; margin: 3px 0;">Scan to open on phone</div>
        </div>
        """, unsafe_allow_html=True)

        try:
            qr_bytes = ui.generate_qr_code(phone_url)
            st.image(qr_bytes, width=150)
            st.caption(f"`{phone_url}`")
        except Exception:
            st.caption(f"Open: `{phone_url}`")

    # Main Area Login & Sign Up Screen
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; padding-top: 10px;">
        <div class="badge-pill" style="background: rgba(37, 99, 235, 0.12); color: #2563EB; border: 1px solid rgba(37, 99, 235, 0.25);">
            🔐 AUTHORIZED ACCESS ONLY
        </div>
        <h1 style="font-size: clamp(24px, 3.8vw, 36px); font-weight: 800; color: #0F172A; margin: 8px 0 4px 0; letter-spacing: -0.5px;">
            UNITED INSTITUTE OF TECHNOLOGY
        </h1>
        <div style="font-size: clamp(14px, 2vw, 17px); color: #2563EB; font-weight: 700;">
            AI SMART ATTENDANCE SYSTEM
        </div>
        <div style="font-size: 13px; color: #64748B; margin-top: 6px;">
            Faculty & Administrator Authentication Portal
        </div>
    </div>
    """, unsafe_allow_html=True)

    auth_c1, auth_c2, auth_c3 = st.columns([1, 2.4, 1])
    with auth_c2:
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up (New Account)"])

        with tab_login:
            st.markdown("""
            <div style="margin: 10px 0 14px 0;">
                <h3 style="margin: 0; color: #1E293B; font-size: 19px;">Sign In to Portal</h3>
                <p style="margin: 2px 0 0 0; color: #64748B; font-size: 13px;">Enter your username or registered email.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                login_user = st.text_input("Username or Email", placeholder="e.g. admin or faculty@uit.edu", key="login_username_input")
                login_pass = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password_input")
                login_submit = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")

                if login_submit:
                    success, msg, user_data = auth.authenticate_user(login_user, login_pass)
                    if success:
                        st.session_state["authenticated"] = True
                        st.session_state["current_user"] = user_data
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

            st.markdown("""
            <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; padding: 10px 14px; border-radius: 10px; font-size: 12px; color: #475569; margin: 15px 0 10px 0;">
                <strong>💡 Default Admin Login:</strong> Username: <code style="color: #2563EB; font-weight: 700;">admin</code> &nbsp;|&nbsp; Password: <code style="color: #2563EB; font-weight: 700;">1234</code>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("❓ Forgot Password? Reset here"):
                with st.form("reset_pwd_form"):
                    st.caption("Enter your registered username or email, and set a new password.")
                    reset_id = st.text_input("Username or Registered Email", key="reset_id_input")
                    reset_new_pwd = st.text_input("New Password (min 4 chars)", type="password", key="reset_new_pwd_input")
                    reset_confirm = st.text_input("Confirm New Password", type="password", key="reset_confirm_pwd_input")
                    reset_btn = st.form_submit_button("🔄 Update Password", use_container_width=True)
                    if reset_btn:
                        if reset_new_pwd != reset_confirm:
                            st.error("❌ Passwords do not match.")
                        else:
                            r_success, r_msg = auth.reset_password(reset_id, reset_new_pwd)
                            if r_success:
                                st.success(f"✅ {r_msg}")
                            else:
                                st.error(f"❌ {r_msg}")

        with tab_signup:
            st.markdown("""
            <div style="margin: 10px 0 14px 0;">
                <h3 style="margin: 0; color: #1E293B; font-size: 19px;">Create New Account</h3>
                <p style="margin: 2px 0 0 0; color: #64748B; font-size: 13px;">Register new authorized faculty, coordinator, or staff.</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                reg_name = st.text_input("Username (No spaces)", placeholder="e.g. anmol_faculty", key="reg_username_input")
                reg_email = st.text_input("Email Address (Optional)", placeholder="e.g. anmol@uit.edu", key="reg_email_input")
                reg_role = st.selectbox("Designation / Role", ["Faculty / Teacher", "Class Coordinator", "Lab Assistant", "Administrator"], index=0, key="reg_role_input")
                reg_pass1 = st.text_input("Password", type="password", placeholder="Choose password (min 4 chars)", key="reg_pass1_input")
                reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="reg_pass2_input")

                signup_submit = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")

                if signup_submit:
                    if reg_pass1 != reg_pass2:
                        st.error("❌ Passwords do not match. Please re-enter identical passwords.")
                    else:
                        reg_success, reg_msg = auth.register_user(reg_name, reg_pass1, reg_email, reg_role)
                        if reg_success:
                            _, _, user_info = auth.authenticate_user(reg_name, reg_pass1)
                            st.session_state["authenticated"] = True
                            st.session_state["current_user"] = user_info or {"username": reg_name, "email": reg_email, "role": reg_role}
                            st.success(f"🎉 {reg_msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {reg_msg}")

    # Stop execution when unauthenticated
    st.stop()

# -----------------------------
# AUTHENTICATED USER SESSION
# -----------------------------
user_info = st.session_state.get("current_user") or {"username": "Admin", "role": "Faculty"}
curr_user = user_info.get("username", "Admin")
curr_role = user_info.get("role", "Faculty")

# -----------------------------
# SIDEBAR (FOR AUTHENTICATED USERS)
# -----------------------------
with st.sidebar:
    if os.path.exists("assets/college_logo.png"):
        st.image("assets/college_logo.png", width=150)
    else:
        st.markdown("### 🎓 Attendance System")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: white; padding: 12px 14px; border-radius: 12px; margin: 8px 0 10px 0; box-shadow: 0 4px 10px rgba(15, 23, 42, 0.15);">
        <div style="font-size: 10px; opacity: 0.8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">🟢 Logged In User</div>
        <div style="font-size: 15px; font-weight: 800; margin-top: 2px;">👤 {curr_user}</div>
        <div style="font-size: 11px; opacity: 0.9; margin-top: 3px;">Role: <span style="background: rgba(255,255,255,0.2); padding: 1px 6px; border-radius: 4px;">{curr_role}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out / Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = None
        st.rerun()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📷 Face Recognition",
            "➕ Register Student",
            "👨‍🎓 Students",
            "📊 Attendance",
            "📈 Analytics",
            "🤖 AI Assistant",
            "📧 Parent Email",
            "🛠 Technology Stack",
            "📸 Project Gallery",
            "👨‍💻 About Developer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Mobile QR Connect in Sidebar
    local_ip = ui.get_local_ip()
    phone_url = f"http://{local_ip}:8501"

    st.markdown(f"""
    <div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: 12px; text-align: center;">
        <div style="font-size: 12px; font-weight: 800; color: #4338CA;">📱 PHONE ACCESS</div>
        <div style="font-size: 11px; color: #64748B; margin: 3px 0;">Scan with phone camera</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        qr_bytes = ui.generate_qr_code(phone_url)
        st.image(qr_bytes, width=150)
        st.caption(f"`{phone_url}`")
    except Exception:
        st.caption(f"Open: `{phone_url}`")

    zip_file_path = r"C:\Users\Anmol\Desktop\AI_Attendance_System_Updated.zip"
    if os.path.exists(zip_file_path):
        with open(zip_file_path, "rb") as zf:
            st.download_button(
                label="📥 Download App (.ZIP)",
                data=zf.read(),
                file_name="AI_Attendance_System_Updated.zip",
                mime="application/zip",
                use_container_width=True
            )


# -----------------------------
# HOME PAGE
# -----------------------------
if page == "🏠 Home":
    st.markdown(f"""
    <div class="hero-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div class="badge-pill">● AI SMART SYSTEM LIVE</div>
            <div style="font-size: 13px; color: #BFDBFE; font-weight: 600;">👤 Active: <b>{curr_user}</b> ({curr_role})</div>
        </div>
        <h1 class="hero-title">AI SMART ATTENDANCE SYSTEM</h1>
        <div class="hero-sub">Face Recognition & Gemini AI Attendance Monitoring (Laptop & Mobile)</div>
    </div>
    """, unsafe_allow_html=True)

    # Real-time Metrics Calculation
    reg_students = fm.get_registered_students()
    total_reg = len(reg_students)

    df_today = fm.get_today_attendance()
    today_present_count = len(df_today) if not df_today.empty else 0
    today_absent_count = max(0, total_reg - today_present_count)
    att_rate = f"{(today_present_count / total_reg * 100):.1f}%" if total_reg > 0 else "0.0%"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">👨‍🎓 Registered Students</div>
            <div class="metric-number" style="color: #2563EB;">{total_reg}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">✅ Present Today</div>
            <div class="metric-number" style="color: #059669;">{today_present_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">❌ Absent Today</div>
            <div class="metric-number" style="color: #DC2626;">{today_absent_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">📊 Attendance Rate</div>
            <div class="metric-number" style="color: #7C3AED;">{att_rate}</div>
        </div>
        """, unsafe_allow_html=True)

    # Mobile Connect Banner
    st.markdown(f"""
    <div class="phone-banner">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px;">
            <div>
                <h3 style="margin: 0; color: white;">📱 Open on Your Phone</h3>
                <p style="margin: 6px 0 0 0; color: #E0E7FF; font-size: 14px; line-height: 1.5;">
                    1. Connect your phone to the same Wi-Fi / Hotspot as this laptop.<br>
                    2. Scan the QR Code or visit: <b style="color: #FDE047;">{phone_url}</b><br>
                    3. Mark attendance using your smartphone camera directly in the browser!
                </p>
            </div>
            <div style="background: white; padding: 6px 12px; border-radius: 10px; text-align: center;">
                <span style="color: #1E1B4B; font-size: 12px; font-weight: 800;">CROSS-PLATFORM</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1.3, 0.7])

    with col_a:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0; color: #1E293B;">📋 Today's Live Attendance Feed</h3>
        """, unsafe_allow_html=True)

        if not df_today.empty:
            st.dataframe(df_today, use_container_width=True)
        else:
            st.info("No attendance marked yet today. Go to '📷 Face Recognition' to scan faces.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0; color: #1E293B;">📖 Project Information</h3>
            <p style="color: #475569; font-size: 14px; line-height: 1.6;">
                AI Smart Attendance Monitoring System utilizes deep facial recognition to identify students and log attendance automatically.
            </p>
            <p style="color: #1E3A8A; font-weight: 700; font-size: 13px; margin: 8px 0 0 0;">
                Developer: Anmol Ojha<br>
                United Institute of Technology
            </p>
        </div>
        """, unsafe_allow_html=True)
# ==========================================
# FACE RECOGNITION PAGE
# ==========================================

elif page == "📷 Face Recognition":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">📷 Face Recognition Attendance Scanner</h2>
        <div class="hero-sub">Works seamlessly with your Phone Camera or Laptop Webcam</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📸 Live Camera Scanner", "📁 Upload Picture", "ℹ️ How It Works"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 8px 0; color: #1E3A8A;">Live Camera Scanner</h4>
            <p style="color: #64748B; font-size: 14px; margin-bottom: 12px;">
                Works with front or back camera on phones, and webcams on laptops.
            </p>
        """, unsafe_allow_html=True)

        cam_pic = st.camera_input("Scan Student Face")

        if cam_pic is not None:
            pil_img = Image.open(cam_pic)
            with st.spinner("🔍 AI Face Recognition in progress..."):
                results, err = fm.match_faces_in_image(pil_img)

            if err:
                st.warning(f"⚠️ {err}")
            else:
                for match in results:
                    name = match["name"]
                    conf = match["confidence"]

                    if match["status"] == "Matched":
                        ok, msg = fm.mark_student_attendance(name)
                        if ok:
                            st.balloons()
                            st.markdown(f"""
                            <div class="success-banner">
                                <h3 style="margin:0; color:white;">✅ Attendance Marked!</h3>
                                <p style="margin:6px 0 0 0; font-size:16px;">
                                    Student: <b>{name}</b> &bull; Confidence: <b>{conf}%</b>
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            ui.play_browser_voice(f"Attendance marked for {name}")
                        else:
                            st.info(f"ℹ️ {msg} (Confidence: {conf}%)")
                    else:
                        st.error("⚠️ UNKNOWN FACE: Face not recognized in student database.")
                        st.caption("Please enroll this student first in '➕ Register Student'.")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 8px 0; color: #1E3A8A;">Upload Image to Verify Attendance</h4>
        """, unsafe_allow_html=True)

        up_file = st.file_uploader("Choose student picture", type=["jpg", "jpeg", "png"])
        if up_file:
            pil_img = Image.open(up_file)
            st.image(pil_img, width=240, caption="Uploaded Image")

            if st.button("🚀 Process Face & Mark Attendance", key="btn_up_mark", type="primary"):
                with st.spinner("Processing..."):
                    results, err = fm.match_faces_in_image(pil_img)

                if err:
                    st.warning(f"⚠️ {err}")
                else:
                    for match in results:
                        name = match["name"]
                        conf = match["confidence"]
                        if match["status"] == "Matched":
                            ok, msg = fm.mark_student_attendance(name)
                            if ok:
                                st.success(f"✅ Attendance marked for **{name}** ({conf}% match)!")
                                ui.play_browser_voice(f"Attendance marked for {name}")
                            else:
                                st.info(f"ℹ️ {msg}")
                        else:
                            st.error("⚠️ Unknown face detected.")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color:#1E3A8A;">Deep Learning Face Recognition Pipeline</h4>
            <ol style="font-size: 15px; line-height: 1.8; color: #334155;">
                <li><b>Input Capture:</b> High-resolution photo via phone camera or laptop webcam.</li>
                <li><b>Face Detection:</b> HOG (Histogram of Oriented Gradients) extracts facial bounding regions.</li>
                <li><b>Pose & Landmark Alignment:</b> Normalizes face orientation using 68 facial landmark coordinates.</li>
                <li><b>128-d Embedding Generation:</b> ResNet-based deep metric network outputs a 128-dimensional embedding.</li>
                <li><b>Distance Classification:</b> Compares euclidean distance with registered encodings (threshold &le; 0.50).</li>
                <li><b>Attendance Logging:</b> Appends student name, timestamp, and status to today's CSV sheet.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# REGISTER STUDENT PAGE
# ==========================================

elif page == "➕ Register Student":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">➕ Register New Student</h2>
        <div class="hero-sub">Enroll students and compute 128-d face encodings right from Phone or Laptop</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        new_name = st.text_input("Student Full Name *", placeholder="e.g. AMIT KUMAR")
        student_id = st.text_input("Roll No / Student ID (Optional)", placeholder="e.g. 2026CS101")
        src_mode = st.radio("Photo Capture Method", ["📸 Camera (Phone/Webcam)", "📁 Upload Image File"])

    photo_captured = None

    with c2:
        if "Camera" in src_mode:
            cam = st.camera_input("Capture Student Face")
            if cam:
                photo_captured = Image.open(cam)
        else:
            up = st.file_uploader("Upload Student Portrait (Clear Face)", type=["jpg", "jpeg", "png"])
            if up:
                photo_captured = Image.open(up)
                st.image(photo_captured, width=200, caption="Preview")

    if st.button("✨ Enroll Student in Database", type="primary", use_container_width=True):
        if not new_name.strip():
            st.error("Please enter the student's name.")
        elif photo_captured is None:
            st.error("Please capture or upload a student photo.")
        else:
            with st.spinner("Generating face encoding and updating database..."):
                ok, msg = fm.register_new_student(new_name, photo_captured)

            if ok:
                st.success(f"🎉 {msg}")
                ui.play_browser_voice(f"Student {new_name} enrolled successfully")
            else:
                st.error(f"❌ {msg}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STUDENTS PAGE
# ==========================================

elif page == "👨‍🎓 Students":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">👨‍🎓 Registered Student Directory</h2>
        <div class="hero-sub">All enrolled students with verified facial embeddings</div>
    </div>
    """, unsafe_allow_html=True)

    students = fm.get_registered_students()
    st.markdown(f"**Total Registered Students:** `{len(students)}`")

    q = st.text_input("🔍 Filter by Student Name", placeholder="Type student name...")
    if q:
        students = [s for s in students if q.upper() in s]

    if not students:
        st.info("No registered students found matching your query.")
    else:
        cols = st.columns(4)
        for i, student in enumerate(students):
            col = cols[i % 4]
            img_path = os.path.join("images", f"{student}.jpg")
            with col:
                st.markdown("""<div class="glass-card" style="text-align: center; padding: 14px;">""", unsafe_allow_html=True)
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    st.markdown("👤", unsafe_allow_html=True)
                st.markdown(f"<b style='color:#1E3A8A; font-size:15px;'>{student}</b>", unsafe_allow_html=True)
                st.caption("Status: Active")
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ATTENDANCE PAGE
# ==========================================

elif page == "📊 Attendance":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">📊 Attendance Reports & Logs</h2>
        <div class="hero-sub">View, filter, and export daily attendance sheets</div>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists("Attendance"):
        reports = [f for f in os.listdir("Attendance") if f.endswith(".csv")]
        reports.sort(reverse=True)

        if reports:
            selected = st.selectbox("Select Attendance Sheet", reports)
            path = os.path.join("Attendance", selected)
            df = pd.read_csv(path)

            st.markdown(f"### Record: `{selected}` ({len(df)} Students Marked)")
            st.dataframe(df, use_container_width=True)

            csv_raw = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV Sheet",
                data=csv_raw,
                file_name=selected,
                mime="text/csv",
                type="primary"
            )
        else:
            st.info("No attendance reports found in Attendance folder.")
    else:
        st.warning("Attendance folder not found.")

# ==========================================
# ANALYTICS PAGE
# ==========================================

elif page == "📈 Analytics":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">📈 Attendance Analytics Dashboard</h2>
        <div class="hero-sub">Visual trends, presence rate, and class consistency insights</div>
    </div>
    """, unsafe_allow_html=True)

    dates, counts = [], []
    if os.path.exists("Attendance"):
        files = [f for f in os.listdir("Attendance") if f.endswith(".csv")]
        files.sort()
        for f in files[-10:]:
            d_str = f.replace("Attendance_", "").replace(".csv", "")
            try:
                df = pd.read_csv(os.path.join("Attendance", f))
                dates.append(d_str)
                counts.append(len(df))
            except Exception:
                pass

    if dates:
        chart_data = pd.DataFrame({"Date": dates, "Present Students": counts})
        st.markdown("#### 📅 Attendance Numbers Over Recent Sessions")
        st.bar_chart(chart_data.set_index("Date"))
        st.line_chart(chart_data.set_index("Date"))
    else:
        st.info("Record daily attendance over multiple days to view analytics graphs.")

# ==========================================
# AI ASSISTANT PAGE
# ==========================================

elif page == "🤖 AI Assistant":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">🤖 Gemini AI Attendance Assistant</h2>
        <div class="hero-sub">Context-Aware AI Assistant powered by Google Gemini (gemini-3.5-flash-lite)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#64748B; font-weight:700; font-size:13px;'>QUICK QUERIES:</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    prompt_to_send = None
    if c1.button("📋 Who is present today?", use_container_width=True):
        prompt_to_send = "Who is present today?"
    if c2.button("❌ Who is absent today?", use_container_width=True):
        prompt_to_send = "Who is absent today?"
    if c3.button("📈 Attendance rate?", use_container_width=True):
        prompt_to_send = "What is today's attendance percentage and summary?"
    if c4.button("💡 Tips to improve?", use_container_width=True):
        prompt_to_send = "Give actionable tips for students to improve attendance consistency."

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I am your AI Attendance Assistant. I have live access to today's student attendance and database. How can I help you?"
            }
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask any question about today's attendance, students, or project...")
    if user_query:
        prompt_to_send = user_query

    if prompt_to_send:
        st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Gemini AI is answering..."):
                reply = ai.answer_attendance_query(prompt_to_send, chat_history=st.session_state.chat_history[:-1])
            st.markdown(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Chat cleared. Ask me any question!"}
        ]
        st.rerun()

# ==========================================
# AI PARENT EMAIL
# ==========================================

elif page == "📧 Parent Email":
    st.markdown("""
    <div class="hero-card">
        <h2 class="hero-title">📧 AI Parent Notification Email</h2>
        <div class="hero-sub">Generate personalized attendance emails with Gemini AI & Send directly to Parents</div>
    </div>
    """, unsafe_allow_html=True)

    registered = fm.get_registered_students()

    st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if registered:
            selected_student = st.selectbox("Select Student", registered)
        else:
            selected_student = st.text_input("Student Name", "ANMOL")

        parent_name = st.text_input("Parent / Guardian Name", "Parent / Guardian")
        parent_email = st.text_input("Parent Email Address *", placeholder="e.g. parent@gmail.com")

    with col2:
        attendance_val = st.slider("Attendance Percentage (%)", 0, 100, 72)
        tone = st.selectbox("Email Tone", ["Formal & Constructive", "Urgent / Low Attendance Alert", "Praise & Encouragement"])
        sender_account = "anmolojha84@gmail.com"
        st.caption(f"Emails will be dispatched securely from: `{sender_account}`")

    # Default template if not yet generated
    default_subj = f"Student Attendance Update: {selected_student} ({attendance_val}%)"
    if "parent_email_subj" not in st.session_state:
        st.session_state.parent_email_subj = default_subj

    if "parent_email_body" not in st.session_state:
        st.session_state.parent_email_body = f"""Dear {parent_name},

This is an academic attendance notification regarding your ward, {selected_student}.
Their current recorded attendance stands at {attendance_val}%.

Regular class attendance is vital for conceptual understanding and overall academic success. Please discuss this report with {selected_student}.

Warm regards,
AI Smart Attendance System
United Institute of Technology"""

    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("✨ Draft Personalized Email with Gemini AI", use_container_width=True):
            with st.spinner("🤖 Gemini AI is drafting a personalized email..."):
                generated = ai.generate_parent_email(selected_student, attendance_val, parent_name=parent_name)
                st.session_state.parent_email_body = generated
                st.session_state.parent_email_subj = default_subj
                st.rerun()

    st.markdown("---")
    st.subheader("📝 Email Preview & Editing")

    subj_input = st.text_input("Email Subject Line", value=st.session_state.parent_email_subj)
    body_input = st.text_area("Email Content (Editable)", value=st.session_state.parent_email_body, height=220)

    st.write("")
    send_col1, send_col2 = st.columns([1.5, 1])

    with send_col1:
        if st.button("📤 Send Email to Parent Now", type="primary", use_container_width=True):
            if not parent_email.strip():
                st.error("⚠️ Please enter the Parent's Email Address above before sending.")
            elif "@" not in parent_email or "." not in parent_email:
                st.error("⚠️ Please enter a valid email address (e.g. parent@gmail.com).")
            else:
                with st.spinner(f"Sending email to {parent_email} via Gmail SMTP..."):
                    ok, msg = ai.send_attendance_email(parent_email, subj_input, body_input)

                if ok:
                    st.balloons()
                    st.success(f"🎉 {msg}")
                    ui.play_browser_voice("Email sent successfully to parent")
                else:
                    st.error(f"❌ {msg}")

    with send_col2:
        import urllib.parse
        mailto_url = f"mailto:{parent_email}?subject={urllib.parse.quote(subj_input)}&body={urllib.parse.quote(body_input)}"
        st.markdown(f"""
        <a href="{mailto_url}" target="_blank" style="text-decoration:none;">
            <button style="width:100%; min-height:44px; background:#F1F5F9; border:1px solid #CBD5E1; border-radius:10px; font-weight:700; color:#334155; cursor:pointer;">
                📨 Open in Mail App
            </button>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

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