from gmail_sender import send_email

send_email(
    to_email="axel.rojas2502@gmail.com",
    subject="Prueba DevOps Pipeline (Zoho)",
    html="""
    <h2>Hola Axel</h2>

    <p>Si recibes este correo significa que el SMTP seguro de Zoho Mail está funcionando correctamente desde tu dominio.</p>

    <p>🚀 DevOps Automated Pipeline listo con tu nuevo correo corporativo.</p>
    """
)

print("Correo de prueba enviado correctamente a través de Zoho SMTP.")
