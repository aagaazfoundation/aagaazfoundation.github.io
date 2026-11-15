# How to update the site yourself

You never need to touch the design. Every change below is a change to a text file.

## How editing works

1. Go to your repository on github.com.
2. Click the file you want to change.
3. Click the **pencil** icon (top right of the file).
4. Make your change.
5. Click **Commit changes** (green button), then **Commit changes** again.
6. Wait about two minutes. Refresh the live site.

**If something goes wrong:** every change is saved in the file's **History**. Open the file → **History** → pick the last good version → **⋯** → **View file** → copy it back. Nothing is ever lost.

## Getting an update from Claude

When Claude changes the site for you, you get a file called `site-upload.zip`.

1. In the repository, tap **Add file** → **Upload files**.
2. Choose `site-upload.zip`. Don't unzip it and don't rename it.
3. Tap **Commit changes**.

The **Publish site** run in the Actions tab unpacks it, replaces the old site files and publishes. About two minutes later the site is updated.

Always start Claude from the latest version: if you edited anything on GitHub yourself, tell Claude, or upload those files to the chat, so your edit isn't overwritten by the next zip.

## What lives where

| To change this | Open this file |
|---|---|
| A helpline number or its description | `_data/helplines.yml` |
| Your contact email, Instagram, Quick exit destination, legal review status | `_config.yml` |
| Home page words and the three big buttons | `index.md` |
| What to do first | `first-steps.md` |
| Know the law pages | the `law` folder |
| Online abuse | `online.md` |
| Helping someone else | `helping-someone.md` |
| About | `about.md` |
| Staying safe on this site | `safety.md` |
| The toolkit chapter list and the PDF | `_data/toolkit.yml` |
| A toolkit chapter | the `_toolkit` folder |
| A workshop | the `_workshops` folder |
| Menu labels, button text, footer small print | `_data/ui/en.yml` |
| The phase 2 directory | `_data/directory.yml` |

Leave `_layouts`, `_includes`, `.github` and `assets/css` alone. Those are the design. The one exception: the site's colours are a short list at the top of `assets/css/site.css`, each with a note saying what it is for. Changing a value there changes it everywhere.

## The top of every page file

Each page starts with a block between two `---` lines. These are the page's settings:

```
---
title: "What to do first"        ← the big heading
summary: "Six steps..."          ← the line under it
toolkit_chapter: first-hours     ← the matching toolkit chapter (see below)
last_updated: 2026-11-11         ← change this whenever you edit the page
---
```

Change the text inside the quotes. Don't delete the `---` lines, and don't change `ref` or `permalink`.

## Writing the text

| You type | You get |
|---|---|
| `## A heading` | A section heading |
| `**important words**` | **important words** |
| `- a point` | A bullet point |
| `[the words to click](/law/adults/)` | A link to another page on the site |
| `[the words to click](https://example.org)` | A link to another website |
| `{% include call.html line="child" %}` | The Child Helpline number, as a tap-to-call link |

The ids for `line=` are in `_data/helplines.yml`: `emergency`, `women`, `child`, `cyber`, `legal-aid`, `mental-health`. **Always write numbers this way.** Then one change in `helplines.yml` updates every page.

**Boxes.** Write the paragraph, then put one of these on the very next line:

- `{: .note}` a soft tinted box
- `{: .key}` a stronger box with a coloured edge, for the one thing people must know
- `{: .fault}` the box used for "It is not your fault"

**Tick and cross lists.** Write a normal bullet list, then put `{: .say}` (green ticks) or `{: .dont}` (red crosses) on the line under the last bullet.

## Common jobs

### Change a helpline number
Open `_data/helplines.yml`. Change the `number:`. Fill in `last_checked:` with today's date. Commit. Every page updates.

### Add your contact email
Open `_config.yml`. Put the address inside the quotes after `contact_email:`. The About page shows it, with the note asking people not to email personal stories.

### Add a workshop
1. Open `templates/workshop-template.md` and copy all of it.
2. In the `_workshops` folder click **Add file** → **Create new file**.
3. Name it like `2026-11-25-school-chandigarh.md` (lowercase, hyphens, no spaces).
4. Paste, fill in the lines, commit.

`status: upcoming` puts it under "Coming up". Change it to `status: past` afterwards and add your write-up below the second `---`.

### Add photos to a workshop
1. Resize each photo to about 1600 pixels wide and under 300 KB. Big photos make the site slow on mobile data.
2. Open the `assets/img/workshops` folder → **Add file** → **Upload files**.
3. In the workshop file, list each one under `photos:` with a `file:` and an `alt:` (one line describing the photo).

**No recognisable faces of students, and nothing that identifies a school that has not agreed in writing.**

### Publish a toolkit chapter
1. Open `_data/toolkit.yml` and find the chapter's `slug` (for example `first-hours`).
2. Copy `templates/toolkit-chapter-template.md`.
3. In the `_toolkit` folder, create a file named after the slug: `first-hours.md`. Paste and write the chapter.
4. Commit.

That is all. The Toolkit page stops saying "Coming soon" for that chapter and links to it, and the matching short page (What to do first) grows a "Read the full chapter" button.

### Make a short page hand over to its chapter completely
When a chapter is live and you no longer want the short version, open the short page and change `when_chapter_is_live: link` to `when_chapter_is_live: replace`. Anyone opening the short page is sent straight to the chapter. One version, nothing to keep in sync.

### Add the toolkit PDF
1. Upload the PDF to `assets/downloads`.
2. In `_data/toolkit.yml`, put its file name after `pdf:` and its size after `pdf_size:`.

### Mark the legal review as done
Open `_config.yml`. Under `legal_review:` set `done: true`, and fill in `reviewer:` and `date:`. The "being checked by a lawyer" notes disappear, each law page shows who checked it, and search engines are allowed to list the site.

### The Hindi pages
Every page has a Hindi version in the `hi` folder, with the same file name (for example `first-steps.md` and `hi/first-steps.md`). A button at the top of each page switches between the two.

- **When you change an English page, change the Hindi page too.** The two don't update each other. If you ask me to make a change, I'll do both.
- Hindi menu labels, buttons and small print are in `_data/ui/hi.yml`.
- Hindi helpline names are the `hi:` lines in `_data/helplines.yml`, and Hindi chapter titles are in `_data/toolkit.yml`.
- For a workshop, fill in the `title_hi`, `place_hi` and other `_hi` lines in its file so the Hindi Workshops page shows it in Hindi.

### Add Punjabi later
It works the same way as Hindi, with the code `pa`:
1. Copy `_data/ui/hi.yml` to `_data/ui/pa.yml` and translate the text after each colon.
2. Add `pa:` lines in `_data/helplines.yml` and `_data/toolkit.yml`.
3. Make a folder called `pa` and copy each page into it, following `templates/hindi-page-template.md` but with `lang: pa` and `/pa/` addresses.
4. In `_config.yml`, add `pa` under `languages:` and a `pa` default under `defaults:` (copy the `hi` lines).

## Rules worth keeping

- Change `last_updated` every time you edit a page.
- Never type a phone number or address you have not checked yourself.
- Re-check the helplines and every directory entry every six months.
- No forms, no comment boxes, no analytics, no embedded videos or maps. Each of those brings tracking with it.
