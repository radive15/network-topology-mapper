import socket
import ipaddress
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import argparse


# Dictionary port umum — key: nomor port, value: nama service
COMMON_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

console = Console()


def is_host_alive(ip: str, port: int = 80, timeout: float = 1.0) -> bool:
    """Cek apakah host aktif dengan mencoba koneksi TCP ke port tertentu."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((ip, port))
    s.close()
    return result == 0


def scan_ports(ip: str) -> list[dict]:
    """
    Scan port-port umum pada satu IP secara paralel.

    Returns:
        List of dict berisi port dan nama service yang terbuka
    """
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(COMMON_PORTS)) as executor:
        future_to_port = {
            executor.submit(is_host_alive, ip, port, 0.5): (port, service)
            for port, service in COMMON_PORTS.items()
        }

        for future in concurrent.futures.as_completed(future_to_port):
            port, service = future_to_port[future]
            is_open = future.result()

            if is_open:
                open_ports.append({"port": port, "service": service})

    return sorted(open_ports, key=lambda x: x["port"])


def scan_network(net_range: str) -> list[str]:
    """Scan seluruh host aktif dalam satu network range."""
    network = ipaddress.ip_network(net_range)
    active_hosts = []

    for ip in network.hosts():
        if is_host_alive(str(ip)):
            active_hosts.append(str(ip))

    return active_hosts


def print_results(hosts: list[str]) -> None:
    """Tampilkan hasil scan dalam format tabel rich."""
    for host in hosts:
        ports = scan_ports(host)

        # Buat tabel baru untuk tiap host
        table = Table(title=f"[bold green]{host}[/bold green]", show_lines=True)
        table.add_column("Port", style="cyan", width=10)
        table.add_column("Protocol", style="white", width=10)
        table.add_column("Status", style="bold green", width=10)
        table.add_column("Service", style="yellow")

        if ports:
            for p in ports:
                table.add_row(str(p["port"]), "tcp", "OPEN", p["service"])
        else:
            table.add_row("-", "-", "none", "tidak ada port terbuka")

        console.print(table)
        console.print()


# --- Main ---
def parse_args() -> argparse.Namespace:
    """Parsing dan validasi argumen dari CLI."""
    parser = argparse.ArgumentParser(
        description="Network Topology Mapper — scan host aktif dan port terbuka",
        epilog="Contoh: python main.py --network 192.168.1.0/24"
    )
    parser.add_argument(
        "--network",
        type=str,
        required=True,
        help="Network range dalam format CIDR (contoh: 192.168.1.0/24)"
    )

    args = parser.parse_args()

    # Validasi format CIDR sebelum lanjut scan
    try:
        ipaddress.ip_network(args.network, strict=False)
    except ValueError:
        parser.error(f"Format network tidak valid: '{args.network}'. Gunakan format CIDR, contoh: 192.168.1.0/24")

    return args



if __name__ == "__main__":
    args = parse_args()

    console.print(f"\n[bold]Scanning network[/bold] [cyan]{args.network}[/cyan]...\n")

    hosts = scan_network(args.network)
    console.print(f"[green]Ditemukan {len(hosts)} host aktif.[/green]\n")

    print_results(hosts)

