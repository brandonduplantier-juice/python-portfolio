# Grammys Website Analytics

An exploratory data analysis of web-traffic and engagement data for The Grammys and
The Recording Academy, centered on how a major live event moves audience behavior.

## What it is
A Python notebook that loads several web-analytics datasets and answers a practical
question: what happens to a website's traffic and engagement around a marquee event
like the Grammy Awards. It is an exploratory analysis and a pandas and visualization
exercise, not a production system.

## What it looks at
- Traffic over time, and the spikes that line up with awards-show night.
- Desktop versus mobile usage patterns.
- Audience age demographics for the Grammys and the Recording Academy.
- A before-and-after comparison of engagement around the event.

## Data
Several CSVs in `datasets/`, including live web-analytics tables for the Grammys and
the Recording Academy, desktop and mobile user data, and age-demographic breakdowns.

## How to run
Open `Analyzing-Website-Performance-Grammys.ipynb` in Jupyter or VS Code and run the
cells top to bottom. It uses pandas for the analysis and standard plotting for the
figures, which are saved in `figs/`.

## Honest framing
This is foundational, exploratory work: clean data loading, sensible questions, and
clear charts. It demonstrates EDA and pandas fluency rather than modeling or
production engineering.
