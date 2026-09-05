"""Pull the characters, abilities and clues out of a Masia Can Travi Nou HTML kit."""
import html
import json
import re
import sys


def _clean(fragment):
    """HTML fragment -> plain text, keeping <strong>/<em> as markers."""
    s = fragment
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</?(strong|b)>', '**', s)
    s = re.sub(r'</?(em|i)>', '__', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def _split_cards(blob, marker):
    """Split a blob into self-contained card chunks starting at `marker`."""
    starts = [m.start() for m in re.finditer(re.escape(marker), blob)]
    chunks = []
    for i, start in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else len(blob)
        page = blob.find('<div class="page', start)
        if 0 <= page < nxt:
            nxt = page
        chunks.append(blob[start:nxt])
    return chunks


def _page(doc, glean_id):
    i = doc.find(f'data-glean-id="{glean_id}"')
    if i < 0:
        raise KeyError(glean_id)
    start = doc.rfind('<div class="page', 0, i)
    end = doc.find('<div class="page', start + 10)
    return doc[start:end if end > 0 else len(doc)]


def characters(doc):
    out = []
    for seg in _split_cards(doc, '<div class="char-card"'):
        cid = re.search(r'data-glean-id="(char-[^"]+)"', seg).group(1)
        title = _clean(re.search(r'char-title">(.*?)</span>', seg, re.S).group(1))
        num, name = re.match(r'(\d+)\.\s*(.*)', title).groups()
        read = _clean(re.search(r'char-intro-read">(.*?)</div>', seg, re.S).group(1))
        read = re.sub(r'^\*\*[^*]*\*\*\s*', '', read).strip()
        secret = _clean(re.search(r'Integrated Secret:</strong>(.*?)</p>', seg, re.S).group(1))
        steps = [_clean(s) for s in re.findall(r'guided-step">(.*?)</div>', seg, re.S)]
        role_txt = _clean(re.search(r'role-secret">(.*?)</div>', seg, re.S).group(1))
        label = _clean(re.search(r'rlabel">(.*?)</span>', seg, re.S).group(1))
        role_txt = role_txt[len(label):].strip()
        out.append({
            'id': cid, 'num': int(num), 'name': name.strip(),
            'read_aloud': read, 'integrated_secret': secret,
            'chapters': steps, 'role_label': label, 'role_text': role_txt,
        })
    return sorted(out, key=lambda c: c['num'])


def abilities(doc):
    blob = ''.join(_page(doc, f'page-abilities-{i}') for i in (1, 2, 3, 4))
    by_char = {}
    for card in _split_cards(blob, '<div class="cut-card">'):
        badge = _clean(re.search(r'cut-card-badge[^>]*>(.*?)</span>', card, re.S).group(1))
        cost = re.search(r'cut-card-footer">(.*?)</div>', card, re.S)
        by_char.setdefault(badge, []).append({
            'title': _clean(re.search(r'cut-card-title">(.*?)</div>', card, re.S).group(1)),
            'body': _clean(re.search(r'cut-card-body">(.*?)</div>', card, re.S).group(1)),
            'tip': _clean(re.search(r'cut-card-tip">(.*?)</div>', card, re.S).group(1)),
            'cost': _clean(cost.group(1)) if cost else '',
        })
    return by_char


def clues(doc):
    blob = _page(doc, 'page-clues-1') + _page(doc, 'page-clues-2')
    out = []
    for card in _split_cards(blob, '<div class="cut-card">'):
        badge = _clean(re.search(r'cut-card-badge[^>]*>(.*?)</span>', card, re.S).group(1))
        ch = int(re.search(r'CHAPTER (\d+)', badge).group(1))
        out.append({
            'chapter': ch,
            'title': _clean(re.search(r'cut-card-title">(.*?)</div>', card, re.S).group(1)),
            'body': _clean(re.search(r'cut-card-body">(.*?)</div>', card, re.S).group(1)),
        })
    return out


def extract(path):
    doc = open(path, encoding='utf-8').read()
    kit = {'characters': characters(doc), 'abilities': abilities(doc), 'clues': clues(doc)}
    for c in kit['characters']:
        key = c['name'].replace('THE ', '')
        c['abilities'] = kit['abilities'][key]
    return kit


if __name__ == '__main__':
    k = extract(sys.argv[1])
    print(json.dumps(k, ensure_ascii=False, indent=1))
