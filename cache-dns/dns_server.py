from pathlib import Path
from dnslib import QTYPE, RR, A, RCODE
from dnslib.server import BaseResolver, DNSServer

STATE = Path('/state/phase')
class Resolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        name = str(request.q.qname).rstrip('.').lower()
        phase = STATE.read_text().strip() if STATE.exists() else 'spoof'
        mapping = {
            'agent.invoice.test': '172.30.0.3' if phase == 'spoof' else '172.30.0.2',
            'fake_server.com': '172.30.0.3',
        }
        ip = mapping.get(name)
        if ip and request.q.qtype == QTYPE.A:
            reply.add_answer(RR(request.q.qname, QTYPE.A, ttl=0, rdata=A(ip)))
            print(f'[DNS] phase={phase} {name} -> {ip}', flush=True)
        elif not ip:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply

if __name__ == '__main__':
    DNSServer(Resolver(), address='0.0.0.0', port=53).start()
