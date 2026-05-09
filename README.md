# Network Topology Mapper

Tool Python untuk melakukan **network discovery** — menemukan host aktif dan memetakan topologi jaringan secara otomatis.

Dibuat sebagai project portofolio untuk mempelajari Python dari perspektif SRE/DevOps.

---

## Status Project

| Tahap | Fitur | Status |
|---|---|---|
| Tahap 1 | Host Discovery (ping sweep via TCP connect) | ✅ Selesai |
| Tahap 2 | Port Scanner | 🔄 In Progress |
| Tahap 3 | Service Detection | ⏳ Planned |
| Tahap 4 | Visual Topology & Report | ⏳ Planned |

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

### Tahap 1 — Host Discovery

```bash
python main.py
```

### Contoh Output (Tahap 1)

```
Scanning 192.168.1.0/24...
[+] 192.168.1.1   - ALIVE
[+] 192.168.1.10  - ALIVE
[+] 192.168.1.20  - ALIVE

Scan complete. 3 host(s) found.
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
- `socket` — TCP connect untuk host discovery
- `ipaddress` — parsing CIDR network range
- `python-dotenv` — konfigurasi dari environment variable

---

## Requirements

Lihat [requirements.txt](requirements.txt)

---

## License

[MIT](LICENSE)
