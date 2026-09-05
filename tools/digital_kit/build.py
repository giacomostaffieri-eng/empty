"""Build a phone-only version of a Masia Can Travi Nou murder mystery kit.

Emits, into --out:
  packets/pacchetto-N.html   one self-contained packet per player, contents shuffled
  clues/clue-K.html          one clue per screen, in play order
  clues/retro.html           card back, interleaved between clues so a swipe
                             never lands on the next clue
  regole.html                the digital rules

Nothing here reveals the shuffle to whoever runs it: the mapping is written to
packets/.assignment.json, which is meant to stay unread until after the game.
"""
import argparse
import html
import json
import os
import random
import re
import shutil

from extract import extract

# The physical kit costs abilities in Action Tokens and answers questions with
# printed YES/NO cards. Neither survives a phone-only game, so both mechanics
# are restated. Every substitution the players need to know about lives here so
# the rules page and the cards can never drift apart.
RULE_SUBS = [
    # The kits phrase the printed answer cards several ways, so match loosely.
    (r'\*{0,2}YES or NO (?:Secret )?Answer Card\*{0,2}',
     'the **SÌ or NO screen** in their packet (pages 2 and 3)'),
    (r'(?:their|the) (?:Secret )?Answer Card',
     'the **SÌ or NO screen** in their packet'),
    (r'Steal 1 Action Token from another player and add it to your (?:own )?stash\.',
     'Choose another player: they may **not use any ability during the next Chapter**.'),
    (r'Pay 1, take 1 &mdash; stay funded while starving a rival\.|Pay 1, take 1 — stay funded while starving a rival\.',
     'Play it on whoever is about to make a move, and they lose their next one.'),
    (r'takes \*\*1 Token from the Bank\*\* AND secretly peeks',
     'may use **one extra ability this Chapter** AND secretly peeks'),
]

# Anything still pointing at a printed component after the substitutions above
# is a rule nobody can follow on a phone, so the build refuses to emit it.
PHYSICAL = re.compile(r'\b(?:Tokens?|Bank|Answer Cards?|stash)\b')

# "Cost: 2 Tokens" marked the powerful abilities. With no economy to save up in,
# the same tension comes from locking them to the second half of the game.
TIMING = {
    '1': 'Usabile in <strong>qualsiasi capitolo</strong>',
    '2': 'Solo nel <strong>Capitolo 3 o 4</strong>',
}

CHAPTER_LABEL = {1: 'CAPITOLO 1', 2: 'CAPITOLO 2', 3: 'CAPITOLO 3', 4: 'CAPITOLO 4'}


def md(text):
    """The markers extract.py leaves behind -> HTML."""
    out = html.escape(text)
    out = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', out, flags=re.S)
    out = re.sub(r'__(.+?)__', r'<em>\1</em>', out, flags=re.S)
    return out.replace('\n', '<br>')


def apply_subs(text):
    for pattern, replacement in RULE_SUBS:
        text = re.sub(pattern, replacement, text)
    return text


def check_playable(kit):
    """Every leftover reference to a component that no longer exists."""
    leftovers = []
    for char in kit['characters']:
        texts = [(char['name'], f, char[f])
                 for f in ('read_aloud', 'integrated_secret', 'role_text')]
        for ability in char['abilities']:
            texts += [(f"{char['name']} / {ability['title']}", f, ability[f])
                      for f in ('body', 'tip')]
        for where, field, text in texts:
            for m in PHYSICAL.finditer(apply_subs(text)):
                leftovers.append(f'{where} [{field}]: {m.group(0)}')
    for clue in kit['clues']:
        for m in PHYSICAL.finditer(apply_subs(clue['body'])):
            leftovers.append(f"clue {clue['title']}: {m.group(0)}")
    return leftovers


def ability_meta(ability):
    """(kind, timing-html) for an ability, from its printed cost/type."""
    tokens = re.search(r'Cost: (\d+) Token', ability['cost'])
    kind = 'Instant' if 'Instant' in ability['cost'] else 'Sorcery'
    return kind, TIMING[tokens.group(1) if tokens else '1']


CSS = """
:root {
  --paper: #e3d4b8;
  --blood: #6b0000;
  --blood-bright: #8f0f0f;
  --gold: #a9843f;
  --ink: #17110f;
  --ink-faded: #3a2c24;
  --border: #1a1416;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; }
body {
  font-family: 'EB Garamond', serif;
  color: var(--ink);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: var(--pw);
  height: var(--ph);
  position: relative;
  overflow: hidden;
  background-color: var(--paper);
  background-image:
    radial-gradient(circle at 14% 16%, rgba(60,35,20,0.20) 0%, transparent 20%),
    radial-gradient(circle at 86% 78%, rgba(60,35,20,0.24) 0%, transparent 24%),
    radial-gradient(ellipse at 50% 45%, #efe4cc 0%, #d8c6a3 58%, #b89f74 100%);
  box-shadow: inset 0 0 70px rgba(50,25,10,0.45), inset 0 0 12px rgba(0,0,0,0.30);
}
.page::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  box-shadow: inset 0 0 60px 10px rgba(20,8,5,0.42);
  border: 3px solid var(--border);
}
.sheet {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 26px 22px 34px;
  transform-origin: top center;
  /* Phone pages are much taller than most screens need; centring the block
     keeps a short screen from looking like a truncated one. */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.page::after {
  content: "\\2619";
  position: absolute;
  bottom: 9px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--gold);
  opacity: 0.55;
  font-size: 13px;
}

h1, h2, h3 { font-family: 'Cinzel Decorative', 'Cinzel', serif; text-align: center; margin: 0; }
h1 { font-size: 26px; color: var(--blood); line-height: 1.12; letter-spacing: 0.5px; }
h2 { font-size: 19px; color: var(--blood); line-height: 1.18; }
h3 { font-size: 15px; color: var(--blood); }

.kicker {
  font-family: 'Special Elite', cursive;
  font-size: 10px;
  letter-spacing: 2.4px;
  text-align: center;
  text-transform: uppercase;
  color: var(--ink-faded);
  margin: 6px 0 14px;
}
.rule {
  border: 0;
  border-top: 1px solid rgba(107,0,0,0.35);
  margin: 14px 0;
}
p { margin: 0 0 9px; font-size: 14.5px; line-height: 1.42; }
.box {
  border: 2px solid var(--border);
  background: rgba(255,250,235,0.5);
  padding: 11px 12px;
  margin: 0 0 12px;
}
.box.warn { border-color: var(--blood); background: rgba(107,0,0,0.07); }
.box.gold { border-color: var(--gold); background: rgba(169,132,63,0.10); }
.box h3 { text-align: left; margin-bottom: 6px; }
.box p:last-child { margin-bottom: 0; }
.label {
  font-family: 'Special Elite', cursive;
  font-size: 10px;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: var(--blood);
  display: block;
  margin-bottom: 4px;
}
.speech { font-style: italic; font-size: 15px; line-height: 1.44; }
ol, ul { margin: 0 0 9px; padding-left: 19px; font-size: 14.5px; line-height: 1.4; }
li { margin-bottom: 5px; }
.chapter-line { margin-bottom: 9px; font-size: 14px; line-height: 1.4; }
.chapter-line .label { display: inline; margin-right: 5px; }
.foot {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4px;
  font-family: 'Special Elite', cursive;
  font-size: 9.5px;
  letter-spacing: 1px;
  text-align: center;
  color: var(--ink-faded);
  text-transform: uppercase;
}
.center-stack { width: 100%; }

/* --- SI / NO answer screens: full bleed, readable at arm's length --- */
.page.answer { background: none; box-shadow: none; }
.page.answer .sheet {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 0 40px;
}
.page.answer::before { border: 0; box-shadow: none; }
.page.answer::after { content: none; }
.page.answer.yes { background: #14521f; }
.page.answer.no { background: #6b0000; }
.answer-word {
  font-family: 'Cinzel Decorative', 'Cinzel', serif;
  font-size: 120px;
  font-weight: 900;
  color: #f6ecd6;
  letter-spacing: 4px;
  text-shadow: 0 4px 14px rgba(0,0,0,0.55);
  line-height: 1;
}
.answer-hint {
  font-family: 'Special Elite', cursive;
  font-size: 12px;
  letter-spacing: 1.6px;
  color: rgba(246,236,214,0.82);
  text-align: center;
  text-transform: uppercase;
  margin-top: 22px;
  padding: 0 30px;
  line-height: 1.6;
}

/* --- the sealed role screen --- */
.page.role { background-color: #1a1113; background-image: none; }
.page.role::before { border-color: #000; box-shadow: inset 0 0 70px 14px rgba(0,0,0,0.75); }
.page.role::after { color: var(--gold); }
.page.role h1, .page.role h2 { color: #d9b060; }
.page.role .kicker { color: #9a8a72; }
.page.role p { color: #ece0cb; }
.page.role .box {
  border-color: var(--gold);
  background: rgba(0,0,0,0.35);
}
.role-badge {
  font-family: 'Cinzel Decorative', 'Cinzel', serif;
  font-size: 30px;
  text-align: center;
  letter-spacing: 2px;
  margin: 4px 0 16px;
  text-transform: uppercase;
}
.role-badge.innocente { color: #63a2d8; }
.role-badge.colpevole { color: #d84b4b; }
.seal {
  font-size: 44px;
  text-align: center;
  margin-bottom: 10px;
}

/* --- clue screens --- */

.page.clue h2 { margin-bottom: 15px; }
.clue-badge {
  font-family: 'Special Elite', cursive;
  font-size: 11px;
  letter-spacing: 2.4px;
  text-align: center;
  text-transform: uppercase;
  color: #f3e2c8;
  background: var(--blood);
  border: 1px solid var(--border);
  padding: 5px 0;
  margin-bottom: 18px;
}

.clue-body p { font-size: 16px; line-height: 1.48; }
.effect {
  border-top: 1px dashed rgba(107,0,0,0.5);
  border-bottom: 1px dashed rgba(107,0,0,0.5);
  padding: 11px 0;
  margin-top: 6px;
}
.effect .label { text-align: center; }
.effect p { font-size: 14.5px; margin: 0; }

/* --- card back --- */
.page.back {
  background-color: #14090b;
  background-image:
    radial-gradient(ellipse at 50% 40%, #3a1c1f 0%, #14090b 70%);
}
.page.back .sheet {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.page.back::before { border-color: var(--gold); box-shadow: inset 0 0 60px 12px rgba(0,0,0,0.8); }
.page.back::after { content: none; }
.back-mark { font-size: 84px; color: var(--gold); opacity: 0.85; }
.back-title {
  font-family: 'Cinzel Decorative', 'Cinzel', serif;
  font-size: 22px;
  color: #d9b060;
  text-align: center;
  letter-spacing: 1.5px;
  margin-top: 18px;
  padding: 0 26px;
  line-height: 1.25;
}
.back-sub {
  font-family: 'Special Elite', cursive;
  font-size: 11px;
  letter-spacing: 2.2px;
  color: #8d7a5e;
  text-transform: uppercase;
  margin-top: 14px;
}
"""


def document(pages, page_w=420, page_h=910):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<style>
:root {{ --pw: {page_w}px; --ph: {page_h}px; }}
{CSS}
</style>
</head>
<body>
{''.join(pages)}
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# packet screens
# --------------------------------------------------------------------------- #

def cover_page(slot):
    return f"""
<div class="page">
  <div class="sheet">
  <div class="center-stack">
    <h1>Pacchetto<br>N&deg; {slot}</h1>
    <div class="kicker">Mas&iacute;a Can Travi Nou &middot; solo per i tuoi occhi</div>
    <div class="box warn">
      <p><strong>Se questo non &egrave; il tuo pacchetto, chiudilo adesso.</strong>
      Dentro c'&egrave; il ruolo segreto di un altro giocatore: aprirlo rovina la partita
      per tutti e otto.</p>
    </div>
    <div class="box">
      <span class="label">Come si usa</span>
      <ol>
        <li><strong>Pag. 2 e 3</strong> &mdash; le tue risposte <strong>S&Igrave;</strong> e
        <strong>NO</strong>. Girale verso chi ti ha fatto la domanda, solo lui deve vederle.</li>
        <li><strong>Pag. 4 e 5</strong> &mdash; chi sei e cosa dici in ogni capitolo.</li>
        <li><strong>Pag. 6, 7, 8</strong> &mdash; le tue tre abilit&agrave;.</li>
        <li><strong>Ultima pagina</strong> &mdash; il tuo ruolo segreto.
        Leggila <strong>una volta</strong>, da solo, prima di iniziare. Poi torna a pag. 2
        e lasciala l&igrave; per tutta la partita.</li>
      </ol>
    </div>
    <p style="text-align:center; font-size:13px; color:var(--ink-faded);">
      Nessuno sa cosa contiene questo file. Nemmeno chi te l'ha mandato.</p>
  </div>
  </div>
</div>
"""


def answer_pages():
    return [
        """
<div class="page answer yes">
  <div class="sheet">
  <div class="answer-word">S&Igrave;</div>
  <div class="answer-hint">Inclina lo schermo verso chi ti ha<br>fatto la domanda &mdash; solo lui</div>
  </div>
</div>
""",
        """
<div class="page answer no">
  <div class="sheet">
  <div class="answer-word">NO</div>
  <div class="answer-hint">Inclina lo schermo verso chi ti ha<br>fatto la domanda &mdash; solo lui</div>
  </div>
</div>
""",
    ]


def character_pages(char):
    who = f"""
<div class="page">
  <div class="sheet">
  <h2>{md(char['name'])}</h2>
  <div class="kicker">il tuo personaggio</div>
  <div class="box">
    <span class="label">&#128226; Leggi ad alta voce nella Fase 0</span>
    <p class="speech">{md(char['read_aloud'])}</p>
  </div>
  <div class="box gold">
    <span class="label">&#129323; Il tuo segreto &mdash; non leggerlo ad alta voce</span>
    <p>{md(char['integrated_secret'])}</p>
    <p style="font-size:13px; color:var(--ink-faded); margin-top:8px;">
      Alcuni segreti puntano davvero al colpevole, altri sono solo veleno.
      Usalo quando ti conviene: una volta detto, non torna indietro.</p>
  </div>
  <div class="foot">pag. 4 &middot; le tue battute alla pagina seguente</div>
  </div>
</div>
"""
    lines = ''.join(
        f'<div class="chapter-line">{md(step)}</div>' for step in char['chapters'])
    says = f"""
<div class="page">
  <div class="sheet">
  <h2>Le tue battute</h2>
  <div class="kicker">una per capitolo &middot; {md(char['name'])}</div>
  <p style="font-size:13px; color:var(--ink-faded);">All'inizio di ogni capitolo, quando
  tocca a te, leggi la battuta di quel capitolo ad alta voce. Sono vere: fanno parte
  delle prove.</p>
  <hr class="rule">
  {lines}
  <div class="foot">pag. 5 &middot; le tue abilit&agrave; dalla pagina seguente</div>
  </div>
</div>
"""
    return [who, says]


def ability_page(char, ability, index):
    kind, timing = ability_meta(ability)
    body = apply_subs(ability['body'])
    tip = apply_subs(ability['tip'])
    # The bracketed "[SORCERY - On Your Turn]" prefix is restated by the box below.
    body = re.sub(r'^\*\*\[.*?\]\*\*\n?', '', body, flags=re.S)
    tip = re.sub(r'^\*\*.*?HOW & WHEN:\*\*\s*', '', tip, flags=re.S)
    return f"""
<div class="page">
  <div class="sheet">
  <h2>{md(ability['title'])}</h2>
  <div class="kicker">abilit&agrave; {index} di 3 &middot; {md(char['name'])}</div>
  <div class="box warn">
    <span class="label">Che cosa fa</span>
    <p>{md(body)}</p>
  </div>
  <div class="box gold">
    <span class="label">&#128161; Come e quando usarla</span>
    <p>{md(tip)}</p>
  </div>
  <div class="box">
    <span class="label">Quando puoi giocarla</span>
    <p>{timing}.</p>
    <p>{'<strong>Instant</strong> &mdash; puoi giocarla in qualsiasi momento, anche nel turno di un altro.'
        if kind == 'Instant' else
        '<strong>Sorcery</strong> &mdash; solo quando tocca a te.'}</p>
    <p style="font-size:13px; color:var(--ink-faded);">Una sola volta per partita, e
    <strong>massimo un'abilit&agrave; a capitolo</strong>. Annunciala ad alta voce quando la usi.</p>
  </div>
  <div class="foot">pag. {5 + index}</div>
  </div>
</div>
"""


def role_page(char):
    label = char['role_label']
    return f"""
<div class="page role">
  <div class="sheet">
  <div class="center-stack">
    <div class="seal">&#128272;</div>
    <h2>Il tuo ruolo segreto</h2>
    <div class="kicker">leggi una volta &middot; da solo &middot; poi torna a pag. 2</div>
    <div class="role-badge {label}">{label}</div>
    <div class="box">
      <p>{md(char['role_text'])}</p>
    </div>
    <p style="text-align:center; font-size:13px; color:#9a8a72;">
      Sei <strong>{md(char['name'])}</strong>. Nessun altro sa cosa c'&egrave; scritto qui.</p>
  </div>
  </div>
</div>
"""


def packet(slot, char):
    pages = [cover_page(slot)]
    pages += answer_pages()
    pages += character_pages(char)
    for i, ability in enumerate(char['abilities'], start=1):
        pages.append(ability_page(char, ability, i))
    pages.append(role_page(char))
    return document(pages)


# --------------------------------------------------------------------------- #
# clues
# --------------------------------------------------------------------------- #

def clue_page(clue, index, total):
    body = apply_subs(clue['body'])
    text, _, effect = body.partition('**EFFECT:**')
    return document([f"""
<div class="page clue">
  <div class="sheet">
  <div class="clue-badge">{CHAPTER_LABEL[clue['chapter']]} &middot; indizio {index} di {total}</div>
  <h2>{md(clue['title'])}</h2>
  <div class="clue-body">
    <p>{md(text.strip())}</p>
    <div class="effect">
      <span class="label">&#9876; Effetto immediato</span>
      <p>{md(effect.strip())}</p>
    </div>
  </div>
  <div class="foot">indizio {index} / {total}</div>
  </div>
</div>
"""])


def back_page():
    return document(["""
<div class="page back">
  <div class="sheet">
  <div class="back-mark">&#9884;</div>
  <div class="back-title">Mas&iacute;a<br>Can Travi Nou</div>
  <div class="back-sub">indizio coperto</div>
  </div>
</div>
"""])


# --------------------------------------------------------------------------- #
# rules
# --------------------------------------------------------------------------- #

def rules_pages():
    return [
        """
<div class="page">
  <div class="sheet">
  <div class="center-stack">
    <h1>Il Delitto di<br>Can Travi Nou</h1>
    <div class="kicker">regole per giocare solo col telefono</div>
    <div class="box warn">
      <p>Otto ospiti a pranzo. Lord Altavista &egrave; stato <strong>avvelenato</strong> in cantina.
      Uno di voi lo ha ucciso e uno lo ha aiutato: il colpevole &egrave; <strong>fisso</strong>,
      e gli indizi portano davvero a lui.</p>
    </div>
    <div class="box">
      <p><strong>Niente stampante, niente gettoni, niente carte.</strong> Serve solo che ognuno
      abbia il proprio pacchetto aperto sul telefono, e che una persona faccia scorrere
      gli indizi.</p>
    </div>
    <div class="box gold">
      <span class="label">Cosa serve davvero</span>
      <ul>
        <li>8 giocatori, un pacchetto a testa</li>
        <li>un telefono a testa</li>
        <li>chi ha la cartella <strong>INDIZI</strong> fa da mazziere &mdash; ma gioca come tutti</li>
      </ul>
    </div>
  </div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Come si distribuiscono<br>i pacchetti</h2>
  <div class="kicker">senza che nessuno sappia niente</div>
  <p>I contenuti degli otto pacchetti sono stati <strong>mescolati a caso</strong>:
  il numero sul file non dice nulla su chi c'&egrave; dentro. Nemmeno chi ve li manda lo sa.</p>
  <div class="box warn">
    <span class="label">Nel gruppo WhatsApp</span>
    <ol>
      <li>Mandate <strong>tutti e otto i file</strong> nel gruppo, in un colpo solo.</li>
      <li>A tavola, uno alla volta, ognuno <strong>dice un numero da 1 a 8</strong> ancora libero.
      Quello &egrave; il suo pacchetto.</li>
      <li>Ognuno apre <strong>solo il proprio</strong> e va all'ultima pagina per il ruolo.</li>
    </ol>
    <p>Sapere che Marco ha il n&deg; 3 non dice niente a nessuno: quello che c'&egrave; dentro
    il 3 lo scopre solo Marco.</p>
  </div>
  <div class="box">
    <span class="label">In alternativa</span>
    <p>Un file per persona in chat privata, senza aprirli. Cos&igrave; nessuno sa nemmeno
    quale numero ha ciascuno.</p>
  </div>
  <div class="foot">pag. 2</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Fase 0<br>Presentazioni</h2>
  <div class="kicker">prima del capitolo 1</div>
  <p>Ognuno ha gi&agrave; letto il proprio ruolo <strong>da solo</strong>, all'ultima pagina
  del pacchetto. Poi tutti tornano a pag. 2 e non riaprono pi&ugrave; l'ultima.</p>
  <hr class="rule">
  <p>In senso orario, ognuno legge ad alta voce il proprio riquadro
  <strong>&laquo;Leggi ad alta voce&raquo;</strong> (pag. 4): chi sei e perch&eacute; eri
  a quel pranzo.</p>
  <div class="box warn">
    <span class="label">&#129309; Come si riconoscono i due colpevoli</span>
    <p>Il ruolo dell'Assassino e quello del Complice si dicono a vicenda <strong>quale
    personaggio</strong> sta giocando l'altro. Durante queste presentazioni, i due si
    riconoscono in silenzio.</p>
    <p>Gli innocenti non capiscono niente. &Egrave; il momento pi&ugrave; bello della partita.</p>
  </div>
  <div class="box">
    <p>Nessuno spegne le luci, nessuno esce dalla stanza, non serve un narratore.
    Giocate tutti e otto.</p>
  </div>
  <div class="foot">pag. 3</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>I quattro capitoli</h2>
  <div class="kicker">il cuore della partita</div>
  <p>Ogni capitolo si gioca cos&igrave;, e dura pi&ugrave; o meno dieci minuti:</p>
  <ol>
    <li>Chi ha gli indizi scopre le <strong>due carte del capitolo</strong>, una alla volta,
    e le legge ad alta voce. L'effetto scritto sulla carta si applica subito.</li>
    <li>Poi, in senso orario, ognuno legge la propria <strong>battuta di quel
    capitolo</strong> (pag. 5 del pacchetto).</li>
    <li>Si discute. Si accusa. Si usano le abilit&agrave;.</li>
  </ol>
  <div class="box gold">
    <span class="label">Regole che valgono sempre</span>
    <ul>
      <li>Ogni rivelazione fatta da una carta &egrave; <strong>pubblica</strong>: vale per tutti.</li>
      <li>Tutto quello che dicono gli indizi &egrave; <strong>vero</strong>. Le persone no.</li>
      <li>Non si mostra mai l'ultima pagina del proprio pacchetto. Mai.</li>
    </ul>
  </div>
  <div class="foot">pag. 4</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>S&Igrave; e NO<br>col telefono</h2>
  <div class="kicker">la regola nuova</div>
  <p>Nel gioco stampato c'erano due cartoncini, uno verde e uno rosso. Adesso sono le
  <strong>pagine 2 e 3</strong> del tuo pacchetto.</p>
  <div class="box warn">
    <span class="label">Come funziona</span>
    <ol>
      <li>Qualcuno ti fa una domanda da s&igrave; o no, con un'abilit&agrave; o con un indizio.</li>
      <li>Tieni il telefono <strong>basso, contro il petto</strong>. Scorri fino alla pagina
      <strong>S&Igrave;</strong> o a quella <strong>NO</strong>.</li>
      <li>Inclina lo schermo <strong>solo verso chi ha chiesto</strong>, due secondi, e riporta
      il telefono a pag. 2.</li>
    </ol>
  </div>
  <div class="box gold">
    <span class="label">&#9888; La regola d'oro</span>
    <p>A queste domande <strong>si risponde sempre la verit&agrave;</strong>, anche se sei
    l'Assassino. &Egrave; l'unica cosa su cui non si pu&ograve; mentire in tutta la partita:
    per questo vale la pena spendere un'abilit&agrave; per chiedere.</p>
  </div>
  <div class="box">
    <p><strong>Se il telefono muore:</strong> pollice su per s&igrave;, pollice gi&ugrave; per no,
    sotto il tavolo, verso chi ha chiesto.</p>
  </div>
  <div class="foot">pag. 5</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Le abilit&agrave;<br>senza gettoni</h2>
  <div class="kicker">la seconda regola nuova</div>
  <p>Via i 40 gettoni da stampare. Ognuno ha le sue <strong>tre abilit&agrave;</strong>
  (pag. 6, 7, 8) e si contano da s&eacute;: sono solo tre.</p>
  <div class="box warn">
    <span class="label">Le tre regole</span>
    <ul>
      <li>Ogni abilit&agrave; si usa <strong>una volta sola per partita</strong>.</li>
      <li><strong>Massimo una abilit&agrave; a capitolo</strong>, per giocatore.</li>
      <li>Le abilit&agrave; segnate <strong>&laquo;solo nel Capitolo 3 o 4&raquo;</strong> sono
      le pi&ugrave; forti: non puoi usarle prima.</li>
    </ul>
  </div>
  <div class="box gold">
    <span class="label">Sorcery e Instant</span>
    <p><strong>Sorcery</strong>: solo quando tocca a te.<br>
    <strong>Instant</strong>: in qualsiasi momento, anche mentre parla un altro &mdash; ma
    resta la tua abilit&agrave; di quel capitolo.</p>
  </div>
  <div class="box">
    <p>Si annuncia ad alta voce: <em>&laquo;uso Interrogatorio Duro&raquo;</em>. Chi bara
    su tre carte in croce non merita di vincere.</p>
  </div>
  <div class="foot">pag. 6</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Gli indizi</h2>
  <div class="kicker">come si scoprono sul telefono</div>
  <p>Una persona sola tiene la cartella <strong>INDIZI</strong>. Dentro ci sono otto indizi,
  due per capitolo, gi&agrave; <strong>nell'ordine giusto</strong>.</p>
  <div class="box warn">
    <span class="label">La regola del dorso</span>
    <p>Tra un indizio e il successivo c'&egrave; sempre un'immagine di <strong>dorso</strong>.
    Chi tiene gli indizi scorre fino al dorso e <strong>si ferma l&igrave;</strong>: cos&igrave;
    non vede mai in anticipo l'indizio dopo, e gioca alla pari con tutti gli altri.</p>
    <p>Un capitolo &rarr; due indizi &rarr; ci si ferma sul dorso.</p>
  </div>
  <div class="box">
    <span class="label">L'abilit&agrave; &laquo;Autopsy&raquo;</span>
    <p>Chi la gioca prende in mano il telefono degli indizi, scorre <strong>solo i due
    del capitolo successivo</strong>, li legge in silenzio e lo riporta indietro fino
    al dorso. Nessun altro guarda.</p>
  </div>
  <div class="foot">pag. 7</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Il voto finale</h2>
  <div class="kicker">segreto, e senza foglietti</div>
  <p>Risolte le due carte del <strong>Capitolo 4</strong>, non si usano pi&ugrave; abilit&agrave;.
  Si parla, e basta.</p>
  <ol>
    <li><strong>Arringhe (30 secondi a testa).</strong> In senso orario, ognuno accusa una
    persona e d&agrave; <strong>una</strong> ragione. Oppure passa.</li>
    <li><strong>Dibattito libero (3 minuti).</strong> Uno alla volta.</li>
    <li><strong>Ultima parola (una frase a testa).</strong></li>
  </ol>
  <div class="box warn">
    <span class="label">&#128241; Come si vota</span>
    <ol>
      <li>Ognuno apre le <strong>Note</strong> del proprio telefono e scrive un nome.
      Nessuno guarda lo schermo di nessuno.</li>
      <li>Al tre, <strong>tutti girano lo schermo insieme</strong>.</li>
      <li>Si conta. Chi ha pi&ugrave; voti &egrave; l'accusato del tavolo.</li>
    </ol>
    <p>Il voto non si cambia e non si annulla. <strong>Votano tutti</strong>, colpevoli compresi.</p>
  </div>
  <div class="foot">pag. 8</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Chi vince</h2>
  <div class="kicker">la rivelazione</div>
  <p>Contati i voti, l'Assassino e il Complice mostrano l'ultima pagina del loro
  pacchetto. Quello &egrave; il momento.</p>
  <div class="box gold">
    <span class="label">&#128309; Gli innocenti</span>
    <p>Vincono se la persona con <strong>pi&ugrave; voti</strong> &egrave; davvero l'Assassino.</p>
  </div>
  <div class="box warn">
    <span class="label">&#128308; Assassino e Complice</span>
    <p>Vincono se prende pi&ugrave; voti <strong>chiunque</strong> tranne l'Assassino.
    Anche il Complice: pu&ograve; farsi accusare per salvare il socio, ed &egrave; una vittoria.</p>
  </div>
  <div class="box">
    <span class="label">&#128260; Pareggio</span>
    <p>Chi ha pari voti si difende <strong>30 secondi a testa</strong>, poi si rivota
    <strong>solo tra loro</strong>, per alzata di mano. Se pareggiano ancora,
    <strong>vincono i colpevoli</strong>.</p>
  </div>
  <div class="foot">pag. 9 &middot; buona fortuna</div>
  </div>
</div>
""",
        """
<div class="page">
  <div class="sheet">
  <h2>Se non siete<br>in otto</h2>
  <div class="kicker">e due premi in pi&ugrave;</div>
  <div class="box warn">
    <p>Il mistero &egrave; scritto per <strong>esattamente otto</strong>: Assassino e Complice
    sono sempre distribuiti.</p>
    <p><strong>In 6 o 7:</strong> una o due persone prendono <strong>due pacchetti</strong>
    e giocano entrambi i personaggi &mdash; ad alta voce, come se fossero due ospiti.
    Tutti e otto i pacchetti devono essere assegnati, sempre.</p>
  </div>
  <div class="box gold">
    <span class="label">&#127942; Nella stessa nota del voto</span>
    <p>Scrivete anche <strong>miglior strategia</strong> e <strong>pi&ugrave; divertente della
    serata</strong>. Si contano subito dopo il verdetto: spesso vale pi&ugrave; del delitto.</p>
  </div>
  <div class="box">
    <span class="label">Le tre cose che rovinano la partita</span>
    <ul>
      <li>Aprire un pacchetto che non &egrave; il tuo.</li>
      <li>Scorrere gli indizi oltre il dorso.</li>
      <li>Mentire su una risposta S&Igrave;/NO.</li>
    </ul>
    <p>Tutto il resto &mdash; bugie, accuse, alleanze &mdash; &egrave; il gioco.</p>
  </div>
  <div class="foot">pag. 10</div>
  </div>
</div>
""",
    ]


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kit', help='source HTML kit')
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=None)
    args = ap.parse_args()

    kit = extract(args.kit)
    leftovers = check_playable(kit)
    if leftovers:
        raise SystemExit('unplayable references left in the text:\n  '
                         + '\n  '.join(leftovers))
    chars = kit['characters']
    clues = sorted(kit['clues'], key=lambda c: c['chapter'])

    rng = random.Random(args.seed)
    order = chars[:]
    rng.shuffle(order)

    packets_dir = os.path.join(args.out, 'packets')
    clues_dir = os.path.join(args.out, 'clues')
    for d in (packets_dir, clues_dir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    for slot, char in enumerate(order, start=1):
        path = os.path.join(packets_dir, f'pacchetto-{slot}.html')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(packet(slot, char))

    with open(os.path.join(packets_dir, '.assignment.json'), 'w', encoding='utf-8') as fh:
        json.dump({str(i): c['name'] for i, c in enumerate(order, start=1)},
                  fh, ensure_ascii=False, indent=1)

    with open(os.path.join(clues_dir, 'retro.html'), 'w', encoding='utf-8') as fh:
        fh.write(back_page())
    for i, clue in enumerate(clues, start=1):
        with open(os.path.join(clues_dir, f'clue-{i}.html'), 'w', encoding='utf-8') as fh:
            fh.write(clue_page(clue, i, len(clues)))

    with open(os.path.join(args.out, 'regole.html'), 'w', encoding='utf-8') as fh:
        fh.write(document(rules_pages()))

    print(f'{len(order)} packets, {len(clues)} clues, rules -> {args.out}')
    print('shuffle written to packets/.assignment.json (do not read before the game)')


if __name__ == '__main__':
    main()
