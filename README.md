# PCAP Traffic Analyzer

A Python-based network traffic analysis tool that processes `.pcap` files to extract insights such as protocol distribution, traffic volume, and top communicating hosts.

## Features

- Parses PCAP files using Scapy
- Computes:
  - Total packets and traffic volume
  - Protocol distribution (TCP, UDP, Other)
  - Top talkers (hosts generating the most traffic)
  - Flow-level traffic breakdown
- Outputs:
  - Console summaries
  - Pandas DataFrame of flows
  - Optional visualizations using Matplotlib

## Technologies Used

- Python 3
- Scapy
- Pandas
- Matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
