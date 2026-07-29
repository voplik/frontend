# -*- coding: utf-8 -*-
"""Страница 02 — Увеличение губ (Figma frame «02»)."""

import seo
from build import (head, foot, HEADER, sec, section_head, media, before_after,
                   steps, list_items, faq, review, form_service, ic)

PATH = 'uslugi/uvelichenie-gub/'
FAQ = [
    ('А если филлер мигрирует?',
     'Миграция — это почти всегда перебор с объёмом или неподходящий препарат. '
     'Я работаю оригинальными филлерами и не ставлю больше, чем держит ваша анатомия. '
     'На осмотре через 14 дней смотрим результат вместе.'),
]


def page():
    p = []
    desc = ('Естественный объём и форма под вашу анатомию. 18 000 ₽ — филлер 1 мл, '
            'включена анестезия. Коррекция 2 000 ₽ в первые 14 дней.')
    p.append(head('Увеличение губ в Казани — цена 18 000 ₽, фото до/после | Косметолог Власова',
                  desc, PATH,
                  ld=(seo.ld_breadcrumbs([('Главная', ''), ('Услуги', 'uslugi/'),
                                          ('Увеличение губ', None)]) +
                      seo.ld_service('Увеличение губ', PATH, 18000, desc) +
                      seo.ld_faq(FAQ))))
    p.append(HEADER)
    p.append('<main>')

    # 01 Hero услуги
    p.append(sec(gap=18, pt=20))
    p.append('<nav class="t-body-sm breadcrumbs">'
             '<a href="@@/index.html">Главная</a><span>/</span>'
             '<a href="@@/index.html#uslugi">Услуги</a><span>/</span>'
             '<span class="breadcrumbs__cur">Увеличение губ</span></nav>')
    p.append('<h1 class="t-h1">Увеличение губ в Казани</h1>')
    p.append('<p class="t-body-l c-muted">Естественный объём и форма под вашу анатомию. '
             'Не делаю «уток» — если объём вам не пойдёт, скажу об этом на консультации.</p>')
    p.append('<div class="price-block price-block--brand">'
             '<span class="price-block__l">'
             '<span class="t-price price-block__v">18 000 ₽</span>'
             '<span class="t-body-sm price-block__note">филлер 1 мл · включена анестезия</span>'
             '</span>'
             '<span class="badge badge--accent">ФЛАГМАН</span>'
             '</div>')
    p.append('<div class="specs">'
             '<div class="spec"><span class="t-label spec__k">ПРЕПАРАТ</span>'
             '<span class="t-body-md spec__v">Оригинал</span></div>'
             '<div class="spec"><span class="t-label spec__k">ВРЕМЯ</span>'
             '<span class="t-body-md spec__v">40 минут</span></div>'
             '<div class="spec"><span class="t-label spec__k">ЭФФЕКТ</span>'
             '<span class="t-body-md spec__v">6–12 мес</span></div>'
             '</div>')
    p.append(media(300, 'ФОТО · РАБОТА НАСТИ'))
    p.append('<div class="stack-4">'
             '<button class="btn btn--primary btn--block" type="button" '
             'data-overlay-open="zapis" data-service="Увеличение губ — 18 000 ₽">'
             'Записаться — 18 000 ₽</button>'
             '<a class="btn btn--tg btn--block" href="#">' + ic('tg', 18, solid=True) +
             '<span>Написать в Telegram</span></a></div>')
    p.append('</section>')

    # 02 До / после
    p.append(sec(gap=16, sid='do-posle'))
    p.append(section_head('РЕЗУЛЬТАТЫ', 'До и после моих клиенток',
                          'Ни одно фото не отретушировано. Все — с письменного согласия.'))
    p.append(before_after())
    p.append(before_after())
    p.append('</section>')

    # 03 Как проходит
    p.append(sec(gap=18))
    p.append(section_head('ПРОЦЕСС', 'Как проходит процедура'))
    p.append(steps([
        {'t': 'Консультация и осмотр',
         'd': 'Смотрим вашу анатомию, обсуждаем желаемую форму. Если объём вам не пойдёт — скажу честно.'},
        {'t': 'Анестезия',
         'd': 'Крем-аппликация 15–20 минут. Больно не будет — это не героизм, а нормальная работа.'},
        {'t': 'Процедура · 30–40 минут',
         'd': 'Ввожу препарат постепенно, показываю результат в зеркале по ходу.'},
        {'t': 'Памятка и связь',
         'd': 'Отправляю памятку в Telegram и остаюсь на связи первые дни — фото-контроль отёка.'},
        {'t': 'Осмотр через 14 дней',
         'd': 'Смотрим, как всё село. Докоррекция при необходимости — 2 000 ₽.'},
    ]))
    p.append('</section>')

    # 04 Препараты
    p.append(sec(gap=16))
    p.append(section_head('БЕЗОПАСНОСТЬ', 'Чем работаю',
                          'Только оригинальные препараты с сертификатами. Упаковку вскрываю при вас.'))
    p.append('<div class="specs">'
             '<div class="drug">' + ic('shield', 22) +
             '<span class="t-card-title">Гиалуроновая кислота</span>'
             '<span class="t-body-sm drug__d">плотность под задачу</span></div>'
             '<div class="drug">' + ic('shield', 22) +
             '<span class="t-card-title">Сертификаты</span>'
             '<span class="t-body-sm drug__d">есть на каждую партию</span></div>'
             '</div>')
    p.append('</section>')

    # 05 Противопоказания
    p.append(sec(gap=16))
    p.append(section_head('ЧЕСТНО', 'Кому подходит и кому нет',
                          'Лучше отказать, чем сделать во вред. Это не про деньги.'))
    p.append('<div class="stack-4">')
    p.append('<div class="panel">'
             '<span class="t-body-md panel__h panel__h--yes">Можно</span>' +
             list_items([
                 {'t': 'Здоровая кожа без воспалений в зоне'},
                 {'t': 'Возраст 18+'},
                 {'t': 'Нет аллергии на компоненты препарата'},
             ]) + '</div>')
    p.append('<div class="panel">'
             '<span class="t-body-md panel__h panel__h--no">Нельзя</span>' +
             list_items([
                 {'t': 'Беременность и грудное вскармливание', 'yes': False},
                 {'t': 'Герпес в активной стадии', 'yes': False},
                 {'t': 'Онкология, аутоиммунные в обострении', 'yes': False},
                 {'t': 'Приём антикоагулянтов', 'yes': False},
             ]) + '</div>')
    p.append('</div>')
    p.append('</section>')

    # 06 Правила коррекции
    p.append(sec(gap=4))
    p.append('<div class="note">' + ic('shield', 20) +
             '<div class="note__t"><span class="t-body-md">Правило коррекции</span>'
             '<p class="t-body-sm note__d">Докоррекция 2 000 ₽ — только в первые 14 дней '
             'после процедуры. Позже это уже новая процедура по полной цене.</p></div></div>')
    p.append('<div class="note">' + ic('shield', 20) +
             '<div class="note__t"><span class="t-body-md">Предоплата за запись</span>'
             '<p class="t-body-sm note__d">Запись закрепляется предоплатой. Она входит в '
             'стоимость процедуры и возвращается при отмене больше чем за сутки.</p></div></div>')
    p.append('</section>')

    # 07 FAQ страхов
    p.append(sec(gap=10, sid='faq'))
    p.append(section_head('СТРАХИ', 'То, о чём боятся спросить'))
    p.append(faq([
        {'q': 'А если филлер мигрирует?', 'open': True,
         'a': 'Миграция — это почти всегда перебор с объёмом или неподходящий препарат. '
              'Я работаю оригинальными филлерами и не ставлю больше, чем держит ваша анатомия. '
              'На осмотре через 14 дней смотрим результат вместе.'},
        {'q': 'Больно ли делать губы?'},
        {'q': 'А если мне не понравится?'},
        {'q': 'Будет ли заметно, что я «делала»?'},
        {'q': 'Через сколько спадёт отёк?'},
        {'q': 'Что нельзя делать после процедуры?'},
    ]))
    p.append('</section>')

    # 08 Отзывы
    p.append(sec(gap=16, sid='otzyvy'))
    p.append(section_head('ОТЗЫВЫ', 'Об этой процедуре'))
    p.append('<div class="reviews">')
    p.append(review('Боялась «утки» больше всего. Настя показала в зеркале на каждом этапе — '
                    'вышло очень естественно, мама не заметила.', 'Алина, 24', 'увеличение губ'))
    p.append(review('Отёк был 2 дня, всё как в памятке — предупредили заранее.',
                    'Ксения, 31', 'увеличение губ'))
    p.append('</div>')
    p.append('</section>')

    # 09 Запись
    p.append(sec(gap=16, sid='zapis-form', extra='pad-bottom'))
    p.append('<div class="form-card">'
             '<div class="form-card__h">'
             '<h2 class="t-h3">Оставьте заявку</h2>'
             '<p class="t-body-sm form-card__sub">Заявка придёт мне в Telegram — отвечу лично.</p>'
             '</div>' + form_service('Увеличение губ — 18 000 ₽') + '</div>')
    p.append('</section>')

    p.append('</main>')
    p.append(foot())
    return '\n'.join(p)
