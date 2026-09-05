# digital_kit

Turns a printable Masía Can Travi Nou HTML kit into a phone-only version:
no printer, no cards, no tokens.

```bash
NODE_PATH=$(npm root -g) python3 tools/digital_kit/package.py <kit.html> --out DIR
```

Output:

| | |
|---|---|
| `PACCHETTI/Pacchetto-N.pdf` | one packet per player, 9 screens |
| `INDIZI/NN-*.jpg` | the 8 clues in play order, a card back between each |
| `INDIZI.pdf` | the same sequence as one swipeable document |
| `REGOLE.pdf` | the rules, rewritten for phone play |

## Blind distribution

`build.py` shuffles which character lands in which packet and never prints the
mapping, so whoever runs it learns nothing. All eight packets can then go into
the group chat at once: players claim a slot number out loud and open only
theirs. Knowing that someone holds packet 3 reveals nothing about packet 3.

`package.py` pads every packet to the same byte size, because the guilty roles
have longer text and a size difference would be a tell.

## Rules that had to change

The printed kit needs 40 cut-out tokens and a pair of YES/NO cards per player.
Neither survives a phone-only game, so:

- **YES/NO** — pages 2 and 3 of each packet are full-bleed `SÌ` and `NO`
  screens, tilted toward the asker. Answers are always truthful, murderer
  included.
- **Abilities** — no token economy. Each ability is once per game, at most one
  ability per chapter, and the ones that cost 2 tokens are locked to Chapters
  3–4 so the powerful plays still have to be saved.
- Cards that referenced components directly are restated in `RULE_SUBS`: the
  interrogation abilities, and the token-theft ones (now: the target loses
  their ability for the next Chapter). The kits phrase these differently from
  each other, so the patterns are deliberately loose and `check_playable`
  fails the build if any reference to a token, the Bank or an answer card
  survives.
- **Voting** — each player types a name in their phone's notes app, then all
  reveal at once.

## Packet layout

`SÌ`/`NO` sit at pages 2–3 so they are two swipes from the default view, and
the secret role is last — the page you least want to flash to the table is the
furthest from where the file opens.
