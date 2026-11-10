"""Cross-subject catalogue; later contributions stay separate from original sources."""
from html import escape as e
import json

def build_catalogue(root, page, heading, book, collection, cards):
    data=json.loads((root/'content/catalogue.json').read_text())
    topics={t['id']:t for t in data['topics']}
    search=json.loads((root/'assets/search-index.json').read_text())
    def tags(ids):
        return '<div class="reader-tools">'+''.join(f'<a href="topic-{i}.html">{e(topics[i]["title"])}</a>' for i in ids)+'</div>'
    def add_search(title,url,text,kind):
        if url.startswith('documents/') and '#page=' in url:url='pdf-viewer/web/viewer.html?file=../../'+url
        search.append(dict(title=title,url=url,text=text,type=kind,page=None))
    def person_link(p):return f'<a href="person-{p["id"]}.html">{e(p["name"])}</a>'
    def people_list(people):return '<ul class="name-index">'+''.join(f'<li>{person_link(p)}</li>' for p in sorted(people,key=lambda p:p['name'].casefold()))+'</ul>'
    def record_links(records):
        return ''.join(f'<article class="catalogue-entry"><span class="eyebrow">1968 · PROGRAMME</span><h3><a href="documents/spalding-masters-1968-searchable.pdf#page={r["printed_pages"][0]+2}">{e(r["title"])}</a></h3><p>{e(r["summary"])}</p></article>' for r in records)
    intro=heading('BROWSE BY SUBJECT','Follow the parts of club life.','People, work, places and events connect across generations. Start with a subject, then follow its stories, original sources and later contributions.')
    doors='<div class="cards subject-cards">'+''.join(f'<a class="card" href="topic-{t["id"]}.html"><div><h2>{e(t["title"])}</h2><p>{e(t["description"])}</p><span class="read">Explore this subject →</span></div></a>' for t in data['topics'])+'</div>'
    page('subjects.html','Browse by subject',intro+doors+'<aside class="note"><h2>A growing history, rooted in the book</h2><p>Dave Mowat’s 2014 book is the backbone. Contemporary documents, earlier stories and contributions after 2014 are indexed alongside it, with their own sources. An item can belong to several subjects.</p><a href="book.html">Read the original book →</a> · <a href="people-index.html">Find an individual →</a> · <a href="supplied-photographs.html">Supplied heritage photographs →</a></aside>')
    page('people-index.html','People index',heading('INDIVIDUALS · FAMILIES · SERVICE','Find a person.','A growing name index linking book accounts and later contributions. This first selection will expand as more stories are added.')+people_list(data['people'])+'<p><a href="search.html">Search every name in the original book →</a></p>')
    for p in data['people']:
        body='<a class="back" href="people-index.html">← People index</a>'+heading('PEOPLE & CLUB LIFE',e(p['name']),e(p['summary']))+tags(p['topics'])
        if p.get('life_membership_year'):
            body+=f'<section class="note"><h2>Life membership · {p["life_membership_year"]}</h2><p>Year added 10 November 2026. This addition extends the roll published in 2014.</p><p>Further biographical material can be added as it is contributed.</p></section>'
        if p['book_pages']:
            body+='<section><h2>Accounts and references in the book</h2><p>These references retain their original 2014 context.</p>'+''.join(f'<p><a href="book-page-{n:03}.html">Pars from the Past · p. {n} →</a></p>' for n in p['book_pages'])+'</section>'
        if p.get('story'):body+=f'<p><a class="button" href="{p["story"]}">Read the contributed account →</a></p>'
        body+=f'<p class="source">Record source: {e(p["source"])}.</p>'
        url=f'person-{p["id"]}.html';page(url,p['name'],body)
        add_search(p['name'],url,p['summary']+' '+p['source']+' '+('Maurice Coad; correction of Maurice Code in Jack Carter’s story.' if p['id']=='jack-carter' else ''),'Person record')
    for t in data['topics']:
        body='<a class="back" href="subjects.html">← All subjects</a>'+heading('SUBJECT INDEX',e(t['title']),e(t['description']))
        if t['id']=='volunteers-benefactors':
            body+='<p><a class="button" href="volunteers-and-benefactors.html">Read the story of service and generosity →</a></p><h2>Explore the work and the people</h2><p>Eight themes bring together 37 accounts from across the book and the 1968 programme. Original pages retain their full detail, names and context.</p><div class="book-themes">'
            for section in data.get('volunteer_sections',[]):
                body+=f'<details id="{section["id"]}"><summary>{e(section["title"])}</summary><div class="chapter-links">'
                for entry in section['entries']:
                    body+=f'<article><h3>{e(entry["title"])}</h3><p>{e(entry["summary"])}</p><p class="source">'
                    body+=' · '.join(f'<a href="book-page-{n:03}.html">Book p. {n}</a>' for n in entry['book_pages']) if entry['book_pages'] else '<a href="documents/spalding-masters-1968-searchable.pdf#page=50">1968 programme acknowledgement →</a>'
                    body+='</p></article>'
                    add_search(entry['title'],'topic-volunteers-benefactors.html#'+section['id'],entry['summary'],'Volunteers and Benefactors')
                body+='</div></details>'
            body+='</div><aside class="note"><h2>A continuing history</h2><p>A later reflection considers changing health-and-safety expectations and board risk tolerance. It is presented separately in the story, alongside space for future accounts of how volunteering changes.</p></aside>'
        if t['id']=='life-members':
            body+='<h2>Life members recorded in the 2014 book</h2><p>Names and date wording follow the book’s roll. Open the original page to check its layout.</p><p><a href="book-page-304.html">Original life-members roll · p. 304 →</a></p><ul class="name-index">'+''.join(f'<li>{e(m["name"])} · {e(m["year"])}</li>' for m in data['life_members'] if not m.get('added_after_book'))+'</ul><h2>Additional life members</h2><p>Contributed by Club heritage contribution, 10 November 2026. Listed by award year; these additions are separate from the original book.</p><ul>'+''.join(f'<li><a href="person-{m["person_id"]}.html">{e(m["name"])}</a> · {e(m["year"])}</li>' for m in sorted((m for m in data['life_members'] if m.get('added_after_book')),key=lambda m:(m['year'],m['name'])))+'</ul>'
        if t['id']=='life-members':body+='<p><a href="life-members.html">Read the contributed life-member profiles →</a></p>'
        if t['id']=='individual-stories':body+='<p><a href="member-memories.html">Member memories and ways to contribute →</a></p>'
        if t['id']=='honours-rules':body+='<p><a href="trophies.html">Explore the seven contributed trophy records →</a></p>'
        if t['id']=='club-groups':body+='<p><a class="button" href="club.html">Browse Juniors, Women, Nine Hole, Men and Senior Men →</a></p>'
        people=[p for p in data['people'] if t['id'] in p['topics']]
        if people:body+='<section><h2>People to follow</h2>'+people_list(people)+'</section>'
        stories=[a for a in collection['articles'] if t['id'] in a.get('topics',[])]
        if stories:body+='<section><h2>Stories and introductions</h2>'+cards(stories)+'</section>'
        records=[r for r in data['source_records'] if t['id'] in r['topics']]
        if records:body+='<section><h2>From the 1968 programme</h2>'+record_links(records)+'</section>'
        if t.get('book_range'):
            lo,hi=t['book_range'];body+='<section><h2>Follow the original book in detail</h2><div class="book-themes">'
            for c in book['chapters']:
                pages=[p for p in book['pages'] if lo<=p['number']<=hi and p['chapter']==c['id']]
                if not pages:continue
                body+=f'<details><summary>{e(c["title"])}</summary><div class="chapter-links">'
                for p in pages:
                    label=' · '.join(p['headings']) or 'Continue the account'
                    body+=f'<p><a href="book-page-{p["number"]:03}.html">p. {p["number"]} · {e(label)}</a></p>'
                body+='</div></details>'
            body+='</div></section>'
        url=f'topic-{t["id"]}.html';page(url,t['title'],body)
        add_search(t['title'],url,t['description']+' '+' '.join(a['title'] for a in stories),'Subject index')
    body=heading('CONTEMPORARY SOURCE · JANUARY 1968','The Spalding Masters programme','A source for tournament history, course care, individual lives and Tauranga’s wider community. Each part is indexed under its relevant subjects.')
    body+='<aside class="note"><h2>Reading this source</h2><p><a href="documents/spalding-masters-1968-searchable.pdf#page=1">Open the complete searchable programme</a>, including every page and the advertisements. The page links below open it at the relevant place. Printed page 1 is PDF page 3.</p><p>Contemporary statements and later recollections may differ. The original book remains available alongside these additions.</p></aside>'
    for record in data['source_records']:
        pages=' · '.join(f'<a href="documents/spalding-masters-1968-searchable.pdf#page={n+2}">Programme p. {n}</a>' for n in record['printed_pages']);pdf=', '.join(str(n+2) for n in record['printed_pages'])
        body+=f'<article class="catalogue-entry" id="{record["id"]}"><h2>{e(record["title"])}</h2><p>{e(record["summary"])}</p><p class="source">{e(record["source"])} · {pages}.</p>'+tags(record['topics'])+'</article>'
        add_search(record['title'],'documents/spalding-masters-1968-searchable.pdf#page='+str(record['printed_pages'][0]+2),record['summary']+' '+record['source']+' printed pages '+', '.join(map(str,record['printed_pages'])),'Programme source record')
    body+='<section><h2>Photographs from the programme</h2><p>Published in the January 1968 programme; individual photograph dates are not independently established. The Rotorua group shows the earlier tournament. Photographer credits have not been established. Reproduction authorised by the project owner on 10 November 2026.</p><div class="book-image-grid">'
    for photo in data.get('programme_photographs',[]):
        body+=f'<figure id="photo-{photo["id"]}"><a href="{photo["path"]}"><img src="{photo["path"]}" alt="{e(photo["caption"])}" loading="lazy"></a><figcaption>{e(photo["caption"])} <a href="documents/spalding-masters-1968-searchable.pdf#page={photo["pdf_page"]}">Programme p. {photo["printed_page"]} · Open original page →</a></figcaption></figure>'
    body+='</div></section>'
    page('source-spalding-1968.html','1968 Spalding Masters programme',body)
    page('editorial-updates.html','Contributions & corrections',heading('A CONTINUING RECORD','Contributions and corrections.','Later additions keep their date and connection to the original sources.')+'<h2>Life-membership additions</h2><p>Five names and award years were added on 10 November 2026: Jack Carter and Alison Holdem (2019), Adrienne Coad (2022), Jackie Reynish (2023), and Chris McAlpine (2024).</p><p><a href="topic-life-members.html">Read the combined life-members index →</a></p><h2>Jack Carter’s story</h2><p>Both mentions of Maurice Code have been corrected to Maurice Coad in the website transcription, on 10 November 2026. The original document is retained unchanged.</p><h2>1968 programme</h2><p>Twelve source records connect the programme to multiple subjects. Disagreements are retained in their summaries rather than silently changing the book.</p><a href="source-spalding-1968.html">Browse the programme records →</a>')
    add_search('Contributions and corrections','editorial-updates.html','Life members 2019 2022 2023 2024; Jack Carter story Maurice Coad not Maurice Code','Editorial record')
    page('looking-ahead.html','Looking ahead',heading('2000–FUTURE · POSSIBILITIES & DISCUSSION','Where might golf take us next?','A few simple possibilities for the game and the club. This is a place to look ahead, alongside the continuing historical record.')+'<div class="prose"><h2>More ways to enjoy the game</h2><p>Golf’s next chapter could offer more choices about how long a round takes and how people take part. Nine-hole golf, short courses, practice and social events provide starting points for imagining a club that fits different ages, abilities and amounts of spare time.</p><p><a href="topic-club-groups.html">Explore the club groups →</a> · <a href="short-course.html">The short-course story →</a></p><h2>A course suited to its place</h2><p>The Windsor Green story suggests a useful question for the future: how can the club keep offering enjoyable playing conditions while caring for water, trees and the land? Future choices may involve different turf, maintenance methods and expectations of what a good course looks like through the seasons.</p><p><a href="topic-greenkeeping.html">Greenkeeping →</a> · <a href="windsor-green.html">Windsor Green →</a></p><h2>New tools, the same pleasure in playing</h2><p>Imagine technology helping people learn, practise, find playing partners and organise competitions. How much could it improve access and enjoyment, and which parts of golf would members want to keep simple and personal?</p><h2>A club people can afford and belong to</h2><p>Membership choices, the cost of maintaining the course and the welcome offered to newcomers could shape who plays. The next generation may value a wider choice of experiences while still wanting the friendships, competition and sense of place that earlier members enjoyed.</p><h2>Keeping the spirit of contribution</h2><p>Volunteers and benefactors helped build this club. Future forms of service could preserve that sense of ownership as skills, available time, safety expectations and the organisation of work change.</p><p><a href="topic-volunteers-benefactors.html">Volunteers and Benefactors →</a></p><h2>Dave’s imagined second century</h2><p>In 2014 Dave Mowat ended his history by imagining someone looking back over the following hundred years. His vision remains part of the original book. It offers another way to begin a conversation about what the club might become.</p><p><a href="book-page-280.html">Open Dave’s imagined future at book page 280 →</a> · <a href="daves-imagined-century.html">Read the introduction →</a></p><p class="source">Editorial discussion prompts prepared for the continuing collection in November 2026. These possibilities are separate from recorded events and from an adopted club plan.</p></div>')
    add_search('Looking ahead: golf and the club’s future','looking-ahead.html','2000 Future; shorter golf, nine holes, learning, technology, water, turf, membership, affordability, volunteering and Dave Mowat’s imagined second century.','Future discussion')
    heritage=json.loads((root/'content/heritage-additions.json').read_text())
    for trophy in heritage['trophies']:
        add_search(trophy['title'],'trophies.html#'+trophy['id'],trophy['context']+' '+trophy['note']+' '+' '.join(str(y)+' '+w for y,w in trophy['winners']),'Trophy record')
    add_search(heritage['jack_carter']['title'],'jack-carter.html',' '.join(heritage['jack_carter']['paragraphs']),'Member recollection')
    add_search('Member memories','member-memories.html','Personal experiences, recollections and interview prompts','Contribution guide')
    add_search('Supplied heritage photographs','supplied-photographs.html',' '.join(p['title']+' '+p['caption'] for p in heritage['photographs']),'Photograph collection')
    (root/'assets/search-index.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':'))+'\n')
