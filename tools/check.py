#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрая проверка после сборки: нет ли классов в разметке, для которых
не осталось CSS-правила, и не сломались ли внутренние ссылки.

Запуск:  cd tools && python3 check.py
"""

import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    css = ''
    for f in glob.glob(os.path.join(ROOT, 'css', '*.css')):
        css += io.open(f, encoding='utf-8').read()
    defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))

    used, links, errors = set(), [], []
    pages = [p for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
             if 'partials' not in p]

    for f in pages:
        html = io.open(f, encoding='utf-8').read()
        for m in re.findall(r'class="([^"]+)"', html):
            used |= set(m.split())
        for h in re.findall(r'href="([^"]+)"', html):
            if re.match(r'^(#|tel:|mailto:|data:|https?:)', h):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), h.split('#')[0]))
            if not os.path.exists(target):
                errors.append('битая ссылка %s → %s' % (os.path.relpath(f, ROOT), h))
            links.append(h)

    missing = sorted(c for c in used - defined if not c.startswith('ic-'))
    for c in missing:
        errors.append('класс без CSS-правила: .%s' % c)

    print('страниц: %d · классов: %d · внутренних ссылок: %d'
          % (len(pages), len(used), len(links)))
    if errors:
        print('\nПРОБЛЕМЫ:')
        for e in errors:
            print(' -', e)
        sys.exit(1)
    print('всё на месте')


if __name__ == '__main__':
    main()
