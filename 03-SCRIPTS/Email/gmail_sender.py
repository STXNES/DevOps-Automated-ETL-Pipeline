import smtplib
import json
from email.mime.text import MIMEText
from email.utils import make_msgid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS_FILE = PROJECT_ROOT / "05-CONFIG" / "email_credentials.json"

# Cargar las credenciales de Zoho
with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
    config = json.loads(f.read(), strict=False)

EMAIL_USER = config["EMAIL"]
EMAIL_PASSWORD = config["APP_PASSWORD"]

def send_email(to_email, subject, html, thread_id=None, in_reply_to=None):
    message = MIMEText(html, "html")
    message["To"] = to_email
    message["From"] = f"Axell Rojas <{EMAIL_USER}>"
    message["Subject"] = subject
    
    # Generar un Message-ID único
    msg_id = make_msgid(domain=os.environ.get("OUTREACH_DOMAIN", "stxnes.dev"))
    message["Message-ID"] = msg_id

    # Si es una respuesta de seguimiento, agregamos las cabeceras estándar de hilos
    if in_reply_to:
        message["In-Reply-To"] = in_reply_to
        message["References"] = in_reply_to

    # Conectar y enviar a través del servidor SMTP de Zoho usando SSL
    with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, message.as_string())

    # Usamos el message_id inicial como thread_id en SMTP estándar
    return {
        "thread_id": thread_id if thread_id else msg_id,
        "message_id": msg_id
    }