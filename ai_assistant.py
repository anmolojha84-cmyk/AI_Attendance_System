import time
from google import genai
from config import GEMINI_API_KEY

# -------------------------------
# Gemini Client
# -------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)


def local_ai(student_name, attendance_percentage):

    if attendance_percentage >= 90:
        status = "Excellent"
        performance = "Outstanding attendance record."
        risk = "Very Low"
        suggestion = "Maintain your excellent consistency."
        motivation = "Excellent work! Keep inspiring others."

    elif attendance_percentage >= 75:
        status = "Good"
        performance = "Attendance is satisfactory."
        risk = "Low"
        suggestion = "Try to maintain above 90% attendance."
        motivation = "Consistency is the key to success."

    elif attendance_percentage >= 60:
        status = "Average"
        performance = "Attendance needs improvement."
        risk = "Medium"
        suggestion = "Attend classes more regularly."
        motivation = "Every class is an opportunity to learn."

    else:
        status = "Poor"
        performance = "Attendance is very low."
        risk = "High"
        suggestion = "Attend every class regularly."
        motivation = "It is never too late to improve."

    return f"""
Attendance Status : {status}

Performance :
{performance}

Risk Level :
{risk}

Suggestions :
{suggestion}

Motivation :
{motivation}
"""


def generate_attendance_summary(student_name, attendance_percentage):

    prompt = f"""
You are an AI Attendance Assistant.

Student Name : {student_name}

Attendance Percentage : {attendance_percentage}%

Generate:

1. Attendance Status
2. Performance
3. Risk Level
4. Suggestions
5. Motivation

Keep response under 150 words.
"""

    for i in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as e:

            print("Gemini Error :", e)
            time.sleep(2)

    print("Switching to Local AI...")

    return local_ai(student_name, attendance_percentage)


# -------------------------------
# Test
# -------------------------------
if __name__ == "__main__":

    print(generate_attendance_summary("Anmol Ojha", 82))