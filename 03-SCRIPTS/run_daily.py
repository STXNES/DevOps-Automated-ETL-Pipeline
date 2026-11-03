import subprocess
import sys
import time
import glob
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Definir las rutas relativas de los scripts básicos
SCRIPTS = [
    {
        "name": "Paso 1: Leer Respuestas (read_replies.py)",
        "path": ROOT / "03-SCRIPTS" / "Gmail_API" / "read_replies.py",
        "cwd": ROOT
    },
    {
        "name": "Paso 2: Enviar Seguimientos (auto_followup.py)",
        "path": ROOT / "03-SCRIPTS" / "Email" / "auto_followup.py",
        "cwd": ROOT
    }
]

# Script de envíos final (se añade al final de la lista)
SEND_SCRIPT = {
    "name": "Paso 3: Enviar Nuevos Correos (send_pipeline.py)",
    "path": ROOT / "03-SCRIPTS" / "Email" / "send_pipeline.py",
    "cwd": ROOT
}

def print_header(title):
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def check_pending_leads():
    """Revisa si hay correos PENDING en los archivos de la carpeta 01-PIPELINE."""
    pipeline_files = glob.glob(str(ROOT / "01-PIPELINE" / "altus_pipeline*.csv"))
    for pf in pipeline_files:
        try:
            with open(pf, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if any(row.get("Status") == "PENDING" for row in reader):
                    return True
        except Exception:
            continue
    return False

def main():
    print_header("INICIANDO DEVOPS AUTOMATED ETL PIPELINE")
    print("Por favor, no cierres esta ventana hasta que termine el proceso.\n")
    
    # 1. Comprobar si hay leads pendientes en los lotes existentes
    has_pending = check_pending_leads()
    
    execution_list = list(SCRIPTS)
    
    if not has_pending:
        print("[INFO] No se detectaron prospectos PENDING en los lotes activos.")
        print("[INFO] Añadiendo Scraper automático al inicio de la cola...")
        execution_list.insert(0, {
            "name": "Scraper Automático (auto_scraper.py)",
            "path": ROOT / "03-SCRIPTS" / "Scraper" / "auto_scraper.py",
            "cwd": ROOT
        })
        execution_list.insert(1, {
            "name": "Limpiador e Importador de Lotes (clean_csv.py)",
            "path": ROOT / "03-SCRIPTS" / "Cleaner" / "clean_csv.py",
            "cwd": ROOT / "03-SCRIPTS" / "Cleaner"
        })
    else:
        print("[INFO] El lote actual tiene prospectos PENDING. Saltando Scraping automático.")

    # Añadir el paso final de envío de correos
    execution_list.append(SEND_SCRIPT)

    # 2. Ejecutar la secuencia de scripts
    for script in execution_list:
        print(f"\n⏳ Ejecutando: {script['name']}...")
        
        if not script["path"].exists():
            print(f"❌ ERROR: No se encontró el archivo {script['path']}")
            print("Abortando la ejecución diaria para evitar errores en la base de datos.")
            sys.exit(1)
            
        try:
            subprocess.run(
                [sys.executable, str(script["path"])],
                check=True,
                cwd=str(script["cwd"]),
                text=True,
                encoding="utf-8"
            )
            print(f"✅ Completado: {script['name']}")
        except subprocess.CalledProcessError as e:
            print(f"❌ FALLÓ: {script['name']} ha fallado con código de error {e.returncode}")
            print("Abortando la ejecución de los siguientes pasos para evitar enviar correos equivocados.")
            sys.exit(1)
            
        # Pequeña pausa entre scripts
        time.sleep(2)

    print_header("🎉 AUTOPILOT COMPLETADO CON ÉXITO")
    print("Se han procesado todas las tareas del día.")
    print("Ya puedes cerrar esta ventana y apagar tu computadora si lo deseas.")
    print("\nEsta ventana se cerrará automáticamente en 10 segundos...")
    time.sleep(10)

if __name__ == "__main__":
    main()
