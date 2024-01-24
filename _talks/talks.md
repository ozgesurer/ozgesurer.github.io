---
layout: archive
title: "Talks"
permalink: /talks/
author_profile: true
---

{% for talk in site.data.presentations %}

  <a href="{{talk.link.url }}" target="_blank"><em>{{ talk.title }}</em></a> <br />
  {{ talk.presenter }} <br />{{ talk.location }}<br />{{ talk.date}}

{% endfor %}
