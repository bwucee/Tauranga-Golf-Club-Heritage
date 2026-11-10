"""Place contributed photographs beside related accounts, outside original book text."""
import json
import re
from html import escape as e
from pathlib import Path

PHOTOS = [p for p in json.loads((Path(__file__).resolve().parents[1] / 'content/heritage-additions.json').read_text())['photographs'] if p.get('people')]

def figures(photos):
    return '<div class="contributed-photos">' + ''.join(
        f'<figure><a href="{e(p["path"])}"><img src="{e(p["path"])}" alt="{e(p["title"])}" loading="lazy"></a><figcaption>{e(p["caption"])}<p class="source">Photograph and identification added {e(p["added"])}. {e(p.get("date_note", "Photograph date not supplied."))}</p></figcaption></figure>'
        for p in photos) + '</div>'

def add_photos(file, body):
    if file.startswith('person-'):
        person = file.removeprefix('person-').removesuffix('.html')
        selected = [p for p in PHOTOS if person in p['people']]
    else:
        selected = [p for p in PHOTOS if p['story'] == file]
    if selected:
        # Place immediately after the introduction, before references or story text.
        body = re.sub(r'(<div class="page-heading">.*?</div>)', lambda m: m[0] + figures(selected), body, count=1, flags=re.S)
    if file == 'life-members.html':
        group = [p for p in PHOTOS if p['id'] == 'club-stalwarts-mowat']
        marker = '<details id="phyll-sandlant">'
        start = body.find(marker)
        if start >= 0:
            pos = body.find('<div class="group-body">', start) + len('<div class="group-body">')
            body = body[:pos] + figures(group) + body[pos:]
    if file == 'life-members.html':
        for photo in PHOTOS:
            if not photo.get('profile'):
                continue
            start = body.find(f'<details id="{photo["profile"]}">')
            if start >= 0:
                pos = body.find('<div class="group-body">', start) + len('<div class="group-body">')
                body = body[:pos] + figures([photo]) + body[pos:]
    if file == 'life-members.html':
        for photo in PHOTOS:
            if photo.get('life_member_name'):
                pattern = r'(<p><strong>' + re.escape(e(photo['life_member_name'])) + r' · .*?</p>)'
                body = re.sub(pattern, lambda m: m[0] + figures([photo]), body, count=1, flags=re.S)
    return body
