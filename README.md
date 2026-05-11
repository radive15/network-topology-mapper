# Network Topology Mapper

Tool Python untuk melakukan **network discovery** — menemukan host aktif, memetakan port terbuka, dan memvisualisasikan topologi jaringan secara otomatis.

Dibuat sebagai project portofolio untuk mempelajari Python dari perspektif SRE/DevOps.

---

## Fitur

- **Host Discovery** — deteksi host aktif via TCP connect (tanpa akses root)
- **Port Scanner** — scan 8 port umum secara paralel per host
- **Export JSON/CSV** — simpan hasil scan dengan timestamp otomatis
- **Network Graph** — visualisasi topologi jaringan sebagai file PNG

---

## Status Project

| Tahap | Fitur | Status |
|---|---|---|
| Tahap 1 | Host Discovery (ping sweep via TCP connect) | ✅ Selesai |
| Tahap 2 | Port Scanner (paralel + tabel output) | ✅ Selesai |
| Tahap 3 | CLI Interface dengan argparse + validasi input | ✅ Selesai |
| Tahap 4 | Export hasil ke JSON/CSV | ✅ Selesai |
| Tahap 5 | Network Graph dengan NetworkX | ✅ Selesai |

---

## Cara Install

```bash
# Clone repository
git clone https://github.com/rifki/network-topology-mapper.git
cd network-topology-mapper

# Buat dan aktifkan virtual environment
python -m venv venv
venv\Scripts\Activate.ps1     # Windows
# source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## Cara Pakai

```bash
# Scan dan tampilkan tabel di terminal
python main.py --network 192.168.1.0/24

# Scan + export ke CSV
python main.py --network 192.168.1.0/24 --output csv

# Scan + export ke JSON
python main.py --network 192.168.1.0/24 --output json

# Scan + generate network graph (PNG)
python main.py --network 192.168.1.0/24 --graph

# Semua sekaligus
python main.py --network 192.168.1.0/24 --output csv --graph

# Lihat semua opsi
python main.py --help
```

### Contoh Output Terminal

```
Scanning network 192.168.1.0/24...

Ditemukan 2 host aktif.

                   192.168.1.1
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Port       ┃ Protocol   ┃ Status     ┃ Service ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ 22         │ tcp        │ OPEN       │ SSH     │
├────────────┼────────────┼────────────┼─────────┤
│ 80         │ tcp        │ OPEN       │ HTTP    │
└────────────┴────────────┴────────────┴─────────┘
```

### Contoh Output CSV (`scan_result_20260511_174037.csv`)

```
ip,port,service
192.168.1.1,22,SSH
192.168.1.1,80,HTTP
192.168.1.4,22,SSH
192.168.1.4,80,HTTP
```

### Contoh Output JSON (`scan_result_*.json`)

```json
{
  "scanned_at": "2026-05-11T17:40:37",
  "total_hosts": 2,
  "hosts": [
    {
      "ip": "192.168.1.1",
      "ports": [
        {"port": 22, "service": "SSH"},
        {"port": 80, "service": "HTTP"}
      ]
    }
  ]
}
```

### Contoh Error Validasi

```
main.py: error: Format network tidak valid: '192.168.1/24'.
Gunakan format CIDR, contoh: 192.168.1.0/24
```

---

## Cara Kerja

Tool ini menggunakan **TCP Connect** (bukan ICMP ping) untuk mendeteksi host aktif:
- Tidak membutuhkan akses administrator
- Mencoba membuka koneksi TCP ke port tertentu (default: 80)
- Jika koneksi berhasil → host aktif
- Jika timeout → host tidak aktif atau port tertutup

Port scanning dilakukan secara **paralel** menggunakan `ThreadPoolExecutor` — mirip seperti menjalankan health check ke banyak endpoint sekaligus.

Pendekatan ini mirip dengan `nmap -sT` (TCP connect scan).

---

## Port yang Di-scan

| Port | Service |
|---|---|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP-Alt |
| 8443 | HTTPS-Alt |

---

## Tech Stack

- Python 3.11+
- `socket` — TCP connect untuk host discovery dan port scan
- `ipaddress` — parsing CIDR network range
- `concurrent.futures` — paralel port scanning dengan ThreadPoolExecutor
- `rich` — output tabel berwarna di terminal
- `argparse` — CLI interface dengan validasi input
- `networkx` — pemodelan network graph (node + edge)
- `matplotlib` — render graph ke file PNG

---

## Requirements

Lihat [requirements.txt](requirements.txt)

---

## License

[MIT](LICENSE)
