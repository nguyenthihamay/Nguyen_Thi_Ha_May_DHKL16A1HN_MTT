import pyshark

# Load the uploaded pcapng file
pcap_file_path = "E:\Bài tập tin học cơ sở\http_wireshark.pcapng"

# Use PyShark to read the file
cap = pyshark.FileCapture(pcap_file_path, use_json=True)

# Prepare a summary list for OSI layer analysis
packets_summary = []

for pkt in cap:
    try:
        packet_info = {
            'No.': pkt.number,
            'Time': pkt.sniff_time.isoformat(),
            'MAC Source': pkt.eth.src if hasattr(pkt, 'eth') else 'N/A',
            'MAC Destination': pkt.eth.dst if hasattr(pkt, 'eth') else 'N/A',
            'IP Source': pkt.ip.src if hasattr(pkt, 'ip') else 'N/A',
            'IP Destination': pkt.ip.dst if hasattr(pkt, 'ip') else 'N/A',
            'Transport Layer': pkt.transport_layer if hasattr(pkt, 'transport_layer') else 'N/A',
            'Protocol': pkt.highest_layer
        }
        packets_summary.append(packet_info)
    except Exception:
        continue

# Limit to first 10 packets for preview
packets_summary[:10]

