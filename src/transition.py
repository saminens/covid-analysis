import numpy as np
from datetime import datetime, timedelta, date
import pandas as pd
import matplotlib.pyplot as plt


def transition(curve_type, dmax, time_to_max, time_in_lag, launch, time, interval):
    """
    Design a transition curve with given choice of inputs; playing with the parameters p,q
    For more info https://businessperspectives.org/journals/Parametric analysis of the Bass model - Business Perspectives.pdf
    Args:
        curve_type: slow uptake - 0, quick uptake - 10
        dmax: max difference between initial value and final
        time_to_max: time to peak
        time_in_lag: the inflection duration
        launch: date of start
        time: end date/inflection date
        interval: for monthly 1/12

    Returns: transition

    """
    # Limit curve type from 0-10
    if curve_type<0:
        curve_type=0
    elif curve_type>10:
        curve_type=10
    else:
        curve_type=curve_type
    # Test for pure S curve using lag parameter
    if time_in_lag==0:
        time_lag=time_to_max/4
    else:
        time_lag=time_in_lag
    # Calculate weight of curve type
    scurve=1-(curve_type/10)
    srapidcurve=1-scurve
    if time_to_max<0:
        transition=0
    else:
        transition=scurve*S_shape_curve(dmax,time_to_max,time_lag,launch,time,interval)+\
        srapidcurve*rapid_curve(dmax,time_to_max,launch,time,interval)
    return transition


def S_shape_curve(dmax, time_to_max, time_lag, launch, time, interval):
    """

    Args:
        dmax: max difference between initial value and final
        time_to_max: time to peak
        time_lag: the inflection duration
        launch: date of start
        time: end date/inflection date
        interval: for monthly 1/12

    Returns: S_shape_curve


    """
    launch = time_index(launch)
    time = time_index(time)
    if time_to_max == time_lag or time_to_max == 0:
        if time_to_max < 0:
            time_to_max = 0
            S_shape_curve = step_func(0, dmax, launch + time_to_max, time, interval)

    if interval != 0:
        lower = max(time, launch)
        upper = max(time + interval, launch)
        con = 1 / (1 - time_lag / time_to_max) * np.log((1 / 0.15 - 1) / ((1 / 0.98 - 1) ** (time_lag / time_to_max)))
        slo = 1 / time_to_max * (np.log(1 / 0.98 - 1) - con)
        lower_limit = dmax / slo * ((con + slo * (lower - launch)) - np.log(1 + np.exp(con + slo * (lower - launch))))
        upper_limit = dmax / slo * ((con + slo * (upper - launch)) - np.log(1 + np.exp(con + slo * (upper - launch))))
        S_shape_curve = (upper_limit - lower_limit) / interval
    return S_shape_curve


def rapid_curve(dmax, time_to_max,launch,time,interval):
    """

    Args:
        dmax: max difference between initial value and final
        time_to_max: time to peak
        launch: date of start
        time: end date/inflection date
        interval: for monthly 1/12

    Returns: rapid_curve

    """
    launch=time_index(launch)
    time=time_index(time)
    if time_to_max<=0:
        rapid_curve=step_function(0, dmax, launch, time, interval)
    if interval!=0:
        lower=max(time,launch)
        upper=max(time+interval,launch)
        slo=np.log(1-0.98)*-1/time_to_max
        lower_limit=dmax *(lower+1/slo*np.exp(-(slo*(lower-launch))))
        upper_limit=dmax *(upper+1/slo*np.exp(-(slo*(upper-launch))))
        rapid_curve=(upper_limit-lower_limit)/interval
    return rapid_curve


def time_index(time):
    """

    Args:
        time: end date/inflection date

    Returns: time_index

    """
#     time=datetime.strptime(time, '%Y-%m-%d')
    if isinstance(time,date):
        time_index=(time.year+(time.month-1)/12 + (time.day-1)/365)
    else:
        if time.isnumeric():
            time_index=time
        else:
            time_index=1/0
    return time_index


def step_function(start, end, launch, time, interval):
    """

    Args:
        start: start value
        end: end value
        launch: date of start
        time: end date/inflection date
        interval: for monthly 1/12

    Returns: step_function

    """
    if time+interval<=launch:
        step_function=start*interval
    elif time>=launch:
        step_function=end*interval
    else:
        weight=(launch-time)/interval
        step_function=weight*start+(1-weight)*end


def transition_curve(datelist, initial_val, final_val, ct, t2p, tlag, tstart):
    """

    Args:
        datelist: dates before/after inflection point
        initial_val: initial guess
        final_val: peak value
        ct: a.k.a. curve type; slow uptake - 0, quick uptake - 10
        t2p: a.k.a. time to peak
        tlag: a.k.a. time_in_lag; the inflection duration
        tstart: start date

    Returns: transition curve

    """
    transition_values = []
    for dt in datelist:
        tr_value = initial_val + transition(ct,final_val-initial_val,t2p,tlag,tstart,dt,1/365)
        transition_values.append(tr_value)
    return transition_values


if __name__ == '__main__':
    datelist = pd.date_range('2019-12-01', end='2020-12-01', freq='M', name='str').date.tolist()
    plt.plot(transition_curve(datelist, 0, 1, 0, 11 / 12, 0, datelist[0]))
    plt.plot(transition_curve(datelist, 0, 1, 5, 11 / 12, 0, datelist[0]))
    plt.plot(transition_curve(datelist, 0, 1, 10, 11 / 12, 0, datelist[0]))
    plt.legend(['Slow uptake', 'Linear uptake', 'Fast uptake'])
    plt.title("Variation of uptakes with respect to curve type")
    plt.xlabel("Time(in Months)")
    plt.grid(b=True, which='major')
    plt.show()
    print("Sucessful")
