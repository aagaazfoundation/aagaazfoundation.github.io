/* Aagaaz Foundation: "Find help near you".
   Everything here runs on the visitor's own phone or computer.
   - What they type, the district they pick and their location are never sent anywhere.
   - Nothing is saved: no cookies, no storage, nothing added to the page address.
   - Without this script the page still works: every place is listed district by district. */
(function () {
  "use strict";
  var dataEl = document.getElementById("finder-data");
  var where = document.querySelector("[data-finder-where]");
  if (!dataEl || !where) { return; }
  var data;
  try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }

  var T = data.t, cfg = data.cfg, hindi = data.lang === "hi";
  var $ = function (sel) { return document.querySelector(sel); };
  var input = $("#finder-q"), suggest = $("#finder-suggest"), msg = $("[data-finder-msg]");
  var results = $("[data-finder-results]"), list = $("[data-finder-list]"), none = $("[data-finder-none]");
  var nearbyBox = $("[data-finder-nearby]"), nearbyList = $("[data-finder-nearby-list]");
  var chosen = $("[data-finder-chosen]"), sorted = $("[data-finder-sorted]"), shared = $("[data-finder-shared]");
  var staticBox = $("[data-finder-static]"), title = $("#finder-results-title");

  /* ---------- the data ---------- */
  var districts = {}, order = [];
  data.districts.forEach(function (d) { districts[d.id] = d; order.push(d.id); });
  function point(text) {
    var p = String(text || "").split(",");
    if (p.length !== 2) { return null; }
    var lat = parseFloat(p[0]), lng = parseFloat(p[1]);
    return (isFinite(lat) && isFinite(lng)) ? [lat, lng] : null;
  }
  var areas = data.areas.map(function (a) {
    /* a[6], a[7]: another name for the same area, such as a Mohali phase, in English and Hindi */
    return { name: a[0], hi: a[1], district: a[2], pin: a[3], centre: point(a[4]), checked: a[5] === 1,
             also: a[6] || "", alsoHi: a[7] || "",
             key: norm(a[0] + " " + a[1] + " " + (a[6] || "") + " " + (a[7] || "")) };
  });
  var cards = Array.prototype.map.call(document.querySelectorAll("[data-place]"), function (el, i) {
    var lat = parseFloat(el.getAttribute("data-lat")), lng = parseFloat(el.getAttribute("data-lng"));
    var kind = (data.types || []).indexOf(el.getAttribute("data-type"));
    return { el: el, i: i, kind: kind === -1 ? 99 : kind, district: el.getAttribute("data-district"),
             needs: (el.getAttribute("data-needs") || "").split(" "),
             wholeDistrict: el.getAttribute("data-scope") === "district",
             start: el.hasAttribute("data-start"),
             pin: (isFinite(lat) && isFinite(lng)) ? [lat, lng] : null,
             dist: el.querySelector("[data-dist]") };
  });

  /* What the visitor has chosen. Kept only while the page is open. */
  var state = { district: null, point: null, source: null, label: "", pincode: null, needs: {} };

  /* ---------- small helpers ---------- */
  function norm(s) {
    return String(s).toLowerCase()
      .replace(/[०-९]/g, function (c) { return String(c.charCodeAt(0) - 0x0966); })
      .replace(/सेक्टर|सैक्टर/g, "sector ").replace(/फ़ेज़|फेज़|फेज/g, "phase ")
      .replace(/\bsec\b\.?/g, "sector ")
      .replace(/([a-zऀ-ॿ])(\d)/g, "$1 $2").replace(/(\d)([a-zऀ-ॿ])/g, "$1 $2")
      .replace(/[^a-z0-9ऀ-ॿ]+/g, " ").replace(/\s+/g, " ").trim();
  }
  function km(a, b) {
    var R = 6371, rad = Math.PI / 180;
    var dLat = (b[0] - a[0]) * rad, dLng = (b[1] - a[1]) * rad;
    var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(a[0] * rad) * Math.cos(b[0] * rad) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  function fill(text, map) {
    return String(text).replace(/%([A-Z]+)%/g, function (m, k) { return (k in map) ? map[k] : m; });
  }
  function areaLabel(a) {
    var also = (hindi && a.alsoHi) ? a.alsoHi : a.also;
    return ((hindi && a.hi) ? a.hi : a.name) + (also ? " (" + also + ")" : "") + ", " + districts[a.district].short;
  }
  function say(text) { msg.textContent = text || ""; }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) { n.className = cls; }
    if (text != null) { n.textContent = text; }
    return n;
  }

  /* ---------- typing an area or a pincode ---------- */
  function search(raw) {
    var q = norm(raw), out = [];
    if (q.length < 2) { return out; }
    var tokens = q.split(" ");

    if (/^\d{6}$/.test(q)) {
      order.forEach(function (id) {
        if (districts[id].pins.indexOf(q) !== -1) {
          out.push({ kind: "pincode", pincode: q, district: id, text: T.pincode + " " + q + ", " + districts[id].short });
        }
      });
    }
    order.forEach(function (id) {
      var d = districts[id];
      var hit = d.names.some(function (n) { n = norm(n); return n && n.indexOf(q) === 0; });
      if (hit) { out.push({ kind: "district", district: id, text: d.name, small: T.whole_district }); }
    });

    var found = [];
    areas.forEach(function (a) {
      var own = (a.key + " " + a.pin).split(" ");
      var words = own.concat(norm(districts[a.district].names.join(" ")).split(" "));
      var score = 0, ownHit = false;
      var ok = tokens.every(function (tk) {
        /* a single letter, as in "12a", must belong to the area itself, not to its district's name */
        var pool = tk.length === 1 ? own : words;
        var exact = pool.indexOf(tk) !== -1;
        var starts = !exact && pool.some(function (w) { return w.indexOf(tk) === 0; });
        if (exact) { score += 2; } else if (starts) { score += 1; }
        if (own.some(function (w) { return w.indexOf(tk) === 0; })) { ownHit = true; }
        return exact || starts;
      });
      /* the area's own name or pincode must match, not only its district's name */
      if (ok && ownHit) { found.push({ a: a, score: score }); }
    });
    found.sort(function (x, y) { return (y.score - x.score) || (x.a.name.length - y.a.name.length) || (x.a.name < y.a.name ? -1 : 1); });
    found.slice(0, 7).forEach(function (x) {
      out.push({ kind: "area", area: x.a, text: areaLabel(x.a), small: x.a.pin });
    });

    /* An area we don't have (or a sector number that exists in more than one city):
       ask which district it is in. We never guess. */
    var hasExact = {};
    found.forEach(function (x) {
      /* "Sector 17 (GPO)" counts as an exact match for "sector 17", and so does each of its phases */
      var names = [x.a.name, x.a.hi].concat(String(x.a.also).split(","), String(x.a.alsoHi).split(","))
        .map(function (n) { return norm(String(n || "").replace(/\(.*?\)/g, " ")); });
      if (names.indexOf(q) !== -1) { hasExact[x.a.district] = true; }
    });
    var isDistrict = out.some(function (o) { return o.kind === "district" || o.kind === "pincode"; });
    var numbered = /[a-z\u0900-\u097f] \d+$/.test(q);          /* "sector 9", "phase 7" */
    if (!isDistrict && !/^\d+$/.test(q) && q.length >= 3 && order.length <= 6 && (numbered || !found.length)) {
      var rest = order.filter(function (id) { return !hasExact[id]; });
      if (rest.length) { out.push({ kind: "heading", text: T.not_listed }); }
      rest.forEach(function (id) {
        out.push({ kind: "typed", district: id, typed: raw.trim(),
                   text: fill(T.ask_district, { Q: raw.trim(), DISTRICT: districts[id].short }) });
      });
    }
    return out;
  }

  function showSuggestions() {
    var items = search(input.value);
    suggest.textContent = "";
    if (!items.length) {
      suggest.hidden = true;
      if (norm(input.value).length >= 3) { say(T.not_listed); } else { say(""); }
      return;
    }
    say("");
    items.forEach(function (item) {
      var li = el("li");
      if (item.kind === "heading") {
        li.className = "suggest__heading"; li.textContent = item.text;
      } else {
        var b = el("button", "suggest__item"); b.type = "button";
        b.appendChild(el("span", "suggest__text", item.text));
        if (item.small) { b.appendChild(el("span", "suggest__small", item.small)); }
        b.addEventListener("click", function () { pick(item); });
        li.appendChild(b);
      }
      suggest.appendChild(li);
    });
    suggest.hidden = false;
  }

  function pick(item) {
    state.pincode = null;
    if (item.kind === "area") {
      var a = item.area;
      var usable = a.centre && (a.checked || cfg.useUnchecked);
      choose({ district: a.district, point: usable ? a.centre : null, source: usable ? "area" : null, label: areaLabel(a) });
    } else if (item.kind === "pincode") {
      state.pincode = item.pincode;
      choose({ district: item.district, point: null, source: null, label: item.text });
    } else if (item.kind === "typed") {
      choose({ district: item.district, point: null, source: null, label: item.typed + ", " + districts[item.district].short });
    } else {
      choose({ district: item.district, point: null, source: null, label: districts[item.district].name });
    }
  }

  /* ---------- "Use my location" ---------- */
  var waiting = null;   /* a location we have, while we ask which district it is in */
  function nearestCentres(p, onlyTrusted) {
    return areas.filter(function (a) { return a.centre && (!onlyTrusted || a.checked || cfg.useUnchecked); })
      .map(function (a) { return { a: a, d: km(p, a.centre) }; })
      .sort(function (x, y) { return x.d - y.d; });
  }
  function located(p) {
    var trusted = nearestCentres(p, true).slice(0, 3);
    var sure = trusted.length === 3 && trusted[2].d <= 6 &&
               trusted.every(function (x) { return x.a.district === trusted[0].a.district; });
    /* Near a district border we ask instead of guessing: any listed area of another district
       within 1.5 km, checked or not, is enough to ask. */
    if (sure) {
      sure = !areas.some(function (a) { return a.centre && a.district !== trusted[0].a.district && km(p, a.centre) <= 1.5; });
    }
    if (sure) {
      choose({ district: trusted[0].a.district, point: p, source: "gps", label: T.your_location });
      return;
    }
    var any = nearestCentres(p, false)[0];
    waiting = p;
    say((any && any.d > 60) ? T.locate_far : T.locate_which);
    var target = where.querySelector(".finder__districts");
    if (target && target.scrollIntoView) { target.scrollIntoView({ block: "center" }); }
  }
  var locateBtn = $("[data-finder-locate]");
  if (locateBtn) {
    if (!("geolocation" in navigator)) {
      $("[data-finder-locate-box]").hidden = true;
    } else {
      locateBtn.addEventListener("click", function () {
        say(T.locate_wait);
        locateBtn.disabled = true;
        navigator.geolocation.getCurrentPosition(function (pos) {
          locateBtn.disabled = false;
          located([pos.coords.latitude, pos.coords.longitude]);
        }, function (err) {
          locateBtn.disabled = false;
          say(err && err.code === 1 && T.locate_denied ? T.locate_denied : T.locate_failed);
        }, { enableHighAccuracy: false, timeout: 20000, maximumAge: 60000 });
      });
    }
  }

  /* ---------- choosing a district directly ---------- */
  function districtChosen(id) {
    if (!districts[id]) { return; }
    state.pincode = null;
    if (waiting) {
      choose({ district: id, point: waiting, source: "gps", label: T.your_location + ", " + districts[id].short });
    } else {
      choose({ district: id, point: null, source: null, label: districts[id].name });
    }
  }
  Array.prototype.forEach.call(where.querySelectorAll("[data-district]"), function (b) {
    b.addEventListener("click", function () { districtChosen(b.getAttribute("data-district")); });
  });
  var select = $("[data-finder-select]");
  if (select) { select.addEventListener("change", function () { districtChosen(select.value); }); }

  /* ---------- showing the places ---------- */
  function choose(c) {
    waiting = null;
    state.district = c.district; state.point = c.point; state.source = c.source; state.label = c.label;
    where.hidden = true;
    results.hidden = false;
    suggest.hidden = true;
    say("");
    render();
    if (title.focus) { title.focus(); }
    if (results.scrollIntoView) { results.scrollIntoView({ block: "start" }); }
  }

  function render() {
    var d = districts[state.district];
    var activeNeeds = Object.keys(state.needs).filter(function (k) { return state.needs[k]; });
    var main = [], nearby = [];

    cards.forEach(function (c) {
      c.km = (state.point && c.pin) ? km(state.point, c.pin) : null;
      var wanted = !activeNeeds.length || activeNeeds.some(function (n) { return c.needs.indexOf(n) !== -1; });
      var place = null;
      if (c.district === state.district) { place = main; }
      else if (!c.wholeDistrict) {
        if (state.point) { if (c.km !== null && c.km <= cfg.nearbyKm) { place = main; } }
        else if (d.near.indexOf(c.district) !== -1) { place = nearby; }
      }
      c.el.hidden = !(place && wanted);
      if (place && wanted) { place.push(c); }
      if (c.dist) {
        if (c.km === null) { c.dist.hidden = true; c.dist.textContent = ""; }
        else {
          c.dist.hidden = false;
          c.dist.textContent = c.km < 1 ? T.under_km : fill(T.km, { N: c.km < 10 ? (Math.round(c.km * 2) / 2) : Math.round(c.km) });
        }
      }
    });

    main.sort(function (x, y) {
      var xs = x.start && x.district === state.district, ys = y.start && y.district === state.district;
      if (xs !== ys) { return xs ? -1 : 1; }
      if (x.km !== null && y.km !== null) { return x.km - y.km; }
      if ((x.km === null) !== (y.km === null)) { return x.km === null ? 1 : -1; }
      return (x.kind - y.kind) || (x.i - y.i);
    });
    nearby.sort(function (x, y) { return (x.kind - y.kind) || (order.indexOf(x.district) - order.indexOf(y.district)) || (x.i - y.i); });

    main.forEach(function (c) { list.appendChild(c.el); });
    nearby.forEach(function (c) { nearbyList.appendChild(c.el); });
    nearbyBox.hidden = !nearby.length;

    chosen.textContent = fill(state.label === d.name ? T.showing_district : T.showing, { PLACE: state.label });
    if (state.pincode && d.shared.indexOf(state.pincode) !== -1) {
      shared.hidden = false; shared.textContent = fill(T.pincode_shared, { DISTRICT: d.name });
    } else { shared.hidden = true; }

    var count = main.length === 1 ? T.count_one : fill(T.count_many, { N: main.length });
    var how = "";
    if (state.source === "gps") { how = T.sorted_gps; }
    else if (state.source === "area") { how = fill(T.sorted_area, { AREA: state.label }); }
    else if (locateBtn && !$("[data-finder-locate-box]").hidden) { how = T.sorted_district; }
    sorted.textContent = main.length ? (count + " " + how) : "";

    if (!main.length) {
      none.hidden = false;
      none.textContent = activeNeeds.length ? T.none_need : fill(T.none_here, { DISTRICT: d.name });
    } else { none.hidden = true; }
  }

  /* ---------- "What do you need?" ---------- */
  var needButtons = results.querySelectorAll("[data-need]");
  Array.prototype.forEach.call(needButtons, function (b) {
    b.addEventListener("click", function () {
      var id = b.getAttribute("data-need");
      if (!id) { state.needs = {}; } else { state.needs[id] = !state.needs[id]; }
      var any = Object.keys(state.needs).some(function (k) { return state.needs[k]; });
      Array.prototype.forEach.call(needButtons, function (x) {
        var k = x.getAttribute("data-need");
        x.setAttribute("aria-pressed", (k ? !!state.needs[k] : !any) ? "true" : "false");
      });
      render();
    });
  });

  /* ---------- "Change" ---------- */
  $("[data-finder-change]").addEventListener("click", function () {
    results.hidden = true;
    where.hidden = false;
    input.value = "";
    suggest.hidden = true;
    say("");
    input.focus();
  });

  /* ---------- start ---------- */
  input.addEventListener("input", showSuggestions);
  input.addEventListener("keydown", function (event) {
    if (event.key !== "Enter") { return; }
    var first = suggest.hidden ? null : suggest.querySelector("button");
    if (first) { first.click(); }
  });
  staticBox.hidden = true;     /* the plain district-by-district list is only for when this script cannot run */
  where.hidden = false;
})();
