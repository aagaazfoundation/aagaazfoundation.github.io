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

### A4. Upload the files

1. Unzip `aagaaz-site.zip` on your laptop. Open the `aagaaz-site` folder so you can see what is inside it (`_config.yml`, `index.md`, `assets`, and so on).
2. On your new repository page, click the link **uploading an existing file**.
3. Select **everything inside** the `aagaaz-site` folder and drag it onto the page. Drag the contents, not the folder itself.
4. Wait for the upload to finish. Scroll down and click **Commit changes**.

### A5. Switch publishing on

1. In the repository, click **Settings** (the tab along the top) → **Pages** (left-hand list).
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Set **Branch** to **main** and the folder to **/ (root)**. Click **Save**.
4. Wait two minutes. Refresh the page. It will show **Your site is live at https://YOURUSERNAME.github.io**.

Open that link on your phone. That is your working site.

**If it does not appear:** click the **Actions** tab. A red cross means the build failed; click it to read the message, and send it to me.

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

1. In your repository: **Settings** → **Pages** → **Custom domain**. Type your domain (for example `aagaazfoundation.org`) and click **Save**. GitHub adds a small file called `CNAME` to the site. Leave it there.

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

4. If you later set up `contact@aagaazfoundation.org` forwarding, it adds its own records (type MX and TXT). Those sit alongside these and don't affect the website.

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

**Do not print a QR code until the lawyer has signed off** and you have set `legal_review: done: true` in `_config.yml`. Until then the law pages carry a "being checked" note and the site hides itself from search engines.

1. The QR code should contain your plain address: `https://yourdomain.org`. Nothing else.
2. **Use a static QR code.** Avoid generators that offer "dynamic" codes, scan tracking or analytics: those send every scan through their servers first, they track the people scanning, and they often stop working when a free trial ends. Ask me and I will make the QR file for you once the domain works.
3. Print one test flyer. Scan it with at least two different phones, including an older Android, before printing the rest.
4. Print the four helpline numbers on the flyer as well, so it helps even if someone never scans it.

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
