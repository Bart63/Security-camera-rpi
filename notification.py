import smtplib
import ssl
from email.message import EmailMessage

app_password = ''
user = ''
phone = ''
Provider = {
    "Plus": {"sms": "text.plusgsm.pl"},
}


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    msg['from'] = user
    password = app_password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def format_provider_email_address(number: str):
    provider_info = Provider["Plus"]
    domain = provider_info.get("sms")
    return f"+{number}@{domain}"


def send_sms_via_email(
    message: str,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = (user, app_password)
    receiver_email = format_provider_email_address(phone)

    email_message = f"Subject: {subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)
