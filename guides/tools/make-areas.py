#!/usr/bin/env python3
"""
Builds _data/areas.yml (the list of areas people can type on "Find help near you")
from India Post's pincode directory.

WHERE THE DATA COMES FROM
  India Post's official pincode directory, as packaged in the Python library
  "indiapins" (MIT licence, data dated February 2026). Each row is one post office:
  its name, pincode, district, state and a map point.

WHAT TO KNOW
  - Pincode -> district is reliable.
  - The map points are NOT reliable. Many are placeholders or plainly wrong.
    This script throws away the obvious bad ones and marks every remaining one
    "checked: false". The website does not use an unchecked point to work out
    distances. See guides/DIRECTORY.md.
  - Areas you have already marked "checked: true" are kept exactly as they are.

HOW TO RUN (ask Claude, or on a computer with Python):
  pip download indiapins --no-deps -d /tmp/pins && cd /tmp/pins && unzip -o indiapins-*.whl
  python3 guides/tools/make-areas.py /tmp/pins/indiapins/pins.json.bz2

TO ADD A DISTRICT: add it to DISTRICTS below, run again, then add its places
to _data/directory.yml.
"""
import bz2, json, math, re, sys, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "_data", "areas.yml")

# id: the short name used in directory.yml.  post: the district name(s) India Post uses.
DISTRICTS = [
    dict(id="chandigarh", post=["CHANDIGARH"], en="Chandigarh", hi="चंडीगढ़", short="Chandigarh", short_hi="चंडीगढ़",
         state_en="Chandigarh (Union Territory)", state_hi="चंडीगढ़ (केंद्र शासित प्रदेश)",
         also=["chd", "ut"], near=["mohali", "panchkula"]),
    dict(id="mohali", post=["S.A.S Nagar"], en="Mohali (SAS Nagar)", hi="मोहाली (एसएएस नगर)", short="Mohali", short_hi="मोहाली",
         state_en="Punjab", state_hi="पंजाब",
         also=["sas nagar", "sahibzada ajit singh nagar", "ajitgarh", "एसएएस नगर"], near=["chandigarh", "panchkula"]),
    dict(id="panchkula", post=["PANCHKULA"], en="Panchkula", hi="पंचकूला", short="Panchkula", short_hi="पंचकूला",
         state_en="Haryana", state_hi="हरियाणा",
         also=["pkl"], near=["chandigarh", "mohali"]),
]

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

def km(a, b):
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1]); dp = p2 - p1
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

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
    m = re.fullmatch(r"Sector (\d+)( \(GPO\))?", name)
    if m:
        return "सेक्टर %s%s" % (m.group(1), " (जीपीओ)" if m.group(2) else "")
    return HINDI.get(name, "")

def main(path):
    rows = [json.loads(l) for l in bz2.open(path, "rt") if l.strip()]
    kept = {}
    if os.path.exists(OUT):
        try:
            import yaml
            old = yaml.safe_load(open(OUT, encoding="utf-8")) or {}
            for a in old.get("areas", []):
                if a.get("checked") is True:
                    kept[(a["district"], a["name"])] = a
        except Exception as e:
            print("Could not read the existing areas.yml, starting fresh:", e)

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
        mid = (sorted(p[0] for p in good)[len(good) // 2], sorted(p[1] for p in good)[len(good) // 2])
        done = set()
        for r in sorted(rs, key=lambda r: (r["BranchType"] == "BO", str(r["Pincode"]), r["Name"])):
            name = clean_name(r["Name"].strip(), d)
            if not name or (name.lower()) in done:
                continue
            done.add(name.lower())
            key = (d["id"], name)
            if key in kept:
                areas.append(kept[key]); continue
            p = None
            try:
                p = (round(float(r["Latitude"]), 4), round(float(r["Longitude"]), 4))
            except Exception:
                pass
            if p and (seen[p] > 1 or km(p, mid) > 40):
                p = None            # placeholder shared by several offices, or far outside the district
            areas.append(dict(name=name, name_hi=hindi_name(name), district=d["id"], pincode=str(r["Pincode"]),
                              centre=("%.4f, %.4f" % p) if p else "", checked=False))

    def q(s): return '"' + str(s).replace('"', '\\"') + '"'
    out = []
    out.append("""# ─────────────────────────────────────────────────────────────
#  AREAS: what people can type on "Find help near you"
#
#  Made by guides/tools/make-areas.py from India Post's pincode directory
#  (data dated February 2026). Area names are post office names, tidied up.
#
#  centre  = a rough map point for the area: "latitude, longitude".
#  checked = false means NOBODY HAS CHECKED THAT POINT. India Post's points are
#            often wrong. While checked is false, the website uses the area only
#            to work out the district, and never shows a distance from it.
#            To check one: see "Checking an area's map point" in guides/DIRECTORY.md,
#            correct the two numbers if needed, then change false to true.
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
        for a in [a for a in areas if a["district"] == d["id"]]:
            out.append("  - { name: %s, name_hi: %s, district: %s, pincode: %s, centre: %s, checked: %s }" % (
                q(a["name"]), q(a.get("name_hi") or ""), a["district"], q(a["pincode"]), q(a.get("centre") or ""),
                "true" if a.get("checked") is True else "false"))
    open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("Wrote", os.path.normpath(OUT), "with", len(areas), "areas;",
          sum(1 for a in areas if a.get("centre")), "have a map point (all unchecked unless you checked them).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
