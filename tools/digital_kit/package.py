"""Render a built digital kit into the files that actually get sent out.

  python3 package.py <kit.html> --out DIR

Produces, under DIR:
  PACCHETTI/Pacchetto-N.pdf     one per player, all padded to the same byte size
  INDIZI/NN-*.png               clues in play order, a card back between each
  INDIZI.pdf                    the same sequence as one swipeable document
  REGOLE.pdf                    the phone rules

The packet shuffle is random and is never printed, so running this does not
tell the operator who is who.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
NODE_ENV = {**os.environ, 'NODE_PATH': os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')}


def run(*cmd):
    subprocess.run(cmd, check=True, env=NODE_ENV, cwd=HERE,
                   stdout=subprocess.DEVNULL if '-q' in cmd else None)


def render_pdf(src, dest):
    subprocess.run(['node', 'render.js', 'pdf', dest, src],
                   check=True, env=NODE_ENV, cwd=HERE, stdout=subprocess.DEVNULL)


def render_png(srcs, dest_dir):
    subprocess.run(['node', 'render.js', 'png', dest_dir, *srcs],
                   check=True, env=NODE_ENV, cwd=HERE, stdout=subprocess.DEVNULL)


def pad_to(path, target):
    """Grow a PDF to exactly `target` bytes without invalidating it.

    A packet's byte size would otherwise leak how long its role text is, which
    is a tell for the two guilty packets. The original cross-reference table
    stays where it is, so re-emitting its offset after the padding keeps the
    trailer valid.
    """
    data = open(path, 'rb').read()
    if len(data) > target:
        raise ValueError(f'{path} is already {len(data)} > {target}')
    if len(data) == target:
        return
    m = None
    for m in re.finditer(rb'startxref\s+(\d+)\s*%%EOF', data):
        pass
    if not m:
        raise ValueError(f'{path}: no startxref/%%EOF trailer to preserve')
    trailer = b'\nstartxref\n' + m.group(1) + b'\n%%EOF\n'
    room = target - len(data) - len(trailer) - 2
    if room < 0:
        raise ValueError(f'{path}: no room to pad to {target}')
    with open(path, 'wb') as fh:
        fh.write(data + b'\n%' + b'0' * room + trailer)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kit')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    work = os.path.join(out, '.build')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(work)

    subprocess.run([sys.executable, 'build.py', args.kit, '--out', work],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL)

    packets_dir = os.path.join(out, 'PACCHETTI')
    clues_dir = os.path.join(out, 'INDIZI')
    os.makedirs(packets_dir)
    os.makedirs(clues_dir)

    # --- packets ---------------------------------------------------------- #
    made = []
    for slot in range(1, 9):
        src = os.path.join(work, 'packets', f'pacchetto-{slot}.html')
        dest = os.path.join(packets_dir, f'Pacchetto-{slot}.pdf')
        render_pdf(src, dest)
        made.append(dest)
    target = max(os.path.getsize(p) for p in made) + 4096
    for p in made:
        pad_to(p, target)
    print(f'{len(made)} packets, all {target} bytes')

    # --- clues: a card back before the first clue and after every clue ---- #
    seq = [os.path.join(work, 'clues', 'retro.html')]
    for i in range(1, 9):
        seq.append(os.path.join(work, 'clues', f'clue-{i}.html'))
        seq.append(os.path.join(work, 'clues', 'retro.html'))

    stage = os.path.join(work, 'png')
    render_png([os.path.join(work, 'clues', 'retro.html')]
               + [os.path.join(work, 'clues', f'clue-{i}.html') for i in range(1, 9)], stage)
    for n, src in enumerate(seq, start=1):
        stem = os.path.basename(src)[:-5]
        label = 'dorso' if stem == 'retro' else 'indizio-' + stem.split('-')[1]
        shutil.copyfile(os.path.join(stage, stem + '.png'),
                        os.path.join(clues_dir, f'{n:02d}-{label}.png'))
    print(f'{len(seq)} clue images (8 clues + 9 backs)')

    # one document with the same alternation, for anyone who prefers a PDF
    with open(os.path.join(work, 'indizi-all.html'), 'w', encoding='utf-8') as fh:
        merged = []
        for src in seq:
            body = open(src, encoding='utf-8').read()
            merged.append(re.search(r'<body>(.*)</body>', body, re.S).group(1))
        head = open(seq[0], encoding='utf-8').read().split('<body>')[0]
        fh.write(head + '<body>' + ''.join(merged) + '</body>\n</html>\n')
    render_pdf(os.path.join(work, 'indizi-all.html'), os.path.join(out, 'INDIZI.pdf'))

    with zipfile.ZipFile(os.path.join(out, 'INDIZI-immagini.zip'), 'w') as z:
        for name in sorted(os.listdir(clues_dir)):
            z.write(os.path.join(clues_dir, name), f'INDIZI/{name}')

    # --- rules ------------------------------------------------------------ #
    render_pdf(os.path.join(work, 'regole.html'), os.path.join(out, 'REGOLE.pdf'))
    print('rules + clue pdf written')


if __name__ == '__main__':
    main()
