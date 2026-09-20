---
layout: publications
title: "Publications"
permalink: /publications/
intro: "Peer-reviewed work in simulation, statistical learning, and data-driven decision-making."
---

{% assign current_year = "" %}
{% for publication in site.data.publist %}
  {% assign year_parts = publication.link.display | split: "(" %}
  {% assign year = year_parts | last | remove: ")" | strip %}
  {% if year != current_year %}
    {% unless forloop.first %}</div></section>{% endunless %}
    <section class="publications__year" aria-labelledby="publications-{{ year }}">
      <h2 id="publications-{{ year }}">{{ year }}</h2>
      <div class="publications__year-list">
    {% assign current_year = year %}
  {% endif %}

  <article class="publication">
    <div class="publication__image">
      <img src="{{ publication.image | prepend: '/images/pubpic/' | prepend: base_path }}" alt="" loading="lazy">
    </div>

    <div class="publication__content">
      <h3>{{ publication.title }}</h3>
      <p class="publication__authors">{{ publication.authors | replace: "Özge Sürer", "<strong>Özge Sürer</strong>" }}</p>
      <p class="publication__venue">{{ publication.link.display | strip }}</p>

      <div class="publication__actions">
        <a class="publication__paper-link" href="{{ publication.link.url }}">Paper <span aria-hidden="true">↗</span><span class="screen-reader-text">: {{ publication.title }}</span></a>
        {% if publication.description %}
          <details class="publication__abstract">
            <summary><span class="publication__read-abstract">Read abstract</span><span class="publication__show-less">Show less</span></summary>
            <p>{{ publication.description | strip }}</p>
          </details>
        {% endif %}
      </div>
    </div>
  </article>

  {% if forloop.last %}</div></section>{% endif %}
{% endfor %}
