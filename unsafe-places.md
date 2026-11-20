---
title: "Report an unsafe place"
ref: unsafe-places
permalink: /unsafe-places/
colour: green
summary: "A dark stretch, a broken streetlight, bushes that block the view. Tell us, and we will take it to the municipality."
last_updated: 2026-11-20
---

**This is not for reporting something that happened to you.** We cannot reply to it or send help. If you are in danger, call {% include call.html line="emergency" %}. If you are under 18, call {% include call.html line="child" %}. [What to do first](/first-steps/) explains the next steps.
{: .note}

## What this is

We are collecting places in Chandigarh, Panchkula and Mohali that feel unsafe to walk through, especially for women and children. We will put them together in a report for the municipal corporations, and check streets in person with local NGOs.

## What to report

- Streetlights that don't work, or stretches with no lights
- Dark or empty underpasses, parks, parking areas and short cuts
- Overgrown bushes or high walls that block the view
- Bus stops, markets or lanes that feel unsafe after dark
- Places where there is no one around: no shops, no guards, no houses facing the road

## What to tell us

- **Where:** the area and a landmark. For example, "Sector 22, the lane behind the market"
- **What the problem is**
- **When it feels unsafe.** For example, after 7 pm, or all the time
- **As much detail about the place as you can:** how long the dark stretch is, what is around it, and since when it has been like this

The form is in English and Hindi. It does not ask for your name, phone number or email, and you don't need to sign in.

## Please don't

- Write about something that happened to a person. Use the numbers above instead
- Name anyone or accuse anyone
- Put yourself at risk to check a place

{% if site.unsafe_places.form_url and site.unsafe_places.form_url != "" %}
<p><a class="button" href="{{ site.unsafe_places.form_url }}" rel="noreferrer noopener">Open the form</a></p>

The form opens on Google Forms. Google stores the answers, and only Aagaaz can read them.
{% else %}
**The form will open here soon.**
{% endif %}

## What happens next

We read every report, remove anything personal, and group the places by area. We then check them with NGOs and take the report to the municipal corporations of Chandigarh, Panchkula and Mohali. We plan to share a summary on this site.

## Photos and videos

{% if site.unsafe_places.photo_form_url and site.unsafe_places.photo_form_url != "" -%}
You can send a photo or a short video through a separate form. Google makes you sign in to upload a file, so we will see the name on your Google account. That is why it is a separate form: the main form needs no sign-in at all.

- Take it in daylight, with no people or number plates in it
- Phone photos can save the exact place they were taken. Turn off location for your camera first, or send a screenshot of the photo
- Don't put yourself at risk to take it

<p><a class="button button--quiet" href="{{ site.unsafe_places.photo_form_url }}" rel="noreferrer noopener">Send a photo or video</a></p>
{%- else -%}
The form doesn't take photos yet. We take photos ourselves during the street checks.
{%- endif %}
