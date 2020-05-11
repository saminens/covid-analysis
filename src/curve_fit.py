from scipy.optimize import curve_fit
from src.transition import transition_curve
import argparse
import pandas as pd
import numpy as np
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


MIN_BOUNDS_B = [0, 100000, 0, 0, 0]
MAX_BOUNDS_B = [99999, 9999999, 10., 2., 1.8]
MIN_BOUNDS_A = [0, 0, 0, 0, 0]
MAX_BOUNDS_A = [99999, 9999999, 10., 2., 1.8]



def prepare_data(input_file_path, country, mitigation_start_date):
    """

    Args:
        input_file_path: path for input file
        country: enter country of choice
        mitigation_start_date: start date of mitigation effects/inflection date

    Returns: data for optimization and plots

    """
    data = pd.read_csv(input_file_path, index_col=None, header=0)
    data = data.drop(['Lat', 'Long', 'Province/State'], axis=1)
    data = data.melt(id_vars="Country/Region", var_name='date', value_name='Confirmed')
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by=['Country/Region', 'date'], inplace=True)
    data = data.pivot_table(index='Country/Region', columns='date', values='Confirmed', aggfunc=np.sum)
    country_data = data.loc[country, :]
    xdata = country_data.index
    ydata = country_data.values
    country_before_m = country_data.loc[:mitigation_start_date]  # slope 1
    country_after_m = country_data.loc[mitigation_start_date:]  # slope 2
    x1 = country_before_m.index
    y1 = country_before_m.values
    x2 = country_after_m.index
    y2 = country_after_m.values
    return x1,y1,x2,y2,xdata,ydata


def plot_curves(popt1, popt2, x2, xdata, ydata, country):
    """

    Args:
        popt1: Optimized parameters before mitigation effects
        popt2: Optimized parameters after mitigation effects
        x2: Index of pivoted data
        xdata: pivoted country data index
        ydata: pivoted country data values
        country: country of choice

    Returns: plots of curve fits

    """
    x1=xdata
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    part_transition = partial(transition_curve, tstart=xdata[0])
    plt.plot(x1, part_transition(x1, *popt1), 'g--')
    plt.plot(x2, part_transition(x2, *popt2), 'b--')
    myFmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(myFmt)
    plt.xlabel('Date')
    plt.ylabel("COVID-19 confirmed cases")
    plt.plot(xdata, ydata)
    plt.grid(which='both')
    # for xy in zip(xdata, ydata):
    #     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
    plt.title(f'Curve fit for {country}')
    plt.xticks(rotation=45)
    ax.legend(["Cases without mitigation", "Cases after mitigation", "Confirmed Cases"], prop={'size': 14})
    plt.show()


def main(input_file_path, country, mitigation_start_date, p0_before, p0_after):
    """

    Args:
        input_file_path:
        country:
        mitigation_start_date:
        p0_before:
        p0_after:

    Returns:

    """
    x1, y1, x2, y2, xdata, ydata = prepare_data(input_file_path, country, mitigation_start_date)
    part_transition = partial(transition_curve, tstart=xdata[0])
    popt1, _ = curve_fit(part_transition, x1, y1, bounds=(MIN_BOUNDS_B, MAX_BOUNDS_B),
                             p0=p0_before)
    popt2, _ = curve_fit(part_transition, x2, y2, bounds=(MIN_BOUNDS_A, MAX_BOUNDS_A),
                             p0=p0_after)
    plot_curves(popt1, popt2, x2, xdata, ydata, country)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-fpth",dest='input_fpth', type=str, help="Provide the path to the input file")
    parser.add_argument("--mitigation-start-date", dest='mitigation_start_date', type=str, help="Mitigation start date")
    parser.add_argument("--country", dest='country', type=str, help="Name of the country to do analysis")
    parser.add_argument('--p0-before', dest='p0_before', nargs='+', help="Initial parameters before mitigation curve")
    parser.add_argument('--p0-after', dest='p0_after', nargs='+', help="Initial parameters after mitigation curve")
    args = parser.parse_args()
    print(main(args.input_fpth,args.country, args.mitigation_start_date, args.p0_before,args.p0_after))

