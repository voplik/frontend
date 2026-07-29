/* ==========================================================================
   Власова · косметология — общая логика
   Чистый JS, без зависимостей.
   ========================================================================== */
(function () {
  'use strict';

  var ERROR = '#c0563f';

  /* ----------------------------------------------------------- Аккордеон -- */
  function initFaq() {
    document.querySelectorAll('.faq-item__top').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.faq-item');
        if (!item) return;
        var open = item.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }

  /* -------------------------------------------- Поп-апы: открыть/закрыть -- */
  var scrollLock = 0;

  function lock() {
    if (scrollLock++ === 0) {
      document.body.style.overflow = 'hidden';
    }
  }

  function unlock() {
    scrollLock = Math.max(0, scrollLock - 1);
    if (scrollLock === 0) document.body.style.overflow = '';
  }

  function setInert(on) {
    var page = document.querySelector('.page');
    if (!page) return;
    if (on) page.setAttribute('inert', '');
    else page.removeAttribute('inert');
  }

  function openOverlay(id, service) {
    var el = document.getElementById(id);
    if (!el || el.classList.contains('is-open')) return;

    // предзаполняем услугу, если кнопка её передала
    if (service) {
      var sel = el.querySelector('select[name="service"]');
      if (sel && [].some.call(sel.options, function (o) { return o.value === service; })) {
        sel.value = service;
        var wrap = sel.closest('.field');
        if (wrap) wrap.classList.add('is-filled');
      }
    }

    el.classList.add('is-open');
    setInert(true);
    lock();
    var firstInput = el.querySelector('.field__input');
    if (firstInput) firstInput.focus({ preventScroll: true });
  }

  function closeOverlay(el) {
    if (!el || !el.classList.contains('is-open')) return;
    el.classList.remove('is-open');
    unlock();
    if (!document.querySelector('.overlay.is-open, .lightbox.is-open')) setInert(false);
  }

  function closeAll() {
    document.querySelectorAll('.overlay.is-open, .lightbox.is-open').forEach(closeOverlay);
  }

  function initOverlays() {
    document.addEventListener('click', function (e) {
      var focuser = e.target.closest('[data-focus]');
      if (focuser) {
        e.preventDefault();
        var target = document.getElementById(focuser.getAttribute('data-focus'));
        if (target) {
          target.focus();
          if (typeof target.showPicker === 'function') {
            try { target.showPicker(); } catch (err) { /* не во всех браузерах */ }
          }
        }
        return;
      }

      var opener = e.target.closest('[data-overlay-open]');
      if (opener) {
        e.preventDefault();
        var current = opener.closest('.overlay, .lightbox');
        if (current) closeOverlay(current);
        openOverlay(opener.getAttribute('data-overlay-open'),
                    opener.getAttribute('data-service'));
        return;
      }
      var closer = e.target.closest('[data-overlay-close]');
      if (closer) {
        e.preventDefault();
        closeOverlay(closer.closest('.overlay, .lightbox'));
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeAll();
    });
  }

  /* --------------------------------------------- Чипы (фильтры и табы) ---- */
  function initChips() {
    document.querySelectorAll('[data-chips]').forEach(function (group) {
      group.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip');
        if (!chip || !group.contains(chip)) return;
        group.querySelectorAll('.chip').forEach(function (c) {
          c.classList.toggle('is-active', c === chip);
        });

        var key = chip.getAttribute('data-filter');
        var targetSel = group.getAttribute('data-chips-target');
        if (!key || !targetSel) return;
        document.querySelectorAll(targetSel + ' [data-cat]').forEach(function (n) {
          var show = key === 'all' || n.getAttribute('data-cat') === key;
          n.style.display = show ? '' : 'none';
        });
      });
    });
  }

  /* ------------------------------------------ Радио-карточки (тарифы) ----- */
  function initRadioGroups() {
    document.querySelectorAll('[data-radiogroup]').forEach(function (group) {
      group.addEventListener('click', function (e) {
        var card = e.target.closest('.radio-card');
        if (!card || !group.contains(card)) return;
        group.querySelectorAll('.radio-card').forEach(function (c) {
          var on = c === card;
          c.classList.toggle('is-active', on);
          var r = c.querySelector('.radio');
          if (r) r.classList.toggle('is-on', on);
        });
      });
    });
  }

  /* ---------------------------------------------- Переключатель До/После -- */
  function initSegmented() {
    document.querySelectorAll('[data-segmented]').forEach(function (group) {
      group.addEventListener('click', function (e) {
        var btn = e.target.closest('button');
        if (!btn || !group.contains(btn)) return;
        group.querySelectorAll('button').forEach(function (b) {
          b.classList.toggle('is-active', b === btn);
        });
      });
    });
  }

  /* --------------------------------- Клик по «до / после» → лайтбокс ------ */
  function initBeforeAfter() {
    if (!document.getElementById('ba')) return;
    document.querySelectorAll('.ba').forEach(function (ba, i) {
      ba.style.cursor = 'pointer';
      ba.addEventListener('click', function () {
        var c = document.querySelector('[data-lb-counter]');
        if (c) c.textContent = (i + 1) + ' / ' + document.querySelectorAll('.ba').length;
        openOverlay('ba');
      });
    });
  }

  /* ------------------------------------------------------- Поля формы ----- */
  function initForms() {
    document.querySelectorAll('.field__input').forEach(function (input) {
      var wrap = input.closest('.field');
      if (!wrap) return;
      var sync = function () {
        wrap.classList.toggle('is-filled', String(input.value).trim() !== '');
        input.style.borderColor = '';
      };
      input.addEventListener('input', sync);
      input.addEventListener('change', sync);
      input.addEventListener('blur', sync);
      sync();
    });

    document.querySelectorAll('form[data-form]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var ok = true;
        var firstBad = null;
        form.querySelectorAll('[required]').forEach(function (f) {
          var bad = f.type === 'checkbox' ? !f.checked : !String(f.value).trim();
          if (bad) {
            ok = false;
            if (!firstBad) firstBad = f;
          }
          if (f.classList.contains('field__input')) {
            f.style.borderColor = bad ? ERROR : '';
          }
          var box = f.closest('.checkbox');
          if (box) box.classList.toggle('is-invalid', bad);
        });
        if (!ok) {
          if (firstBad) firstBad.focus({ preventScroll: false });
          return;
        }

        closeOverlay(form.closest('.overlay'));
        openOverlay('sent');

        form.reset();
        form.querySelectorAll('.field').forEach(function (f) {
          f.classList.remove('is-filled');
        });
        form.querySelectorAll('.checkbox').forEach(function (f) {
          f.classList.remove('is-invalid');
        });
        form.querySelectorAll('.field__input').forEach(function (f) {
          f.style.borderColor = '';
        });
      });
    });
  }

  function init() {
    initFaq();
    initOverlays();
    initChips();
    initRadioGroups();
    initSegmented();
    initBeforeAfter();
    initForms();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
