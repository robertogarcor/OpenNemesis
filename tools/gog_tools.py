import logging
import subprocess
import os
import json
from typing import Optional

GOG_PATH = "/opt/gogcli/gog"
GOG_ACCOUNT = os.getenv("GOG_ACCOUNT", "")
GOG_CREDENTIALS = os.path.join(os.path.dirname(__file__), "..", "credentials")

def run_gog_command(args: list) -> str:
    """Ejecuta un comando gog y devuelve el resultado."""
    try:
        cmd = [GOG_PATH] + args
        if GOG_ACCOUNT:
            cmd.extend(["--account", GOG_ACCOUNT])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            logging.error(f"GOG error: {result.stderr}")
            return f"Error: {result.stderr}"
        
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Timeout ejecutando comando GOG"
    except Exception as e:
        logging.error(f"Error ejecutando GOG: {e}")
        return f"Error: {str(e)}"


def gmail_list_labels() -> str:
    """Lista todas las etiquetas de Gmail."""
    return run_gog_command(["gmail", "labels", "list"])


def gmail_search(query: str, max_results: int = 5) -> str:
    """Busca emails en Gmail."""
    return run_gog_command(["gmail", "search", query, "--max", str(max_results)])


def gmail_list_emails(max_results: int = 10) -> str:
    """Lista los últimos emails."""
    return run_gog_command(["gmail", "list", "--max", str(max_results)])


def gmail_send(to: str, subject: str, body: str) -> str:
    """Envía un email."""
    return run_gog_command([
        "gmail", "send",
        "--to", to,
        "--subject", subject,
        "--body", body
    ])


def calendar_list_events(calendar_id: str = "primary", max_results: int = 10, from_date: str = "", to_date: str = "") -> str:
    """Lista eventos del calendario.
    
    Args:
        calendar_id: ID del calendario (default: primary)
        max_results: Número máximo de resultados
        from_date: Fecha inicio (RFC3339, fecha, o relative: today, tomorrow)
        to_date: Fecha fin (RFC3339, fecha, o relative: today, tomorrow)
    """
    args = ["calendar", "events", calendar_id]
    
    if from_date:
        args.extend(["--from", from_date])
    if to_date:
        args.extend(["--to", to_date])
    if not from_date and not to_date:
        args.append("--today")
    
    args.extend(["--results-only"])
    
    return run_gog_command(args)


def calendar_create_event(
    calendar_id: str = "primary",
    summary: str = "",
    start_time: str = "",
    end_time: str = ""
) -> str:
    """Crea un evento en el calendario.
    
    Args:
        calendar_id: ID del calendario (default: primary)
        summary: Título del evento
        start_time: Hora inicio (RFC3339: 2026-03-15T10:00:00+01:00)
        end_time: Hora fin (RFC3339: 2026-03-15T11:00:00+01:00)
    """
    if not summary or not start_time or not end_time:
        return "Error: Faltan parámetros. Se requiere summary, start_time y end_time"
    
    # Añadir zona horaria si no la tiene
    if "+" not in start_time and "Z" not in start_time:
        start_time = start_time + "+01:00"
    if "+" not in end_time and "Z" not in end_time:
        end_time = end_time + "+01:00"
    
    return run_gog_command([
        "calendar", "create", calendar_id,
        "--summary", summary,
        "--from", start_time,
        "--to", end_time,
        "--force"
    ])


def drive_list_files(query: str = "", max_results: int = 10) -> str:
    """Lista archivos en Drive."""
    if query:
        return run_gog_command(["drive", "search", query, "--max", str(max_results)])
    return run_gog_command(["drive", "ls", "--max", str(max_results)])


def drive_download_file(file_id: str, output_path: str) -> str:
    """Descarga un archivo de Drive."""
    return run_gog_command(["drive", "download", file_id, "--output", output_path])


def contacts_list(max_results: int = 20) -> str:
    """Lista contactos."""
    return run_gog_command(["contacts", "list", "--max", str(max_results)])
