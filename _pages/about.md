---
permalink: /
title: "About me"
excerpt: "About me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am an Assistant Professor of [Analytics at Miami University](https://www.miamioh.edu/fsb/academics/isa/). Prior to this appointment, I was a postdoctoral research fellow at the Northwestern Argonne Institute of Science and Engineering. My postdoctoral research focused on applying and developing novel techniques based on Bayesian uncertainty quantification and computational statistics. I completed my Ph.D. in December 2020 in the Industrial Engineering and Management Sciences Department at Northwestern University. The objective of my research is to develop new statistical methods in the presence of data. 

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

