""" Try to predict the spread of the Coronavirus.
    Perfect your model, collect data, or present your
    simulation in new ways."""

# Imports
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import worldometer_scrapping


R0 = 2.48  # Basic Reproductive Rate
days_of_infectivity = 11
recovery_rate = 1 / days_of_infectivity
transmission_rate = R0 * recovery_rate


def init_data(scenario="world"):
    # 22nd of January is the starting date
    timestamp_start = 1579651200
    if scenario == "without China":
        data = worldometer_scrapping.mine_data(scope="world")
    else:
        data = worldometer_scrapping.mine_data(scope=scenario)
    # Population of simulation
    n = data["demographics"]["population"]  # Here, it is the population of the entire planet

    total_list = data["cases"]
    deaths_list = data["deaths"]
    R_list = data["recovered"]
    I_list = data["active"]
    S_list = []
    for i, val in enumerate(total_list):
        S_list.append(n - val)

    new_cases_list = []
    date_list = []
    death_rate = []
    for i, val in enumerate(total_list):
        if i == 0:
            new_cases_list.append(val)
        else:
            new_cases_list.append(val - total_list[i - 1])
        date_list.append(timestamp_start + i * 24 * 3600)
        rate = deaths_list[i] / (R_list[i] + 1)
        death_rate.append(rate)

    if scenario == "without China":
        data_ = worldometer_scrapping.mine_data(scope="China")
        n -= data_["demographics"]["population"]
        for i, val in enumerate(total_list):
            total_list[i] = val - data_["cases"][i]
        for i, val in enumerate(deaths_list):
            deaths_list[i] = val - data_["deaths"][i]
        for i, val in enumerate(R_list):
            R_list[i] = val - data_["recovered"][i]
        for i, val in enumerate(I_list):
            I_list[i] = val - data_["active"][i]

        S_list = []
        for i, val in enumerate(total_list):
            S_list.append(n - val)

        new_cases_list = []
        death_rate = []
        for i, val in enumerate(total_list):
            if i == 0:
                new_cases_list.append(val)
            else:
                new_cases_list.append(val - total_list[i - 1])
            rate = deaths_list[i] / (R_list[i] + 1)
            death_rate.append(rate)

    data = {"N": n, "T start": timestamp_start, "Total list": total_list, "Deaths list": deaths_list,
            "R list": R_list, "I list": I_list, "S list": S_list, "New cases list": new_cases_list,
            "Date list": date_list, "Death rate": death_rate}
    return data


def weigh_by_death_rate(data):
    actual_i_list = []
    actual_death_rate = 0.034
    previously_recovered = 0
    for i, val in enumerate(data["I list"]):
        if i > 46:
            actual_death_rate += 0.03 / 25

        ratio = data["Death rate"][i] / actual_death_rate
        if ratio < 1.01:
            ratio = 1.01
        actual_recovered = data["R list"][i] * ratio
        dr_dt_actual = actual_recovered - previously_recovered
        actual_i_list.append(dr_dt_actual / recovery_rate)
        previously_recovered = actual_recovered

    data["Actual I list"] = actual_i_list
    return data


def calculate_recovery_rate(data):
    recov_rate_list = []
    prev = 0
    for j, val in enumerate(data["R list"]):
        dr_dt = val - prev
        k = dr_dt / (data["I list"][j] + 1)
        recov_rate_list.append(k)
        prev = val
    data["Recovery rate list"] = recov_rate_list
    return data


def calculate_r_0(data):
    N = data["N"]

    s_list = data["S list"]
    i_list = data["I list"]

    c_list = [2.5]
    for j, val in enumerate(i_list):
        if j > 0:
            di_ds = (val - i_list[j-1]) / (s_list[j] - s_list[j - 1])
            c = 1 / (di_ds + 1)
            c = c * N / s_list[j]
            c_list.append(c)
    return c_list


def sir_method(data, b=transmission_rate, k=recovery_rate, start=0, duration=90):

    date_list = data["Date list"][:-start]
    S_list = data["S list"][:-start]
    R_list = data["R list"][:-start]
    I_list = data["I list"][:-start]
    N = data["N"]
    total_list = data["Total list"][:-start]
    new_cases_list = data["New cases list"][:-start]
    deaths_list = data["Deaths list"][:-start]
    death_rate = data["Death rate"][:-start]

    print(total_list)

    for j in range(duration):
        # Calculating the date i + 1 days after today
        date = date_list[-1] + 24 * 3600
        date_list.append(date)

        S = S_list[-1]
        R = R_list[-1]
        I = I_list[-1]

        s = S_list[-1]/N
        r = R_list[-1]/N
        i = I_list[-1]/N
        i_r = 0
        for day in range(-2, 8, 1):
            i_r += 0.1 * (new_cases_list[-days_of_infectivity + day])/N

        ds_dt = -b*s*i
        dr_dt = i_r
        di_dt = -(ds_dt + dr_dt)

        rnew = int((dr_dt) * N)
        snew = int((ds_dt) * N)
        inew = int((di_dt) * N)

        R_list.append(R + rnew)
        S_list.append(S + snew)
        I_list.append(I + inew)
        total_list.append(total_list[-1] - snew)
        new_cases_list.append(-snew)
        deaths_list.append(deaths_list[-1] + int(death_rate[-1] * rnew))
        death_rate.append(death_rate[-1])

        # Printing each days information
        print(str(datetime.date.fromtimestamp(date)) + ": " + str(format(-snew, ',d')) + " new cases and "
              + str(format(total_list[-1], ',d')) + " total cases and "
              + str(format(deaths_list[-1], ',d')) + " deaths.")

    data["Total list"] = total_list
    data["Deaths list"] = deaths_list
    data["R list"] = R_list
    data["I list"] = I_list
    data["S list"] = S_list
    data["New cases list"] = new_cases_list
    data["Date list"] = date_list
    data["Death rate"] = death_rate
    return data


def plotting(data, selection):
    """ This function plots the number of new daily cases, total cases,
        and total deaths against time elapsed in the simulation, using
        matplotlib."""

    dates = data["Date list"]

    y_axis = []
    for sel in selection:
        y_axis.append(np.array(data[sel]))

    for i, date in enumerate(dates):
        dates[i] = datetime.date.fromtimestamp(date)

    t = np.array(dates)

    fig, ax = plt.subplots()
    plt.yscale("linear")
    for pl in y_axis:
        ax.plot(t, pl)

    ax.set(xlabel='Days', ylabel=str(selection),
           title='Flatten the curve, folks')
    ax.grid()

    # fig.savefig("test.png")
    plt.show()


Data = init_data(scenario="South Korea")
print(len(Data["Total list"]))
Data = sir_method(Data, start=50, duration=50)
Data = calculate_recovery_rate(Data)

plotting(Data, ["Total list"])


