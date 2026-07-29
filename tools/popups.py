# -*- coding: utf-8 -*-
"""
Поп-апы — по макетам Figma:
  «Запись», «Заявка отправлена», «Меню», «Выбор тарифа»,
  «Заказать средство», «До после».
"""

from build import ic, service_select


def _field(fid, label, placeholder, value='', link='', required=True,
           itype='text', autocomplete=''):
    lab = '<span>%s</span>' % label
    if link:
        lab += ('<button class="t-label field__link" type="button" '
                'data-focus="%s">%s</button>' % (fid, link))
    ac = ' autocomplete="%s"' % autocomplete if autocomplete else ''
    return ('<div class="field%s">'
            '<label class="t-label field__label" for="%s">%s</label>'
            '<input class="field__input" id="%s" name="%s" type="%s"%s '
            'placeholder="%s" value="%s"%s></div>'
            % (' is-filled' if value else '', fid, lab, fid, fid, itype, ac,
               placeholder, value, ' required' if required else ''))


def _service_field(fid):
    """Поле «Услуга» — выпадающий список из прайса, вид как у обычного поля."""
    return ('<div class="field">'
            '<label class="t-label field__label" for="%s"><span>УСЛУГА</span>'
            '<button class="t-label field__link" type="button" data-focus="%s">Изменить</button>'
            '</label>%s</div>' % (fid, fid, service_select(fid)))


AGREE = ('<label class="checkbox"><input type="checkbox" required>'
         '<span class="t-body-sm">Согласен(на) на обработку персональных данных</span></label>')


# --------------------------------------------------------------- Запись ----

ZAPIS = '''<div class="overlay" id="zapis" role="dialog" aria-modal="true" aria-label="Записаться">
  <div class="overlay__scrim" data-overlay-close></div>
  <div class="sheet">
    <button class="sheet__grip" type="button" data-sheet-close aria-label="Закрыть"><span class="sheet__handle"></span></button>
    <div class="sheet__h">
      <h2 class="t-h2 sheet__title">Записаться</h2>
      <p class="t-body-sm sheet__sub">Заявка придёт мне в Telegram — отвечу лично</p>
    </div>
    <form class="form" data-form novalidate>
      {name}
      {contact}
      {service}
      {agree}
      <div class="sheet__b">
        <button class="btn btn--primary btn--block" type="submit">Отправить заявку</button>
        <a class="btn btn--tg btn--block" href="#">{tg}<span>Написать в Telegram</span></a>
      </div>
    </form>
  </div>
</div>'''.format(
    name=_field('z-name', 'ВАШЕ ИМЯ', 'Анастасия', autocomplete='name'),
    contact=_field('z-contact', 'TELEGRAM ИЛИ ТЕЛЕФОН', '@nickname', autocomplete='tel'),
    service=_service_field('z-service'),
    agree=AGREE,
    tg=ic('tg', 18, solid=True),
)


# ---------------------------------------------------- Заявка отправлена ----

SENT = '''<div class="overlay" id="sent" role="dialog" aria-modal="true" aria-label="Заявка отправлена">
  <div class="overlay__scrim" data-overlay-close></div>
  <div class="modal">
    <div class="modal__ic">%s</div>
    <h2 class="t-h2 modal__title">Заявка отправлена</h2>
    <p class="t-body modal__d">Она уже у меня в Telegram. Отвечу лично — обычно в течение дня. Если вопрос срочный, напишите прямо сейчас.</p>
    <a class="btn btn--tg btn--block" href="#">%s<span>Написать в Telegram</span></a>
    <button class="modal__link" type="button" data-overlay-close>Вернуться на сайт</button>
  </div>
</div>''' % (ic('check', 28), ic('tg', 18, solid=True))


# ----------------------------------------------------------------- Меню ----

_MENU_ROWS = [
    ('@@/index.html#uslugi', 'Услуги', 'от 2 000 ₽', True),
    ('@@/index.html#problemy', 'Проблемы', 'подбор по симптому', False),
    ('@@/pamyatki/index.html', 'Памятки', 'до и после процедур', False),
    ('@@/index.html#ceny', 'Цены', 'весь прайс', False),
    ('@@/index.html#do-posle', 'Результаты', 'до / после и отзывы', False),
    ('@@/index.html#obo-mne', 'Обо мне', 'врач и принципы', False),
]

MENU = '''<div class="overlay" id="menu" role="dialog" aria-modal="true" aria-label="Меню">
  <div class="overlay__scrim" data-overlay-close></div>
  <div class="sheet">
    <div class="menu__top">
      <span class="menu__logo">
        <span class="t-label">КОСМЕТОЛОГ</span>
        <span class="t-card-title">Власова</span>
      </span>
      <button class="icon-btn" type="button" data-overlay-close aria-label="Закрыть">%s</button>
    </div>
    <nav class="menu-list">%s</nav>
    <div class="menu__card">
      <span class="t-h3">Не знаете, что выбрать?</span>
      <p class="t-body-sm">Разберу вашу кожу и уход по фото на онлайн-консультации — и честно скажу, что нужно, а что нет.</p>
      <a class="btn btn--sm btn--primary btn--block" href="@@/uslugi/online-konsultaciya/index.html">Онлайн-консультация — 3 000 ₽</a>
    </div>
    <a class="menu__phone" href="tel:+79600401151">%s<span class="t-body-md">+7 960 040-11-51</span></a>
    <button class="btn btn--primary btn--block" type="button" data-overlay-open="zapis">Записаться</button>
  </div>
</div>''' % (
    ic('close', 20),
    '\n      '.join(
        '<a href="%s"><span class="t-h3">%s</span>'
        '<span class="t-body-sm menu-list__sub">%s</span>'
        '<span class="radio%s"></span></a>' % (h, t, s, ' is-on' if on else '')
        for h, t, s, on in _MENU_ROWS),
    ic('phone', 20),
)


# -------------------------------------------------------- Выбор тарифа -----

TARIF = '''<div class="overlay" id="tarif" role="dialog" aria-modal="true" aria-label="Выбор тарифа">
  <div class="overlay__scrim" data-overlay-close></div>
  <div class="sheet">
    <button class="sheet__grip" type="button" data-sheet-close aria-label="Закрыть"><span class="sheet__handle"></span></button>
    <div class="sheet__h">
      <h2 class="t-h2 sheet__title">Онлайн-консультация</h2>
      <p class="t-body-sm sheet__sub">Выберите формат — оплата после того, как договоримся о времени</p>
    </div>
    <div data-radiogroup>
      <button class="radio-card is-active" type="button">
        <span class="radio-card__top">
          <span class="radio is-on"></span>
          <span class="t-price-sm radio-card__p">3 000 ₽</span>
        </span>
        <span class="t-body-md">Консультация + схема</span>
        <span class="t-body-sm radio-card__sub">анкета, созвон 60 минут, схема документом</span>
      </button>
      <button class="radio-card" type="button">
        <span class="radio-card__top">
          <span class="radio"></span>
          <span class="t-price-sm radio-card__p">по запросу</span>
        </span>
        <span class="t-body-md">С сопровождением</span>
        <span class="t-body-sm radio-card__sub">всё из базового + фото-контроль через месяц</span>
      </button>
    </div>
    <form class="form" data-form novalidate style="margin-top:1rem">
      {name}
      {contact}
      {agree}
      <div class="sheet__b">
        <button class="btn btn--primary btn--block" type="submit">Записаться на разбор</button>
      </div>
    </form>
  </div>
</div>'''.format(
    name=_field('t-name', 'ВАШЕ ИМЯ', 'Анастасия', autocomplete='name'),
    contact=_field('t-contact', 'TELEGRAM ИЛИ ТЕЛЕФОН', '@nickname', autocomplete='tel'),
    agree=AGREE,
)


# ---------------------------------------------------- Заказать средство ----

PRODUCT = '''<div class="overlay" id="product" role="dialog" aria-modal="true" aria-label="Заказать средство">
  <div class="overlay__scrim" data-overlay-close></div>
  <div class="sheet">
    <button class="sheet__grip" type="button" data-sheet-close aria-label="Закрыть"><span class="sheet__handle"></span></button>
    <div class="sheet__h">
      <h2 class="t-h2 sheet__title">Заказать средство</h2>
      <p class="t-body-sm sheet__sub">Заявка придёт мне в Telegram — подтвержу наличие и сроки</p>
    </div>
    <div class="product">
      <span class="product__img"></span>
      <span class="product__t">
        <span class="t-body-md">Крем Аквабаланс увлажняющий</span>
        <span class="t-body-sm product__sub">восстановление барьера · 50 мл</span>
        <span class="t-price-sm product__p">7 500 ₽</span>
      </span>
    </div>
    <form class="form" data-form novalidate>
      {name}
      {contact}
      {city}
      <div class="note">{shield}
        <div class="note__t">
          <span class="t-body-md">Доставка по России</span>
          <p class="t-body-sm note__d">Бесплатно, если заказываете схему ухода целиком. Иначе — по тарифу СДЭК или Почты.</p>
        </div>
      </div>
      <div class="sheet__b">
        <button class="btn btn--primary btn--block" type="submit">Отправить заявку</button>
      </div>
    </form>
  </div>
</div>'''.format(
    name=_field('p-name', 'ВАШЕ ИМЯ', 'Анастасия', autocomplete='name'),
    contact=_field('p-contact', 'TELEGRAM ИЛИ ТЕЛЕФОН', '@nickname', autocomplete='tel'),
    city=_field('p-city', 'ГОРОД ДОСТАВКИ', 'Новосибирск', required=False, autocomplete='address-level2'),
    shield=ic('shield', 20),
)


# ------------------------------------------------------------ До / после ---

_LB_CHIPS = ['Губы', 'Ботокс', 'Чистка', 'Пилинги', 'Акне']

LIGHTBOX = '''<div class="lightbox" id="ba" role="dialog" aria-modal="true" aria-label="До и после">
  <div class="lightbox__in">
    <div class="lightbox__top">
      <span class="t-btn-sm lightbox__counter" data-lb-counter>3 / 12</span>
      <button class="icon-btn lightbox__close" type="button" data-overlay-close aria-label="Закрыть">%s</button>
    </div>
    <div class="hscroll hscroll--chips" data-chips>%s</div>
    <div class="lightbox__card">
      <span class="t-body-md">Увеличение губ · филлер 1 мл</span>
      <p class="t-body-sm">Фото «после» — через 14 дней, на осмотре. Алина, 24 года. Опубликовано с согласия клиентки.</p>
    </div>
    <div class="segmented" data-segmented>
      <button class="is-active" type="button">До</button>
      <button type="button">После</button>
    </div>
    <div class="lightbox__media"></div>
  </div>
</div>''' % (
    ic('close', 20),
    ''.join('<button class="chip%s" type="button">%s</button>'
            % (' is-active' if i == 0 else '', c) for i, c in enumerate(_LB_CHIPS)),
)


ALL = '\n'.join([MENU, ZAPIS, TARIF, PRODUCT, SENT, LIGHTBOX])
