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

<section class="home__about" aria-labelledby="about-heading">
  <h2 id="about-heading">About</h2>

  <p>My research focuses on developing statistical methods for complex computer models and simulation-based systems. I am particularly interested in uncertainty quantification, statistical calibration, computer experiments, and active learning, with applications to scientific computing and digital twins.</p>

  <p>Prior to joining Miami University, I was a postdoctoral research fellow at the Northwestern Argonne Institute of Science and Engineering (NAISE), where I worked on Bayesian uncertainty quantification and computational statistics. I received my Ph.D. in Industrial Engineering and Management Sciences from Northwestern University in 2020.</p>
</section>

**Education:**
  - PhD in Industrial Engineering and Management Sciences
      - *Northwestern University*, 2020
  - MS in Industrial Engineering
      - *Bogazici University*, 2014
  - BS in Industrial Engineering
      - *Istanbul Technical University*, 2011

**Interests:**
- Uncertainty quantification
- Statistical computing
- Statistical learning for large data sets

**News:**
{% for new in site.data.news %}

  {{ new.date }}<br />{{ new.headline}}

{% endfor %}
