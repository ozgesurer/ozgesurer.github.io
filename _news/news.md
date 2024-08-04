---
layout: archive
title: "News"
permalink: /news/
author_profile: true
---

{% for new in site.data.news %}

  <a href="{{new.date }}" target="_blank"><em>{{ new.headline }}</em></a> <br />
  {{ talk.location }}<br />{{ talk.date}}

{% endfor %}