---
permalink: /
layout: home
title: "About me"
excerpt: "About me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<div class="home__columns">
  <div class="home__primary">
    <section class="home__about" aria-labelledby="about-heading">
      <h2 id="about-heading">About</h2>

      <p>My research focuses on developing statistical methods for complex computer models and simulation-based systems. I am particularly interested in uncertainty quantification, statistical calibration, computer experiments, and active learning, with applications to scientific computing and digital twins.</p>

      <p>Prior to joining Miami University, I was a postdoctoral research fellow at the Northwestern Argonne Institute of Science and Engineering (NAISE), where I worked on Bayesian uncertainty quantification and computational statistics. I received my Ph.D. in Industrial Engineering and Management Sciences from Northwestern University in 2020.</p>
    </section>

<section class="home__research" aria-labelledby="research-interests-heading">
  <h2 id="research-interests-heading">Research Interests</h2>

  <div class="home__research-grid">
    <div class="home__research-area">
      <h3>Uncertainty Quantification</h3>
      <p>Bayesian methods for quantifying uncertainty in complex computational models.</p>
    </div>

    <div class="home__research-area">
      <h3>Computer Experiments &amp; Calibration</h3>
      <p>Statistical design, emulation, and calibration of deterministic and stochastic computer models.</p>
    </div>

    <div class="home__research-area">
      <h3>Active &amp; Sequential Learning</h3>
      <p>Adaptive experimental design for efficiently learning from expensive simulations and data.</p>
    </div>
  </div>
</section>

<section class="home__education" aria-labelledby="education-heading">
  <h2 id="education-heading">Education</h2>

  <div class="home__education-grid">
    <div class="home__education-entry">
      <h3>Ph.D.</h3>
      <p class="home__education-field">Industrial Engineering and Management Sciences</p>
      <p class="home__education-meta">Northwestern University <span aria-hidden="true">&middot;</span> 2020</p>
    </div>

    <div class="home__education-entry">
      <h3>M.S.</h3>
      <p class="home__education-field">Industrial Engineering</p>
      <p class="home__education-meta">Boğaziçi University <span aria-hidden="true">&middot;</span> 2014</p>
    </div>

    <div class="home__education-entry">
      <h3>B.S.</h3>
      <p class="home__education-field">Industrial Engineering</p>
      <p class="home__education-meta">Istanbul Technical University <span aria-hidden="true">&middot;</span> 2011</p>
    </div>
  </div>
</section>

  </div>

  <aside class="home__secondary">
    <section class="home__news" aria-labelledby="latest-news-heading">
      <h2 id="latest-news-heading">Latest News</h2>

      <div class="home__news-list">
        {% for new in site.data.news limit: 4 %}
          <article class="home__news-item">
            <p class="home__news-date">{{ new.date }}</p>
            {% capture news_text %}{{ new.headline | markdownify | strip_html | strip_newlines }}{% endcapture %}
            {% assign news_excerpt = news_text | split: ". " | first %}
            {% assign news_remainder = news_text | remove_first: news_excerpt | remove_first: "." | strip %}
            <p class="home__news-excerpt">{{ news_excerpt }}.</p>
            {% if news_remainder != "" %}
              <details class="home__news-details">
                <summary><span class="home__news-read-more">Read more</span><span class="home__news-show-less">Show less</span></summary>
                <p>{{ news_remainder }}</p>
              </details>
            {% endif %}
          </article>
        {% endfor %}
      </div>
      <a class="home__news-archive-link" href="{{ base_path }}/news/">View all news &rarr;</a>
    </section>
  </aside>
</div>
