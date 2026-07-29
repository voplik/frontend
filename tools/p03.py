# -*- coding: utf-8 -*-
"""Страница 03 — Акне и высыпания (Figma frame «03»)."""

import seo
from build import (head, foot, HEADER, sec, section_head, media, before_after,
                   steps, list_items, faq, card_problem, ic)

PATH = 'problemy/akne/'


def page():
    p = []
    desc = ('Акне не решается одной чисткой: нужна схема и время. Диагностика, '
            'схема ухода и ведение с фото-контролем. Консультация 2 500 ₽.')
    p.append(head('Акне и высыпания в Казани — схема и ведение | Косметолог Власова',
                  desc, PATH,
                  ld=seo.ld_breadcrumbs([('Главная', ''), ('Проблемы', 'problemy/'),
                                         ('Акне и высыпания', None)])))
    p.append(HEADER)
    p.append('<main>')

    # 01 Hero проблемы
    p.append(sec(gap=18, pt=20))
    p.append('<nav class="t-body-sm breadcrumbs">'
             '<a href="@@/index.html">Главная</a><span>/</span>'
             '<a href="@@/index.html#problemy">Проблемы</a><span>/</span>'
             '<span class="breadcrumbs__cur">Акне</span></nav>')
    p.append('<h1 class="t-h1">Акне и высыпания в Казани</h1>')
    p.append('<p class="t-body-l c-muted">Если вы уже перепробовали половину аптеки и советы '
             'из интернета — это не ваша вина. Акне не лечится одной чисткой: нужна схема '
             'и время. Я веду вас всё это время.</p>')
    p.append('<div class="infocard">'
             '<span class="t-body-md infocard__t">Что я обещаю честно</span>' +
             list_items([
                 {'t': 'Первые изменения — через 4–6 недель, а не «за один визит»'},
                 {'t': 'Схема подбирается под ваш бюджет, а не под мой прайс'},
                 {'t': 'Веду с фото-контролем и корректирую по результату'},
             ]) + '</div>')
    p.append(media(280, 'ФОТО · РАБОТА С КОЖЕЙ'))
    p.append('<button class="btn btn--primary btn--block" type="button" '
             'data-overlay-open="zapis" data-service="Консультация в кабинете — 2 500 ₽">'
             'Записаться на консультацию</button>')
    p.append('</section>')

    # 02 Как я работаю
    p.append(sec(gap=18))
    p.append(section_head('ПОДХОД', 'Как я работаю с акне',
                          'Три этапа. Ни один нельзя пропустить — иначе всё вернётся.'))
    p.append(steps([
        {'t': 'Диагностика',
         'd': 'Разбираем причины: гормоны, уход, питание, привычки. При необходимости '
              'отправлю к смежному врачу — это нормально.'},
        {'t': 'Схема',
         'd': 'Процедуры в кабинете + домашний уход под ваш бюджет. Расписываю по шагам: '
              'утро, вечер, чем и когда.'},
        {'t': 'Ведение с фото-контролем',
         'd': 'Присылаете фото раз в 2–4 недели, я корректирую схему. Это и есть основная '
              'работа, а не сама чистка.'},
    ]))
    p.append('</section>')

    # 03 Какие процедуры решают
    p.append(sec(gap=14))
    p.append(section_head('ЧТО ВХОДИТ', 'Процедуры, которые работают',
                          'Конкретный набор зависит от стадии — определим на консультации.'))
    p.append('<div class="stack-4">')
    p.append(card_problem('Чистка лица', '5 000 ₽ · раз в 1–2 месяца', '@@/index.html#ceny'))
    p.append(card_problem('Миндальный пилинг', '2 000 ₽ · мягкий старт', '@@/index.html#ceny'))
    p.append(card_problem('Пилинг PRX', '4 000 ₽ · по постакне', '@@/index.html#ceny'))
    p.append(card_problem('Подбор домашнего ухода', 'входит в консультацию',
                          '@@/uslugi/online-konsultaciya/index.html'))
    p.append('</div>')
    p.append('</section>')

    # 04 До / после
    p.append(sec(gap=16, sid='do-posle'))
    p.append(section_head('РЕЗУЛЬТАТЫ', 'Мои клиентки с акне',
                          'Разные сроки и разные стадии — покажу похожий на ваш случай '
                          'на консультации.'))
    p.append(before_after())
    p.append('</section>')

    # 05 Консультация — первый шаг
    p.append(sec(gap=16))
    p.append(section_head('ПЕРВЫЙ ШАГ', 'С чего начать'))
    p.append('<div class="stack-4">')
    p.append('<div class="consult">'
             '<div class="consult__r">'
             '<div class="consult__l">'
             '<span class="t-card-title">В кабинете</span>'
             '<span class="t-body-sm consult__sub">Казань · осмотр, схема, план</span>'
             '</div>'
             '<span class="t-price-sm consult__p">2 500 ₽</span>'
             '</div>'
             '<button class="btn btn--sm btn--primary btn--block" type="button" '
             'data-overlay-open="zapis" data-service="Консультация в кабинете — 2 500 ₽">'
             'Записаться</button>'
             '</div>')
    p.append('<div class="consult consult--accent">'
             '<div class="consult__r">'
             '<div class="consult__l">'
             '<span class="t-card-title">Онлайн</span>'
             '<span class="t-body-sm consult__sub">из любого города · 60 минут</span>'
             '</div>'
             '<span class="t-price-sm consult__p">3 000 ₽</span>'
             '</div>'
             '<a class="btn btn--sm btn--white btn--block" href="@@/uslugi/online-konsultaciya/index.html">'
             'Как проходит онлайн</a>'
             '</div>')
    p.append('</div>')
    p.append('</section>')

    # 06 FAQ
    p.append(sec(gap=10, sid='faq', extra='pad-bottom'))
    p.append(section_head('ЧАСТЫЕ ВОПРОСЫ', 'Про акне спрашивают это'))
    p.append(faq([
        {'q': 'Сколько времени займёт лечение?', 'open': True,
         'a': 'Миграция — это почти всегда перебор с объёмом или неподходящий препарат. '
              'Я работаю оригинальными филлерами и не ставлю больше, чем держит ваша анатомия. '
              'На осмотре через 14 дней смотрим результат вместе.'},
        {'q': 'Можно ли выдавливать самой?'},
        {'q': 'Поможет ли одна чистка?'},
        {'q': 'Нужно ли сдавать анализы?'},
        {'q': 'А если у меня уже постакне?'},
    ]))
    p.append('</section>')

    p.append('</main>')
    p.append(foot())
    return '\n'.join(p)
