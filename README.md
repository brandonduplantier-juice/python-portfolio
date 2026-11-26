# Engineering, Research and Data Science Portfolio

The repository behind my portfolio site, including software engineering case studies, research summaries, and a collection of standalone analytics projects. The flagship longevity and bioinformatics work lives in its own dedicated
repositories (linked below); this repo holds the portfolio site itself and a set of
healthcare, BI, and foundational projects.

Live site: https://brandonpython.netlify.app
Profile: https://github.com/brandonduplantier-juice

## Software engineering and product case studies

The public portfolio includes case studies of deployed applications and development-stage products. Each distinguishes implemented behavior, validation evidence, and remaining limitations. Private project source code is not included here.

- [Loadout Oracle](https://github.com/brandonduplantier-juice/loadout-oracle) - game inventory integration and loadout analysis.
- [CraftPath](https://github.com/brandonduplantier-juice/CraftPath) - crafting probability and decision-support tooling.
- [Beauty storefront and merchant platform](case-study-beauty-platform.html) - commerce and operations case study.
- [Unphucked](case-study-unphucked.html) - mobile product and privacy architecture case study.
- [Night Shift](case-study-night-shift.html) - game development case study.
- [Genomic AI](case-study-genomic-ai.html) - experimental variant-effect prediction and baseline comparison.

## Flagship projects (separate repositories)

These are the lead projects, each with its own result-first, plain-language README:

- [aging-clock](https://github.com/brandonduplantier-juice/aging-clock) - DNA methylation biological-age predictor. Predicts age to within 5.65 years on held-out blood (r 0.892), holds at 6.36 on an independent cohort.
- [nhanes-phenoage](https://github.com/brandonduplantier-juice/nhanes-phenoage) - biological age (Levine PhenoAge) vs mortality in 28,510 NHANES adults. Each year of acceleration carries 4.5 percent higher mortality risk, independent of age.
- [rnaseq-aging-de](https://github.com/brandonduplantier-juice/rnaseq-aging-de) - differential expression in young vs old human brain. 119 genes at 5 percent FDR, led by myelin and oligodendrocyte genes.
- [longevity-evidence-explorer](https://github.com/brandonduplantier-juice/longevity-evidence-explorer) - grades longevity interventions by evidence strength on a transparent rubric, with citations resolved live from PubMed.
- [single-cell-aging](https://github.com/brandonduplantier-juice/single-cell-aging) - single-cell aging analysis done the statistically correct way (pseudobulk, mice as replicates).

## Projects in this repository

### Healthcare and clinical analytics
The same 300-patient hospital readmission dataset, analyzed across several tools to
show the result holds independent of the stack. The R logistic regression is the
interpretable lead; the others demonstrate range.

- [R-Readmission-Logistic-Regression](R-Readmission-Logistic-Regression) - logistic regression (glm), odds ratios with CIs, ROC AUC 0.714. The strongest version.
- [Readmission-Prediction-Model](Readmission-Prediction-Model) - Python Random Forest classifier for the same outcome.
- [Hospital-Readmission-PowerBI](Hospital-Readmission-PowerBI) - Power BI dashboard on the readmission data.
- [Snowflake-Readmission-Analysis](Snowflake-Readmission-Analysis) - the analysis run in a Snowflake cloud data warehouse.
- [Excel-Readmission-Analysis](Excel-Readmission-Analysis) - the spreadsheet cut: pivot summaries, formulas, and a dashboard sheet.
- [HR-Attrition-PowerBI](HR-Attrition-PowerBI) - Python-engineered attrition risk score plus a Power BI dashboard.

### Data and BI
- [SQL-Analytics-Portfolio](SQL-Analytics-Portfolio) - 6 queries across 4 PostgreSQL databases: CTEs, window functions, conditional aggregation.
- [Tableau-Happiness-Dashboard](Tableau-Happiness-Dashboard) - 2019 World Happiness Report dashboard, 156 countries.

### Foundations and practice
Earlier exploratory and skill-building work, kept for completeness.

- [LiveLab](LiveLab) - nine hands-on practice notebooks across varied real datasets.
- [Grammys - Website Analytics Project](Grammys%20-%20Website%20Analytics%20Project) - a web-analytics EDA of Grammy Awards traffic.
- SkillBuilder-01 through SkillBuilder-09 - a nine-part Python and data-analysis practice series.

## Note on the live site
The portfolio site (index.html) is served from this repository and deploys
automatically to Netlify on push. It is the front door; the project cards link out to
the flagship repos above and the folders here.

## Project navigation

- [Engineering guide](ENGINEERING.md): directory map, development workflow and review standards.
- [Documentation index](DOCUMENTATION.md): technical documents and existing project resources.
