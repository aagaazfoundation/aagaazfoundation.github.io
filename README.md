# Aagaaz Foundation website

From awareness to action. Information on sexual violence awareness and survivor support for Chandigarh, Panchkula and Mohali.

Start with the guides:

- `guides/PUBLISHING.md`: how to put the site online and connect a domain
- `guides/HOW-TO-UPDATE.md`: how to change text, add workshops and publish toolkit chapters
- `guides/LEGAL-REVIEW-CHECKLIST.md`: every legal claim on the site, for the reviewing lawyer

What the site does not do, on purpose: no logins, no forms, no cookies, no analytics, no requests to any other website. Fonts are stored with the site (Atkinson Hyperlegible and Bricolage Grotesque, both under the SIL Open Font License).

## Phase 2: "Find help near you"

Planned, not built. The data file is ready at `_data/directory.yml`.

- Someone picks their area (Chandigarh, Panchkula, Mohali) or types a pincode
- They see the nearest One Stop Centre, government hospitals, legal aid (DLSA), women police station and child rights commission, with the first-steps guide alongside
- Each entry shows its "last verified" date
- **An entry with no `last_verified` date is never shown.** Nothing unchecked can reach a survivor
- The lookup will run entirely on the visitor's phone. The pincode is never sent anywhere
- When the toolkit's "Where to go in the Tri-City" chapter is published, it will read from the same file, so there is one list to maintain

Before building it: verify every entry by phone, and fill in the pincode lists from India Post.
