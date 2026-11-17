"""Views for separately supplied club heritage records."""
import json
from html import escape as e
from club_records import life_members_roll

def build_heritage_additions(root, page, heading, records):
    data = json.loads((root / 'content/heritage-additions.json').read_text())
    body = heading('SERVICE TO THE CLUB', 'Our Life Members.',
                   'The club’s continuing roll of Life Members, with award dates and sources.')
    body += life_members_roll(records['life_members'])
    body += '<p><a href="feedback.html">Contribute a date or correction →</a></p>'
    if data.get('life_member_profiles'):
        body += '<h2>The people behind the honour roll</h2><p>Profiles added from the supplied Life Members compilation on 10 November 2026. Some reproduce or overlap Mowat’s account; others add later club notices or biographical context. Sources and dates stay with each profile.</p><div class="group-list">'
        for profile in data['life_member_profiles']:
            body += f'<details id="{e(profile["id"])}"><summary>{e(profile["name"])}<span>Read the profile</span></summary><div class="group-body">'
            body += ''.join(f'<p>{e(p)}</p>' for p in profile['paragraphs'])
            if profile['note']:
                body += f'<p class="source">{e(profile["note"])}</p>'
            body += f'<p class="source">Supplied source: Life Members Landscape.pdf, PDF pp. {", ".join(str(n) for n in profile["pdf_pages"])}.</p>'
            body += '<p class="source">Compare with Mowat: '+ ' · '.join(f'<a href="book-page-{n:03}.html">p. {n}</a>' for n in profile['book_pages'])+'</p></div></details>'
        body += '</div><p class="source">The compilation also contains correspondence, a historical subscription sheet and third-party clippings. The profiles summarise the relevant history; private email headers, signatures and administrative instructions are not reproduced.</p>'
    page('life-members.html', 'Life Members', body)

    if data.get('jack_carter'):
        jack = data['jack_carter']
        body = heading('A MEMBER’S OWN ACCOUNT', e(jack['title']), e(jack['intro']))
        body += f'<div class="prose"><p class="source">By Jack Carter · {e(jack["date_note"])}</p><p>Jack’s recollections are presented in his own words. His account of membership and handicap arrangements describes his experience at the time, rather than a current club policy. Mowat also records Jack’s administrative service and his work with Jay in the pro shop on p. 78.</p>'
        body += ''.join(f'<p>{e(p)}</p>' for p in jack['paragraphs'])
        body += f'<p class="source">Editorial correction: {e(jack.get("editorial_note",""))}</p>'
        body += '<p class="source">Source: JACK CARTERS GOLF HISTORY.docx, supplied 10 November 2026. The text retains the contributor’s wording; a paragraph split within “Championship Plate” has been joined.</p><p><a href="life-members.html">Life Members →</a> · <a href="book-page-078.html">Jack and Jay in Mowat’s account · p. 78 →</a> · <a href="club.html#juniors">Junior golf →</a></p></div>'
        body += '<div class="reader-tools"><a href="topic-individual-stories.html">Individual stories</a><a href="topic-life-members.html">Life members</a><a href="topic-resident-professionals.html">Resident professionals</a><a href="topic-tournaments.html">Tournaments</a><a href="topic-club-groups.html">Club groups</a></div>'
        page('jack-carter.html', jack['title'], body)

    body = heading('MEMBER MEMORIES', 'What do you remember?',
                   'Help preserve the people, places and everyday experiences that made Tauranga Golf Club part of your life.')
    body += '<div class="prose"><p>A short recollection can add something that an honours board cannot: a personality, a friendship or the way a day at the club once felt.</p>'
    if data.get('jack_carter'):
        body += '<h2>Jack Carter’s golfing life</h2><p>Jack recalls his first job at the club in 1957, golf in Canada, the development of junior competition and service to club and provincial teams.</p><p><a href="jack-carter.html">Read Jack’s own account →</a></p>'
    body += '<h2>A few ways to begin</h2><p>These questions are adapted from the supplied Member Nostalgia interview template.</p><ul>'
    for prompt in data['memory_prompts']:
        body += f'<li>{e(prompt)}</li>'
    body += '</ul><h2>Share a memory or arrange an interview</h2><p>Send your recollection to the club member who shared this collection with you, or use the <a href="feedback.html">feedback options</a>. Please include your name, when you joined, approximate dates and the names of people mentioned. For photographs, include the photographer or owner where known and permission for online use.</p><p>Personal recollections will be credited to the contributor. Historical details will be compared with Mowat’s book and the club’s official history before being incorporated into the wider account.</p><p class="source">Interview prompts adapted from Interview Template for Member Nostalgia.docx, Club History All. Jack Carter’s written recollection was supplied separately.</p></div>'
    page('member-memories.html', 'Member memories', body)

    body = heading('FROM THE CLUB HERITAGE FOLDER', 'Photographs, more connections.',
                   'Separately supplied portraits and event photographs, with their captions and connections to the existing collection.')
    body += '<p class="source">Some subjects also appear in the book. These files are additional supplied copies or views, not necessarily newly discovered events. Original captions remain within the images where supplied. Photographer credits are not provided in these files.</p><div class="archive-grid">'
    for photo in data['photographs']:
        body += f'<article class="supplied-photo"><figure><a href="{e(photo["path"])}"><img src="{e(photo["path"])}" alt="{e(photo["title"])}" loading="lazy"></a><figcaption>{e(photo["title"])}</figcaption></figure><h2>{e(photo["title"])}</h2><p>{e(photo["caption"])}</p>'
        body += f'<p><a href="{e(photo["story"])}">Read the related account →</a></p>'
        for n in photo['book_pages']:
            body += f'<p class="source"><a href="book-page-{n:03}.html">Compare with Mowat’s account · p. {n} →</a></p>'
        body += f'<p class="source">Source: Club History All / {e(photo["source"])}. Added {e(photo.get("added", "9 November 2026"))}.</p></article>'
    body += '</div>'
    page('supplied-photographs.html', 'Supplied heritage photographs', body)
