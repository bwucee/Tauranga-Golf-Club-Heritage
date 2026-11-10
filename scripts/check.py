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
# Only the two explicitly approved complete source documents are published.
import json,hashlib,re
source_documents=json.loads((R/'content/documents.json').read_text())
allowed={R/doc['path'] for doc in source_documents}
assert set(R.rglob('*.pdf'))==allowed
for doc in source_documents:
 path=R/doc['path']
 assert path.read_bytes().startswith(b'%PDF-')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==doc['sha256']
 assert path.stat().st_size==doc['bytes']
for path,scan in scans.items():
 for link in scan.links:
  u=urlsplit(link)
  if not u.scheme and u.path.endswith('.pdf'):
   target=path.parent/unquote(u.path)
   assert target in allowed
   if u.fragment:
    match=re.fullmatch(r'page=(\d+)',u.fragment)
    assert match, f'Unexpected PDF fragment: {link}'
    source=next(doc for doc in source_documents if R/doc['path']==target)
    assert 1<=int(match[1])<=source['pages']

assert not (R/'.github/workflows').exists(),'No automatic publication before review'
print(f'PASS: {len(scans)} pages; local links, PDF page destinations, images and approved source documents checked.')

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
catalogue=json.loads((R/'content/catalogue.json').read_text())
assert len(index)==305+len(collection['articles'])+len(catalogue['topics'])+len(catalogue['people'])+len(catalogue['source_records'])+1+len(json.loads((R/'content/heritage-additions.json').read_text())['trophies'])+3+sum(len(s['entries']) for s in catalogue.get('volunteer_sections',[]))+1
for item in index:
 target=urlsplit(item['url'])
 assert (R/target.path).exists()
 if target.fragment and R/target.path in scans:assert target.fragment in scans[R/target.path].ids
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

# Cross-subject membership and contributor-supplied additions must survive each build.
topics={t['id'] for t in catalogue['topics']}
for article in collection['articles']:
 assert article['topics'] and set(article['topics'])<=topics
for record in catalogue['source_records']:
 assert set(record['topics'])<=topics
 assert all(1<=n<=48 for n in record['printed_pages'])
expected={'Jack Carter':2019,'Alison Holdem':2019,'Adrienne Coad':2022,'Jackie Reynish':2023,'Chris McAlpine':2024}
assert {p['name']:p['life_membership_year'] for p in catalogue['people'] if p.get('life_membership_year')}==expected
assert all('Bruce Partridge' in p['source'] for p in catalogue['people'] if p.get('life_membership_year'))
assert len([m for m in catalogue['life_members'] if not m.get('added_after_book')])==33
assert 'Maurice Code' not in ' '.join(json.loads((R/'content/heritage-additions.json').read_text())['jack_carter']['paragraphs'])
assert (R/'jack-carter.html').read_text().count('Maurice Coad')>=2
assert len({p['id'] for p in catalogue['people']})==len(catalogue['people'])
assert all(not (280<=n<=284) for p in catalogue['people'] for n in p['book_pages'])
print('PASS: subject cross-links, programme references, original life-members roll and five later additions.')

for section in catalogue.get('volunteer_sections',[]):
 for entry in section['entries']:
  assert all(1<=n<=305 and not 280<=n<=284 for n in entry['book_pages'])
assert 'volunteers-benefactors' in topics
print('PASS: volunteer subject entries retain valid source pages and exclude the imagined future.')

programme=json.loads((R/'content/catalogue.json').read_text())
for record in programme['source_records']:
 expected=f'pdf-viewer/web/viewer.html?file=../../documents/spalding-masters-1968-searchable.pdf#page={record["printed_pages"][0]+2}'
 for topic in record['topics']:assert expected in (R/f'topic-{topic}.html').read_text()
assert 'pdf-viewer/web/viewer.html?file=../../documents/pars-from-the-past.pdf#page=186' in (R/'book-page-186.html').read_text()
assert all('pdf-viewer/web/viewer.html?file=../../'+doc['path']+'#page=1' in (R/'archive.html').read_text() for doc in source_documents)
print('PASS: archive contains complete PDFs; programme references map printed pages to PDF pages.')

from urllib.parse import parse_qs
for path,scan in scans.items():
 for link in scan.links:
  u=urlsplit(link)
  if u.path=='pdf-viewer/web/viewer.html':
   file=parse_qs(u.query).get('file',[''])[0]
   source=(R/'pdf-viewer/web'/file).resolve()
   assert source in {p.resolve() for p in allowed}
   doc=next(doc for doc in source_documents if (R/doc['path']).resolve()==source)
   assert re.fullmatch(r'page=\d+',u.fragment)
   assert 1<=int(u.fragment.split('=')[1])<=doc['pages']
assert '2000–Future' in (R/'timeline.html').read_text()
assert 'Looking ahead' in (R/'chapter-modern.html').read_text()
assert 'person-jackie-reynish.html' in (R/'timeline.html').read_text()
assert 'looking-ahead.html' not in {t[3]+'.html' for t in collection['timeline']}
assert all(s in (R/'index.html').read_text() for s in ['collection-shortcuts','people-index.html','archive.html','editorial-updates.html'])
print('PASS: reader links target valid original PDF pages; 2000–Future distinguishes milestones and future discussion.')
