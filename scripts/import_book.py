"""Import supplied book text and images, without copying the source PDF.
Run with the separate PyMuPDF environment: python import_book.py /absolute/source.pdf
Generated text is a review transcription; appendix facsimiles preserve table layouts.
"""
from pathlib import Path
import json,re,sys,unicodedata
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1])
doc=fitz.open(source)
chapter_specs=[
(0,1,'The book and its contributors','Introduction','Acknowledgements, foreword and the story behind Dave’s research.'),
(1,6,'Setting the scene','Beginnings','The landscape and community in which golf took root.'),
(2,10,'The first tee','Beginnings','Dr Brown, the Domain course and the club’s earliest records.'),
(3,21,'More distant fairways','The course','The move to the Racecourse Reserve and the work of making a course.'),
(4,32,'The original Gate Pa links','The course','A hole-by-hole account of the original layout, including the racecourse oval.'),
(5,36,'Out of the oval','The course','Redesign, playing conditions and changes to the course.'),
(6,52,'Post war revitalisation','Club life','Membership growth, buildings and the pressures of a flourishing club.'),
(7,59,'Men’s golf','People & club groups','Competition, representative golf and the many personalities of the men’s game.'),
(8,89,'Women’s golf','People & club groups','Players, committee records, life stories and the development of nine-hole golf.'),
(9,116,'Veteran men’s golf','People & club groups','The Veterans’ Society: its founders, tournaments, service and personalities.'),
(10,134,'The women veterans’ golf club','People & club groups','The women veterans’ group, its competition, friendships and growth.'),
(11,139,'Administration','Behind the scenes','Committees, the Board, club leadership and clubhouse redevelopment.'),
(12,164,'Resident professionals','Behind the scenes','The professionals who taught, played and served the membership.'),
(13,176,'Greenkeeping','Behind the scenes','The staff, methods and machinery behind the playing surfaces.'),
(14,183,'Water supply','The course','The long search for dependable water and irrigation.'),
(15,188,'Trees','The course','Planting, shelter, memories and the character of the landscape.'),
(16,194,'Twilight golf','Club life','Summer evenings, volunteers, shared meals and Business House golf.'),
(17,199,'Handicapping through the years','Behind the scenes','From handwritten records to computer systems, as described in 2014.'),
(18,203,'Personal experiences','People & club groups','Members’ own recollections and the stories that give club life its texture.'),
(19,224,'The Ward dynasty','People & club groups','A family’s playing achievements and contribution across generations.'),
(20,229,'The professionals come to play','Tournaments','Year-by-year accounts of the invitation tournament from the 1950s onward.'),
(21,240,'The Spalding Masters and the NZPGA Championship','Tournaments','Major visitors, remarkable rounds and the tournament stage at Gate Pa.'),
(22,254,'Exhibition matches','Tournaments','Leading players visiting for matches and the memories they left.'),
(23,259,'Professional golf returns to Tauranga','Tournaments','The return of professional tournament golf through the Carrus Open.'),
(24,267,'The Una Wickham Memorial Tournament','Tournaments','The women’s match-play tournament and its memorial to Una.'),
(25,277,'The second one hundred years, 2014–2114','Looking ahead','The short-course facility, followed by Dave’s imagined future. Predictions are not historical events.'),
(26,285,'Honours, office holders and trophies','Reference','Championship lists, office holders, trophy histories, life members and the closing photograph.')]
chapters=[]
for pos,(num,start,title,theme,summary) in enumerate(chapter_specs):
 end=chapter_specs[pos+1][1]-1 if pos+1<len(chapter_specs) else len(doc)
 chapters.append(dict(number=num,id=f'book-{num:02}',title=title,theme=theme,summary=summary,start=start,end=end,source_kind='original-book',review_status='transcription-review'))
def clean(value):
 return ''.join(c for c in unicodedata.normalize('NFC',value) if c in '\n\t' or unicodedata.category(c)[0]!='C').strip()
def is_heading(t):
 letters=''.join(c for c in t if c.isalpha())
 return 3<=len(letters) and len(t)<120 and letters.isupper() and len(t.split())<19
pages=[];assets=[];seen={}
asset_dir=ROOT/'assets/book';asset_dir.mkdir(exist_ok=True)
for idx,p in enumerate(doc):
 n=idx+1;ch=next(x for x in chapters if x['start']<=n<=x['end']);blocks=[]
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  lines=[clean(''.join(sp['text'] for sp in line['spans'])) for line in b['lines']]
  lines=[x for x in lines if x and not re.fullmatch(r'Page\s*\d+',x) and x!='Tauranga Golf Club - Pars from the Past']
  if not lines:continue
  if sum(len(x)<=2 for x in lines)/len(lines)>.7 and len(lines)>4:continue
  lines=[x for x in lines if len(x)>1]
  if not lines:continue
  # Separate a named story heading from the paragraph beneath it.
  if len(lines)>1 and is_heading(lines[0]):
   blocks.append(dict(kind='heading',text=lines.pop(0)))
  if not lines:continue
  verse=n in (12,13) and len(lines)>3 and sum(map(len,lines))/len(lines)<52
  text=('\n' if verse else ' ').join(lines)
  blocks.append(dict(kind='verse' if verse else 'heading' if is_heading(text) else 'paragraph',text=text))
 if n in [89,116,134]:blocks=[dict(kind='heading',text=ch['title'])]
 # The original title and illustration pages are kept, not mistaken for missing prose.
 imgs=[]
 for info in p.get_images(full=True):
  xref,_,w,h=info[:4]
  if min(w,h)<130 or w*h<60000:continue
  if xref not in seen:
   pix=fitz.Pixmap(doc,xref)
   if pix.colorspace is None:continue
   if pix.colorspace.n!=3:pix=fitz.Pixmap(fitz.csRGB,pix)
   if pix.alpha:pix=fitz.Pixmap(pix,0)
   if max(pix.width,pix.height)>1800:
    scale=1800/max(pix.width,pix.height);pix=fitz.Pixmap(pix,round(pix.width*scale),round(pix.height*scale))
   name=f'assets/book/image-{xref}.jpg';pix.save(ROOT/name,jpg_quality=84);seen[xref]=name
  name=seen[xref]
  if name not in imgs:imgs.append(name)
 facsimile=None
 # Preserve the original multicolumn reference pages, avoiding misleading flattened tables.
 if 286<=n<=304:
  facsimile=f'assets/book/reference-{n}.jpg'
  p.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(ROOT/facsimile,jpg_quality=88)
 text='\n\n'.join(x['text'] for x in blocks)
 headings=[x['text'] for x in blocks if x['kind']=='heading' and not x['text'].startswith('CHAPTER')]
 pages.append(dict(number=n,chapter=ch['id'],blocks=blocks,text=text,images=imgs,facsimile=facsimile,headings=headings,speculative=n>=280 and n<=284))
 for k,name in enumerate(imgs):assets.append(dict(id=f'book-page-{n}-image-{k+1}',page=n,chapter=ch['id'],path=name,caption_context=text[:2600],permission='Authorised by project owner, 9 November 2026.'))
book=dict(title='Pars from the Past',editor='David G. S. Mowat',year=2014,chapters=chapters,pages=pages,images=assets)
(ROOT/'content/book.json').write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n')
print('Imported',len(pages),'source pages;',len(chapters),'sections;',len(assets),'image placements;',len(seen),'unique images.')
print('Text characters:',sum(len(p['text']) for p in pages))
