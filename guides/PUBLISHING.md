# Publishing the site: step by step

You will do this once. It takes about 45 minutes, plus waiting time for the domain. You need a laptop, not a phone.

**What you are setting up**

- **GitHub** stores the site's files and publishes them for free. You edit text in your browser and the live site updates about a minute later.
- **Your own domain** (for example `aagaazfoundation.org`) is the address people type or scan. You pay for this yearly. Because you own it, the QR code on your flyers keeps working even if you ever move the site somewhere else.

Do the parts in order. Part A gets you a working free link the same day. Part B adds your domain. Part C is the QR code.

---

## Part A: Put the site on GitHub (free)

### A1. Make a foundation email first

Create a new email address for Aagaaz (for example a Gmail). Use it for GitHub, for the domain, and as the public contact address. Don't use your personal or school email: this address will be public, and you may want to hand the project to someone else one day.

### A2. Create a GitHub account

1. Go to **github.com** and choose **Sign up**.
2. Use the foundation email.
3. **Choose the username carefully: it becomes part of your free web address.** Try `aagaazfoundation`. If it is taken, try `aagaaz-foundation`.
4. Finish the sign-up and verify the email.
5. Click your profile picture (top right) → **Settings** → **Emails** → tick **Keep my email addresses private**.

### A3. Create the repository (the folder that holds the site)

1. Click the **+** at the top right → **New repository**.
2. **Repository name:** type your username followed by `.github.io`. For example `aagaazfoundation.github.io`. It must match your username exactly.
3. Choose **Public**. (Free publishing needs this. The site has no secrets in it.)
4. Leave everything else unticked. Click **Create repository**.

### A4. Add the publishing file (once)

The site is uploaded as one zip file, which works from an iPad or a laptop. A small publishing file unpacks it into the right folders and puts the site online. You add that file once.

1. In the repository, tap **Add file** → **Create new file**.
2. In the file name box, type exactly: `.github/workflows/publish.yml`
   Each `/` you type turns the part before it into a folder. That is expected.
3. Open `publish.yml` (sent to you with this guide), copy all of it, and paste it into the big text box.
4. Tap **Commit changes**, then **Commit changes** again.

### A5. Switch publishing on

1. Tap **Settings** (the tab along the top) → **Pages** (left-hand list).
2. Under **Build and deployment**, set **Source** to **GitHub Actions**. (Not "Deploy from a branch".)

### A6. Upload the site

1. Go back to the **Code** tab. Tap **Add file** → **Upload files**.
2. Choose `site-upload.zip`. **Do not unzip it.** Keep the name exactly `site-upload.zip`.
3. Tap **Commit changes**.
4. Tap the **Actions** tab. A run called **Publish site** starts. It unpacks the zip, then builds and publishes. It takes about two minutes. A green tick means done.

Open `https://YOURUSERNAME.github.io` on your phone. That is your working site.

**If it fails:** a red cross appears in the Actions tab. Tap it, take screenshots of the error, and send them to me.

**Every later update from me works the same way:** I send you a new `site-upload.zip`, you upload it (step A6), and the site updates. Small text edits you can still make directly on GitHub, and those publish on their own too.

---

## Part B: Add your own domain

### B1. Buy aagaazfoundation.org from GoDaddy India

Do Part A first, so the site already works on its free github.io address.

1. Go to **godaddy.com/en-in** and sign up with the foundation Gmail.
2. Search for `aagaazfoundation.org` and add it to the cart.
3. In the cart, before paying:
   - **Remove everything except the domain:** Domain Protection, hosting, email, Microsoft 365, website builder, and anything called "Airo" or AI.
   - **Check the renewal price** listed for year 2. The first-year price is a sale price.
   - Choose **1 year**.
4. Pay in rupees (UPI, net banking or card). GST of 18% is added.
5. After paying, open **My Products → aagaazfoundation.org** and check:
   - **Domain privacy is on** (your name and address hidden)
   - **Auto-renew is on**

### B2. Tell GitHub about the domain

1. In your repository: **Settings** → **Pages** → **Custom domain**. Type `aagaazfoundation.org` and tap **Save**.

### B3. Point the domain at GitHub (in GoDaddy)

1. In GoDaddy, open **My Products**, find the domain and click **DNS** (or **Manage DNS**).
2. **Delete** the record of type A whose value says **Parked**, and the record of type CNAME whose name is `www`. These are GoDaddy's defaults. Leave the NS and SOA records alone.
3. Add these five records:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `YOURUSERNAME.github.io` |

These values come from [GitHub's own instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). Type them exactly. Leave TTL at the default.

4. Google Search Console (Part D) adds one record of type TXT, and email forwarding, if you ever set it up, adds records of type MX and TXT. Those sit alongside these and don't affect the website.

### B4. Wait, then switch on HTTPS

1. DNS changes can take up to 24 hours, though it is often under an hour.
2. Go back to **Settings** → **Pages**. When the domain check shows a green tick, tick **Enforce HTTPS**. (If the box is greyed out, wait longer and refresh.)
3. Open `https://yourdomain.org` on your phone. Check the padlock shows.

### B5. Tell the site its own address

In the repository, open `_config.yml`, click the pencil, and change `url: ""` to `url: "https://yourdomain.org"`. Commit.

### B6. Protect the domain (recommended)

Click your profile picture → **Settings** → **Pages** → **Add a domain**, and follow the steps to verify it. This stops anyone else attaching your domain to their own GitHub site.

---

## Part C: The QR code

**Do not print a QR code until the lawyer has signed off** and you have set `legal_review: done: true` in `_config.yml`. Until then the site hides itself from search engines.

1. The QR code should contain your plain address: `https://yourdomain.org`. Nothing else.
2. **Use a static QR code.** Avoid generators that offer "dynamic" codes, scan tracking or analytics: those send every scan through their servers first, they track the people scanning, and they often stop working when a free trial ends. Ask me and I will make the QR file for you once the domain works.
3. Print one test flyer. Scan it with at least two different phones, including an older Android, before printing the rest.
4. Print the four helpline numbers on the flyer as well, so it helps even if someone never scans it.

---

## Part D: Google Search Console (free)

Search Console shows which Google searches bring people to the site, tells Google about new pages, and warns you about problems. It adds nothing to the site itself, so visitors are not tracked.

**Do this after the newest `site-upload.zip` is on GitHub.** Until then the site still tells Google not to list it, and the list of pages (`sitemap.xml`) doesn't exist yet.

### D1. Add the site

1. Go to [search.google.com/search-console](https://search.google.com/search-console) and sign in with the foundation Gmail.
2. Choose **Domain** (the left-hand box). Type `aagaazfoundation.org`, with no `https://` and no `www`, and tap **Continue**.

### D2. Prove you own the domain

- **If Search Console names GoDaddy and shows a Start verification button:** tap it, log in to GoDaddy and approve. Search Console then says the domain is verified.
- **Otherwise:** copy the value it shows (it starts with `google-site-verification=`). In GoDaddy, open the domain's DNS page (as in B3) and add a record: type **TXT**, name `@`, and paste the value. Save. Back in Search Console, tap **Verify**. If it fails, wait an hour and try again. Google says it can take a day or two.
- **If GoDaddy gives an error (what happened on 19 Nov):** use a **URL prefix** property for `https://aagaazfoundation.org/` instead, with the **HTML file** method. The file `googlee470a1cbeb5cdc08.html` is already in the site. Never delete it.
- **Never delete that TXT record.** Google checks it again from time to time, and the site stops being verified if it's gone.

### D3. Give Google the list of pages

1. In the left menu, open **Sitemaps**.
2. Under "Add a new sitemap", type `https://aagaazfoundation.org/sitemap.xml` and tap **Submit**. The status should say **Success** (it can say "Couldn't fetch" for the first few hours).

### D4. What to expect

- New sites take a few days to a few weeks to show up in Google. Searching `site:aagaazfoundation.org` on Google shows which pages it has so far.
- The search numbers start after a few days.
- Optional, to speed up the home page: paste `https://aagaazfoundation.org` into the search bar at the top of Search Console and tap **Request indexing**.
- The "Find help near you" page stays out of the list of pages until you switch the finder on. After that, Google finds it on its own.

---

## Before you share the link with anyone

- [ ] The lawyer has checked the pages in `guides/LEGAL-REVIEW-CHECKLIST.md`
- [ ] `legal_review` is set to done in `_config.yml`
- [ ] 181 is confirmed for Chandigarh
- [ ] `contact_email` is filled in, and someone checks that inbox
- [ ] The About page says what you want it to say about you
- [ ] The Workshops page shows only sessions that are confirmed
- [ ] You have opened every page on your own phone and tapped Quick exit
- [ ] The school has agreed to anything that names or shows it
