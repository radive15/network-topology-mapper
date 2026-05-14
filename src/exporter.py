import json
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def export_json(results: list[dict], output_path: str) -> None:
    """
    Export hasil scan ke file JSON.

    Args:
        results: Data hasil scan dari collect_results()
        output_path: Path file tujuan (contoh: 'scan_result.json')
    """
    # Tambah metadata: waktu scan dan jumlah host
    payload = {
        "scanned_at": datetime.now().isoformat(),
        "total_hosts": len(results),
        "hosts": results
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.info(f"Hasil disimpan ke {output_path}")
    except OSError as e:
        logger.error(f"Gagal menulis file JSON: {e}")
        raise


def export_csv(results: list[dict], output_path: str) -> None:
    """
    Export hasil scan ke file CSV.

    Args:
        results: Data hasil scan dari collect_results()
        output_path: Path file tujuan (contoh: 'scan_result.csv')
    """
    # CSV flat — tiap baris = satu port terbuka per host
    fieldnames = ["ip", "port", "service"]

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for host in results:
                if host["ports"]:
                    for p in host["ports"]:
                        writer.writerow({
                            "ip": host["ip"],
                            "port": p["port"],
                            "service": p["service"]
                        })
                else:
                    # Tetap tulis host meski tidak ada port terbuka
                    writer.writerow({"ip": host["ip"], "port": "-", "service": "-"})

        logger.info(f"Hasil disimpan ke {output_path}")
    except OSError as e:
        logger.error(f"Gagal menulis file CSV: {e}")
        raise
