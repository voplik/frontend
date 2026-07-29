# -*- coding: utf-8 -*-
"""
SEO-обвязка: canonical, Open Graph, микроразметка Schema.org.
Решения — по документу «Структура сайта — kosmetolog-vlasova.ru», раздел 11.
"""

import json

SITE = 'https://kosmetolog-vlasova.ru'
BRAND = 'Косметолог Власова'
DOCTOR = 'Анастасия Власова'
PHONE = '+7 960 040-11-51'
PHONE_RAW = '+79600401151'
ADDR = 'Туфана Миннуллина, 8А'
CITY = 'Казань'

# Картинка для соцсетей. Положите файл в assets/img/og.jpg (1200×630)
# и впишите сюда путь — теги og:image появятся сами.
OG_IMAGE = ''


def url(path=''):
    return SITE + '/' + path.lstrip('/')


def _ld(obj):
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(obj, ensure_ascii=False, separators=(',', ':')))


def ld_physician():
    """Physician + LocalBusiness — сильный сигнал E-E-A-T, ставится на все страницы.
    Медицинские типы (MedicalClinic / MedicalProcedure) добавляются после лицензии."""
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'Physician',
        '@id': url() + '#doctor',
        'name': 'Врач-косметолог ' + DOCTOR,
        'alternateName': BRAND,
        'url': url(),
        'telephone': PHONE,
        'priceRange': '2000–18000 ₽',
        'medicalSpecialty': 'Dermatology',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': ADDR,
            'addressLocality': CITY,
            'addressRegion': 'Республика Татарстан',
            'addressCountry': 'RU',
        },
        'areaServed': {'@type': 'City', 'name': CITY},
        'openingHoursSpecification': [{
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'opens': '10:00',
            'closes': '20:00',
        }],
        'sameAs': [],
    })


def ld_breadcrumbs(items):
    """items: [(name, path|None)] — последний элемент без ссылки."""
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            dict([('@type', 'ListItem'), ('position', i + 1), ('name', n)] +
                 ([('item', url(p))] if p is not None else []))
            for i, (n, p) in enumerate(items)
        ],
    })


def ld_service(name, path, price, description, min_price=False):
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': name,
        'url': url(path),
        'description': description,
        'serviceType': name,
        'provider': {'@id': url() + '#doctor'},
        'areaServed': {'@type': 'City', 'name': CITY},
        'offers': {
            '@type': 'Offer',
            'price': price,
            'priceCurrency': 'RUB',
            'availability': 'https://schema.org/InStock',
            'url': url(path),
        },
    })


def ld_faq(pairs):
    """pairs: [(question, answer)] — только пункты, у которых есть ответ."""
    pairs = [(q, a) for q, a in pairs if a]
    if not pairs:
        return ''
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{
            '@type': 'Question',
            'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a},
        } for q, a in pairs],
    })


def ld_howto(name, description, steps):
    """steps: [(name, text)] — таймлайн восстановления в памятке."""
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'HowTo',
        'name': name,
        'description': description,
        'step': [{
            '@type': 'HowToStep',
            'position': i + 1,
            'name': n,
            'text': t,
        } for i, (n, t) in enumerate(steps)],
    })


def ld_article(headline, description, path):
    return _ld({
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': headline,
        'description': description,
        'url': url(path),
        'author': {'@id': url() + '#doctor'},
        'publisher': {'@id': url() + '#doctor'},
        'inLanguage': 'ru-RU',
    })


def meta(title, description, path, og_type='website'):
    """canonical + Open Graph + Twitter."""
    u = url(path)
    tags = [
        '<link rel="canonical" href="%s">' % u,
        '<meta property="og:type" content="%s">' % og_type,
        '<meta property="og:site_name" content="%s">' % BRAND,
        '<meta property="og:locale" content="ru_RU">',
        '<meta property="og:title" content="%s">' % title,
        '<meta property="og:description" content="%s">' % description,
        '<meta property="og:url" content="%s">' % u,
    ]
    if OG_IMAGE:
        tags.append('<meta property="og:image" content="%s">' % url(OG_IMAGE))
        tags.append('<meta name="twitter:card" content="summary_large_image">')
    else:
        tags.append('<meta name="twitter:card" content="summary">')
    return '\n'.join(tags)
