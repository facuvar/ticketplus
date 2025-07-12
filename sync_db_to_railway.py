import os
import subprocess
import sys
from urllib.parse import urlparse
from dotenv import load_dotenv

def print_color(text, color):
    """Imprime texto en color en la terminal."""
    colors = {
        "header": "\033[95m",
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "endc": "\033[0m",
        "bold": "\033[1m",
    }
    sys.stdout.write(f"{colors.get(color, '')}{text}{colors['endc']}\n")

def parse_db_url(url: str):
    """Parsea una URL de base de datos para obtener los componentes."""
    try:
        creds = urlparse(url)
        return {
            "user": creds.username,
            "password": creds.password,
            "host": creds.hostname,
            "port": creds.port,
            "db_name": creds.path.lstrip('/'),
        }
    except Exception as e:
        print_color(f"❌ Error parseando la URL de la base de datos: {url}", "red")
        print_color(f"   Asegúrate de que tenga el formato: mysql+pymysql://user:pass@host:port/db", "red")
        print_color(f"   Error: {e}", "red")
        sys.exit(1)

def main():
    """
    Script principal para sincronizar la base de datos local con Railway
    usando un archivo de dump local.
    """
    print_color("🚀 INICIANDO SINCRONIZACIÓN DESDE ARCHIVO LOCAL A RAILWAY 🚀", "header")

    # 1. Cargar variables de entorno desde .env
    load_dotenv()
    railway_url = os.getenv("RAILWAY_DATABASE_URL")
    local_dump_file = "ticketplus_dev.sql"

    if not railway_url:
        print_color("❌ Error: Falta la variable 'RAILWAY_DATABASE_URL' en el archivo .env.", "red")
        sys.exit(1)

    if not os.path.exists(local_dump_file):
        print_color(f"❌ Error: No se encuentra el archivo de volcado '{local_dump_file}'.", "red")
        print_color(f"   Asegúrate de haber exportado la base de datos a '{local_dump_file}' en el root del proyecto.", "yellow")
        sys.exit(1)

    print_color("✅ Variables de entorno y archivo de dump encontrados.", "green")

    # 2. Parsear URL de la base de datos de Railway
    railway_creds = parse_db_url(railway_url)
    print_color(f"   DB Destino (Railway): {railway_creds['db_name']} en {railway_creds['host']}", "blue")

    # 3. Construir el comando para mysql import
    mysql_bin_path = "C:\\xampp\\mysql\\bin"
    mysql_path = os.path.join(mysql_bin_path, "mysql.exe")

    import_cmd = [
        mysql_path,
        "-h", railway_creds['host'],
        f"-P{railway_creds['port']}",
        f"-u{railway_creds['user']}",
        f"-p{railway_creds['password']}",
        railway_creds['db_name']
    ]

    # 4. Ejecutar el proceso de importación desde el archivo
    print_color("\n🔄 Importando datos desde archivo... (esto puede tardar unos segundos)", "yellow")
    try:
        with open(local_dump_file, 'r', encoding='latin-1') as f:
            import_process = subprocess.Popen(import_cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='latin-1')
            
            # Esperamos a que el proceso termine y capturamos la salida
            import_stdout, import_stderr = import_process.communicate()

            if import_process.returncode != 0:
                raise RuntimeError(f"Error durante la importación a Railway: {import_stderr}")

        print_color("\n✅ ¡SINCRONIZACIÓN COMPLETADA EXITOSAMENTE!", "green")
        print_color("   Tu base de datos de Railway ahora tiene los mismos datos que tu archivo local.", "bold")

    except FileNotFoundError:
        print_color("❌ Error: 'mysql.exe' no se encontró.", "red")
        print_color("   Asegúrate de que la ruta 'C:\\xampp\\mysql\\bin' es correcta.", "yellow")
        sys.exit(1)
    except Exception as e:
        print_color(f"\n❌ Ocurrió un error durante la sincronización:", "red")
        print_color(str(e), "yellow")
        sys.exit(1)

if __name__ == "__main__":
    main() 