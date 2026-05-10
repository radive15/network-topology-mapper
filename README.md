# Network Topology Mapper

Tool Python untuk melakukan **network discovery** — menemukan host aktif dan memetakan topologi jaringan secara otomatis.

Dibuat sebagai project portofolio untuk mempelajari Python dari perspektif SRE/DevOps.

---

## Status Project

| Tahap | Fitur | Status |
|---|---|---|
| Tahap 1 | Host Discovery (ping sweep via TCP connect) | ✅ Selesai |
| Tahap 2 | Port Scanner (paralel + tabel output) | ✅ Selesai |
| Tahap 3 | CLI Interface (argparse) | ⏳ Planned |
| Tahap 4 | Export hasil ke JSON/CSV | ⏳ Planned |

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

# Setup environment variables
cp .env.example .env
# Edit .env sesuai kebutuhan
```

---

## Cara Pakai

```bash
python main.py
```

### Contoh Output

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

---

## Cara Kerja

Tool ini menggunakan **TCP Connect** (bukan ICMP ping) untuk mendeteksi host aktif:
- Tidak membutuhkan akses administrator
- Mencoba membuka koneksi TCP ke port tertentu (default: 80)
- Jika koneksi berhasil → host aktif
- Jika timeout → host tidak aktif atau port tertutup

Pendekatan ini mirip dengan `nmap -sT` (TCP connect scan).

---

## Tech Stack

- Python 3.11+
- `socket` — TCP connect untuk host discovery dan port scan
- `ipaddress` — parsing CIDR network range
- `concurrent.futures` — paralel port scanning dengan ThreadPoolExecutor
- `rich` — output tabel berwarna di terminal
- `python-dotenv` — konfigurasi dari environment variable

---

## Requirements

Lihat [requirements.txt](requirements.txt)

---

## License

[MIT](LICENSE)
