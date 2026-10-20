import time
from pathlib import Path
import requests_cache

DISCOVERY = 'http://agent.invoice.test:8080/.well-known/agent-card.json'
STATE = Path('/state/phase')
MESSAGE = 'Client sending invoice #1337 details'

session = requests_cache.CachedSession(
    backend='memory', cache_control=True,
    allowable_methods=('GET',), expire_after=None,
)

def discover(label):
    response = session.get(DISCOVERY, timeout=5)
    response.raise_for_status()
    card = response.json()
    print(f'[{label}] HTTP response from_cache={getattr(response,"from_cache",False)}',flush=True)
    print(f'[{label}] Cache-Control={response.headers.get("Cache-Control")}',flush=True)
    print(f'[{label}] Agent endpoint={card["supportedInterfaces"][0]["url"]}',flush=True)
    return card

def task(label, card):
    endpoint = card['supportedInterfaces'][0]['url']
    response = session.post(endpoint,json={'message':{'parts':[{'text':MESSAGE}]}},timeout=5)
    response.raise_for_status()
    print(f'[{label}] Task handled by {response.json().get("handledBy")}',flush=True)

if __name__ == '__main__':
    STATE.write_text('spoof')
    time.sleep(2)
    print('** Phase 1, connecting to evil server through spoofed DNS **',flush=True)
    card1 = discover('PHASE 1')
    task('PHASE 1',card1)
    STATE.write_text('real')
    print('** Phase 2, DNS records have been restored but client still connects to evil server using cached address **',flush=True)
    time.sleep(2)
    card2 = discover('PHASE 2')
    task('PHASE 2',card2)
    print('** Control phase, forcefully bypassing cache, should connect to legit server **',flush=True)
    response = session.get(DISCOVERY,headers={'Cache-Control':'no-cache'},timeout=5)
    response.raise_for_status()
    print(f'[CONTROL] from_cache={getattr(response,"from_cache",False)} endpoint={response.json()["supportedInterfaces"][0]["url"]}',flush=True)
