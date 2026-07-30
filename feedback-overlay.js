/**
 * feedback-overlay.js — standalone visual-feedback overlay.
 *
 * Drop-in: <script src="/feedback-overlay.js" defer
 *            data-supabase-url="https://xxxx.supabase.co"
 *            data-supabase-key="PUBLIC_ANON_KEY"></script>
 *
 * Or configure via window.FEEDBACK_CONFIG = { supabaseUrl, supabaseKey } before the script loads.
 *
 * With no Supabase config it falls back to localStorage so it works instantly for a single browser.
 *
 * Design goals:
 *  - Never interfere with the host page (isolated container, scoped styles, pointer-events off by default).
 *  - Single floating button toggles the overlay on/off. When on, the element
 *    picker and an always-visible comment list are shown together.
 */
(function () {
  "use strict";

  // Guard against double-injection.
  if (window.__feedbackOverlayLoaded) return;
  window.__feedbackOverlayLoaded = true;

  // ---------------------------------------------------------------------------
  // Config
  // ---------------------------------------------------------------------------
  var script = document.currentScript;
  var cfg = window.FEEDBACK_CONFIG || {};
  var SUPABASE_URL = cfg.supabaseUrl || (script && script.getAttribute("data-supabase-url")) || "";
  var SUPABASE_KEY = cfg.supabaseKey || (script && script.getAttribute("data-supabase-key")) || "";
  var TABLE = cfg.table || "feedback_comments";
  var USE_SUPABASE = !!(SUPABASE_URL && SUPABASE_KEY);

  // Normalize the current page URL used to scope comments (ignore hash & query by default).
  var PAGE_URL = location.origin + location.pathname;

  // ---------------------------------------------------------------------------
  // Client identity (lets an author delete their own comments)
  // ---------------------------------------------------------------------------
  var CLIENT_ID = localStorage.getItem("fb_client_id");
  if (!CLIENT_ID) {
    CLIENT_ID = "c_" + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem("fb_client_id", CLIENT_ID);
  }
  var AUTHOR = localStorage.getItem("fb_author") || "";

  // ---------------------------------------------------------------------------
  // Storage layer — Supabase REST, or localStorage fallback
  // ---------------------------------------------------------------------------
  var store = {
    list: function () {
      if (USE_SUPABASE) {
        var url =
          SUPABASE_URL +
          "/rest/v1/" +
          TABLE +
          "?select=*&page_url=eq." +
          encodeURIComponent(PAGE_URL) +
          "&order=created_at.asc";
        return fetch(url, { headers: sbHeaders() })
          .then(function (r) {
            return r.ok ? r.json() : [];
          })
          .catch(function () {
            return [];
          });
      }
      return Promise.resolve(lsRead());
    },
    add: function (comment) {
      if (USE_SUPABASE) {
        return fetch(SUPABASE_URL + "/rest/v1/" + TABLE, {
          method: "POST",
          headers: Object.assign(sbHeaders(), {
            "Content-Type": "application/json",
            Prefer: "return=representation",
          }),
          body: JSON.stringify(comment),
        })
          .then(function (r) {
            return r.ok ? r.json() : [];
          })
          .then(function (rows) {
            return rows[0] || comment;
          });
      }
      var saved = Object.assign({}, comment, {
        id: "l_" + Date.now(),
        created_at: new Date().toISOString(),
      });
      var all = lsRead();
      all.push(saved);
      lsWrite(all);
      return Promise.resolve(saved);
    },
    remove: function (id) {
      if (USE_SUPABASE) {
        return fetch(
          SUPABASE_URL +
            "/rest/v1/" +
            TABLE +
            "?id=eq." +
            encodeURIComponent(id) +
            "&client_id=eq." +
            encodeURIComponent(CLIENT_ID),
          { method: "DELETE", headers: sbHeaders() }
        ).then(function () {});
      }
      lsWrite(
        lsRead().filter(function (c) {
          return c.id !== id;
        })
      );
      return Promise.resolve();
    },
  };

  function sbHeaders() {
    return { apikey: SUPABASE_KEY, Authorization: "Bearer " + SUPABASE_KEY };
  }
  function lsKey() {
    return "fb_comments_" + PAGE_URL;
  }
  function lsRead() {
    try {
      return JSON.parse(localStorage.getItem(lsKey()) || "[]");
    } catch (e) {
      return [];
    }
  }
  function lsWrite(arr) {
    localStorage.setItem(lsKey(), JSON.stringify(arr));
  }

  // ---------------------------------------------------------------------------
  // CSS selector: build a stable-ish path to an element, and resolve it back
  // ---------------------------------------------------------------------------
  function buildSelector(el) {
    if (!el || el.nodeType !== 1) return "";
    if (el.id) return "#" + CSS.escape(el.id);
    var parts = [];
    var node = el;
    while (node && node.nodeType === 1 && node !== document.body && parts.length < 6) {
      var part = node.tagName.toLowerCase();
      var parent = node.parentElement;
      if (parent) {
        var siblings = Array.prototype.filter.call(parent.children, function (c) {
          return c.tagName === node.tagName;
        });
        if (siblings.length > 1) {
          part += ":nth-of-type(" + (siblings.indexOf(node) + 1) + ")";
        }
      }
      parts.unshift(part);
      node = node.parentElement;
    }
    return parts.join(" > ");
  }

  function resolve(selector) {
    try {
      return document.querySelector(selector);
    } catch (e) {
      return null;
    }
  }

  // ---------------------------------------------------------------------------
  // DOM: isolated root, styles, floating button
  // ---------------------------------------------------------------------------
  var root = document.createElement("div");
  root.id = "fb-overlay-root";
  root.setAttribute("data-fb", "1");
  document.body.appendChild(root);

  var style = document.createElement("style");
  style.textContent = css();
  root.appendChild(style);

  // Layer that draws element highlight + pins. pointer-events managed per-mode.
  var layer = document.createElement("div");
  layer.className = "fb-layer";
  root.appendChild(layer);

  var highlight = document.createElement("div");
  highlight.className = "fb-highlight";
  layer.appendChild(highlight);

  // Always-on list docked to the right while the overlay is on.
  var listPanel = document.createElement("div");
  listPanel.className = "fb-panel fb-list-panel";
  root.appendChild(listPanel);

  // Floating popover for the new-comment editor and for reading a single comment.
  var popover = document.createElement("div");
  popover.className = "fb-panel fb-popover";
  root.appendChild(popover);

  var btn = document.createElement("button");
  btn.className = "fb-btn";
  btn.type = "button";
  btn.title = "Режим правок";
  btn.innerHTML = pinSvg();
  root.appendChild(btn);

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  var mode = "off"; // off | on
  var comments = [];
  var activeId = null; // currently focused comment
  var hoverEl = null;

  btn.addEventListener("click", cycleMode);

  function cycleMode() {
    setMode(mode === "off" ? "on" : "off");
  }

  function setMode(next) {
    mode = next;
    root.setAttribute("data-mode", mode);
    if (mode === "off") {
      teardownAnnotate();
      listPanel.style.display = "none";
      popover.style.display = "none";
      clearPins();
      highlight.style.display = "none";
      btn.classList.remove("fb-btn--active");
      activeId = null;
      return;
    }
    // mode === "on": annotate + always-visible list together.
    btn.classList.add("fb-btn--active");
    enableAnnotate();
    listPanel.style.display = "block";
    refresh();
  }

  // ---------------------------------------------------------------------------
  // Load + render pins
  // ---------------------------------------------------------------------------
  function refresh() {
    return store.list().then(function (rows) {
      comments = rows || [];
      renderPins();
      if (mode === "on") renderList();
    });
  }

  function clearPins() {
    Array.prototype.forEach.call(layer.querySelectorAll(".fb-pin"), function (p) {
      p.remove();
    });
  }

  function renderPins() {
    clearPins();
    comments.forEach(function (c) {
      var el = resolve(c.selector);
      if (!el) return;
      var r = el.getBoundingClientRect();
      var pin = document.createElement("button");
      pin.type = "button";
      pin.className = "fb-pin";
      // The overlay layer is position:fixed, so it shares the viewport coordinate
      // space that getBoundingClientRect() returns — no scroll offset needed.
      pin.style.left = r.left + c.x * r.width + "px";
      pin.style.top = r.top + c.y * r.height + "px";
      pin.title = c.text;
      pin.textContent = "";
      if (c.id === activeId) pin.classList.add("fb-pin--active");
      pin.addEventListener("click", function (e) {
        e.stopPropagation();
        focusComment(c.id);
      });
      layer.appendChild(pin);
    });
  }

  function focusComment(id) {
    activeId = id;
    var c = comments.find(function (x) {
      return x.id === id;
    });
    if (!c) return;
    var el = resolve(c.selector);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      moveHighlight(el);
      highlight.style.display = "block";
    }
    renderPins();
    renderList();
    showBubble(c);
  }

  // ---------------------------------------------------------------------------
  // Annotate mode — hover highlight + click to place a pin
  // ---------------------------------------------------------------------------
  function enableAnnotate() {
    highlight.style.display = "none";
    document.addEventListener("mousemove", onHover, true);
    document.addEventListener("click", onPick, true);
    window.addEventListener("scroll", reposition, true);
    window.addEventListener("resize", reposition);
  }
  function disableAnnotate() {
    document.removeEventListener("mousemove", onHover, true);
    document.removeEventListener("click", onPick, true);
  }
  function teardownAnnotate() {
    disableAnnotate();
    window.removeEventListener("scroll", reposition, true);
    window.removeEventListener("resize", reposition);
  }

  function isOwn(el) {
    return el && el.closest && el.closest("#fb-overlay-root");
  }

  var hoverRaf = false;
  var lastX = 0;
  var lastY = 0;
  function onHover(e) {
    if (mode !== "on") return;
    lastX = e.clientX;
    lastY = e.clientY;
    if (hoverRaf) return;
    hoverRaf = true;
    requestAnimationFrame(function () {
      hoverRaf = false;
      // Resolve the topmost host-page element under the cursor. Our overlay layer
      // has pointer-events:none, so elementFromPoint returns the real target and
      // never the highlight box — steadier than e.target on nested nodes.
      var el = document.elementFromPoint(lastX, lastY);
      if (!el || isOwn(el)) {
        highlight.style.display = "none";
        hoverEl = null;
        return;
      }
      if (el === hoverEl) return; // same element — nothing to redraw
      hoverEl = el;
      moveHighlight(el);
      highlight.style.display = "block";
    });
  }

  function moveHighlight(el) {
    var r = el.getBoundingClientRect();
    highlight.style.left = r.left + "px";
    highlight.style.top = r.top + "px";
    highlight.style.width = r.width + "px";
    highlight.style.height = r.height + "px";
  }

  function onPick(e) {
    if (mode !== "on") return;
    if (isOwn(e.target)) return; // let overlay UI work normally
    e.preventDefault();
    e.stopPropagation();
    // Use the same resolution as the hover highlight so the pinned element
    // matches exactly what was outlined under the cursor.
    var el = document.elementFromPoint(e.clientX, e.clientY) || e.target;
    if (isOwn(el)) return;
    var r = el.getBoundingClientRect();
    var x = (e.clientX - r.left) / Math.max(r.width, 1);
    var y = (e.clientY - r.top) / Math.max(r.height, 1);
    openEditor(el, clamp01(x), clamp01(y), e.clientX, e.clientY);
  }

  function clamp01(n) {
    return Math.min(1, Math.max(0, n));
  }

  // ---------------------------------------------------------------------------
  // Editor bubble (new comment)
  // ---------------------------------------------------------------------------
  function openEditor(el, x, y, vpX, vpY) {
    var selector = buildSelector(el);
    popover.style.display = "block";
    popover.innerHTML = "";
    positionPanel(vpX, vpY);

    var wrap = document.createElement("div");
    wrap.className = "fb-editor";
    wrap.innerHTML =
      '<div class="fb-editor__title">Новый комментарий</div>' +
      '<input class="fb-input fb-name" placeholder="Ваше имя (необязательно)" value="' +
      escapeAttr(AUTHOR) +
      '"/>' +
      '<textarea class="fb-input fb-text" rows="3" placeholder="Например: этот блок должен быть красным"></textarea>' +
      '<div class="fb-editor__row">' +
      '<button class="fb-cancel" type="button">Отмена</button>' +
      '<button class="fb-save" type="button">Сохранить</button>' +
      "</div>";
    popover.appendChild(wrap);

    var textEl = wrap.querySelector(".fb-text");
    var nameEl = wrap.querySelector(".fb-name");
    textEl.focus();

    wrap.querySelector(".fb-cancel").addEventListener("click", function () {
      popover.style.display = "none";
    });
    wrap.querySelector(".fb-save").addEventListener("click", function () {
      var text = textEl.value.trim();
      if (!text) {
        textEl.focus();
        return;
      }
      var author = nameEl.value.trim() || "Аноним";
      localStorage.setItem("fb_author", author === "Аноним" ? "" : author);
      AUTHOR = author === "Аноним" ? "" : author;
      var payload = {
        page_url: PAGE_URL,
        selector: selector,
        x: x,
        y: y,
        text: text,
        author: author,
        client_id: CLIENT_ID,
      };
      store.add(payload).then(function () {
        popover.style.display = "none";
        refresh();
      });
    });
  }

  // Positions the floating popover. Coordinates are viewport-relative
  // (the popover lives in the fixed overlay root).
  function positionPanel(vpX, vpY) {
    var maxLeft = window.innerWidth - 320;
    var maxTop = window.innerHeight - 120;
    popover.style.left = Math.max(8, Math.min(vpX + 12, maxLeft)) + "px";
    popover.style.top = Math.max(8, Math.min(vpY + 12, maxTop)) + "px";
    popover.style.right = "auto";
    popover.style.bottom = "auto";
  }

  // ---------------------------------------------------------------------------
  // Read bubble (existing comment)
  // ---------------------------------------------------------------------------
  function showBubble(c) {
    var el = resolve(c.selector);
    var r = el ? el.getBoundingClientRect() : { left: 40, top: 40, width: 0, height: 0 };
    popover.style.display = "block";
    positionPanel(r.left + c.x * r.width, r.top + c.y * r.height);
    popover.innerHTML = "";
    var wrap = document.createElement("div");
    wrap.className = "fb-bubble";
    var canDelete = c.client_id === CLIENT_ID;
    wrap.innerHTML =
      '<div class="fb-bubble__head"><b>' +
      escapeHtml(c.author || "Аноним") +
      "</b><span>" +
      timeAgo(c.created_at) +
      "</span></div>" +
      '<div class="fb-bubble__text">' +
      escapeHtml(c.text) +
      "</div>" +
      '<div class="fb-editor__row">' +
      (canDelete ? '<button class="fb-del" type="button">Удалить</button>' : "<span></span>") +
      '<button class="fb-close" type="button">Закрыть</button>' +
      "</div>";
    popover.appendChild(wrap);
    wrap.querySelector(".fb-close").addEventListener("click", function () {
      popover.style.display = "none";
      activeId = null;
      renderPins();
      renderList();
    });
    if (canDelete) {
      wrap.querySelector(".fb-del").addEventListener("click", function () {
        store.remove(c.id).then(function () {
          activeId = null;
          popover.style.display = "none";
          refresh();
        });
      });
    }
  }

  // ---------------------------------------------------------------------------
  // List mode
  // ---------------------------------------------------------------------------
  function renderList() {
    listPanel.innerHTML =
      '<div class="fb-list__head">' +
      "<span>Комментарии (" +
      comments.length +
      ")</span>" +
      '<button class="fb-refresh" type="button" title="Загрузить заново из базы">↻</button>' +
      "</div>";
    listPanel.querySelector(".fb-refresh").addEventListener("click", function (e) {
      var b = e.currentTarget;
      b.disabled = true;
      b.classList.add("fb-refresh--spin");
      refresh().then(function () {
        // renderList() re-runs inside refresh(), replacing this button — nothing else to reset.
      });
    });
    var list = document.createElement("div");
    list.className = "fb-list";
    if (!comments.length) {
      list.innerHTML = '<div class="fb-empty">Пока нет комментариев на этой странице.</div>';
    }
    comments.forEach(function (c) {
      var item = document.createElement("button");
      item.type = "button";
      item.className = "fb-list__item" + (c.id === activeId ? " is-active" : "");
      item.innerHTML =
        '<div class="fb-list__meta"><b>' +
        escapeHtml(c.author || "Аноним") +
        "</b> · " +
        timeAgo(c.created_at) +
        "</div>" +
        '<div class="fb-list__text">' +
        escapeHtml(c.text) +
        "</div>";
      item.addEventListener("click", function () {
        focusComment(c.id);
      });
      list.appendChild(item);
    });
    listPanel.appendChild(list);
  }

  // ---------------------------------------------------------------------------
  // Reposition pins/highlight on scroll & resize
  // ---------------------------------------------------------------------------
  var rafPending = false;
  function reposition() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function () {
      rafPending = false;
      if (mode === "off") return;
      renderPins();
      if (activeId) {
        var c = comments.find(function (x) {
          return x.id === activeId;
        });
        if (c) {
          var el = resolve(c.selector);
          if (el) {
            moveHighlight(el);
            // Keep an open comment popover anchored to its element while scrolling.
            if (mode === "on") {
              var r = el.getBoundingClientRect();
              positionPanel(r.left + c.x * r.width, r.top + c.y * r.height);
            }
          }
        }
      }
    });
  }
  window.addEventListener("scroll", reposition, true);
  window.addEventListener("resize", reposition);

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (m) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
    });
  }
  function escapeAttr(s) {
    return escapeHtml(s).replace(/"/g, "&quot;");
  }
  function timeAgo(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    var s = Math.floor((Date.now() - d.getTime()) / 1000);
    if (s < 60) return "только что";
    if (s < 3600) return Math.floor(s / 60) + " мин назад";
    if (s < 86400) return Math.floor(s / 3600) + " ч назад";
    return d.toLocaleDateString();
  }

  function pinSvg() {
    return (
      '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" ' +
      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
    );
  }

  function css() {
    return [
      "#fb-overlay-root{position:fixed;inset:0;z-index:2147483000;pointer-events:none;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;}",
      "#fb-overlay-root *{box-sizing:border-box;}",
      ".fb-btn{pointer-events:auto;position:fixed;right:20px;bottom:20px;width:52px;height:52px;border-radius:50%;border:none;cursor:pointer;background:rgba(30,30,40,.55);color:#fff;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(6px);box-shadow:0 6px 20px rgba(0,0,0,.25);transition:transform .15s,background .2s;}",
      ".fb-btn:hover{transform:scale(1.06);background:rgba(30,30,40,.8);}",
      ".fb-btn--active{background:#e5484d;color:#fff;}",
      ".fb-layer{position:absolute;inset:0;pointer-events:none;}",
      ".fb-highlight{position:absolute;display:none;border:2px solid #4c8bf5;background:rgba(76,139,245,.12);border-radius:4px;pointer-events:none;will-change:transform,width,height;}",
      ".fb-pin{pointer-events:auto;position:absolute;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#e5484d;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.35);cursor:pointer;padding:0;}",
      ".fb-pin--active{background:#111;z-index:2;}",
      ".fb-panel{pointer-events:auto;position:absolute;display:none;width:300px;max-width:calc(100vw - 32px);background:#fff;color:#1a1a1a;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.25);padding:14px;font-size:14px;line-height:1.4;overflow:auto;}",
      ".fb-list-panel{top:16px;right:16px;bottom:90px;max-height:none;}",
      ".fb-popover{z-index:2;max-height:70vh;}",
      ".fb-editor__title{font-weight:600;margin-bottom:8px;}",
      ".fb-input{width:100%;border:1px solid #d9d9e0;border-radius:8px;padding:8px 10px;font:inherit;margin-bottom:8px;outline:none;}",
      ".fb-input:focus{border-color:#4c8bf5;}",
      ".fb-editor__row{display:flex;justify-content:space-between;gap:8px;align-items:center;margin-top:4px;}",
      ".fb-save{background:#e5484d;color:#fff;border:none;border-radius:8px;padding:8px 14px;cursor:pointer;font:inherit;}",
      ".fb-cancel,.fb-close,.fb-del{background:transparent;border:1px solid #d9d9e0;border-radius:8px;padding:8px 12px;cursor:pointer;font:inherit;color:#555;}",
      ".fb-del{color:#e5484d;border-color:#f3c6c7;}",
      ".fb-bubble__head{display:flex;justify-content:space-between;color:#888;font-size:12px;margin-bottom:6px;}",
      ".fb-bubble__head b{color:#1a1a1a;font-size:13px;}",
      ".fb-bubble__text{margin-bottom:10px;white-space:pre-wrap;}",
      ".fb-list__head{font-weight:600;margin-bottom:10px;display:flex;align-items:center;justify-content:space-between;gap:8px;}",
      ".fb-refresh{border:1px solid #d9d9e0;background:#fff;color:#555;width:28px;height:28px;border-radius:8px;cursor:pointer;font-size:16px;line-height:1;display:flex;align-items:center;justify-content:center;padding:0;}",
      ".fb-refresh:hover{background:#f2f3f6;}",
      ".fb-refresh:disabled{opacity:.6;cursor:default;}",
      "@keyframes fb-spin{to{transform:rotate(360deg)}}",
      ".fb-refresh--spin{animation:fb-spin .6s linear infinite;}",
      ".fb-list{display:flex;flex-direction:column;gap:6px;}",
      ".fb-list__item{text-align:left;background:#f7f7f9;border:1px solid transparent;border-radius:8px;padding:8px 10px;cursor:pointer;font:inherit;}",
      ".fb-list__item:hover{background:#eef1f6;}",
      ".fb-list__item.is-active{border-color:#e5484d;background:#fff;}",
      ".fb-list__meta{font-size:12px;color:#888;margin-bottom:2px;}",
      ".fb-list__text{color:#1a1a1a;}",
      ".fb-empty{color:#999;padding:8px 0;}",
    ].join("");
  }

  // ---------------------------------------------------------------------------
  // Boot: preload comments so pins can show as soon as a mode is opened.
  // ---------------------------------------------------------------------------
  store.list().then(function (rows) {
    comments = rows || [];
  });
})();
