# My Coffee Analytics

[![Pylint](https://github.com/DenysGonzaga/my-coffee-analytics/actions/workflows/pylint.yml/badge.svg)](https://github.com/DenysGonzaga/my-coffee-analytics/actions/workflows/pylint.yml)

An application to store and analyze data regarding my coffee brews. \
This app was born out of my personal need to analyze different variables of a coffee brew, such as the method used, water temperature, grinder clicks, and so on. \
The main idea is, when I have necessary data collected, I'll able to generate data points (with graphs in future improvements) to improve my recipes.

## Development

Basically, I've been developing using Python3.10 with Poetry. \
For database, DuckDb, it's easy, fast and embedded. \
Unit test are being developed with Pytest/Pycov. \
Sphinx for documentation. (TBD)

## About

It's meant to be a simple application, so I developed it with a focus on an intuitive console command interface.

![screen](assets\images\screen1.png?raw=true)

## Running tests

Install Poetry environment:

```bash
poetry install
```

Running default mode.

```bash
poetry run python -m pytest
```

Generating HTML Coverage Report

```bash
poetry run python -m pytest --cov=. tests/ --cov-report html:cov_html
```

## Install

Building the app:

```bash
poetry build
```

After building, you can find the `tar` and `egg` file on `dist` folder. To install on current system, you might use:

```bash
pip install .\dist\coffeeanalytics-0.1.0.tar.gz
```

Then, you can run the app using:

```bash
coffeea
```