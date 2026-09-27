---
layout: talks
title: "Talks"
permalink: /talks/
---

<div class="talks">
  <p class="talks__intro">Selected conference presentations, invited seminars, and workshops.</p>

  <div class="talks__archive">
    {% assign current_year = "" %}
    {% for talk in site.data.talks %}
      {% assign talk_date = talk.date | strip %}
      {% assign talk_year = talk_date | split: "," | last | strip %}
      {% if talk_year != current_year %}
        {% unless forloop.first %}
          </div>
        </section>
        {% endunless %}
        <section class="talks__year" aria-labelledby="talks-{{ talk_year }}">
          <h2 id="talks-{{ talk_year }}" class="talks__year-heading">{{ talk_year }}</h2>
          <div class="talks__list">
        {% assign current_year = talk_year %}
      {% endif %}

      <article class="talks__item">
        <h3 class="talks__title">{{ talk.title }}</h3>
        <p class="talks__venue">{{ talk.venue | strip }}</p>
        <div class="talks__details">
          <span>{{ talk.location | strip }}</span>
          <span aria-hidden="true">&middot;</span>
          <time datetime="{{ talk_year }}">{{ talk_date }}</time>
          {% if talk.link.url and talk.link.url != "" %}
            <a class="talks__link" href="{{ talk.link.url }}" target="_blank" rel="noopener noreferrer">Event <span aria-hidden="true">↗</span><span class="screen-reader-text"> (opens in a new tab)</span></a>
          {% endif %}
        </div>
      </article>
    {% endfor %}
    {% if site.data.talks.size > 0 %}
          </div>
        </section>
    {% endif %}
  </div>
</div>
