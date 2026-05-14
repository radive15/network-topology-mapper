import logging
import matplotlib.pyplot as plt
import networkx as nx

logger = logging.getLogger(__name__)


def generate_graph(results: list[dict], output_path: str = "network_graph.png") -> None:
    """
    Generate visualisasi network graph dari hasil scan.

    Args:
        results: Data hasil scan dari collect_results()
        output_path: Path file gambar output (default: network_graph.png)
    """
    G = nx.Graph()

    # Node "scanner" = mesin kamu sendiri, titik pusat graph
    G.add_node("scanner", label="You (scanner)")

    for host in results:
        ip = host["ip"]
        port_count = len(host["ports"])

        # Tambah node untuk tiap host yang ditemukan
        G.add_node(ip, label=ip, port_count=port_count)

        # Edge = koneksi antara scanner dan host
        G.add_edge("scanner", ip)

    # Warna node: scanner = biru, host = hijau jika ada port terbuka, merah jika tidak
    node_colors = []
    for node in G.nodes():
        if node == "scanner":
            node_colors.append("steelblue")
        elif G.nodes[node].get("port_count", 0) > 0:
            node_colors.append("mediumseagreen")
        else:
            node_colors.append("tomato")

    # Label yang ditampilkan di tiap node
    labels = {node: G.nodes[node].get("label", node) for node in G.nodes()}

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=2)  # k=2 = jarak antar node lebih jauh


    nx.draw(
        G, pos,
        labels=labels,
        with_labels=True,
        node_color=node_colors,
        node_size=3000,        # ← naikan dari 2000
        font_size=8,
        font_color="white",
        font_weight="bold",    # ← tambah ini supaya lebih terbaca
        edge_color="gray",
        width=2,               # ← edge lebih tebal
    )


    plt.title("Network Topology Map", fontsize=14, fontweight="bold")

    try:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Graph disimpan ke {output_path}")
    except OSError as e:
        logger.error(f"Gagal menyimpan graph: {e}")
        raise
    finally:
        plt.close()  # Bebaskan memory — penting kalau dipakai di loop
