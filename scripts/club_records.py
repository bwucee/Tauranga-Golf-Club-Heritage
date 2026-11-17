"""Continuing club registers and their entry-level provenance."""
from html import escape as e


def source_label(entry):
    label = entry['source']
    if entry.get('recorded_on'):
        label += ' · Added ' + entry['recorded_on']
    link = entry.get('source_link')
    if entry.get('book_page'):
        link = f'book-page-{entry["book_page"]:03}.html'
    return f'<a href="{e(link)}">{e(label)}</a>' if link else e(label)


def member_link(member):
    name = e(member['name'])
    if member.get('person_id'):
        return f'<a href="person-{e(member["person_id"])}.html">{name}</a>'
    return name


def record_table(headers, rows):
    return ('<div class="heritage-table-wrap"><table class="heritage-table"><thead><tr>'
            + ''.join(f'<th scope="col">{header}</th>' for header in headers)
            + '</tr></thead><tbody>'
            + ''.join(f'<tr><th scope="row">{first}</th>'
                      + ''.join(f'<td>{cell}</td>' for cell in rest) + '</tr>'
                      for first, *rest in rows)
            + '</tbody></table></div>')


def life_members_roll(members):
    return record_table(
        ('Member', 'Award date', 'Source'),
        ((member_link(m), e(m['year']), source_label(m))
         for m in sorted(members, key=lambda m: ('1947' if m['year'] == 'Honoured prior to 1948' else m['year'], m['name']))),
    )


RECORD_AREAS = {
    'roles': ('Club leadership', 'book-page-295.html', 'Historical office holders · book pp. 295–298'),
    'greenkeeping': ('Greenkeeping', 'topic-greenkeeping.html', 'Greenkeeping stories and sources'),
    'professional': ('Club professionals', 'topic-resident-professionals.html', 'Club professional stories and sources'),
    'championships': ('Club champions', 'book-page-286.html', 'Historical championship results · book pp. 286–295'),
    'clubhouse': ('Clubhouse', 'topic-clubhouses-administration.html', 'Clubhouse stories and sources'),
    'course': ('Course', 'topic-course-development.html', 'Course development stories and sources'),
}


def build_club_records(records, page, heading):
    body = heading('TAURANGA GOLF CLUB', 'Club records',
                   'The club’s continuing registers of people, results and developments.')
    body += '<ul>' + ''.join(f'<li><a href="#{key}">{title}</a></li>'
                            for key, (title, _, _) in RECORD_AREAS.items())
    body += ('<li><a href="life-members.html">Life Members</a></li>'
             '<li><a href="trophies.html">Trophy register</a></li></ul>')
    for key, (title, link, label) in RECORD_AREAS.items():
        body += f'<section id="{key}"><h2>{title}</h2>'
        appointments = sorted(
            (r for r in records['roles'] if r.get('area', 'roles') == key),
            key=lambda r: (-r['start_year'], r['role']),
        )
        developments = sorted(
            (r for r in records['developments'] if key in r['areas']),
            key=lambda r: r['date'], reverse=True,
        )
        results = sorted(records['championships'], key=lambda r: (-r['year'], r['competition'])) if key == 'championships' else []
        if appointments:
            body += record_table(
                ('Role', 'Office holder or staff member', 'Term', 'Source'),
                ((e(r['role']), e(r['name']), e(r['term']), source_label(r)) for r in appointments),
            )
        if developments:
            body += record_table(
                ('Date', 'Development', 'Source'),
                ((e(r['date']), e(r['event']), source_label(r)) for r in developments),
            )
        if results:
            body += record_table(
                ('Year', 'Championship', 'Winner or result', 'Source'),
                ((str(r['year']), e(r['competition']), e(r['result']), source_label(r)) for r in results),
            )
        if not (appointments or developments or results):
            body += '<p>Entries are awaiting transcription or submission.</p>'
        body += f'<p><a href="{link}">{label} →</a></p></section>'
    body += '<p><a href="feedback.html">Contribute a record or correction →</a></p>'
    page('club-records.html', 'Club records', body)

    body = heading('COMPETITION RESULTS', 'Trophy register',
                   'Recorded winners and results, with a source for each entry.')
    body += ('<p>Coverage varies by trophy and year. Gaps in a source show where a result '
             'was left blank.</p><div class="group-list">')
    for trophy in records['trophies']:
        body += (f'<details id="{e(trophy["id"])}"><summary>{e(trophy["title"])}</summary>'
                 f'<div class="group-body"><p>{e(trophy["context"])}</p>')
        if trophy['note']:
            body += f'<p>{e(trophy["note"])}</p>'
        if trophy['winners']:
            body += record_table(
                ('Year', 'Winner or entry', 'Source'),
                ((str(row['year']), e(row['winner'] or 'Result blank in source'), source_label(trophy | row))
                 for row in sorted(trophy['winners'], key=lambda row: row['year'], reverse=True)),
            )
        else:
            body += f'<p>The supplied record contains no winners.</p><p class="source">{source_label(trophy)}</p>'
        for n in trophy['book_pages']:
            body += f'<p class="source"><a href="book-page-{n:03}.html">Historical context · Pars from the Past, p. {n} →</a></p>'
        body += '</div></details>'
    page('trophies.html', 'Trophy register', body + '</div>')
