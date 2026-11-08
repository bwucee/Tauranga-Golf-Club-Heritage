from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
R=Path(__file__).resolve().parents[1]
class Scan(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.ids=set();self.imgs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag in ('img','link'):
   url=a.get('src') if tag=='img' else a.get('href')
   if url:self.links.append(url)
  if tag=='img':assert 'alt' in a,'Missing image alt'
scans={}
for p in R.glob('*.html'):
 s=Scan();s.feed(p.read_text());scans[p]=s
for p,s in scans.items():
 for link in s.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  t=p.parent/unquote(u.path) if u.path else p
  assert t.exists(),f'{p.name}: missing {link}'
  if u.fragment and t in scans:assert u.fragment in scans[t].ids,f'{p.name}: missing fragment {link}'
assert not list(R.rglob('*.pdf')),'PDF must remain outside website'
assert not (R/'.github/workflows').exists(),'No automatic publication before review'
print(f'PASS: {len(scans)} pages; local links, fragments, images and source exclusion checked.')
