---
layout: archive
title: "News"
permalink: /news/
author_profile: true
---

{% for new in site.data.news %}

## {{ new.date }}

{{ new.headline | markdownify }}

{% unless forloop.last %}---{% endunless %}

{% endfor %}
