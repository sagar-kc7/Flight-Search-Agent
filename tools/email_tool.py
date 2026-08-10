"""
Sends the final result via SMTP (e.g. Gmail with an App Password).
"""
import os
import smtplib
from email.mime.text import MIMEText


def send_deal_email(best_deal: dict, origin: str, destination: str, departure_date: str) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.environ["SMTP_PORT"])
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]
    to_addr = os.environ["EMAIL_TO"]

    subject = f"Best flight deal: {origin} -> {destination} on {departure_date}"
    body = (
        f"Best price found: {best_deal['price']} {best_deal['currency']}\n"
        f"Airline: {best_deal['airline']}\n"
        f"Source: {best_deal['source']}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_addr

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())
