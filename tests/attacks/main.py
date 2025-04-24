import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from uuid import uuid4
def send_email(sender, recipients, subject, html_file):
    tracking_id = str(uuid4())
    with open(html_file, 'r') as f:
        html_content = f.read()
    tracking_pixel = f'<img src="http://192.168.244.129:5000/track/{tracking_id}" width="1" height="1">'
    html_content = html_content.replace('<!-- TRACKING_PIXEL -->', tracking_pixel)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    with smtplib.SMTP('192.168.50.52', 1025) as server:
        server.sendmail(sender, recipients, msg.as_string())
    print(f"Письмо отправлено. Tracking ID: {tracking_id}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sender', required=True,
                        help='Отправитель (например: "Конкурс шейдеров <noreply@example.com>")')
    parser.add_argument('-r', '--recipients', nargs='+', required=True,
                        help='Получатели через пробел')
    parser.add_argument('-su', '--subject', required=True,
                        help='Тема письма')
    parser.add_argument('-f', '--html-file', required=True,
                        help='Путь к HTML-файлу письма')
    args = parser.parse_args()

    send_email(
        sender=args.sender,
        recipients=args.recipients,
        subject=args.subject,
        html_file=args.html_file
    )
