"""Static views for the complete, attributed book collection."""
from html import escape as e
import json
import re

def build_book_views(root, page, heading, book, collection):
    chapters=book['chapters']
    chapter_map={c['id']:c for c in chapters}
    source_pages=book['pages']
    grouped={c['id']:[p for p in source_pages if p['chapter']==c['id']] for c in chapters}
    def source_link(n,label=None):
        return f'<a href="book-page-{n:03}.html">{e(label or f"Page {n}")}</a>'
    def chapter_link(c):
        return f'<a href="{c["id"]}.html">{e(c["title"])}</a>'
    def tools():
        return '<div class="reader-tools"><a href="book.html">All book chapters</a><a href="search.html">Search names &amp; stories</a><a href="book-26.html">Honours &amp; trophies</a></div>'
    themes=list(dict.fromkeys(c['theme'] for c in chapters))
    contents='<div class="book-themes">'
    for theme in themes:
        selected=[c for c in chapters if c['theme']==theme]
        contents+=f'<details><summary>{e(theme)}<span>{len(selected)} section'+('s' if len(selected)!=1 else '')+'</span></summary><div class="chapter-links">'
        for c in selected:
            label=f'Chapter {c["number"]}' if 1<=c['number']<=25 else 'Front matter' if c['number']==0 else 'Appendices'
            contents+=f'<article><span class="eyebrow">{label} · pp. {c["start"]}–{c["end"]}</span><h2>{chapter_link(c)}</h2><p>{e(c["summary"])}</p></article>'
        contents+='</div></details>'
    contents+='</div>'
    page('book.html','Explore Dave’s book',heading('PARS FROM THE PAST · DAVID G. S. MOWAT · 2014','The book, a story at a time.','All 25 chapters, the introduction, photographs and reference pages. Choose a subject, then follow the stories at your own pace.')+'<p><a class="button" href="search.html">Find a name, place or story →</a></p>'+contents+'<aside class="note"><h2>Dave’s words, clearly identified</h2><p>The book pages preserve the original account in a review transcription, separate from the website’s shorter introductions. Page numbers, image captions and attribution stay with the source. The final chapter includes an imagined future, clearly labelled. Tables retain their original page layout.</p></aside>')
    for c in chapters:
        pages=grouped[c['id']]
        # Use the book’s own headings as additional routes into its detail.
        topics=[]
        for p in pages:
            for h in p['headings']:
                if h.casefold()==c['title'].casefold() or h.startswith('CHAPTER'):continue
                topics.append((p['number'],h))
        body='<a class="back" href="book.html">← The book collection</a>'+heading(f'PARS FROM THE PAST · PP. {c["start"]}–{c["end"]}',e(c['title']),e(c['summary']))+tools()
        if c['number']==25:
            body+='<aside class="speculation"><h2>A note on the ending</h2><p>The opening pages describe the short-course facility. The later account is Dave’s imagined future, written in 2014 as if looking back from another century. Its predictions are not historical events.</p></aside>'
        if c['number']==26:
            body+='<p class="lead">Championships, office holders, trophies and life members are preserved as original reference pages. Open a page and enlarge its image to read across the columns.</p>'
        if topics:
            body+='<details class="subject-list"><summary>Stories and subjects in this chapter</summary><ul>'+''.join(f'<li>{source_link(n,h)} <span class="source">· p. {n}</span></li>' for n,h in topics)+'</ul></details>'
        body+='<h2 class="small-heading">Choose a page</h2><div class="source-page-list">'
        for p in pages:
            labels=p['headings'][:2]
            if not labels:labels=[('Photographs and captions' if p['images'] and len(p['text'])<800 else 'Continue the account')]
            body+=f'<a href="book-page-{p["number"]:03}.html"><span>p. {p["number"]}</span><span>{e(" · ".join(labels)[:160])}</span>'+('<span class="image-marker">Images</span>' if p['images'] else '')+'</a>'
        body+='</div>'
        pos=chapters.index(c)
        body+='<div class="reader-pagination">'+(chapter_link(chapters[pos-1]) if pos else '<span></span>')+(chapter_link(chapters[pos+1]) if pos+1<len(chapters) else '<a href="book.html">Back to the collection →</a>')+'</div>'
        page(c['id']+'.html',c['title'],body)
    search_entries=[]
    def readable_paragraphs(text):
        # Reflow long PDF blocks at sentence boundaries without changing their words.
        words=0; start=0; chunks=[]
        for match in re.finditer(r'(?<=[.!?])\s+(?=[A-Z“‘"(])',text):
            candidate=text[start:match.start()]
            if len(candidate.split())<110:continue
            if re.search(r'\b(?:Mr|Mrs|Ms|Dr|St|No)\.$',candidate):continue
            chunks.append(candidate);start=match.end()
        if start<len(text):chunks.append(text[start:])
        return chunks or [text]
    for p in source_pages:
        n=p['number'];c=chapter_map[p['chapter']]
        pagination='<div class="reader-pagination">'+(source_link(n-1,'← Previous page') if n>1 else '<span></span>')+f'<span>Book p. {n} / 305</span>'+(source_link(n+1,'Next page →') if n<305 else '<a href="book.html">The collection →</a>')+'</div>'
        body=f'<a class="back" href="{c["id"]}.html">← {e(c["title"])}</a>'+heading(f'PARS FROM THE PAST · ORIGINAL BOOK · PAGE {n}',e(c['title']),'David G. S. Mowat, editor · Published 2014')+pagination
        if c['number']==25:
            body+='<aside class="speculation"><strong>Original ending: includes an imagined future.</strong> The short-course account is followed by predictions written in 2014, not a record of later events. Historical side anecdotes also appear in the printed chapter.</aside>'
        body+='<div class="source-notice">From the book: original views, recollections and terminology are retained. References to “today”, rules, staff or programmes describe the time of writing. Text extraction is being reviewed; use the page reference when suggesting a correction.</div>'
        if p['facsimile']:
            body+=f'<figure class="reference-facsimile"><a href="{p["facsimile"]}"><img src="{p["facsimile"]}" alt="Original reference page {n} from Pars from the Past; select to enlarge and read its columns" loading="lazy"></a><figcaption>Original book page {n} · Select to enlarge. Layout preserved for accurate reading across columns.</figcaption></figure><details class="source-transcription"><summary>Searchable text from this reference page</summary><p class="source">The extracted text does not retain column relationships. Read the image above for the authoritative layout.</p>'
        body+='<article class="book-prose" aria-label="Original book text">'
        for b in p['blocks']:
            tag='h2' if b['kind']=='heading' else 'pre' if b['kind']=='verse' else 'p'
            if tag=='p':body+=''.join(f'<p>{e(t)}</p>' for t in readable_paragraphs(b['text']))
            else:body+=f'<{tag}>{e(b["text"])}</{tag}>'
        if not p['blocks']:
            body+='<p class="source">This is an illustration page with no extracted text.</p>'
        body+='</article>'
        if p['facsimile']:body+='</details>'
        if p['images']:
            body+='<section class="page-images"><h2>Images from this book page</h2><p class="source">Original caption text is retained in the passage above. Image positions differ from the printed page; no identities or dates have been inferred from position.</p><div class="book-image-grid">'
            for i,img in enumerate(p['images']):
                body+=f'<figure><a href="{img}"><img src="{img}" alt="Book page {n}, image {i+1}; refer to the original caption text" loading="lazy"></a><figcaption>Pars from the Past, p. {n} · Image {i+1} · Select to enlarge</figcaption></figure>'
            body+='</div></section>'
        body+=pagination+tools()
        page(f'book-page-{n:03}.html',f'Book page {n}: {c["title"]}',body)
        search_entries.append(dict(title=c['title']+f' · p. {n}',url=f'book-page-{n:03}.html',text=p['text'],type='Original book',page=n))
    for a in collection['articles']:
        search_entries.append(dict(title=a['title'],url=a['id']+'.html',text=a['intro']+' '+ ' '.join(a['paragraphs']),type='Story introduction',page=None))
    (root/'assets/search-index.json').write_text(json.dumps(search_entries,ensure_ascii=False,separators=(',',':'))+'\n')
    page('search.html','Search the collection',heading('NAMES · PLACES · STORIES','Follow a name or a memory.','Search the original book and the website’s story introductions. Try a surname, a tournament, a year or a place.')+'<form id="collection-search" class="search-form" role="search"><label for="search-input">Search the collection</label><div><input id="search-input" name="q" type="search" placeholder="For example: Mirrielees, juniors, Carrus" autocomplete="off" maxlength="150"><button type="submit">Search</button></div></form><p id="search-status" role="status" aria-live="polite">Enter at least two characters. Search runs within your browser.</p><div id="search-results"></div><noscript><p>Search needs JavaScript. You can still <a href="book.html">browse all chapters</a> and read every page without it.</p></noscript><script src="assets/search.js" defer></script>')
    # All book photographs are grouped by chapter, rather than loading into one huge gallery.
    gallery='<div class="book-themes">'
    for c in chapters:
        entries=[p for p in grouped[c['id']] if p['images']]
        if not entries:continue
        gallery+=f'<details><summary>{e(c["title"])}<span>{sum(len(p["images"]) for p in entries)} images</span></summary><div class="book-image-grid">'
        for p in entries:
            for i,img in enumerate(p['images']):
                caption=p['text'] if len(p['text'])<850 else ''
                gallery+=f'<figure><a href="book-page-{p["number"]:03}.html"><img src="{img}" alt="Book image from page {p["number"]}; open the source page for its context" loading="lazy"></a><figcaption><a href="book-page-{p["number"]:03}.html">Book p. {p["number"]} · View caption and context →</a>'+ (f'<p>{e(caption)}</p>' if caption else '')+'</figcaption></figure>'
        gallery+='</div></details>'
    gallery+='</div>'
    page('book-images.html','Photographs throughout the book',heading('THE BOOK’S PHOTOGRAPHIC RECORD','Photographs, in their context.','Explore the images by chapter. Open any image’s source page for its original caption and surrounding account.')+gallery+'<p class="source">Images authorised for publication by the project owner on 9 November 2026. Where dates, identities or original photographers are not supplied, none have been added. Decorative rules and tiny printer graphics are excluded.</p>')
