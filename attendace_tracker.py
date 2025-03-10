import sqlite3
import smtplib
from email.mime.text import MIMEText

# Constants
THRESHOLD_PERCENTAGE = 70
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
SUBJECTS = [
    "Basic Mechanical Engineering",
    "Engineering Physics",
    "Differential Equation",
    "CS",
    "Mechanical Workshop",
    "Physics Lab",
    "Communication Lab",
    "CS Lab",
    "HS Communication",
    "HS Ethics"
]

# Database setup
def setup_database():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            total_classes INTEGER,
            attended_classes INTEGER,
            student_email TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to add or update attendance
def update_attendance(subject, attended, total, email):
    if subject not in SUBJECTS:
        print(f"Invalid subject: {subject}")
        return

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM attendance WHERE subject=? AND student_email=?", (subject, email))
    record = cursor.fetchone()
    
    if record:
        cursor.execute("""
            UPDATE attendance SET attended_classes = attended_classes + ?, total_classes = total_classes + ?
            WHERE subject = ? AND student_email = ?
        """, (attended, total, subject, email))
    else:
        cursor.execute("INSERT INTO attendance (subject, attended_classes, total_classes, student_email) VALUES (?, ?, ?, ?)", 
                       (subject, attended, total, email))
    
    conn.commit()
    conn.close()
    
# Function to check attendance and send email if necessary
def check_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT subject, attended_classes, total_classes, student_email,
               (attended_classes * 100.0 / total_classes) AS attendance_percentage
        FROM attendance
        WHERE total_classes > 0
    """)
    records = cursor.fetchall()
    
    for subject, attended, total, email, percentage in records:
        if percentage < THRESHOLD_PERCENTAGE:
            send_email_alert(subject, percentage, email)
    
    conn.close()

# Function to send email alert
def send_email_alert(subject, percentage, email):
    body = f"Your attendance in {subject} is {percentage:.2f}%, which is below the required threshold of {THRESHOLD_PERCENTAGE}%. Attend more classes to avoid issues."
    msg = MIMEText(body)
    msg["Subject"] = "Low Attendance Warning"
    msg["From"] = EMAIL_SENDER
    msg["To"] = email
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, msg.as_string())
        print(f"Email sent to {email} for {subject}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

if __name__ == "__main__":
    setup_database()
    
    # Example usage
    update_attendance("Basic Mechanical Engineering", 1, 1, "student@example.com")
    update_attendance("Engineering Physics", 0, 1, "student@example.com")
    
    check_attendance()
