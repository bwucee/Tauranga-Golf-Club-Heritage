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
  if tag in ('img','link','script'):
   url=a.get('href') if tag=='link' else a.get('src')
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

# Every source page belongs to exactly one chapter and is available to the reader.
import json
book=json.loads((R/'content/book.json').read_text())
assert [p['number'] for p in book['pages']]==list(range(1,306))
assert [c['number'] for c in book['chapters'] if 1<=c['number']<=25]==list(range(1,26))
for p in book['pages']:
 assert (R/f"book-page-{p['number']:03}.html").exists()
 assert all((R/img).exists() for img in p['images'])
 assert len([c for c in book['chapters'] if c['start']<=p['number']<=c['end']])==1
 if 286<=p['number']<=304:assert p['facsimile'] and (R/p['facsimile']).exists()
 if 280<=p['number']<=284:assert 'imagined future' in (R/f"book-page-{p['number']:03}.html").read_text()
collection=json.loads((R/'content/collection.json').read_text())
index=json.loads((R/'assets/search-index.json').read_text())
additions=json.loads((R/'content/heritage-additions.json').read_text())
assert len(index)==305+len(collection['articles'])+len(additions['trophies'])+len(additions['photographs'])+2
for item in index:assert (R/urlsplit(item['url']).path).exists()
print('PASS: complete 305-page coverage, 25 chapters, images, reference layouts, speculation labels and search targets.')

class SourceText(HTMLParser):
 def __init__(self):super().__init__();self.inside=False;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag=='article' and dict(attrs).get('aria-label')=='Original book text':self.inside=True
 def handle_endtag(self,tag):
  if tag=='article':self.inside=False
 def handle_data(self,data):
  if self.inside:self.parts.append(data)
for p in book['pages']:
 reader=SourceText();reader.feed((R/f"book-page-{p['number']:03}.html").read_text())
 expected=' '.join(p['text'].split())
 actual=' '.join(' '.join(reader.parts).split())
 if expected:assert actual==expected,f"Source text changed while rendering page {p['number']}"
seen=set();todo=[R/'index.html']
while todo:
 current=todo.pop()
 if current in seen:continue
 seen.add(current)
 for link in scans[current].links:
  url=urlsplit(link)
  if url.scheme or url.netloc or not url.path.endswith('.html'):continue
  target=current.parent/unquote(url.path)
  if target in scans:todo.append(target)
assert seen==set(scans),f"Unreachable pages: {set(scans)-seen}"
print(f'PASS: source words preserved in all readers; all {len(seen)} pages reachable from home.')
