"""Verified full-name links; source text and spelling remain unchanged."""
from html import escape
import re

class PersonLinks:
    def __init__(self, people):
        aliases = {}
        for person in people:
            for name in [person['name'], *person.get('aliases', [])]:
                key = name.casefold()
                if key in aliases and aliases[key] != person['id']:
                    raise ValueError(f'Ambiguous person alias: {name}')
                aliases[key] = person['id']
        self.aliases = aliases
        self.pattern = re.compile(r'(?<!\w)(?:' + '|'.join(
            re.escape(name).replace(r'\ ', r'\s+') for name in sorted(aliases, key=len, reverse=True)
        ) + r')(?!\w)', re.I)

    def person_id(self, match):
        return self.aliases[' '.join(match.group().split()).casefold()]

    def ids(self, text):
        return {self.person_id(m) for m in self.pattern.finditer(text)}

    def render(self, text):
        result = []; start = 0
        for match in self.pattern.finditer(text):
            result.append(escape(text[start:match.start()]))
            result.append(f'<a class="person-link" href="person-{self.person_id(match)}.html">{escape(match.group())}</a>')
            start = match.end()
        result.append(escape(text[start:]))
        return ''.join(result)
