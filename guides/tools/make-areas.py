#!/usr/bin/env python3
"""
Builds _data/areas.yml (the list of areas people can type on "Find help near you").

WHERE THE DATA COMES FROM
  1. India Post's official pincode directory, as packaged in the Python library
     "indiapins" (MIT licence, data dated February 2026). Each row is one post office:
     its name, pincode, district, state and a map point. This gives most area names,
     and the district of each.
  2. Optional: OpenStreetMap (openstreetmap.org, (c) OpenStreetMap contributors,
     Open Database License). It has the middle of every sector in Chandigarh, Mohali
     and Panchkula, and most villages. How to get the file: see OPENSTREETMAP below.
  3. Optional: GeoNames (geonames.org, CC BY 4.0): villages and towns with map points.
     Download https://download.geonames.org/export/dump/IN.zip and unzip it.
  4. guides/tools/extra-areas.yml: a few areas from Wikidata (CC0).
  5. PHASES below: which Mohali phase is in which sector.
  6. Villages India Post does not list, when OpenStreetMap and GeoNames both have the
     village within 2 km of each other, and GeoNames puts at least 4 of its 5 nearest
     neighbouring places in the same district (so border villages are left out).

WHAT TO KNOW
  - Pincode -> district is reliable.
  - India Post's map points are NOT reliable. Many are placeholders or plainly wrong.
    The obvious bad ones are thrown away.
  - An area comes out "checked: true" only when two or more sources agree on its map
    point: within 1 km for a sector, 2 km for anything else. Ayesha decided on
    18 Nov 2026 that this counts as checked (AUTO_CHECK below). Everything else comes
    out "checked: false", and the website does not use its point to work out distances.
    See guides/DIRECTORY.md.
  - Areas already marked "checked: true" are kept exactly as they are.
  - "note" flags an area whose district may be wrong: another district has a place with
    the same name close by.

HOW THE MAP POINT ("centre") IS CHOSEN
  - A sector: OpenStreetMap's middle of the sector, if it has one. (India Post's point
    is a post office somewhere in the sector, at best.)
  - Anything else: India Post's point, else Wikidata's, else GeoNames', else
    OpenStreetMap's. But if India Post's point is more than 2 km from both GeoNames and
    OpenStreetMap, and those two agree, India Post's point is taken to be wrong and
    OpenStreetMap's is used.
  - Every other source's point goes in "second", with how far it is from the one used.

OPENSTREETMAP
  Its servers could not be reached from Claude's workspace, so the file is made by hand:
  open https://overpass-turbo.eu, paste this query, press Run, then Export, then
  "raw OSM data". If the download does not work, copy the text and paste it to Claude.

    [out:json][timeout:120];
    (
      nwr["place"~"^(suburb|neighbourhood|quarter|village|hamlet|town|city|locality)$"](30.35,76.45,30.95,77.15);
      nwr["name"~"^(Sector|Phase) ?[0-9]",i](30.35,76.45,30.95,77.15);
      nwr["amenity"~"^(hospital|police|courthouse)$"](30.35,76.45,30.95,77.15);
    );
    out center tags;

  Licence: the Open Database License (ODbL). The page must credit
  "(c) OpenStreetMap contributors", and _data/areas.yml, which then contains
  OpenStreetMap data, is shared under the same licence. Both are already done.

HOW TO RUN (ask Claude, or on a computer with Python 3 and PyYAML):
  pip download indiapins --no-deps -d /tmp/pins && cd /tmp/pins && unzip -o indiapins-*.whl
  python3 guides/tools/make-areas.py /tmp/pins/indiapins/pins.json.bz2 [IN.txt] [export.json]
  The GeoNames file (.txt) and the OpenStreetMap file (.json) can come in either order,
  and either can be left out.

TO ADD A DISTRICT: add it to DISTRICTS below, run again, then add its places
to _data/directory.yml. Sector numbering is worked out by sector_district() below,
which only knows the Chandigarh, Mohali and Panchkula grid: extend it for a new city.
"""
import bz2, json, math, re, sys, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "_data", "areas.yml")

# id: the short name used in directory.yml.  post: the district name(s) India Post uses.
DISTRICTS = [
    dict(id="chandigarh", post=["CHANDIGARH"], geonames=("05", "055"), en="Chandigarh", hi="चंडीगढ़", short="Chandigarh", short_hi="चंडीगढ़",
         state_en="Chandigarh (Union Territory)", state_hi="चंडीगढ़ (केंद्र शासित प्रदेश)",
         also=["chd", "ut"], near=["mohali", "panchkula"]),
    dict(id="mohali", post=["S.A.S Nagar"], geonames=("23", "052"), en="Mohali (SAS Nagar)", hi="मोहाली (एसएएस नगर)", short="Mohali", short_hi="मोहाली",
         state_en="Punjab", state_hi="पंजाब",
         also=["sas nagar", "sahibzada ajit singh nagar", "ajitgarh", "एसएएस नगर"], near=["chandigarh", "panchkula"]),
    dict(id="panchkula", post=["PANCHKULA"], geonames=("10", "069"), en="Panchkula", hi="पंचकूला", short="Panchkula", short_hi="पंचकूला",
         state_en="Haryana", state_hi="हरियाणा",
         also=["pkl"], near=["chandigarh", "mohali"]),
]

# Mohali's phases and the sector each is in. The website shows the phase next to the
# sector ("Sector 61 (Phase 7)"), so typing either finds it.
#   Phases 1, 3A, 3B-2, 6, 7, 9: addresses in OpenStreetMap that name both (17 Nov 2026).
#   Phases 2, 3B-1, 4, 5, 8, 10, 11: Ayesha's check (18 Nov 2026), each also found in
#   India Post locality names or property listings. Phase 2 is Sector 54, not 56: the
#   district's own website puts the Civil Hospital at "Phase 6, Sector 56".
AUTO_CHECK = True     # two or more sources that agree count as checked (Ayesha, 18 Nov 2026)
PHASES = {
    "mohali": [("Sector 55", "Phase 1"), ("Sector 54", "Phase 2"), ("Sector 53", "Phase 3A"),
               ("Sector 60", "Phase 3B-1"), ("Sector 60", "Phase 3B-2"), ("Sector 59", "Phase 4"),
               ("Sector 59", "Phase 5"), ("Sector 56", "Phase 6"), ("Sector 61", "Phase 7"),
               ("Sector 62", "Phase 8"), ("Sector 63", "Phase 9"), ("Sector 64", "Phase 10"),
               ("Sector 65", "Phase 11")],
}

# Post office names that need a hand-written area name. None = leave it out.
RENAME = {
    "Chandigarh GPO": "Sector 17 (GPO)",
    "New Sectt Chandigarh SO": "New Secretariat",
    "High Court SO Chandigarh": "High Court",
    "Vidhansadan SO": None, "NDC Chandigarh": None, "Engg College SO": None, "Aerodrome SO": None,
    "Raj Bhawan SO Chandigarh": None, "TCKharar BO": None, "Kalka R.S. S.O": None, "Dappar Ad SO": None,
    "G.K. Panchkula S.O": None, "Sunny Enclave S.O.": "Sunny Enclave",
    "Ind Area Chandigarh SO": "Industrial Area", "Industrial Estate  Panchkula S.O": "Industrial Area",
    "Airforce Highground SO": "Air Force Station, High Grounds",
    "Mhc Manimajra SO": "Modern Housing Complex, Manimajra",
    "Mansa  Devi Sec 5 S.O": "Mansa Devi Complex, Sector 5",
    "B.C.W. Suraj Pur S.O": "Surajpur", "H.M.T.Pinjore S.O": "HMT, Pinjore",
    "I.T.B.P.  Bhanu S.O": "ITBP Bhanu", "C.R.P.F. Pinjore S.O": "CRPF, Pinjore",
    "Chandi Mandir Cantt S.O": "Chandi Mandir Cantonment", "Dadu Majra Colony SO": "Dadu Majra",
    "Maloya Colony SO": "Maloya", "Amravati  Enclave SO": "Amravati Enclave",
    "Khizrabad West SO": "Khizrabad", "Derabassi SO": "Dera Bassi", "Naya Gaon SO Mohali": "Naya Gaon",
    "Mubarakpur SO Patiala": "Mubarakpur", "Kharar SO Rupnagar": "Kharar", "Barwala S.O (Panchkula)": "Barwala",
    "Aerocity S.O": "Aerocity", "Dhakaoli SO": "Dhakoli",
}

# Hindi spellings for well-known places only. Everything else stays in English letters.
HINDI = {
    "Manimajra": "मनीमाजरा", "Zirakpur": "ज़ीरकपुर", "Kharar": "खरड़", "Dera Bassi": "डेराबस्सी", "Kurali": "कुराली",
    "Lalru": "लालड़ू", "Banur": "बनूड़", "Pinjore": "पिंजौर", "Kalka": "कालका", "Baltana": "बलटाना",
    "Mullanpur": "मुल्लांपुर", "Naya Gaon": "नयागांव", "Sohana": "सोहाना", "Landran": "लांडरां", "Burail": "बुड़ैल",
    "Dhanas": "धनास", "Maloya": "मलोया", "Barwala": "बरवाला", "Raipur Rani": "रायपुर रानी", "Morni": "मोरनी",
    "Balongi": "बलौंगी", "Hallomajra": "हल्लोमाजरा", "Ram Darbar": "राम दरबार", "Mauli Jagran": "मौली जागरां",
    "Kishangarh": "किशनगढ़", "Chandi Mandir": "चंडी मंदिर", "Dhakoli": "ढकोली", "Industrial Area": "इंडस्ट्रियल एरिया",
    "High Court": "हाई कोर्ट", "Aerocity": "एरोसिटी", "Surajpur": "सूरजपुर", "Dadu Majra": "डड्डूमाजरा",
}
LETTER_HI = {"A": "ए", "B": "बी", "C": "सी", "D": "डी", "E": "ई"}

SECTOR_RE = re.compile(r"^Sector[\s-]*(\d+)([A-Z])?(?:\s+(West|East))?(?:\s+(.+))?$")


def km(a, b):
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1]); dp = p2 - p1
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def point(text):
    try:
        lat, lng = (float(v) for v in str(text).split(","))
        return (round(lat, 4), round(lng, 4))
    except Exception:
        return None

def show(p):
    return "%.4f, %.4f" % p

def clean_name(raw, d):
    if raw in RENAME:
        return RENAME[raw]
    m = re.search(r"\bSec(?:tor)?\s*(\d+)", raw, re.I)
    if m:
        return "Sector %d" % int(m.group(1))
    s = re.sub(r"\(.*?\)", " ", raw)
    s = re.sub(r"\b[SBH]\.?\s?O\b\.?", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" .,")
    for tail in (d["short"], "Chandigarh", "Patiala", "Rupnagar"):
        if s.lower().endswith(" " + tail.lower()):
            s = s[: -len(tail)].strip(" ,")
    return s or None

def hindi_name(name):
    m = re.fullmatch(r"Sector (\d+)([A-E])?(?: (West|East))?( \(GPO\))?", name or "")
    if m:
        return "सेक्टर %s%s%s%s" % (m.group(1), LETTER_HI.get(m.group(2) or "", ""),
                                  {"West": " वेस्ट", "East": " ईस्ट"}.get(m.group(3) or "", ""),
                                  " (जीपीओ)" if m.group(4) else "")
    m = re.fullmatch(r"Phase (\d+)([A-E])?(?:-(\d))?", name or "")
    if m:
        return "फेज़ %s%s%s" % (m.group(1), LETTER_HI.get(m.group(2) or "", ""), ("-" + m.group(3)) if m.group(3) else "")
    return HINDI.get(name, "")

def norm(s):
    s = re.sub(r"[^a-z0-9 ]+", " ", str(s).lower())
    return re.sub(r"\s+", " ", s).strip()

def squash(s):
    """Loose key for spelling variants: 'Naya Gaon' = 'Nayagaon', 'Mullanpur' = 'Mulanpur'."""
    return re.sub(r"(.)\1+", r"\1", norm(s).replace(" ", ""))

def sector_key(name):
    """'Sector 17 (GPO)' -> 'Sector 17'. None if the name is not a sector."""
    m = re.match(r"^Sector (\d+[A-Z]?(?: West| East)?)\b", name or "")
    return ("Sector " + m.group(1)) if m else None

def spread(points):
    return max((km(points[0], p) for p in points), default=0)


def sector_district(num, kind, lat, lng):
    """Which district a sector of the Chandigarh-Mohali-Panchkula grid is in.
    Chandigarh's sectors run 1 to 56 plus 61 and 63; Mohali's run 53 to 127;
    Panchkula's are the ones east of the Ghaggar. Sectors 53 to 56, 61 and 63 are cut
    by the Chandigarh-Mohali border, so they exist in both: OpenStreetMap draws the
    Chandigarh part as a boundary, and marks the Mohali part with a point."""
    if not (30.60 <= lat <= 30.80 and 76.60 <= lng <= 76.95):
        return None                      # Ambala, Parwanoo and others: not ours
    if lng >= 76.825:
        return "panchkula"
    if num <= 52:
        return "chandigarh"
    if num in (53, 54, 55, 56, 61, 63):
        return "chandigarh" if kind == "boundary" else "mohali"
    return "mohali"


def load_osm(path):
    """Sectors (district -> name -> best point) and other named places from an Overpass export."""
    data = json.load(open(path, encoding="utf-8"))
    rank = {"boundary": 0, "place": 1, "landuse": 2}
    sectors = collections.defaultdict(dict)       # district -> name -> dict(point, kind, id, also)
    places = collections.defaultdict(list)        # squash(name) -> [(point, id)]
    names = collections.defaultdict(list)         # id -> the names it goes by
    for e in data.get("elements", []):
        t = e.get("tags", {})
        name = (t.get("name:en") or t.get("name") or "").strip()
        if "lat" in e:
            p = (round(e["lat"], 4), round(e["lon"], 4))
        elif e.get("center"):
            p = (round(e["center"]["lat"], 4), round(e["center"]["lon"], 4))
        else:
            continue
        oid = "%s/%s" % (e["type"], e["id"])
        m = SECTOR_RE.match(name)
        if m:
            if t.get("boundary") == "administrative":
                kind = "boundary"
            elif t.get("place"):
                kind = "place"
            elif t.get("landuse") in ("residential", "industrial", "commercial") and not m.group(4):
                kind = "landuse"
            else:
                continue                             # markets, roads, parks, substations...
            num, letter, side, extra = int(m.group(1)), m.group(2) or "", m.group(3), m.group(4)
            district = sector_district(num, kind, *p)
            if not district:
                continue
            sname = "Sector %d%s%s" % (num, letter, (" " + side) if side else "")
            old = sectors[district].get(sname)
            if old is None or rank[kind] < rank[old["kind"]]:
                sectors[district][sname] = dict(point=p, kind=kind, id=oid, also=(old or {}).get("also") or extra or "")
            elif extra and not old.get("also"):
                old["also"] = extra
            continue
        if t.get("place") in ("suburb", "neighbourhood", "quarter", "village", "hamlet", "town", "city", "locality") and name:
            for n in [name, t.get("name", "")] + re.split(r";", t.get("alt_name", "")):
                if n and not re.match(r"(?i)^(sector|phase)\b", n) and n not in names[oid]:
                    places[squash(n)].append((p, oid))
                    names[oid].append(n)
    # A lettered sector drawn only as land use ("Sector 20A") is part of the numbered one.
    for district, byname in sectors.items():
        for sname in list(byname):
            m = re.fullmatch(r"Sector (\d+)[A-Z]", sname)
            if m and byname[sname]["kind"] == "landuse" and ("Sector " + m.group(1)) in byname:
                del byname[sname]
    return sectors, places, names


def load_geonames(path):
    """GeoNames rows for our districts, indexed by name. Columns: see geonames.org readme."""
    want = {d["geonames"]: d["id"] for d in DISTRICTS}
    index = collections.defaultdict(list)
    for line in open(path, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 12 or p[6] != "P":          # populated places only (towns, villages, neighbourhoods)
            continue
        district = want.get((p[10], p[11]))
        if not district:
            continue
        pt = (round(float(p[4]), 4), round(float(p[5]), 4))
        names = {norm(p[1]), norm(p[2])} | {norm(a) for a in p[3].split(",") if re.search("[A-Za-z]", a)}
        for n in names:
            if n:
                index[(district, n)].append(pt)
    return index


def load_geonames_nearby(path):
    """Every populated place in and around our districts, with its district id, or None
    for a district the site does not cover. Used to leave out villages near a border."""
    want = {d["geonames"]: d["id"] for d in DISTRICTS}
    out = []
    for line in open(path, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 12 or p[6] != "P":
            continue
        lat, lng = float(p[4]), float(p[5])
        if 30.25 <= lat <= 31.05 and 76.30 <= lng <= 77.30:
            out.append(((lat, lng), want.get((p[10], p[11]))))
    return out


def tidy(name):
    """'SABILPAR KALA' -> 'Sabilpar Kala'."""
    return name.title() if name.isupper() else name


def main(pins_path, geonames_path=None, osm_path=None):
    rows = [json.loads(l) for l in bz2.open(pins_path, "rt") if l.strip()]
    kept = {}
    if os.path.exists(OUT):
        try:
            import yaml
            old = yaml.safe_load(open(OUT, encoding="utf-8")) or {}
            for a in old.get("areas", []):
                if a.get("checked") is True:
                    if "from" in a:
                        a["centre_from"] = a.pop("from")
                    kept[(a["district"], a["name"])] = a
        except Exception as e:
            print("Could not read the existing areas.yml, starting fresh:", e)

    # 1. India Post: names, districts, pincodes, and its map points where they look possible
    areas = []
    by_pin = collections.defaultdict(set)
    for r in rows:
        by_pin[str(r["Pincode"])].add(r["District"])
    ours = set(n for d in DISTRICTS for n in d["post"])
    for d in DISTRICTS:
        rs = [r for r in rows if r["District"] in d["post"]]
        d["pins"] = sorted(set(str(r["Pincode"]) for r in rs))
        d["shared"] = sorted(p for p in d["pins"] if any(x and x not in ours for x in by_pin[p]))
        pts = [(round(float(r["Latitude"]), 4), round(float(r["Longitude"]), 4)) for r in rs
               if isinstance(r["Latitude"], (int, float)) and isinstance(r["Longitude"], (int, float))]
        seen = collections.Counter(pts)
        good = sorted(p for p in pts if seen[p] == 1)
        d["mid"] = (sorted(p[0] for p in good)[len(good) // 2], sorted(p[1] for p in good)[len(good) // 2])
        done = set()
        for r in sorted(rs, key=lambda r: (r["BranchType"] == "BO", str(r["Pincode"]), r["Name"])):
            name = clean_name(r["Name"].strip(), d)
            if not name or (name.lower()) in done:
                continue
            done.add(name.lower())
            key = (d["id"], name)
            if key in kept:
                areas.append(kept.pop(key)); continue
            p = None
            try:
                p = (round(float(r["Latitude"]), 4), round(float(r["Longitude"]), 4))
            except Exception:
                pass
            if p and (seen[p] > 1 or km(p, d["mid"]) > 40):
                p = None            # placeholder shared by several offices, or far outside the district
            areas.append(dict(name=name, name_hi=hindi_name(name), district=d["id"], pincode=str(r["Pincode"]),
                              pts=[("India Post", p)] if p else [], checked=False))
    mids = {d["id"]: d["mid"] for d in DISTRICTS}
    areas.extend(kept.values())      # checked areas that did not come from India Post (sectors, villages)

    def find(district, name):
        return [a for a in areas if a["district"] == district and norm(a["name"]) == norm(name)]

    # 2. Wikidata extras
    extra_path = os.path.join(HERE, "extra-areas.yml")
    if os.path.exists(extra_path):
        import yaml
        for x in yaml.safe_load(open(extra_path, encoding="utf-8")) or []:
            same = find(x["district"], x["name"])
            if same and same[0].get("checked") is True:
                continue
            if same:
                same[0]["pts"].append((x["source"], point(x["centre"])))
            else:
                areas.append(dict(name=x["name"], name_hi=hindi_name(x["name"]), district=x["district"], pincode="",
                                  pts=[(x["source"], point(x["centre"]))], checked=False))

    # 3. OpenStreetMap: every sector it knows, added if missing
    osm_sectors, osm_places, osm_names, new_sectors = {}, {}, {}, 0
    if osm_path:
        osm_sectors, osm_places, osm_names = load_osm(osm_path)
        for district, byname in osm_sectors.items():
            have = {sector_key(a["name"]) for a in areas if a["district"] == district}
            for sname, s in byname.items():
                if sname not in have:
                    areas.append(dict(name=sname, name_hi=hindi_name(sname), district=district, pincode="",
                                      pts=[], checked=False, also=s["also"], also_hi=hindi_name(s["also"])))
                    new_sectors += 1
                else:
                    for a in areas:
                        if a["district"] == district and sector_key(a["name"]) == sname and s["also"] and not a.get("also"):
                            a["also"], a["also_hi"] = s["also"], hindi_name(s["also"])

    # 4. Mohali phases: show the phase with its sector, and fold a separate "Phase N" area into it
    linked = merged = 0
    for district, links in PHASES.items():
        grouped = collections.OrderedDict()
        for sname, phase in links:
            grouped.setdefault(sname, []).append(phase)
        for sname, phases in grouped.items():
            sec = [a for a in areas if a["district"] == district and sector_key(a["name"]) == sname]
            if not sec:
                print("Note: %s is not in the list, so %s could not be linked to it." % (sname, ", ".join(phases)))
                continue
            s = sec[0]
            s["also"] = ", ".join(phases)
            s["also_hi"] = ", ".join(hindi_name(p) for p in phases)
            linked += len(phases)
            for a in [a for phase in phases for a in find(district, phase)]:
                phase = a["name"]
                if a is not s and a.get("checked") is not True:
                    s.setdefault("pts", []).extend((label + " (as " + phase + ")", p) for label, p in a.get("pts", []))
                    areas.remove(a)
                    merged += 1

    # 5. Villages India Post does not list: OpenStreetMap and GeoNames agree on where
    #    they are, and GeoNames' neighbouring places are in the same district
    gn = load_geonames(geonames_path) if geonames_path else {}
    villages = 0
    if gn and osm_places:
        nearby = load_geonames_nearby(geonames_path)
        gn_sq = collections.defaultdict(list)
        for (district, n), pts in gn.items():
            gn_sq[(district, squash(n))].extend(pts)
        have = {(a["district"], squash(a["name"])) for a in areas}
        skip = {squash(d[k]) for d in DISTRICTS for k in ("en", "short")} | {squash(x) for d in DISTRICTS for x in d["also"]}
        for key, found in sorted(osm_places.items()):
            if key in skip:
                continue
            for d in DISTRICTS:
                g = gn_sq.get((d["id"], key), [])
                if (d["id"], key) in have or not g or spread(g) > 3:
                    continue
                close = [(p, oid) for p, oid in found if km(p, g[0]) <= 2]
                if not close:
                    continue
                o = close[0][0]
                neighbours = sorted(nearby, key=lambda x: km(x[0], o))[1:6]
                if sum(1 for _, nd in neighbours if nd == d["id"]) < 4:
                    continue          # near a district border: leave it out rather than risk the wrong district
                name = tidy(next((n for n in osm_names.get(close[0][1], []) if squash(n) == key), key))
                areas.append(dict(name=name, name_hi=hindi_name(name), district=d["id"], pincode="", checked=False,
                                  pts=[("GeoNames", (round(g[0][0], 4), round(g[0][1], 4))), ("OpenStreetMap", o)], given=True))
                have.add((d["id"], key))
                villages += 1

    # 6. Choose each map point, and note the other sources
    stats = collections.Counter()
    switched = []
    for a in areas:
        if a.get("checked") is True:
            continue
        pts = [(label, p) for label, p in a.pop("pts", []) if p]
        given = a.pop("given", False)
        is_sector = sector_key(a["name"]) is not None
        ref = pts[0][1] if pts else None
        # GeoNames
        g = None
        cands = gn.get((a["district"], norm(a["name"])), []) if not (is_sector or given or a["name"].startswith("Phase")) else []
        if cands:
            if ref:
                g = min(cands, key=lambda p: km(ref, p))
            elif spread(cands) <= 3:
                g = cands[0]
        # OpenStreetMap
        o = None
        if is_sector:
            s = osm_sectors.get(a["district"], {}).get(sector_key(a["name"]))
            o = s["point"] if s else None
        elif osm_places and not given:
            cands = [p for p, _ in osm_places.get(squash(a["name"]), [])]
            r = g or ref        # GeoNames first: its points are already sorted by district
            if cands and r:
                best = min(cands, key=lambda p: km(r, p))
                o = best if km(r, best) <= 3 else None     # further away is usually another village of the same name
            elif cands:
                near = [p for p in cands if km(p, mids[a["district"]]) <= 20]
                o = near[0] if near and spread(near) <= 3 else None
        if g:
            pts.append(("GeoNames", g))
        if o:
            pts.append(("OpenStreetMap", o))
        if not pts:
            a["centre"] = ""
            continue
        if is_sector and o:
            centre = ("OpenStreetMap", o)
        else:
            centre = pts[0]
            if centre[0] not in ("GeoNames", "OpenStreetMap") and g and o and km(g, o) <= 2 \
                    and km(centre[1], g) > 2 and km(centre[1], o) > 2:
                switched.append("%s (%s): %s was %.0f km off" % (a["name"], a["district"], centre[0], km(centre[1], o)))
                centre = ("OpenStreetMap", o)
        a["centre"] = show(centre[1])
        if centre[0] != "India Post":
            a["centre_from"] = centre[0]
        others = [(label, p) for label, p in pts if (label, p) != centre]
        if others:
            a["second"] = "; ".join("%s %s (%.1f km away)" % (label, show(p), km(centre[1], p)) for label, p in others)
        limit = 1.0 if is_sector else 2.0
        if not is_sector and gn:
            for d in DISTRICTS:
                if d["id"] != a["district"]:
                    near = [p for p in gn.get((d["id"], norm(a["name"])), []) if km(p, centre[1]) <= 3]
                    if near:
                        a["note"] = "GeoNames puts a place called %s %.1f km from here in %s. Check which district it is in." % (
                            a["name"], km(near[0], centre[1]), d["short"])
                        stats["notes"] += 1
        if others and all(km(centre[1], p) <= limit for _, p in others):
            stats["agree_sector" if is_sector else "agree_other"] += 1
            if AUTO_CHECK and "note" not in a:
                a["checked"] = True
                stats["auto_checked"] += 1
        elif others:
            stats["disagree"] += 1
        else:
            stats["one_source"] += 1
        if centre[0] == "OpenStreetMap":
            stats["from_osm"] += 1

    # 6. Write the file
    def q(s): return '"' + str(s).replace('"', '\\"') + '"'
    def order(a):
        m = re.match(r"^Sector (\d+)", a["name"])
        return (0, int(m.group(1)), a["name"]) if m else (1, 0, a["name"].lower())
    out = []
    out.append("""# ─────────────────────────────────────────────────────────────
#  AREAS: what people can type on "Find help near you"
#
#  Made by guides/tools/make-areas.py. Area names and districts come from India Post's
#  pincode directory (February 2026), plus sectors from OpenStreetMap and a few areas
#  from Wikidata. Map points also come from GeoNames.
#
#  LICENCE: this file contains data from OpenStreetMap, (c) OpenStreetMap contributors,
#  and is available under the Open Database License (ODbL 1.0):
#  https://opendatacommons.org/licenses/odbl/1-0/  It also uses India Post's directory
#  (Open Government Data Licence, India), GeoNames (CC BY 4.0) and Wikidata (CC0).
#
#  centre  = a rough map point for the middle of the area: "latitude, longitude".
#  from    = where that point came from, if not India Post.
#  second  = other sources' points for the same place, and how far each is from "centre".
#            Points within about 1 km (sectors) or 2 km (villages and towns) of each other
#            are probably right. Far apart means one of them is wrong.
#  also    = another name for the same area, shown in brackets: Mohali's phases.
#  note    = this area's district may be wrong: check it.
#  checked = true when someone checked the point on a map, OR two sources agree on it
#            (within 1 km for a sector, 2 km for anything else: Ayesha's decision,
#            18 Nov 2026). Only checked points are used for distances.
#            checked: false means NOBODY HAS CHECKED THAT POINT. The website then uses the
#            area only to work out the district. To check one: see "Check an area's map
#            point" in guides/DIRECTORY.md, correct the two numbers if needed, then change
#            false to true.
#
#  You can add an area by hand: copy a line, change it, and keep the same shape.
#  A missing area is not a problem: people can still type a pincode or pick a district.
# ─────────────────────────────────────────────────────────────

districts:""")
    for d in DISTRICTS:
        out.append("  - id: %s" % d["id"])
        out.append("    name: { en: %s, hi: %s }" % (q(d["en"]), q(d["hi"])))
        out.append("    short: { en: %s, hi: %s }" % (q(d["short"]), q(d["short_hi"])))
        out.append("    state: { en: %s, hi: %s }" % (q(d["state_en"]), q(d["state_hi"])))
        out.append("    also_called: [%s]      # other names people may type" % ", ".join(q(a) for a in d["also"]))
        out.append("    near: [%s]             # neighbouring districts already on the site" % ", ".join(d["near"]))
        out.append("    pincodes: [%s]" % ", ".join(q(x) for x in d["pins"]))
        out.append("    pincodes_shared: [%s]      # these also cover places outside this district" % ", ".join(q(x) for x in d["shared"]))
    out.append("\nareas:")
    for d in DISTRICTS:
        out.append("  # ── %s ──" % d["en"].upper())
        for a in sorted([a for a in areas if a["district"] == d["id"]], key=order):
            extra = ""
            if a.get("also"):
                extra += ", also: %s, also_hi: %s" % (q(a["also"]), q(a.get("also_hi") or ""))
            if a.get("centre_from"):
                extra += ", from: %s" % q(a["centre_from"])
            if a.get("second"):
                extra += ", second: %s" % q(a["second"])
            if a.get("note"):
                extra += ", note: %s" % q(a["note"])
            out.append("  - { name: %s, name_hi: %s, district: %s, pincode: %s, centre: %s%s, checked: %s }" % (
                q(a["name"]), q(a.get("name_hi") or ""), a["district"], q(a.get("pincode") or ""), q(a.get("centre") or ""),
                extra, "true" if a.get("checked") is True else "false"))
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")

    print("Wrote", os.path.normpath(OUT), "with", len(areas), "areas;",
          sum(1 for a in areas if a.get("centre")), "have a map point;",
          sum(1 for a in areas if a.get("checked") is True), "are checked.")
    if osm_path:
        print("OpenStreetMap: %d sectors added that India Post does not list; %d map points now come from it." % (new_sectors, stats["from_osm"]))
    print("Phases linked to sectors: %d (separate phase areas folded in: %d)." % (linked, merged))
    print("Villages added (OpenStreetMap and GeoNames agree, not near a border): %d." % villages)
    print("Marked checked because two or more sources agree: %d. District notes: %d." % (stats["auto_checked"], stats["notes"]))
    print("Two or more sources agree: %d sectors (within 1 km), %d other areas (within 2 km). They disagree: %d. Only one source: %d."
          % (stats["agree_sector"], stats["agree_other"], stats["disagree"], stats["one_source"]))
    for s in switched:
        print("  India Post's point replaced, GeoNames and OpenStreetMap agree: " + s)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not 1 <= len(args) <= 3:
        sys.exit(__doc__)
    txt = next((a for a in args[1:] if a.lower().endswith(".txt")), None)
    js = next((a for a in args[1:] if a.lower().endswith(".json")), None)
    main(args[0], txt, js)
