# Aagaaz Foundation website

From awareness to action. Information on sexual violence awareness and survivor support for Chandigarh, Panchkula and Mohali.

Start with the guides:

- `guides/PUBLISHING.md`: how to put the site online and connect a domain
- `guides/HOW-TO-UPDATE.md`: how to change text, add workshops and publish toolkit chapters
- `guides/LEGAL-REVIEW-CHECKLIST.md`: every legal claim on the site, for the reviewing lawyer

What the site does not do, on purpose: no logins, no forms, no cookies, no analytics, no requests to any other website. Fonts are stored with the site (Noto Sans and Noto Sans Devanagari, under the SIL Open Font License).

## Phase 2: "Find help near you"

Built on 17 November 2026 and switched off (`directory: live: false` in `_config.yml`). It stays off until places have been verified by phone. The guide is `guides/DIRECTORY.md`.

- Someone types a sector, area or pincode, taps "Use my location", or picks a district (Chandigarh, Mohali, Panchkula)
- They see the district's One Stop Centre first, then the nearest hospitals, police, legal aid and child protection offices, with the first-steps guide alongside
- Each entry shows its "last verified" date
- **An entry with no `last_verified` date is never shown.** Nothing unchecked can reach a survivor
- The lookup runs entirely on the visitor's phone. What they type, and their location, are never sent anywhere
- When the toolkit's "Where to go in the Tri-City" chapter is published, it can read from the same file, so there is one list to maintain
- Data licence: `_data/areas.yml` contains OpenStreetMap data (© OpenStreetMap contributors) and is shared under the Open Database License (ODbL). The page credits it
