import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

def send_timetable_email(to_email, timetable_data):
    """
    formats and sends the timetable to the specified email address using smtplib.
    requires EMAIL_SENDER and EMAIL_PASSWORD in .env.
    """
    load_dotenv(override=True)
    sender_email = os.environ.get("EMAIL_SENDER")
    sender_password = os.environ.get("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        return False, "email credentials not configured in .env file."

    # create the email structure
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Your Generated Timetable"

    # generate html table from timetable data
    html_content = """
    <html>
      <head>
        <style>
          table { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; }
          th, td { border: 1px solid #dddddd; text-align: center; padding: 8px; }
          th { background-color: #f2f2f2; }
          .priority { font-weight: bold; color: #4daa80; }
        </style>
      </head>
      <body>
        <h2>Your Study Timetable</h2>
        <p>Here is your generated schedule:</p>
        <table>
          <tr>
            <th>Day</th>
            <th>Time</th>
            <th>Subject</th>
            <th>Priority</th>
          </tr>
    """

    for entry in timetable_data:
        html_content += f"""
          <tr>
            <td>{entry.get('day', '')}</td>
            <td>{entry.get('time', '')}</td>
            <td><strong>{entry.get('subject', '')}</strong></td>
            <td class="priority">{entry.get('priority', '')}</td>
          </tr>
        """

    html_content += """
        </table>
        <br>
        <p>Happy studying!</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_content, 'html'))

    try:
        # connect to gmail smtp server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        return True, "email sent successfully"
    except Exception as e:
        return False, str(e)
