import subprocess
from pathlib import Path
import zipfile

DATASET = "davidcariboo/player-scores"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def update_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("⬇️ Descargando dataset...")

    result = subprocess.run(
        [
            "kaggle",
            "datasets",
            "download",
            "-d",
            DATASET,
            "-p",
            str(DATA_DIR),
            "-o"
        ],
        capture_output=True,
        text=True
    )

    # 🔴 Manejo de error
    if result.returncode != 0:
        print("❌ Error descargando dataset:")
        print(result.stderr)
        return

    print("📦 Extrayendo archivos...")

    zip_files = list(DATA_DIR.glob("*.zip"))

    if not zip_files:
        print("⚠️ No se encontró ningún archivo ZIP")
        return

    # 👉 usar solo el más reciente
    latest_zip = max(zip_files, key=lambda f: f.stat().st_mtime)

    with zipfile.ZipFile(latest_zip, "r") as z:
        z.extractall(DATA_DIR)

    latest_zip.unlink()

    print("✅ Dataset actualizado correctamente")

if __name__ == "__main__":
    update_dataset()