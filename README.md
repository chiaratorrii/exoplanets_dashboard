# Exoplanets Dashboard

Interactive Python dashboard for exploring exoplanet data from NASA archives using Plotly Dash visualizations.

## Overview

This project provides an interactive dashboard to analyze confirmed exoplanets, featuring comparisons with Earth and Jupyter, discovery facilities map, and a clustering analysis (coming soon).

## Plotly Dash Integration

It leverages Plotly Dash, which is a Python framework that enables creation of interactive web dashboards through layouts of HTML/DCC components and reactive callback functions linking user inputs (eg. dropdowns, sliders, etc.) to dynamic Plotly graph updates.

## Installation

Clone and set up the environment for Jupyter-based exoplanet analysis.

1. Clone: `git clone https://github.com/chiaratorrii/exoplanets_dashboard.git` then `cd exoplanets_dashboard`.
2. Virtual environment: `python -m venv env`; activate with `source env/bin/activate` (Unix) or `env\Scripts\activate` (Windows).
3. Install: `pip install jupyterlab dash pandas matplotlib seaborn plotly astropy`.

## Usage

Execute  `app.py` script.

## Data Sources

- NASA Exoplanet Archive for confirmed planets.
- Wikipedia (web scraping) for Discovery Facilities information.
- OpenStreetMap for Discovery Facilities geolocation.
