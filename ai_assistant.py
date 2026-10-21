import os
import time
import pandas as pd
from datetime import datetime
from google import genai
from config import GEMINI_API_KEY

# -------------------------------
# Gemini Client Setup
# -------------------------------
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")

PRIMARY_MODEL = "gemini-3.5-flash-lite"
BACKUP_MODEL = "gemini-3.8-flash"


def call_gemini(prompt, system_instruction=None):
    """Safely calls Gemini with model fallback and error handling."""
    if not client:
        return None

    for model_name in [PRIMARY_MODEL, BACKUP_MODEL]:
        try:
            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                **({"config": config} if config else {})
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API ({model_name}) error: {e}")
            time.sleep(1)

    return None


def get_system_attendance_context():
    """Gathers real-time attendance statistics and student information for AI context."""
    today = datetime.now().strftime("%d-%m-%Y")
    attendance_file = os.path.join("Attendance", f"Attendance_{today}.csv")

    registered_students = []
    if os.path.exists("images"):
        registered_students = [
            os.path.splitext(f)[0].upper()
            for f in os.listdir("images")
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

    present_students = []
    attendance_records = []
    if os.path.exists(attendance_file):
        try:
            df = pd.read_csv(attendance_file)
            if not df.empty and "Name" in df.columns:
                present_students = [str(n).upper() for n in df["Name"].tolist()]
                attendance_records = df.to_dict(orient="records")
        except Exception:
            pass

    total_registered = len(registered_students)
    total_present = len(present_students)
    absent_students = [s for s in registered_students if s not in present_students]

    context = {
        "today_date": today,
        "total_registered": total_registered,
        "registered_list": registered_students,
        "total_present": total_present,
        "present_list": present_students,
        "absent_list": absent_students,
        "attendance_rate": f"{(total_present / total_registered * 100):.1f}%" if total_registered > 0 else "N/A",
        "records": attendance_records
    }
    return context


def answer_attendance_query(query, chat_history=None):
    """Answers user queries using fast hybrid intelligence with Gemini AI fallback."""
    ctx = get_system_attendance_context()
    q_lower = query.lower().strip()

    # 1. Instant precision responses for attendance status
    if any(k in q_lower for k in ["present", "upastith", "aaj kaun aaya", "who is present", "who's present"]):
        if ctx["present_list"]:
            names_str = "\n".join([f"• **{n}**" for n in ctx["present_list"]])
            return f"✅ **Today's Present Students ({ctx['total_present']}/{ctx['total_registered']})**:\n\n{names_str}\n\n📊 Current Attendance Rate: **{ctx['attendance_rate']}**"
        else:
            return f"ℹ️ No students have been marked present yet today ({ctx['today_date']}). Total registered: **{ctx['total_registered']}**."

    if any(k in q_lower for k in ["absent", "anupasthit", "chhutti", "who is absent", "who's absent", "who is not here"]):
        if ctx["absent_list"]:
            names_str = "\n".join([f"• **{n}**" for n in ctx["absent_list"]])
            return f"❌ **Today's Absent Students ({len(ctx['absent_list'])}/{ctx['total_registered']})**:\n\n{names_str}\n\nPresent count: **{ctx['total_present']}**"
        else:
            return f"🎉 **100% Attendance Today!** All {ctx['total_registered']} registered students are present."

    if any(k in q_lower for k in ["percentage", "rate", "summary", "report", "aaj ki attendance", "today's attendance", "today attendance"]):
        return f"""📊 **Attendance Summary ({ctx['today_date']})**:
• **Total Registered Students:** {ctx['total_registered']}
• **Present Today:** {ctx['total_present']}
• **Absent Today:** {len(ctx['absent_list'])}
• **Attendance Rate:** {ctx['attendance_rate']}

Present list: {', '.join(ctx['present_list']) if ctx['present_list'] else 'None yet'}"""

    if any(k in q_lower for k in ["registered", "total student", "all student", "student list", "kitne student", "kaun kaun hai"]):
        if ctx["registered_list"]:
            names_str = "\n".join([f"{i+1}. **{n}**" for i, n in enumerate(ctx["registered_list"])])
            return f"👨‍🎓 **Registered Students in Database ({ctx['total_registered']})**:\n\n{names_str}"
        else:
            return "⚠️ No students are currently registered in the database. Please add students in '➕ Register Student'."

    if any(k in q_lower for k in ["developer", "creator", "who made", "kisne banaya", "author"]):
        return "👨‍💻 **Developer Information**:\nDeveloped by **Anmol Ojha**, B.Tech CSE, United Institute of Technology, Prayagraj."

    if any(k in q_lower for k in ["about project", "project details", "technology", "tech stack", "features"]):
        return """🎓 **AI Smart Attendance System**:
• **Face Recognition:** Deep metric learning (128-d embeddings) with 99.38% benchmark accuracy.
• **Cross-Platform:** Works on mobile smartphones (Android/iOS) and laptops via responsive web interface.
• **AI Assistant:** Google Gemini AI integration for contextual student attendance analysis and parent communication.
• **Stack:** Python 3.10, Streamlit, OpenCV, face_recognition, Pandas, Google Gemini API."""

    if any(k in q_lower for k in ["improve", "tips", "advice", "consistency"]):
        return """💡 **Actionable Tips to Improve Student Attendance**:
1. **Regular Monitoring:** Use daily attendance notifications to keep parents informed early.
2. **Attendance Rewards:** Acknowledge and reward students maintaining >90% attendance.
3. **Engaging Lectures:** Incorporate interactive sessions and practical problem-solving.
4. **Early Intervention:** Schedule counseling for students falling below the 75% threshold.
5. **Clear Policy:** Communicate the academic and examination eligibility benefits of regular attendance."""

    # 2. General / complex conversational queries: query Gemini
    system_prompt = f"""
You are the intelligent AI Assistant for the "AI Smart Attendance System" developed by Anmol Ojha (United Institute of Technology, B.Tech CSE).
You are polite, professional, and knowledgeable. Answer in English or Hindi/Hinglish based on the user's question.

LIVE SYSTEM CONTEXT ({ctx['today_date']}):
- Total Registered: {ctx['total_registered']} ({', '.join(ctx['registered_list']) if ctx['registered_list'] else 'None'})
- Present Today: {ctx['total_present']} ({', '.join(ctx['present_list']) if ctx['present_list'] else 'None'})
- Absent Today: {len(ctx['absent_list'])} ({', '.join(ctx['absent_list']) if ctx['absent_list'] else 'None'})
- Rate: {ctx['attendance_rate']}

Keep responses crisp, clear, and well formatted.
"""
    history_text = ""
    if chat_history:
        for msg in chat_history[-3:]:
            role = "User" if msg.get("role") == "user" else "Assistant"
            history_text += f"{role}: {msg.get('content', '')}\n"

    full_prompt = f"{history_text}User Question: {query}\nAssistant:"
    response_text = call_gemini(full_prompt, system_instruction=system_prompt)

    if response_text:
        return response_text

    return f"🤖 I am your AI Attendance Assistant. Today ({ctx['today_date']}), **{ctx['total_present']}** out of **{ctx['total_registered']}** students are present ({ctx['attendance_rate']}). Ask me about attendance, absent students, records, or advice!"


def generate_parent_email(student_name, attendance_percentage, parent_name="Parent/Guardian"):
    """Generates a professional email to parents regarding student attendance."""
    prompt = f"""
Write a formal, compassionate, and professional email to the parent of a student concerning their class attendance.

Details:
- Student Name: {student_name}
- Attendance Percentage: {attendance_percentage}%
- Parent/Guardian: {parent_name}
- Institution: United Institute of Technology, AI Smart Attendance System

Requirements:
- Proper subject line
- Clear status (Excellent/Good/Average/Critical if below 75%)
- Constructive advice on maintaining or improving attendance
- Polite sign-off
Keep it under 180 words.
"""
    ai_email = call_gemini(prompt)
    if ai_email:
        return ai_email

    # Offline Template Fallback
    status = "satisfactory" if attendance_percentage >= 75 else "critically low"
    action = "maintain this consistency" if attendance_percentage >= 75 else "meet with academic counselors to improve attendance"
    return f"""Subject: Academic Attendance Update: {student_name}

Dear {parent_name},

We are writing to provide you with the current academic attendance report for your ward, {student_name}.

As of today, {student_name}'s recorded attendance stands at {attendance_percentage}%, which is currently considered {status}. Regular attendance is vital for academic comprehension, coursework success, and overall excellence.

We kindly request you to discuss this with {student_name} to {action}.

If you have any questions or require support, please do not hesitate to contact the department.

Warm regards,
Academic Coordinator
United Institute of Technology
AI Smart Attendance System
"""


def local_ai(student_name, attendance_percentage):
    if attendance_percentage >= 90:
        status, performance, risk = "Excellent", "Outstanding attendance record.", "Very Low"
        suggestion, motivation = "Maintain your excellent consistency.", "Excellent work! Keep inspiring others."
    elif attendance_percentage >= 75:
        status, performance, risk = "Good", "Attendance is satisfactory.", "Low"
        suggestion, motivation = "Try to maintain above 90% attendance.", "Consistency is the key to success."
    elif attendance_percentage >= 60:
        status, performance, risk = "Average", "Attendance needs improvement.", "Medium"
        suggestion, motivation = "Attend classes regularly to cross 75%.", "Every class is an opportunity to learn."
    else:
        status, performance, risk = "Poor", "Attendance is critically low.", "High"
        suggestion, motivation = "Immediate parent meeting recommended.", "It is never too late to turn things around."

    return f"""Attendance Status : {status}
Performance : {performance}
Risk Level : {risk}
Suggestions : {suggestion}
Motivation : {motivation}"""


def generate_attendance_summary(student_name, attendance_percentage):
    prompt = f"""
You are an AI Attendance Assistant.
Student Name: {student_name}
Attendance: {attendance_percentage}%
Generate: Attendance Status, Performance Evaluation, Risk Level, Actionable Suggestions, and Motivation.
Keep it under 150 words.
"""
    result = call_gemini(prompt)
    if result:
        return result
    return local_ai(student_name, attendance_percentage)


def send_attendance_email(to_email, subject, body):
    """Sends attendance email to parent using configured Gmail SMTP credentials."""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email_config import EMAIL, APP_PASSWORD
    except Exception as e:
        return False, f"Email configuration error: {e}"

    clean_email = to_email.strip() if to_email else ""
    if not clean_email or "@" not in clean_email or "." not in clean_email:
        return False, "Please provide a valid recipient email address."

    if not body.strip():
        return False, "Email content cannot be empty."

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = f"AI Smart Attendance System <{EMAIL}>"
        msg["To"] = clean_email

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=12)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD.replace(" ", ""))
        server.send_message(msg)
        server.quit()
        return True, f"Email sent successfully to {clean_email}!"
    except Exception as e:
        return False, f"Email delivery failed: {e}"


if __name__ == "__main__":
    print(answer_attendance_query("Who is present today?"))