"""Views for separately supplied club heritage records."""
import json
from html import escape as e

def build_heritage_additions(root, page, heading):
    data = json.loads((root / 'content/heritage-additions.json').read_text())
    body = heading('TROPHIES & HONOUR ROLLS', 'Names carried forward.',
                   'Seven trophy records from the club heritage collection, with the recorded winners and links to Dave Mowat’s historical account.')
    body += '<div class="prose"><p>These are partial transcriptions of the supplied trophy records. A blank year means no winner was entered in that document; it does not establish that no competition took place. Names retain the supplied spelling. The book provides the historical context; additions beyond its coverage are identified here as separate records.</p><p><a href="book-09.html">Veteran men’s golf in Dave’s book →</a> · <a href="life-members.html">Life Members →</a></p></div><div class="group-list">'
    for trophy in data['trophies']:
        body += f'<details id="{e(trophy["id"])}"><summary>{e(trophy["title"])}<span>{len(trophy["winners"])} recorded years</span></summary><div class="group-body">'
        body += f'<p>{e(trophy["context"])}</p>'
        for n in trophy['book_pages']:
            body += f'<p class="source"><a href="book-page-{n:03}.html">Historical context · Pars from the Past, p. {n} →</a></p>'
        if trophy['note']:
            body += f'<p>{e(trophy["note"])}</p>'
        if trophy['winners']:
            body += '<div class="heritage-table-wrap"><table class="heritage-table"><caption>Winners recorded in the supplied document</caption><thead><tr><th scope="col">Year</th><th scope="col">Winner or entry</th></tr></thead><tbody>'
            for year, winner in trophy['winners']:
                body += f'<tr><th scope="row">{year}</th><td>{e(winner or "Not entered in the supplied record")}</td></tr>'
            body += '</tbody></table></div>'
        else:
            body += '<p>No winners are entered in the supplied record.</p>'
        body += f'<p class="source">Source: Club History All / Club Heritage / Men Vets / {e(trophy["source"])}. Added 9 November 2026.</p></div></details>'
    body += '</div>'
    page('trophies.html', 'Trophy register', body)

    body = heading('SERVICE TO THE CLUB', 'Our Life Members.',
                   'The honour roll published in Pars from the Past in 2014, presented as a starting point for a growing record of service.')
    body += '<div class="prose"><p>This list follows Mowat’s published roll. Dates are the dates of recognition as recorded there. “Prior to 1948” and “1948–49” retain the book’s dating. The list is historical through 2014; later appointments can be added from club records.</p><p><a href="book-page-304.html">View the original honour roll · p. 304 →</a> · <a href="book-page-061.html">Read about the early Life Members · p. 61 →</a></p></div><div class="heritage-table-wrap"><table class="heritage-table"><caption>Life Members recorded in the 2014 book</caption><thead><tr><th scope="col">Member</th><th scope="col">Recognition</th></tr></thead><tbody>'
    for name, date in data['life_members']:
        body += f'<tr><th scope="row">{e(name)}</th><td>{e(date)}</td></tr>'
    body += '</tbody></table></div><p class="source">Source: David G. S. Mowat, editor, Pars from the Past (2014), p. 304. Read the original page for the printed layout.</p>'
    page('life-members.html', 'Life Members', body)

    body = heading('MEMBER MEMORIES', 'What do you remember?',
                   'Help preserve the people, places and everyday experiences that made Tauranga Golf Club part of your life.')
    body += '<div class="prose"><p>A short recollection can add something that an honours board cannot: a personality, a friendship or the way a day at the club once felt. These questions are adapted from the supplied Member Nostalgia interview template.</p><h2>A few ways to begin</h2><ul>'
    for prompt in data['memory_prompts']:
        body += f'<li>{e(prompt)}</li>'
    body += '</ul><h2>Share a memory or arrange an interview</h2><p>Send your recollection to the club member who shared this collection with you, or use the <a href="feedback.html">feedback options</a>. Please include your name, when you joined, approximate dates and the names of people mentioned. For photographs, include the photographer or owner where known and permission for online use.</p><p>Personal recollections will be credited to the contributor. Historical details will be compared with Mowat’s book and the club’s official history before being incorporated into the wider account.</p><p class="source">Adapted from Interview Template for Member Nostalgia.docx, Club History All. No completed interviews have been added on this page.</p></div>'
    page('member-memories.html', 'Member memories', body)

    body = heading('FROM THE CLUB HERITAGE FOLDER', 'Five photographs, more connections.',
                   'Separately supplied portraits and event photographs, with their captions and connections to the existing collection.')
    body += '<p class="source">Some subjects also appear in the book. These files are additional supplied copies or views, not five newly discovered events. Original captions remain within the images where supplied. Photographer credits are not provided in these files.</p><div class="archive-grid">'
    for photo in data['photographs']:
        body += f'<article class="supplied-photo"><figure><a href="{e(photo["path"])}"><img src="{e(photo["path"])}" alt="{e(photo["title"])}" loading="lazy"></a><figcaption>{e(photo["title"])}</figcaption></figure><h2>{e(photo["title"])}</h2><p>{e(photo["caption"])}</p>'
        body += f'<p><a href="{e(photo["story"])}">Read the related account →</a></p>'
        for n in photo['book_pages']:
            body += f'<p class="source"><a href="book-page-{n:03}.html">Compare with Mowat’s account · p. {n} →</a></p>'
        body += f'<p class="source">Source: Club History All / {e(photo["source"])}. Added 9 November 2026.</p></article>'
    body += '</div>'
    page('supplied-photographs.html', 'Supplied heritage photographs', body)
