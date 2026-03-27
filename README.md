# PCAP Traffic Analyzer

A Python-based network traffic analysis tool that reads `.pcap` files and extracts useful traffic insights such as protocol distribution, total traffic volume, top talkers, and flow-level communication summaries.

This project is designed to be simple enough for learning and demonstration purposes while still being structured clearly enough for someone else to pick up, run, modify, and extend later.

---

# Overview

Packet capture (`.pcap`) files contain raw network traffic that can be inspected to understand how devices communicate across a network. This project uses **Scapy** to parse packets, then organizes the captured data into useful summaries for quick analysis.

The analyzer focuses on a few core questions:

- How many packets were captured?
- How much traffic was transmitted?
- Which protocols appear most often?
- Which hosts generated the most traffic?
- Which source/destination/protocol flows carried the most bytes?

This tool is especially useful for:
- Learning packet analysis basics
- Small-scale traffic inspection
- Security/networking class projects
- Demonstrating Python-based network analysis workflows

---

# Features

- Parses `.pcap` files using Scapy
- Filters for IP-based traffic
- Computes:
  - Total packets analyzed
  - Total traffic volume
  - Protocol distribution (`TCP`, `UDP`, `OTHER`)
  - Top talkers by bytes sent
  - Flow-level traffic totals
- Outputs:
  - Console summary
  - Flow table as a Pandas DataFrame
  - Optional visualizations using Matplotlib
- Includes command-line argument support with `argparse`

---

# Project Structure

```text
PCAP-Traffic-Analyzer/
│
├── analyzer.py
├── capture.pcap
├── example_output.txt
└── README.md
```

## File Descriptions

### `analyzer.py`
Main project file.

Contains:
- The `TrafficAnalyzer` class
- Packet parsing logic
- Summary printing
- Flow table generation
- Plotting functions
- Command-line interface

### `example_output.txt`
Example of what the analyzer prints after processing a `.pcap` file.

### `README.md`
Project documentation, setup instructions, and maintenance notes.

---

# How It Works

## 1. PCAP Loading
The program reads the packet capture file using Scapy:

```python
self.packets = scapy.all.rdpcap(pcap_file)
```

This loads all packets from the provided `.pcap` file into memory.

## 2. Packet Filtering
Only packets that contain an IP layer are analyzed:

```python
if scapy.all.IP not in pkt:
    continue
```

Non-IP traffic is skipped.

## 3. Packet Metrics
For each valid packet, the analyzer collects:
- Source IP
- Destination IP
- Packet size
- Protocol type

It updates running totals for:
- Packet count
- Total bytes
- Per-host byte counts
- Per-protocol counts
- Per-flow byte counts

## 4. Protocol Classification
Traffic is grouped into three protocol categories:
- `TCP`
- `UDP`
- `OTHER`

Logic:
- If packet contains TCP → `TCP`
- Else if packet contains UDP → `UDP`
- Else → `OTHER`

## 5. Flow Tracking
Each flow is represented as:

```text
(source IP, destination IP, protocol)
```

The analyzer sums total bytes sent for each flow.

## 6. Optional Plotting
If the `--plots` flag is provided, the analyzer generates:
- A bar chart of protocol distribution
- A bar chart of top talkers

---

# Core Data Structures

The program uses `defaultdict(int)` to keep counting logic simple.

## `self.flows`
Stores total bytes per flow.

Example key:
```python
("192.168.1.10", "8.8.8.8", "TCP")
```

## `self.protocols`
Stores packet count by protocol.

Example:
```python
{
    "TCP": 500,
    "UDP": 120,
    "OTHER": 75
}
```

## `self.host_bytes`
Stores total bytes sent per source host.

Example:
```python
{
    "192.168.1.10": 1048576,
    "10.0.0.5": 524288
}
```

---

# Technologies / Libraries Used

| Library | Purpose |
|---|---|
| Python | Core programming language |
| Scapy | Reads and inspects packets from `.pcap` files |
| pandas | Builds and formats the flow table |
| matplotlib | Creates charts for protocol distribution and top talkers |
| collections.defaultdict | Simplifies counting and aggregation |
| argparse | Adds command-line argument support |

---

# Dependency Breakdown

## Python
The project is written in Python and is intended for Python 3.

Recommended version:
```text
Python 3.10+
```

It may also work on nearby Python 3 versions, but newer Python 3 releases are preferred for compatibility with current libraries.

---

## Scapy
Used for packet capture parsing and packet-layer inspection.

Used for:
- Reading `.pcap` files
- Checking for `IP`, `TCP`, and `UDP` layers
- Accessing source and destination IP addresses

Relevant usage in this project:
```python
scapy.all.rdpcap(pcap_file)
scapy.all.IP
scapy.all.TCP
scapy.all.UDP
```

If Scapy changes in a future release:
- Check import paths first
- Confirm `rdpcap()` still works the same way
- Confirm packet layer checks still use the same syntax

If Scapy becomes deprecated or incompatible:
Possible replacements include:
- `pyshark`
- `dpkt`
- `pcapy`

Important note: if you replace Scapy, the packet parsing layer logic will need to be rewritten, because those libraries do not use the same API.

---

## pandas
Used to create a flow table from aggregated flow data.

Used for:
- Converting flow records into a `DataFrame`
- Sorting flows by byte count
- Printing top flows clearly

Relevant usage:
```python
pd.DataFrame(data)
df.sort_values("bytes", ascending=False)
```

If pandas changes or becomes deprecated:
Possible replacements:
- Python built-in `csv`
- Polars
- Plain lists/dictionaries with manual formatting

If replacing pandas with standard Python only:
- Return the raw list of flow dictionaries
- Sort using `sorted(...)`
- Write CSV output with the `csv` module if needed

---

## matplotlib
Used for optional bar charts.

Used for:
- Protocol distribution plot
- Top talkers plot

Relevant usage:
```python
plt.figure()
plt.bar(...)
plt.title(...)
plt.show()
```

If matplotlib changes or becomes deprecated:
Possible replacements:
- seaborn
- plotly
- pandas built-in plotting

Important note: plotting is optional in this project, so the analyzer still works without visualization support as long as the summary and flow table logic remain intact.

---

## argparse
Used to handle command-line arguments.

Used for:
- The input `.pcap` filename
- The optional `--plots` flag

Relevant usage:
```python
parser = argparse.ArgumentParser()
parser.add_argument("pcap", help="pcap file to analyze")
parser.add_argument("--plots", action="store_true")
```

Because `argparse` is part of Python’s standard library, it is very stable and unlikely to need replacement.

---

# Installation

## 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

## 2. Install Dependencies
```bash
pip install scapy pandas matplotlib
```

## 3. Recommended `requirements.txt`
You may want to include a `requirements.txt` file in the repository:

```text
scapy
pandas
matplotlib
```

Then install with:

```bash
pip install -r requirements.txt
```

---

# How to Run

## Basic Usage
```bash
python analyzer.py your_file.pcap
```

## Run with Plots
```bash
python analyzer.py your_file.pcap --plots
```

---

# Example Output

```text
Analyzing PCAP file...

--- Traffic Summary ---
Packets analyzed: 752
Total traffic: 0.09 MB

Protocol Breakdown:
TCP: 70.35%
OTHER: 21.41%
UDP: 8.24%

Top Talkers:
127.0.0.1 -> 0.07 MB

               src              dst protocol  bytes
0        127.0.0.1        127.0.0.1      TCP  57689
4  122.122.122.134   122.122.122.10    OTHER   7628
2        127.0.0.1        127.0.0.1    OTHER   6164
5   122.122.122.10  122.122.122.134    OTHER   5128
3        127.0.0.1        127.0.0.1      UDP   2240
```

---

# Output Explanation

## Traffic Summary
Shows:
- Total number of IP packets analyzed
- Total traffic size in megabytes

## Protocol Breakdown
Shows what percentage of packets belong to:
- TCP
- UDP
- OTHER

This is based on packet counts, not byte counts.

## Top Talkers
Shows the top source IPs by total bytes sent.

Important note: in the current implementation, only **source hosts** are counted toward `host_bytes`. This means the chart/report represents **senders**, not total combined send/receive volume.

## Top Flows
Shows the highest-byte flows, where a flow is defined as:
```text
(source IP, destination IP, protocol)
```

---

# Code Walkthrough

## `TrafficAnalyzer.__init__(pcap_file)`
Initializes the analyzer by:
- Saving the `.pcap` filename
- Loading packets with Scapy
- Creating dictionaries for aggregation
- Setting packet/byte counters to zero

## `analyze()`
Main processing loop.

For each packet:
1. Skip if it is not an IP packet
2. Extract source and destination IP
3. Compute packet size
4. Increment total counters
5. Update source host byte count
6. Detect protocol (`TCP`, `UDP`, or `OTHER`)
7. Update protocol count
8. Update flow byte count

## `print_summary()`
Prints:
- Total packet count
- Total traffic volume
- Protocol percentages
- Top 5 talkers

## `flow_table()`
Builds a Pandas DataFrame from the flow dictionary.

Columns:
- `src`
- `dst`
- `protocol`
- `bytes`

## `plot_protocols()`
Creates a bar chart showing protocol counts.

## `plot_top_talkers()`
Creates a bar chart showing the top 5 source hosts by MB sent.

## `main()`
Handles the CLI workflow:
1. Parse arguments
2. Create analyzer object
3. Run analysis
4. Print summary
5. Print top flows
6. Generate plots if requested

---

# Assumptions and Limitations

This project is intentionally lightweight and uses simplified assumptions.

## Current Assumptions
- Only IP packets are analyzed
- Only `TCP` and `UDP` are explicitly categorized
- All other IP traffic is grouped as `OTHER`
- Host traffic is counted by source IP only
- The full `.pcap` file is loaded into memory at once

## Limitations
- Does not inspect ports, flags, or payload contents
- Does not reconstruct sessions
- Does not distinguish application-layer protocols
- Does not track bidirectional conversations as a single merged flow
- Large `.pcap` files may use significant memory because `rdpcap()` loads everything at once
- Does not export flow tables to CSV by default
- Does not currently support filtering by IP, protocol, or port

---

# Future-Proofing / Maintenance Guide

This section is meant to help future developers keep the project usable if dependencies or APIs change.

## If Scapy Changes or Becomes Deprecated
This is the most important dependency in the project.

Current Scapy-specific logic includes:
```python
scapy.all.rdpcap(...)
scapy.all.IP
scapy.all.TCP
scapy.all.UDP
```

If Scapy changes:
1. Check whether imports must change
2. Check whether `rdpcap()` still returns packet objects in the same way
3. Confirm layer membership tests still work:
   ```python
   if scapy.all.IP in pkt
   ```

If Scapy becomes deprecated:
Possible replacements:
- `pyshark`
- `dpkt`
- `pcapy`

Be aware:
- Replacing Scapy is not a simple drop-in swap
- Packet parsing logic will need to be rewritten
- Layer inspection syntax will change

If long-term stability matters, consider abstracting packet parsing into a separate helper module so the rest of the analyzer does not depend directly on one packet library.

---

## If pandas Changes or Becomes Deprecated
Current pandas usage is limited and easy to replace.

Current usage:
```python
df = pd.DataFrame(data)
df.sort_values("bytes", ascending=False).head()
```

Fallback options:
- Use `sorted(data, key=lambda x: x["bytes"], reverse=True)`
- Print dictionaries directly
- Write structured data to CSV using Python’s built-in `csv` module

Example CSV fallback:
```python
import csv

with open("flows.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["src", "dst", "protocol", "bytes"])
    writer.writeheader()
    writer.writerows(data)
```

---

## If matplotlib Changes or Becomes Deprecated
Plotting is optional, so this is easy to replace.

Current plotting functions only depend on:
- `plt.figure()`
- `plt.bar(...)`
- `plt.title(...)`
- `plt.ylabel(...)`
- `plt.xlabel(...)`
- `plt.xticks(...)`
- `plt.show()`

Fallback options:
- seaborn
- plotly
- plain text summaries only

If a future maintainer removes plotting entirely, the main analyzer still remains useful.

---

## If Large PCAP Files Become a Problem
Current implementation:
```python
self.packets = scapy.all.rdpcap(pcap_file)
```

This loads the full file into memory.

If memory usage becomes an issue:
- Investigate Scapy streaming approaches
- Consider `PcapReader`
- Process packets one at a time rather than loading all at once

A future improvement could change the analyzer to stream packets instead of storing them all up front.

---

## If the Project Needs Better Protocol Detection
Current protocol categories are intentionally simple:
- TCP
- UDP
- OTHER

If more detail is needed later, you can extend the logic to classify:
- ICMP
- ARP
- DNS
- HTTP/HTTPS
- DHCP
- Application-layer traffic by port number

That would make the tool more useful for deeper network analysis.

---

# Suggested Improvements

Possible ways to extend the project:

- Export flow tables to CSV
- Add protocol filters
- Add IP address filters
- Add port-based analysis
- Add packet size distribution plots
- Add time-series traffic visualization
- Add support for bidirectional flow grouping
- Add detection for ICMP and ARP
- Add per-host receive totals in addition to send totals
- Add support for very large `.pcap` files using streaming reads
- Add unit tests
- Add sample `.pcap` files for demonstration
- Add Jupyter notebook support for analysis workflows

---

# Reproducibility and Environment Notes

Because this project analyzes captured traffic rather than generating random data, results depend entirely on the input `.pcap` file.

To improve reproducibility:
- Keep sample `.pcap` files consistent
- Pin dependency versions if needed
- Document the Python version used for development

Example pinned dependencies:
```text
scapy==2.5.0
pandas==2.2.2
matplotlib==3.8.4
```

You only need strict version pinning if future compatibility becomes a concern.

---

# Recommended Future Repository Additions

To make the project more maintainable, consider adding:

## `requirements.txt`
```text
scapy
pandas
matplotlib
```

## `.gitignore`
```text
__pycache__/
*.pyc
.venv/
venv/
```

## Example project structure
```text
PCAP-Traffic-Analyzer/
│
├── analyzer.py
├── example_output.txt
├── capture.pcap
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Summary

This project demonstrates a clean Python workflow for analyzing packet capture data using Scapy, aggregating network statistics with dictionaries and Pandas, and optionally visualizing traffic patterns with Matplotlib.

# Quick Start

```bash
pip install scapy pandas matplotlib
python analyzer.py your_file.pcap
python analyzer.py your_file.pcap --plots
```
