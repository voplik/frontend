#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор статических страниц.
Содержимое взято 1:1 из Figma (файл Ckn3hzyn6SI9vWznzmC86X, страница Web).
Результат — обычные .html файлы в корне проекта: никакой сборки для запуска
сайта не нужно, скрипт нужен только чтобы не дублировать разметку руками.

Запуск:  python3 tools/build.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE = open(os.path.join(ROOT, 'partials', 'sprite.html'), encoding='utf-8').read().strip()

NBSP = ' '


def ic(name, size=20, solid=False, extra=''):
    cls = 'ic ic--%d' % size
    if solid:
        cls += ' ic--solid'
    if extra:
        cls += ' ' + extra
    return '<svg class="%s" aria-hidden="true"><use href="#ic-%s"></use></svg>' % (cls, name)


# --------------------------------------------------------------- каркас ----

def head(title, description, path='', ld='', og_type='website'):
    """path — чистый URL страницы без домена, например 'uslugi/uvelichenie-gub/'."""
    import seo
    extra = seo.meta(title, description, path, og_type)
    blocks = seo.ld_physician() + (ld or '')
    return '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#f6f3ec">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' rx='8' fill='%%232f6a4f'/%%3E%%3Cpath d='M9 10l7 13 7-13' fill='none' stroke='%%23fff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%%3E%%3C/svg%%3E">
%s
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=Onest:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="@@/css/tokens.css">
<link rel="stylesheet" href="@@/css/base.css">
<link rel="stylesheet" href="@@/css/components.css">
%s
</head>
<body>
%s
<div class="page">
''' % (title, description, extra, blocks, SPRITE)


HEADER = '''<header class="header">
  <a class="header__logo" href="@@/index.html">
    <span class="t-label header__kicker">КОСМЕТОЛОГ</span>
    <span class="t-card-title header__name">Власова</span>
  </a>
  <div class="header__act">
    <a class="icon-btn" href="tel:+79600401151" aria-label="Позвонить">%s</a>
    <button class="icon-btn" type="button" data-overlay-open="menu" aria-label="Меню">%s</button>
  </div>
</header>''' % (ic('phone', 20), ic('menu', 20))


FOOTER = '''<footer class="footer">
  <div class="footer__in">
    <div class="footer__logo">
      <span class="t-label c-mute">КОСМЕТОЛОГ</span>
      <span class="t-h3 c-onbrand">Власова Анастасия</span>
    </div>
    <nav class="footer__cols">
      <div class="footer__col">
        <span class="t-label c-mute">УСЛУГИ</span>
        <a class="t-body-sm" href="@@/uslugi/uvelichenie-gub/index.html">Увеличение губ</a>
        <a class="t-body-sm" href="@@/index.html#ceny">Ботокс</a>
        <a class="t-body-sm" href="@@/index.html#ceny">Чистка лица</a>
        <a class="t-body-sm" href="@@/index.html#ceny">Пилинг PRX</a>
        <a class="t-body-sm" href="@@/uslugi/online-konsultaciya/index.html">Онлайн-консультация</a>
      </div>
      <div class="footer__col">
        <span class="t-label c-mute">РАЗДЕЛЫ</span>
        <a class="t-body-sm" href="@@/problemy/akne/index.html">Проблемы</a>
        <a class="t-body-sm" href="@@/pamyatki/index.html">Памятки</a>
        <a class="t-body-sm" href="@@/index.html#ceny">Цены</a>
        <a class="t-body-sm" href="@@/index.html#do-posle">До / после</a>
        <a class="t-body-sm" href="@@/index.html#otzyvy">Отзывы</a>
        <a class="t-body-sm" href="@@/index.html#obo-mne">Обо мне</a>
        <a class="t-body-sm" href="@@/index.html#kontakty">Контакты</a>
      </div>
    </nav>
    <div class="footer__contacts">
      <div class="footer__r">%s<span class="t-body-sm c-soft">Казань, Туфана Миннуллина, 8А</span></div>
      <div class="footer__r">%s<a class="t-body-md c-onbrand" href="tel:+79600401151">+7 960 040-11-51</a></div>
    </div>
    <div class="footer__soc">
      <a class="icon-btn icon-btn--ghost" href="#" aria-label="Telegram">%s</a>
      <a class="icon-btn icon-btn--ghost" href="#" aria-label="Instagram">%s</a>
      <a class="icon-btn icon-btn--ghost" href="#" aria-label="VK">%s</a>
    </div>
    <div class="footer__d"></div>
    <p class="t-body-sm footer__legal">Имеются противопоказания, необходима консультация специалиста. Врач-косметолог, частный кабинет. Политика обработки персональных данных.</p>
  </div>
</footer>''' % (ic('pin', 18), ic('phone', 18), ic('tg', 20, solid=True),
                ic('spark', 20, solid=True), ic('drop', 20))


BOTTOM_BAR = '''<div class="bottom-bar">
  <button class="btn btn--primary" type="button" data-overlay-open="zapis">Записаться</button>
  <a class="bottom-bar__tg" href="#" aria-label="Написать в Telegram">%s</a>
</div>''' % (ic('tg', 24, solid=True))


def foot():
    import popups
    return '''%s
%s
</div>
%s
<script src="@@/js/main.js"></script>
</body>
</html>
''' % (FOOTER, BOTTOM_BAR, popups.ALL)


# ---------------------------------------------------------------- услуги ----
# Список для селектов в формах. Порядок и цены — из прайса и мега-меню
# документа «Структура сайта», раздел 06.
SERVICES = [
    ('Инъекции', [
        'Ботокс — от 12 000 ₽',
        'Увеличение губ — 18 000 ₽',
        'Биоревитализация — от 6 000 ₽',
        'Липолитики — от 3 000 ₽',
        'Мезотерапия — от 3 500 ₽',
    ]),
    ('Эстетика', [
        'Чистка лица — 5 000 ₽',
        'Чистка + пилинг + маска — 4 500 ₽',
        'Пилинги — от 2 000 ₽',
    ]),
    ('Консультации', [
        'Консультация в кабинете — 2 500 ₽',
        'Онлайн-консультация — 3 000 ₽',
        'Подбор домашнего ухода',
    ]),
]


def service_select(fid, selected='', name='service'):
    """Выпадающий список услуг — вид как у обычного поля формы."""
    known = [it for _, items in SERVICES for it in items]
    if selected and selected not in known:
        raise ValueError('нет такой услуги в прайсе: %r' % selected)
    out = ['<select class="field__input" id="%s" name="%s" required>' % (fid, name)]
    out.append('<option value="" disabled%s>Выберите услугу</option>'
               % ('' if selected else ' selected'))
    for group, items in SERVICES:
        out.append('<optgroup label="%s">' % group)
        for it in items:
            out.append('<option%s>%s</option>'
                       % (' selected' if it == selected else '', it))
        out.append('</optgroup>')
    out.append('</select>')
    return ''.join(out)


def sec(gap=None, pt=None, sid='', extra=''):
    """Открывающий тег секции с точными отступами из макета."""
    st = []
    if gap is not None:
        st.append('gap:%srem' % (gap / 16))
    if pt is not None:
        st.append('padding-top:%srem' % (pt / 16))
    a = ' id="%s"' % sid if sid else ''
    c = 'section' + ((' ' + extra) if extra else '')
    return '<section class="%s"%s style="%s">' % (c, a, ';'.join(st))


# ----------------------------------------------------------- компоненты ----

def section_head(kicker='', title='', sub='', tag='h2'):
    out = ['<div class="section-head">']
    if kicker:
        out.append('<span class="t-label section-head__kicker">%s</span>' % kicker)
    if title:
        out.append('<%s class="t-h2 section-head__title">%s</%s>' % (tag, title, tag))
    if sub:
        out.append('<p class="t-body section-head__sub">%s</p>' % sub)
    out.append('</div>')
    return '\n'.join(out)


def media(height, label='', radius=''):
    style = 'height:%srem' % (height / 16)
    if radius:
        style += ';border-radius:%srem' % (radius / 16)
    inner = '<span class="t-label media__label">%s</span>' % label if label else ''
    return '<div class="media" style="%s">%s</div>' % (style, inner)


def before_after(before='ДО', after='ПОСЛЕ'):
    return '''<div class="ba">
  <div class="ba__col"><div class="ba__img"></div><span class="t-label ba__tag">%s</span></div>
  <div class="ba__col"><div class="ba__img"></div><span class="t-label ba__tag ba__tag--after">%s</span></div>
</div>''' % (before, after)


def faq(items):
    out = ['<div class="faq">']
    for i, it in enumerate(items):
        opened = it.get('open')
        cls = 'faq-item is-open' if opened else 'faq-item'
        out.append('<div class="%s">' % cls)
        out.append('<button class="faq-item__top" type="button" aria-expanded="%s">'
                   % ('true' if opened else 'false'))
        out.append('<span class="t-body-md faq-item__q">%s</span>' % it['q'])
        out.append('<span class="faq-item__ic">%s%s</span>'
                   % (ic('plus', 20, extra='ic-plus'), ic('minus', 20, extra='ic-minus')))
        out.append('</button>')
        out.append('<p class="t-body faq-item__a">%s</p>' % it.get('a', ''))
        out.append('</div>')
    out.append('</div>')
    return '\n'.join(out)


def steps(items):
    out = ['<div class="steps">']
    for i, it in enumerate(items, 1):
        out.append('''<div class="step">
  <span class="step__num">%d</span>
  <div class="step__tx">
    <span class="t-card-title">%s</span>%s
  </div>
</div>''' % (i, it['t'],
              ('\n    <p class="t-body step__d">%s</p>' % it['d']) if it.get('d') else ''))
    out.append('</div>')
    return '\n'.join(out)


def list_items(items):
    out = ['<div class="list">']
    for it in items:
        yes = it.get('yes', True)
        out.append('<div class="list-item list-item--%s">%s<p class="t-body list-item__t">%s</p></div>'
                   % ('yes' if yes else 'no',
                      ic('check' if yes else 'minus', 20),
                      it['t']))
    out.append('</div>')
    return '\n'.join(out)


def review(text, name, role, stars=5):
    s = ''.join(ic('star', 16, solid=True) for _ in range(stars))
    return '''<article class="review">
  <div class="review__stars">%s</div>
  <p class="t-body">%s</p>
  <div class="review__a">
    <div class="review__av"></div>
    <div class="review__n">
      <span class="t-body-md">%s</span>
      <span class="t-body-sm review__role">%s</span>
    </div>
  </div>
</article>''' % (s, text, name, role)


def review_video(name):
    """Видео-отзыв — Card / Variant2 из библиотеки Figma."""
    return ('<button class="review review--video" type="button">'
            '<span class="review__av-big"></span>'
            '<span class="review__pill"><span class="t-body-sm">%s</span>%s</span>'
            '</button>' % (name, ic('volume-mute', 16)))


def price_rows(rows):
    out = ['<div class="price-list">']
    for i, r in enumerate(rows):
        if i:
            out.append('<div class="divider"></div>')
        out.append('''<div class="price-row">
  <div class="price-row__l">
    <span class="t-body-md">%s</span>
    <span class="t-body-sm price-row__note">%s</span>
  </div>
  <span class="t-price-sm price-row__v">%s</span>
</div>''' % (r['n'], r['note'], r['p']))
    out.append('</div>')
    return '\n'.join(out)


def card_problem(title, sub, href='#', icon='drop'):
    return '''<a class="card-problem" href="%s">
  <span class="card-problem__ico">%s</span>
  <span class="card-problem__t">
    <span class="t-card-title">%s</span>
    <span class="t-body-sm card-problem__sub">%s</span>
  </span>
  <span class="card-problem__arrow">%s</span>
</a>''' % (href, ic(icon, 22), title, sub, ic('chevron', 20))


def card_service(label, title, price, href='#'):
    return '''<a class="card-service" href="%s">
  <span class="card-service__media media" style="height:7.75rem;border-radius:1rem">
    <span class="t-label media__label">%s</span>
  </span>
  <span class="card-service__body">
    <span class="t-card-title">%s</span>
    <span class="t-price-sm card-service__price">%s</span>
  </span>
</a>''' % (href, label, title, price)


def form_service(service, submit='Отправить заявку'):
    """Форма записи со страницы услуги (Form/Запись из библиотеки)."""
    return '''<form class="form" data-form novalidate>
  <div class="field">
    <label class="t-label field__label" for="s-name"><span>ВАШЕ ИМЯ</span></label>
    <input class="field__input" id="s-name" name="name" type="text" autocomplete="name" placeholder="Анастасия" required>
  </div>
  <div class="field">
    <label class="t-label field__label" for="s-phone"><span>ТЕЛЕФОН</span></label>
    <input class="field__input" id="s-phone" name="phone" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required>
  </div>
  <div class="field is-filled">
    <label class="t-label field__label" for="s-service"><span>УСЛУГА</span>
      <button class="t-label field__link" type="button" data-focus="s-service">Изменить</button>
    </label>
    %s
  </div>
  <label class="checkbox">
    <input type="checkbox" required>
    <span class="t-body">Согласен(на) на обработку персональных данных</span>
  </label>
  <button class="btn btn--primary btn--block" type="submit">%s</button>
</form>''' % (service_select('s-service', service), submit)


def cta(title, sub, primary='Оставить заявку', tg='Написать в Telegram'):
    return '''<div class="cta">
  <div class="cta__h">
    <p class="cta__title">%s</p>
    <p class="t-body cta__sub">%s</p>
  </div>
  <div class="cta__b">
    <button class="btn btn--accent btn--block" type="button" data-overlay-open="zapis">%s</button>
    <a class="btn btn--tg btn--block" href="#">%s<span>%s</span></a>
  </div>
</div>''' % (title, sub, primary, ic('tg', 18, solid=True), tg)


# =========================================================== СТРАНИЦА 01 ====

def page_index():
    p = []
    import seo
    desc = ('Губы, кожа и домашний уход. Цены на первом экране, противопоказания '
            'и понятный план. Казань, частный кабинет.')
    p.append(head('Врач-косметолог в Казани — Анастасия Власова | Цены, до/после, запись',
                  desc, '',
                  ld=seo.ld_faq([
                      ('А если филлер мигрирует?',
                       'Миграция — это почти всегда перебор с объёмом или неподходящий '
                       'препарат. Я работаю оригинальными филлерами и не ставлю больше, '
                       'чем держит ваша анатомия. На осмотре через 14 дней смотрим '
                       'результат вместе.'),
                  ])))
    p.append(HEADER)
    p.append('<main>')

    # 01 Hero
    p.append('''<section class="section section--hero">
  <span class="badge badge--brand">ЧАСТНЫЙ КАБИНЕТ · КАЗАНЬ</span>
  <h1 class="t-h1">Врач-косметолог<br>Анастасия Власова</h1>
  <p class="t-body-l c-muted">Губы, кожа и домашний уход — честно: с ценой на первом экране, противопоказаниями и понятным планом. Без «узнайте у администратора».</p>
  <div class="facts">
    <div class="fact"><span class="t-h3 fact__n">Высшее</span><span class="t-body-sm fact__t">медицинское</span></div>
    <div class="fact"><span class="t-h3 fact__n">5+ лет</span><span class="t-body-sm fact__t">практики</span></div>
    <div class="fact"><span class="t-h3 fact__n">1000+</span><span class="t-body-sm fact__t">пациентов</span></div>
  </div>
  ''' + media(320) + '''
  <div class="stack-4">
    <button class="btn btn--primary btn--block" type="button" data-overlay-open="zapis">Записаться на приём</button>
    <a class="btn btn--tg btn--block" href="#">''' + ic('tg', 18, solid=True) + '''<span>Написать в Telegram</span></a>
  </div>
</section>''')

    # 02 Флагман
    p.append('<section class="section">')
    p.append(section_head('ФЛАГМАН', 'Увеличение губ',
                          'Естественно, без «утки». Смотрим форму вместе и не ставим больше, чем держит анатомия.'))
    p.append(before_after())
    p.append('''<a class="price-block" href="@@/uslugi/uvelichenie-gub/index.html">
  <span class="price-block__l">
    <span class="t-price price-block__v">18 000 ₽</span>
    <span class="t-body-sm price-block__note">коррекция 2 000 ₽ — в первые 14 дней</span>
  </span>
  <span class="price-block__arrow">''' + ic('chevron', 22) + '''</span>
</a>''')
    p.append('<a class="btn btn--white btn--block" href="@@/uslugi/uvelichenie-gub/index.html">Подробно о процедуре</a>')
    p.append('</section>')

    # 03 Услуги
    p.append('<section class="section" id="uslugi">')
    p.append(section_head('УСЛУГИ', 'Что я делаю',
                          'Цены открыто. Каждая процедура — со сроком, подготовкой и памяткой после.'))
    p.append('<div class="grid-2">')
    p.append(card_service('ЛОБ · МЕЖБРОВЬЕ', 'Ботокс', 'от 12 000 ₽', '@@/uslugi/uvelichenie-gub/index.html'))
    p.append(card_service('ЧИСТКА', 'Чистка лица', '5 000 ₽', '@@/uslugi/uvelichenie-gub/index.html'))
    p.append(card_service('ПИЛИНГ', 'Пилинг PRX', '4 000 ₽', '@@/uslugi/uvelichenie-gub/index.html'))
    p.append(card_service('ПРИЁМ', 'Консультация', '2 500 ₽', '@@/uslugi/uvelichenie-gub/index.html'))
    p.append('</div>')
    p.append('<a class="btn btn--sm btn--ghost btn--inline" href="@@/index.html#ceny">Все услуги и цены</a>')
    p.append('</section>')

    # 04 Подбор по проблеме
    p.append(sec(gap=14, sid='problemy'))
    p.append(section_head('НЕ ЗНАЕТЕ, ЧТО ВЫБРАТЬ', 'Что вас беспокоит?',
                          'Расскажите словами — подберу процедуру сама.'))
    p.append('<div class="stack-4">')
    p.append(card_problem('Акне и высыпания', 'диагностика → схема → ведение', '@@/problemy/akne/index.html'))
    p.append(card_problem('Постакне: пятна и следы', 'пилинги + домашний уход', '@@/problemy/akne/index.html'))
    p.append(card_problem('Морщины и заломы', 'ботокс, от 12 000 ₽', '@@/uslugi/uvelichenie-gub/index.html'))
    p.append(card_problem('Пигментация и тусклый тон', 'пилинги + сыворотки', '@@/problemy/akne/index.html'))
    p.append('</div>')
    p.append('</section>')

    # 05 Обо мне
    p.append('''<section class="section" id="obo-mne">
  <div class="about">
    ''' + media(220, 'ФОТО · КАБИНЕТ') + '''
    <div class="about__t">
      <h2 class="t-h2">Обо мне</h2>
      <p class="t-body about__d">Я врач с высшим медицинским образованием, а не «мастер с курсов». Работаю на результат: если процедура вам не нужна — так и скажу. Подойдёт средство за 500 ₽ — порекомендую его, а не дорогое.</p>
    </div>
    <button class="btn btn--sm btn--white" type="button">Познакомиться</button>
  </div>
</section>''')

    # 06 До / после
    p.append('<section class="section" id="do-posle">')
    p.append(section_head('РЕЗУЛЬТАТЫ', 'До и после', 'Реальные работы, все с согласия клиенток.'))
    p.append('''<div class="hscroll hscroll--chips" data-chips>
  <button class="chip is-active" type="button">Губы</button>
  <button class="chip" type="button">Ботокс</button>
  <button class="chip" type="button">Чистка</button>
  <button class="chip" type="button">Пилинги</button>
  <button class="chip" type="button">Акне</button>
</div>''')
    p.append(before_after())
    p.append('</section>')

    # 07 Отзывы
    p.append('<section class="section" id="otzyvy">')
    p.append(section_head('ОТЗЫВЫ', 'Что говорят клиенты'))
    p.append('<div class="reviews reviews--mixed">')
    p.append(review_video('Алина, 24'))
    p.append(review('Год мучилась с высыпаниями. Дали схему на 3 месяца, ведут '
                    'с фотоконтролем. Врач объяснил, почему…',
                    'Камила, 19', 'лечение акне'))
    p.append('</div>')
    p.append('</section>')

    # 08 Цены
    p.append('<section class="section" id="ceny">')
    p.append(section_head('ЧЕСТНО', 'Цены', 'Без «цена в директ». Полный прайс — на отдельной странице.'))
    p.append(price_rows([
        {'n': 'Увеличение губ', 'note': 'филлер, 1 мл', 'p': '18 000 ₽'},
        {'n': 'Ботокс Диспорт', 'note': 'лоб, межбровье', 'p': '12 000 ₽'},
        {'n': 'Чистка лица', 'note': 'с пилингом и маской', 'p': '5 000 ₽'},
        {'n': 'Пилинг PRX', 'note': '1 процедура', 'p': '4 000 ₽'},
        {'n': 'Онлайн-консультация', 'note': 'вся Россия', 'p': '3 000 ₽'},
    ]))
    p.append('<a class="btn btn--sm btn--ghost btn--inline" href="#">Весь прайс и бонусы</a>')
    p.append('</section>')

    # 09 Онлайн-мост
    p.append('''<section class="section">
  <div class="bridge">
    <span class="badge badge--neutral">ВСЯ РОССИЯ</span>
    <h2 class="t-h2">Не в Казани?</h2>
    <p class="t-body bridge__d">Разберу вашу кожу и косметичку по видео — и составлю схему ухода, которая останется у вас документом. Средства пришлю с доставкой.</p>
    <a class="btn btn--sm btn--primary btn--block" href="@@/uslugi/online-konsultaciya/index.html">Онлайн-консультация — 3 000 ₽</a>
  </div>
</section>''')

    # 10 FAQ
    p.append(sec(gap=10, sid='faq'))
    p.append(section_head('ЧАСТЫЕ ВОПРОСЫ', 'Спрашивают почти все'))
    p.append(faq([
        {'q': 'А если филлер мигрирует?', 'open': True,
         'a': 'Миграция — это почти всегда перебор с объёмом или неподходящий препарат. Я работаю оригинальными филлерами и не ставлю больше, чем держит ваша анатомия. На осмотре через 14 дней смотрим результат вместе.'},
        {'q': 'Больно ли делать губы?'},
        {'q': 'Когда можно краситься после чистки?'},
        {'q': 'Можно ли в баню после ботокса?'},
        {'q': 'Сколько держится результат?'},
    ]))
    p.append('</section>')

    # 11 CTA
    p.append('<section class="section">')
    p.append(cta('Записаться на приём',
                 'Отвечаю лично в течение дня. Можно просто спросить — без записи.'))
    p.append('</section>')

    # 12 Контакты
    p.append('<section class="section pad-bottom" id="kontakty">')
    p.append(section_head('КАК НАЙТИ', 'Контакты', 'Стеклянная дверь на углу — ориентируйтесь на неё.'))
    p.append(media(180, 'КАРТА · ФОТО ВХОДА'))
    p.append('''<div class="contacts">
  <div class="contacts__r">%s<span class="t-body-md">Казань, Туфана Миннуллина, 8А</span></div>
  <div class="contacts__r">%s<span class="t-body-md">Пн–Сб · 10:00–20:00</span></div>
  <div class="contacts__r">%s<a class="t-body-md" href="tel:+79600401151">+7 960 040-11-51</a></div>
</div>''' % (ic('pin', 20), ic('clock', 20), ic('phone', 20)))
    p.append('</section>')

    p.append('</main>')
    p.append(foot())
    return '\n'.join(p)


PAGES = [
    # (файл, глубина вложенности, чистый URL, сборщик)
    ('index.html', 0, '', 'index'),
    ('uslugi/uvelichenie-gub/index.html', 2, 'uslugi/uvelichenie-gub/', 'p02'),
    ('problemy/akne/index.html', 2, 'problemy/akne/', 'p03'),
    ('uslugi/online-konsultaciya/index.html', 2, 'uslugi/online-konsultaciya/', 'p04'),
    ('pamyatki/index.html', 1, 'pamyatki/', 'pamyatki_hub'),
    ('pamyatki/posle-uvelicheniya-gub/index.html', 2, 'pamyatki/posle-uvelicheniya-gub/', 'pamyatka:guby'),
    ('pamyatki/posle-botoksa/index.html', 2, 'pamyatki/posle-botoksa/', 'pamyatka:botoks'),
    ('pamyatki/posle-biorevitalizacii/index.html', 2, 'pamyatki/posle-biorevitalizacii/', 'pamyatka:biorevitalizaciya'),
    ('pamyatki/posle-chistki-lica/index.html', 2, 'pamyatki/posle-chistki-lica/', 'pamyatka:chistka'),
    ('privacy/index.html', 1, 'privacy/', 'privacy'),
    ('404.html', 0, '404.html', 'notfound'),
]


def _build(kind):
    if kind == 'index':
        return page_index()
    if kind == 'p02':
        import p02
        return p02.page()
    if kind == 'p03':
        import p03
        return p03.page()
    if kind == 'p04':
        import p04
        return p04.page()
    import pamyatki
    if kind == 'pamyatki_hub':
        return pamyatki.hub()
    if kind == 'privacy':
        return pamyatki.privacy()
    if kind == 'notfound':
        return pamyatki.notfound()
    if kind.startswith('pamyatka:'):
        return pamyatki.page(kind.split(':', 1)[1])
    raise ValueError(kind)


def main():
    import seo
    for out, depth, clean, kind in PAGES:
        html = _build(kind).replace('@@/', '../' * depth)
        full = os.path.join(ROOT, out)
        d = os.path.dirname(full)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(html)
        print('written', out, len(html), 'bytes')

    # sitemap.xml
    urls = [seo.url(c) for _, _, c, k in PAGES if k not in ('notfound',)]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append('  <url><loc>%s</loc></url>' % u)
    sm.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sm) + '\n')

    # robots.txt
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: %s\n' % seo.url('sitemap.xml'))
    print('written sitemap.xml, robots.txt')


if __name__ == '__main__':
    main()
