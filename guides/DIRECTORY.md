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
| `todo` | A private reminder for you. Never shown |
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

## 4. Check an area's map point

`_data/areas.yml` lists about 195 areas, taken from India Post's post office list. Each has a rough map point and `checked: false`.

**India Post's map points are often wrong.** So while an area says `checked: false`, the page uses it only to work out the district. It does not show distances from it. Someone who types that area gets the district's places, without "nearest first".

To switch on "nearest first" for an area:
1. Find the middle of the area on Google Maps and copy the two numbers, as in step 3.
2. Put them in `centre: "..."` on that area's line.
3. Change `checked: false` to `checked: true`.

Start with the areas where most people live. You do not have to do them all. "Use my location" gives nearest-first results without any of this.

Until three checked areas sit near someone, the page cannot tell which district their location is in, so after "Use my location" it asks them to tap their district. That is deliberate: a wrong guess would show the wrong legal aid office.

**Many sectors are missing from the list,** because not every sector has a post office. That is fine. If someone types "Sector 38", the page asks "Which district is it in?" and carries on. You can add an area by copying a line.

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

`_config.preview.yml` is for testing only. The real site never uses it. Claude builds the site with it to show you the page before any place is verified. In that view every unverified place is stamped "NOT VERIFIED", and a few made-up places stamped "SAMPLE" show how nearest-first sorting looks.

## Known limits of this first version

- **Area names come from post office names.** A fuller list of sectors, each with a map point, could come from OpenStreetMap. That site could not be reached when this was built. If it is added later, the page must credit "© OpenStreetMap contributors".
- **Distances are straight-line,** not by road. The page says so.
- **No "get directions" link.** A link to Google Maps would tell Google where the person is going. People can copy the address.
