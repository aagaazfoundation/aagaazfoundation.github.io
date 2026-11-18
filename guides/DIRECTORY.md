# "Find help near you": how it works and how to run it

Built 17 November 2026. **The page is switched off.** It goes live only when you change one line (step 5 below), and you should not do that until you have verified places to show.

## What visitors will see

1. **Where are you?** They type a sector, area or pincode, or tap "Use my location", or pick a district.
2. **What do you need?** Medical care, police, free legal help, counselling and support, a safe place to stay, help for a child. All are selected to begin with.
3. **Places that can help.** The district's One Stop Centre comes first, then the nearest places. Each shows what kind of place it is, whether it is government, private or an NGO, the address, a tap-to-call number, the hours and the date you last checked it.

Without JavaScript the page still works: it lists every place, district by district.

## What stays private

- What someone types, the district they pick and their location never leave their phone. The page does all the matching itself.
- Nothing is saved: no cookies, no storage, nothing added to the web address.
- No maps and no outside services are loaded.
- One thing the page cannot control: if someone taps "Use my location" and allows it, their browser may remember that this site was allowed. The page says so under the button and tells people who are worried to type their area instead. To remove the button altogether, set `use_my_location: false` in `_config.yml`.

## The three files

| File | What it holds |
|---|---|
| `_data/directory.yml` | The places. This is the one you will edit most |
| `_data/areas.yml` | The districts, their pincodes, and the area names people can type |
| `_config.yml` | The on/off switch, under `directory:` |

## 1. Verify a place

A place appears on the site **only** when it has a `last_verified` date and an address. No date, no display.

1. Phone the number, or visit.
2. Confirm the name, the address, the phone number and the hours. Ask: "If a survivor of sexual assault comes to you, what do you do for them?"
3. In `_data/directory.yml`, correct the entry and fill in:
   - `last_verified: "2027-01-15"` (the date you checked, year-month-day)
   - `verified_how: "phoned, spoke to the front desk"`
4. Anything you could not confirm stays as `""`.

**Never type an address, phone number or map point you have not checked yourself.**

## 2. Add a new place

Copy this block to the end of `_data/directory.yml`, under the right city heading, and fill it in. Keep the two spaces at the start of each line.

```
  - type: hospital
    sector: government
    district: chandigarh
    name: ""
    address: ""
    phone: ""
    hours: ""
    notes: ""
    pin: ""
    todo: ""
    last_verified: ""
    verified_how: ""
```

| Line | What to write |
|---|---|
| `type` | `one-stop-centre`, `hospital`, `police`, `legal-aid`, `child-rights`, `counselling`, `shelter`, `support-group` or `campus` |
| `sector` | `government`, `private` or `ngo` |
| `district` | `chandigarh`, `mohali` or `panchkula` |
| `notes` | One short line people will see. For example "Ask for the gynaecology emergency" |
| `pin` | The map point. Optional. See step 3 |
| `pin_suggested` | A map point found online, usually on OpenStreetMap. The real site never uses it. Check it, then copy it into `pin` (step 3) |
| `todo` | A private reminder for you. Never shown |
| `source` | Where an address or number was found online, and when. Never shown. Finding something online is not verifying it |
| `needs` | Optional. Only if this place helps with something unusual for its type. For example `needs: [support, legal]` |
| `phone2` | Optional second number |
| `name_hi`, `address_hi`, `hours_hi`, `notes_hi` | Optional Hindi versions. Without them the English shows on the Hindi page |

### Extra checks for an NGO

Listing an NGO tells a survivor that you trust it. An NGO appears only when these four lines are also filled in:

```
    ngo_check:
      free: true
      works_with_survivors: true
      spoken_to: "Name and role of the person you spoke to"
      spoken_on: "2027-01-15"
```

`free: false` is allowed. The page then shows "Ask about fees". `works_with_survivors` must be `true`.

## 3. Add a map point (optional, but it is what makes "nearest first" work)

A place without a map point still shows. It just has no distance and comes after the places that do.

On a laptop:
1. Open Google Maps and find the building. Zoom in until you can see the entrance.
2. Right-click on the entrance.
3. The first line of the menu is two numbers, like `30.74123, 76.77901`. Click it to copy.
4. Paste it between the quotes: `pin: "30.74123, 76.77901"`

Some places already have a `pin_suggested` line, from OpenStreetMap. To check one, paste its two numbers into the Google Maps search box. If the pin lands on the right building, copy the numbers into `pin`. If it does not, use the steps above.

## 4. Check an area's map point

`_data/areas.yml` lists about 560 areas: post office names from India Post, every sector OpenStreetMap knows in the three cities, about 240 villages that OpenStreetMap and GeoNames both place, and a few areas from Wikidata.

**About 320 are marked `checked: true`, because two sources agree on where they are** (within 1 km for a sector, 2 km for anything else). You decided on 18 November that this is good enough, so the script now does it by itself, for any new district too. Only checked areas get "nearest first".

The rest say `checked: false`: nobody has checked their map point, or the sources disagree. The page uses those only to work out the district, and does not show distances from them. Someone who types one gets the district's places, without "nearest first".

To switch on "nearest first" for an area:
1. Paste its `centre` numbers into the Google Maps search box and see where the pin lands. If it is roughly in the middle of the area, it is right.
2. If not, find the middle of the area, right-click, and copy the two numbers into `centre: "..."`, as in step 3.
3. Change `checked: false` to `checked: true`.

Start with the areas where most people live. You do not have to do them all. "Use my location" gives nearest-first results without any of this.

After "Use my location", the page picks the district by itself only when the three nearest checked areas are all in the same district and within 6 km, and no area of another district is within 1.5 km. Otherwise it asks the person to tap their district. That is deliberate: a wrong guess would show the wrong legal aid office. (Tested on 18 November at every sector and village: no wrong guesses; near borders, such as the sectors split between Chandigarh and Mohali, it asks.)

**Where the points come from.** An area's line can also have:
- `from:` where the map point came from, when it is not India Post: OpenStreetMap, GeoNames (a free world list of places) or Wikidata
- `second:` the other sources' points for the same place, and how far each is from the one used
- `also:` another name for the same area, shown in brackets. This is how Mohali's phases are linked, so "Phase 7" and "Sector 61" both find it.
- `note:` this area's district may be wrong, because another district has a place with the same name close by. Two have one: Tira (India Post says Chandigarh, GeoNames says Mohali) and Ramgarh in Panchkula (India Post's point is probably the other Ramgarh, near Zirakpur). Check these before relying on them.

For a sector, OpenStreetMap's point is used, because it is the middle of the sector as drawn on the map. India Post's point is only a post office somewhere inside it, and for five sectors it is between 1.7 and 7.6 km off. For a village or town, India Post's point is used, unless GeoNames and OpenStreetMap agree with each other and both put the place more than 2 km away from it. Then India Post's point is taken to be wrong (Kharar, Dera Bassi and Haripur, for example).

Where two sources are far apart, one of them is wrong: those areas stay unchecked until someone looks.

**Sectors on the border.** Sectors 53 to 56, 61 and 63 are split between Chandigarh and Mohali, so they are listed for both, and the person picks the city.

**Mohali's phases** are all linked to their sectors: Phase 1 (Sector 55), 2 (54), 3A (53), 3B-1 and 3B-2 (60), 4 and 5 (59), 6 (56), 7 (61), 8 (62), 9 (63), 10 (64) and 11 (65). They are listed in `PHASES` near the top of `guides/tools/make-areas.py`, with where each came from.

**Villages near a district border are left out on purpose.** A village is added only when GeoNames puts most of its neighbouring places in the same district, because a wrong district would show the wrong One Stop Centre and legal aid office. Someone from a village that is not listed can still pick their district.

**A missing area is fine.** If someone types an area that is not listed, the page asks "Which district is it in?" and carries on. You can add an area by copying a line.

## 5. Switch the page on

When you have verified places for all three districts:

1. Open `_config.yml`.
2. Under `directory:` change `live: false` to `live: true`.
3. Commit.

Three things then appear:
- a light yellow strip, "Find help near you", under the header of every page, so nobody has to scroll or go back to the home page
- a "Find help near you" button under the headline on the home page
- "Find help" in the phone menu, and a card on "What to do first"

To switch it off again, change it back.

## 6. Keep it current

- Re-check every place every six months and update `last_verified`.
- If a place closes or a number stops working, delete its `last_verified` date straight away. It disappears from the site and stays in your file.

## 7. Adding another district or state later

The page is built on districts, because that is how these services are organised everywhere in India: one One Stop Centre, one legal aid office and one Child Welfare Committee per district.

To add one, ask Claude to:
1. Add the district to the list at the top of `guides/tools/make-areas.py` and run it. That rebuilds `_data/areas.yml` with the new district's pincodes and area names, and keeps every area you have already checked.
2. Add the district's places to `_data/directory.yml`, unverified, for you to check.

With more than six districts, the district buttons turn into a drop-down list grouped by state. Nothing needs redesigning.

## The test view

`_config.preview.yml` is for testing only. The real site never uses it. Claude builds the site with it to show you the page before any place is verified. In that view every unverified place is stamped "NOT VERIFIED" and uses its suggested map point, and a few made-up places stamped "SAMPLE" show how nearest-first sorting looks.

## Credits and licence

The area list uses OpenStreetMap. Its licence, the Open Database License (ODbL), asks for two things, and both are done:
- The page credits "© OpenStreetMap contributors", with a link, under the list of places.
- `_data/areas.yml` says at the top that it is shared under the same licence, so anyone may reuse it on those terms.

Do not remove either. The same credit line also names India Post, GeoNames and Wikidata.

## Known limits of this first version

- **Some villages are missing,** and about 60 listed areas, mostly villages, have no map point yet, because no source had them, or a source had several villages with the same name. Every sector of the three cities is listed.
- **A village's district comes from India Post, or for the added villages from GeoNames.** For a village right on a district border, check it if you are unsure: it decides which One Stop Centre and legal aid office people see.
- **Distances are straight-line,** not by road. The page says so.
- **No "get directions" link.** A link to Google Maps would tell Google where the person is going. People can copy the address.
