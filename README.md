# covid-analysis
A Framework for quantifying mitigation efforts by various countries. 
The detailed analysis can be found here. [Mitigation Efforts Analysis](https://medium.com/@soujanyas_9480/quantifying-covid-mitigation-efforts-by-countries-4b6e909f8162)

# Installation
```buildoutcfg
git clone https://github.com/saminens/covid-analysis
```
# How to use this repository?

1. Download the data from [John Hopkins Repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)
2. Run the following script in this repository
```buildoutcfg
cd ./covid-analysis
python -m src.curve_fit --input-fpth ~/Desktop/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv --mitigation-start-date 2020-02-18 --p0-before 0 200000 0 0.08333 0 --p0-after 0 83403 5 0.08333 0 --country China
```

# Future Work:

1. Deaths can be modeled in similar fashion.
2. Other parameterized curves can be explored instead of Bass Model Diffusion curves.
