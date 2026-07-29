# -*- coding: utf-8 -*-
"""Страница 04 — Онлайн-консультация (Figma frame «04»)."""

import seo
from build import (head, foot, HEADER, sec, section_head, media, steps,
                   list_items, faq, review, ic)

PATH = 'uslugi/online-konsultaciya/'


def tariff(title, price, feats, btn='Выбрать тариф', pro=False):
    cls = 'tariff tariff--pro' if pro else 'tariff'
    bcls = 'btn btn--sm btn--white btn--block' if pro else 'btn btn--sm btn--primary btn--block'
    out = ['<div class="%s">' % cls]
    out.append('<div class="tariff__hd">'
               '<span class="t-h3 tariff__title">%s</span>'
               '<span class="t-price tariff__price">%s</span></div>' % (title, price))
    out.append('<div class="tariff__feats">')
    for f in feats:
        out.append('<div class="tariff__f">%s<p class="t-body">%s</p></div>' % (ic('check', 18), f))
    out.append('</div>')
    out.append('<button class="%s" type="button" data-overlay-open="tarif">%s</button>' % (bcls, btn))
    out.append('</div>')
    return '\n'.join(out)


def page():
    p = []
    desc = ('Час по видео и персональная схема ухода документом. От 3 000 ₽, '
            'из любого города России.')
    p.append(head('Онлайн-консультация косметолога — 3 000 ₽, схема ухода | Косметолог Власова',
                  desc, PATH,
                  ld=(seo.ld_breadcrumbs([('Главная', ''), ('Услуги', 'uslugi/'),
                                          ('Онлайн-консультация', None)]) +
                      seo.ld_service('Онлайн-консультация косметолога', PATH, 3000, desc))))
    p.append(HEADER)
    p.append('<main>')

    # 01 Hero
    p.append(sec(gap=18, pt=24))
    p.append('<span class="badge badge--accent">ИЗ ЛЮБОГО ГОРОДА РОССИИ</span>')
    p.append('<h1 class="t-h1">Разберу вашу кожу<br>и вашу косметичку</h1>')
    p.append('<p class="t-body-l c-muted">Час по видео — и у вас остаётся персональная схема '
             'ухода документом: что оставить, что выбросить, чего не хватает. '
             'Врач-косметолог, 5+ лет, 1000+ пациентов.</p>')
    p.append('<div class="infocard infocard--brand">'
             '<span class="t-body-md infocard__t">«Сейчас насоветует своего дорогого»</span>'
             '<p class="t-body-sm infocard__d">Если вам подойдёт средство за 500 ₽ из аптеки — '
             'я так и скажу. Я регулярно советую масс-маркет, когда он решает задачу. '
             'Продавать уход — не цель консультации.</p>'
             '</div>')
    p.append('<div class="price-block">'
             '<span class="price-block__l">'
             '<span class="t-price price-block__v">от 3 000 ₽</span>'
             '<span class="t-body-sm price-block__note">видео-созвон 60 минут + схема ухода</span>'
             '</span></div>')
    p.append(media(260, 'ФОТО · СОЗВОН / СХЕМА НА ЭКРАНЕ'))
    p.append('<div class="stack-4">'
             '<button class="btn btn--primary btn--block" type="button" '
             'data-overlay-open="zapis" data-service="Онлайн-консультация — 3 000 ₽">'
             'Записаться на разбор</button>'
             '<a class="btn btn--tg btn--block" href="#">' + ic('tg', 18, solid=True) +
             '<span>Написать в Telegram</span></a></div>')
    p.append('</section>')

    # 02 Как проходит — 5 шагов
    p.append(sec(gap=18))
    p.append(section_head('ПРОЦЕСС', 'Пять шагов',
                          'В конце — не «ощущение от разговора», а документ, по которому '
                          'вы живёте каждый день.'))
    p.append(steps([
        {'t': 'Анкета и фото',
         'd': 'Присылаете фото кожи и всех своих баночек — до созвона. Я успеваю разобраться заранее.'},
        {'t': 'Видео-созвон 60 минут',
         'd': 'Диагностика и разбор каждой баночки: что оставить, что выбросить, чего не хватает.'},
        {'t': 'Персональная схема ухода',
         'd': 'Итоговый документ: утро и вечер, порядок нанесения, как вводить активы. '
              'Он остаётся у вас.'},
        {'t': 'Средства под ваш бюджет',
         'd': 'Из моего ассортимента с доставкой по России — или честный подбор из аптеки '
              'и масс-маркета.'},
        {'t': 'Контроль через месяц',
         'd': 'Фото-контроль и корректировка схемы по результату — в расширенном тарифе.'},
    ]))
    p.append('</section>')

    # 03 Что получите
    p.append(sec(gap=16))
    p.append(section_head('РЕЗУЛЬТАТ', 'Вот что у вас останется',
                          'Схема ухода — фирменный документ с вашим именем. Её можно '
                          'распечатать и повесить на зеркало.'))
    p.append('<div class="doc">' + media(420, 'МАКЕТ PDF · «СХЕМА УХОДА»', radius=16) +
             '<div class="doc__l">' + list_items([
                 {'t': 'Утро и вечер по шагам, с порядком нанесения'},
                 {'t': 'Таблица средств: что, где взять и сколько стоит'},
                 {'t': 'Заметки врача лично для вас'},
                 {'t': 'Схема привыкания к активам'},
             ]) + '</div></div>')
    p.append('</section>')

    # 04 Тарифы
    p.append(sec(gap=14, sid='tarify'))
    p.append(section_head('ТАРИФЫ', 'Выберите формат',
                          'Базовый — если нужна схема. С сопровождением — если хотите, '
                          'чтобы вас вели.'))
    p.append('<div class="tariffs">')
    p.append(tariff('Консультация + схема', '3 000 ₽', [
        'Анкета и разбор фото',
        'Видео-созвон 60 минут',
        'Персональная схема ухода документом',
    ]))
    p.append(tariff('С сопровождением', 'по запросу', [
        'Всё из базового тарифа',
        'Фото-контроль через месяц',
        'Корректировка схемы по результату',
        'Приоритетные ответы на вопросы',
    ], pro=True))
    p.append('</div>')
    p.append('</section>')

    # 05 Кому подходит
    p.append(sec(gap=16))
    p.append(section_head('ЧЕСТНО', 'Кому подходит, а кому нет',
                          'Онлайн решает не всё — и я скажу об этом до оплаты, а не после.'))
    p.append('<div class="stack-4">')
    p.append('<div class="panel panel--soft">'
             '<span class="t-body-md panel__h panel__h--yes">Подойдёт</span>' +
             list_items([
                 {'t': 'Вы не знаете, что из вашей полки работает, а что нет'},
                 {'t': 'Хочется системного ухода, а не случайных покупок'},
                 {'t': 'Вы в другом городе и не можете приехать'},
                 {'t': 'Нужен уход под конкретный бюджет'},
             ]) + '</div>')
    p.append('<div class="panel">'
             '<span class="t-body-md panel__h panel__h--no">Не заменит очный приём</span>' +
             list_items([
                 {'t': 'Инъекционные процедуры — только очно', 'yes': False},
                 {'t': 'Активное воспаление, требующее осмотра', 'yes': False},
                 {'t': 'Состояния, где нужен дерматолог и анализы', 'yes': False},
             ]) + '</div>')
    p.append('</div>')
    p.append('</section>')

    # 06 Отзывы иногородних
    p.append(sec(gap=16, sid='otzyvy'))
    p.append(section_head('ОТЗЫВЫ', 'Клиенты из других городов'))
    p.append('<div class="reviews">')
    p.append(review('Живу в Новосибирске. Прислала фото своих банок — половину сказали '
                    'выбросить, и это было бесплатно честно. Схема пришла на следующий день, '
                    'средства — через неделю.', 'Рената, 26', 'онлайн-консультация'))
    p.append(review('Купила по схеме вместо пяти банок три — вышло дешевле.',
                    'Ольга, 34', 'онлайн-консультация'))
    p.append('</div>')
    p.append('</section>')

    # 07 FAQ
    p.append(sec(gap=10, sid='faq'))
    p.append(section_head('ЧАСТЫЕ ВОПРОСЫ', 'Как всё устроено'))
    p.append(faq([
        {'q': 'Как проходит созвон и где?', 'open': True,
         'a': 'Миграция — это почти всегда перебор с объёмом или неподходящий препарат. '
              'Я работаю оригинальными филлерами и не ставлю больше, чем держит ваша анатомия. '
              'На осмотре через 14 дней смотрим результат вместе.'},
        {'q': 'Что подготовить заранее?'},
        {'q': 'Как оплатить?'},
        {'q': 'Как я получу средства?'},
        {'q': 'А если схема не подойдёт?'},
    ]))
    p.append('</section>')

    # 08 Запись
    p.append(sec(gap=16, sid='zapis-form', extra='pad-bottom'))
    p.append(section_head('ЗАПИСЬ', 'Оставьте заявку',
                          'Отвечу лично и пришлю анкету. Оплата — после того, как '
                          'договоримся о времени.'))
    p.append('<div class="hscroll hscroll--chips" data-chips>'
             '<button class="chip is-active" type="button">Консультация + схема</button>'
             '<button class="chip" type="button">С сопровождением</button>'
             '</div>')
    p.append('<div class="form-card">'
             '<div class="form-card__h">'
             '<h3 class="t-h3">Оставьте заявку</h3>'
             '<p class="t-body-sm form-card__sub">Заявка придёт мне в Telegram — отвечу лично.</p>'
             '</div>'
             '<form class="form" data-form novalidate>'
             '<div class="field">'
             '<label class="t-label field__label" for="o-name"><span>ВАШЕ ИМЯ</span></label>'
             '<input class="field__input" id="o-name" name="name" type="text" '
             'autocomplete="name" placeholder="Анастасия" required></div>'
             '<div class="field">'
             '<label class="t-label field__label" for="o-tg"><span>TELEGRAM ИЛИ ТЕЛЕФОН</span></label>'
             '<input class="field__input" id="o-tg" name="contact" type="text" '
             'autocomplete="tel" placeholder="@nickname" required></div>'
             '<div class="field">'
             '<label class="t-label field__label" for="o-city"><span>ГОРОД</span></label>'
             '<input class="field__input" id="o-city" name="city" type="text" '
             'autocomplete="address-level2" placeholder="Новосибирск"></div>'
             '<label class="checkbox"><input type="checkbox" required>'
             '<span class="t-body">Согласен(на) на обработку персональных данных</span></label>'
             '<button class="btn btn--primary btn--block" type="submit">Отправить заявку</button>'
             '</form></div>')
    p.append('</section>')

    p.append('</main>')
    p.append(foot())
    return '\n'.join(p)
