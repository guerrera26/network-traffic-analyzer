import scapy.all
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse


class TrafficAnalyzer:

    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.packets = scapy.all.rdpcap(pcap_file)

        self.flows = defaultdict(int)
        self.protocols = defaultdict(int)
        self.host_bytes = defaultdict(int)

        self.total_bytes = 0
        self.packet_count = 0

    def analyze(self):

        for pkt in self.packets:

            if scapy.all.IP not in pkt:
                continue

            src = pkt[scapy.all.IP].src
            dst = pkt[scapy.all.IP].dst
            size = len(pkt)

            self.packet_count += 1
            self.total_bytes += size

            self.host_bytes[src] += size

            proto = "OTHER"

            if scapy.all.TCP in pkt:
                proto = "TCP"
            elif scapy.all.UDP in pkt:
                proto = "UDP"

            self.protocols[proto] += 1

            flow = (src, dst, proto)
            self.flows[flow] += size

    def print_summary(self):

        print("\n--- Traffic Summary ---")
        print(f"Packets analyzed: {self.packet_count}")
        print(f"Total traffic: {self.total_bytes / (1024*1024):.2f} MB\n")

        print("Protocol Breakdown:")

        total = sum(self.protocols.values())

        for proto, count in self.protocols.items():
            percent = (count / total) * 100
            print(f"{proto}: {percent:.2f}%")

        print("\nTop Talkers:")

        sorted_hosts = sorted(
            self.host_bytes.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for host, bytes_sent in sorted_hosts[:5]:
            print(f"{host} -> {bytes_sent/(1024*1024):.2f} MB")

    def flow_table(self):

        data = []

        for (src, dst, proto), bytes_sent in self.flows.items():

            data.append({
                "src": src,
                "dst": dst,
                "protocol": proto,
                "bytes": bytes_sent
            })

        df = pd.DataFrame(data)
        return df

    def plot_protocols(self):

        labels = list(self.protocols.keys())
        values = list(self.protocols.values())

        plt.figure()
        plt.bar(labels, values)
        plt.title("Protocol Distribution")
        plt.ylabel("Packet Count")
        plt.xlabel("Protocol")

        plt.show()

    def plot_top_talkers(self):

        sorted_hosts = sorted(
            self.host_bytes.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        hosts = [h[0] for h in sorted_hosts]
        traffic = [h[1] / (1024*1024) for h in sorted_hosts]

        plt.figure()
        plt.bar(hosts, traffic)

        plt.title("Top Talkers")
        plt.ylabel("MB Sent")
        plt.xticks(rotation=30)

        plt.show()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("pcap", help="pcap file to analyze")
    parser.add_argument("--plots", action="store_true")

    args = parser.parse_args()

    analyzer = TrafficAnalyzer(args.pcap)

    print("Analyzing PCAP file...")

    analyzer.analyze()
    analyzer.print_summary()

    df = analyzer.flow_table()

    print("\nTop Flows:")
    print(df.sort_values("bytes", ascending=False).head())

    if args.plots:
        analyzer.plot_protocols()
        analyzer.plot_top_talkers()


if __name__ == "__main__":
    main()