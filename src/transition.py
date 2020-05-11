import numpy as np

def transition(curve_type,dmax,time_to_max,time_in_lag,launch,time,interval):
    """
    Design a transition curve with given choice of inputs; playing with the parameters p,q
    For more info https://businessperspectives.org/journals/Parametric analysis of the Bass model - Business Perspectives.pdf
    Args:
        curve_type:
        dmax:
        time_to_max:
        time_in_lag:
        launch:
        time:
        interval:

    Returns:

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
        dmax:
        time_to_max:
        time_lag:
        launch:
        time:
        interval:

    Returns:

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


def rapid_curve(dmax,time_to_max,launch,time,interval):
    """

    Args:
        dmax:
        time_to_max:
        launch:
        time:
        interval:

    Returns:

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

if __name__ == '__main__':
    pass
