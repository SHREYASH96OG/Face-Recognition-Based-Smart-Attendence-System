import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "faceattendance01@gmail.com"
APP_PASSWORD = "fanihodzptgurmra"


print("Mail Start")
msg = EmailMessage()
msg['Subject'] = "Student Face Attendance Using Image Processing"
msg['From'] = SENDER_EMAIL
msg['To'] = "hrutiksargar@gmail.com"
msg.set_content('Todays Student Face Attendance Xls sheet is attached Please find attachment')

with open('C:/Users/Hrutik/OneDrive/Desktop/final BE Project/100%-Face Attendance with Excel Sheet/100%-Face Attendance with Excel Sheet/pandas_to_excel.xls', 'rb') as f:
        file_data = f.read()
msg.add_attachment(file_data, maintype="application", subtype="vnd.ms-excel", filename='C:/Users/Hrutik/OneDrive/Desktop/final BE Project/100%-Face Attendance with Excel Sheet/100%-Face Attendance with Excel Sheet/pandas_to_excel.xls')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
        print("Mail send successfully")
