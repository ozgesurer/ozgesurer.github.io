---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---

{% include base_path %}

Bayesian analysis of physical-statistical models
======

With the increased access to parallel computing environments, computer models have become pervasive throughout much of science
to understand large and complex physical processes in many engineering and science disciplines. These models can be used for 
system design and optimization, forecasting and prediction, and to guide future data collection. Two major challenges exist 
in the usage of these models: the presence of unknown or observable parameters which must be inferred using data and the reality
that all models are at least somewhat wrong. While there are Bayesian statistical tools to handle this in theory, this project 
aims to use computational research to transform these theoretical relationships into tools and techniques for making reliable
computational predictions of complex systems with well-quantified uncertainties. This requires using cutting edge research 
in machine learning and statistical learning that can handle big data environments. 

The focus of Bayesian analysis of nuclear dynamics (BAND) framework is on building cyberinfrastructure for problems in the nuclear-physics domain. 
You can find more about the [Bayesian analysis of nuclear dynamics framework](https://bandframework.github.io) from the link.

[[See our paper at Physical Review C](https://journals.aps.org/prc/abstract/10.1103/PhysRevC.106.024607)]




COVID-19 response
======

***Multi-tier opening policy for Austin to control COVID-19***

In this study, we apply stochastic optimization to recommend policy triggers governing stages of community mitigation to prevent overwhelming hospital surges and ensure adequate capacity in the unlikely case that they occur.

[[See our paper at Nature Communications](https://www.nature.com/articles/s41467-021-23989-x)]


***Optimal vaccine allocation policy***

Vaccines are the best tools to control the COVID-19 pandemic. Multiple types of vaccines with different dose requirements become available over time. We have been working on an age and risk-stratified mathematical model to obtain an optimal vaccine allocation policy.

[[See the technical report](https://covid-19.tacc.utexas.edu/media/filer_public/15/4d/154defa8-9217-478e-a459-8fc4144c61b5/austin_covid_alert_stage_and_mortality_trends_-_ut_-_may_2021.pdf)]

Interpretable, fast, and accurate predictive models
======

My dissertation proposes a new algorithm, ***coefficient tree regression***, that fits regression models in a fundamentally different way to discover the group structure from high-dimensional data.

[[See our paper at Machine Learning](https://link.springer.com/article/10.1007/s10994-021-06091-7)]


***Coefficient tree regression for discovering structure in generalized linear models***

Massive regression data sets are now commonplace, with so many predictors that they cannot or should not all be included individually. In practice, derived predictors that are the sum of groups of individual predictors (which is equivalent to predictors within groups sharing the same coefficient) are often relevant. However, the groups of predictors are often not known in advance, and they must be discovered from the data. In this study, we extend our coefficient tree regression algorithm to generalized linear models to discover the group structure from the data.

[[See our paper at Statistical Analysis and Data Mining](https://onlinelibrary.wiley.com/doi/10.1002/sam.11534)]


***Discovering structure in longitudinal data***

When the data have a spatial and/or temporal component, we often expect that predictor variables that are closer in space and/or time are more likely to be associated with the response in the same way. In such situations, we can exploit those aspects and discover groups of predictors that share the same coefficient according to their spatial and/or temporal proximity. In this study, we propose a new algorithm called coefficient tree regression for longitudinal data to understand the underlying spatial and/or temporal characteristics of the data.

The use of statistical learning algorithms in recommender systems
======

Beyond my dissertation, recently, I have been interested in two closely-related topics:

***Multi-stakeholder recommendation***, which refers to a recommendation application in which parties other than just the end user need to be considered in computing recommendation outcomes.

***Fairness-aware recommendation*** is a sub-class of multistakeholder recommendation in which the system has a concern for delivering results that meet some criterion of fairness. Besides accuracy, fairness in machine learning has
begun to be extended to recommender systems.

[See our paper in RecSys'18](https://dl.acm.org/citation.cfm?id=3240350)

My interest in interpretable models comes from our initial study in recommender systems.

[See our paper in RecSys'17](https://dl.acm.org/citation.cfm?id=3109863)

In this study, we improved the prediction accuracy of learning algorithms by integrating ontological information into the recommender systems. However, when the ontological information is not known in advance, it should be estimated from the data. This problem brought a new perspective to my current research in discovering a hidden ontology from the data, and it is the focus of my dissertation as explained above.
