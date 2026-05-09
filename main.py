import socket
import ipaddress

def is_host_alive(ip: str, port: int = 80, timeout: float = 1.0) -> bool:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    result = s.connect_ex((ip,port))
        
    s.close()
    return result == 0


def scan_network(net_range: str) -> list[str]:
    network = ipaddress.ip_network(net_range)
    
    active_hosts = []
    for ip in network.hosts():
        if is_host_alive(str(ip)):
            active_hosts.append(str(ip))
    return active_hosts
    

network_range = "8.8.8.0/30"

print(f"Scanning {network_range}...")

results = scan_network(network_range)

for host in results:
    print(f"  [+] {host} - ALIVE")

print(f"\nScan complete. {len(results)} host(s) found.")


