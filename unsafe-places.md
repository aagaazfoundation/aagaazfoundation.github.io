---
title: "Report an unsafe place"
ref: unsafe-places
permalink: /unsafe-places/
colour: green
summary: "A dark lane, a broken streetlight, high bushes. Tell us, and we will take it to the municipality."
last_updated: 2026-11-20
---

{% assign uf = site.unsafe_places %}
{%- if uf.form_url and uf.form_url != "" %}
<p class="form-buttons"><a class="button" href="{{ uf.form_url }}" rel="noreferrer noopener">Report a place</a>{% if uf.photo_form_url and uf.photo_form_url != "" %} <a class="button button--quiet" href="{{ uf.photo_form_url }}" rel="noreferrer noopener">Send a photo or video</a>{% endif %}</p>

The report form is in English and Hindi. It doesn't ask for your name, and you don't need to sign in. To send a photo or video, Google makes you sign in, so we will see your Google name. We never share who sent a report.
{%- else %}
**The form will open here soon.**
{%- endif %}

**This is not for reporting something that happened to you.** We cannot reply or send help. If you are in danger, call {% include call.html line="emergency" %}. If you are under 18, call {% include call.html line="child" %}.
{: .note}

## What to report

Dark or empty lanes, broken streetlights, bushes or walls that block the view, and underpasses, parks, parking areas or bus stops that feel unsafe.

## Please don't

- Write about something that happened to a person, or name anyone
- Show people or number plates in a photo or video
- Put yourself at risk to check a place or take a photo

## What happens next

We read every report and remove anything personal. We check the places with NGOs and take the report to the municipal corporations of Chandigarh, Panchkula and Mohali.
