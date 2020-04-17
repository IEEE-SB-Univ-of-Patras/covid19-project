import sir_prediction as sir


def calculate_beta(data):
    beta_list = []
    beta_list_smooth = []
    N = data["N"]
    S_list = data["S list"]
    I_list = data["I list"]
    i_prev = I_list[0]
    s_prev = S_list[0]
    b_prev = 0
    alpha = 0.25

    for t in range(len(S_list)):
        s = S_list[t]
        b = (s_prev - s) / (s_prev * (i_prev + 1)) * N
        beta_list.append(b)
        b_smooth = alpha * b + (1 - alpha) * b_prev
        beta_list_smooth.append(b_smooth)
        i_prev = I_list[t]
        s_prev = s
        b_prev = b_smooth

    data["beta_list"] = beta_list
    data["beta_list_smooth"] = beta_list_smooth
    return data


def calculate_gamma(data, lag=0, smooth=0.2):
    gamma_list = []
    gamma_list_smooth = []
    N = data["N"]
    R_list = data["R list"]
    I_list = data["I list"]
    i_prev = I_list[0]
    r_prev = R_list[0]
    g_prev = 0
    alpha = 1/(lag + 1)

    for t in range(len(R_list)):
        r = R_list[t]
        g = (r - r_prev) / (i_prev + 1)
        if g < 0:
            g = 0
        gamma_list.append(g)
        g_smooth = smooth * g + (1 - smooth) * g_prev
        gamma_list_smooth.append(g_smooth)

        i_prev = alpha * I_list[t] + (1 - alpha) * i_prev
        r_prev = r
        g_prev = g_smooth

    data["gamma_list"] = gamma_list
    data["gamma_list_smooth"] = gamma_list_smooth
    return data


def calculate_death_rate(data, lag=0, smooth=0.2):
    """Death rate = deaths / (deaths[t] + recovered[t])"""
    death_rate_list = []
    death_rate_list_smooth = []
    N = data["N"]
    deaths = data["Deaths list"]
    R_list = data["R list"]
    I_list = data["I list"]
    i_prev = 0
    r_prev = R_list[0]
    d_prev = 0
    death_rate_prev = 0

    for t in range(len(R_list)):
        r = R_list[t]
        d = deaths[t]
        death_rate = d / (r + 1)
        if death_rate < 0:
            death_rate = 0
        death_rate_list.append(death_rate)
        death_rate_smooth = smooth * death_rate + (1 - smooth) * death_rate_prev
        death_rate_list_smooth.append(death_rate_smooth)
        if t >= lag:
            i_prev = I_list[t - lag]
        r_prev = r
        d_prev = d
        death_rate_prev = death_rate_smooth

    data["death_rate_list"] = death_rate_list
    data["death_rate_list_smooth"] = death_rate_list_smooth
    return data


def calculate_lag(data, min, max):
    deaths = data["Deaths list"]
    R_list = data["R list"]
    I_list = data["I list"]
    total_list = data["Total list"]
    true_recovered = []
    ratio = [[] for j in range(max - min)]
    for t, removed in enumerate(R_list):
        true_recovered.append(removed - deaths[t])
        if t >= max:
            for i in range(min, max):
                total = true_recovered[t - i] + deaths[t - i]
                rat = total_list[t - i] / (R_list[t] + 1)
                ratio[i - min].append(rat)
    for i in range(min, max):
        data["ratio," + str(i)] = ratio[i - min]
    return data


def calculate_CFR(data, lag=0, smooth=0.2):
    """CFR = deaths / (deaths[t] + recovered[t])"""
    death_rate_list = []
    death_rate_list_smooth = []
    N = data["N"]
    deaths = data["Deaths list"]
    R_list = data["R list"]
    I_list = data["I list"]
    i_prev = 0
    r_prev = R_list[0]
    d_prev = 0
    death_rate_prev = 0

    for t in range(len(R_list)):
        r = R_list[t]
        d = deaths[t]
        death_rate = d / (r + 1)
        if death_rate < 0:
            death_rate = 0
        death_rate_list.append(death_rate)
        death_rate_smooth = smooth * death_rate + (1 - smooth) * death_rate_prev
        death_rate_list_smooth.append(death_rate_smooth)
        if t >= lag:
            i_prev = I_list[t - lag]
        r_prev = r
        d_prev = d
        death_rate_prev = death_rate_smooth

    data["death_rate_list"] = death_rate_list
    data["death_rate_list_smooth"] = death_rate_list_smooth
    return data


if __name__ == "__main__":
    scen = input("Choose a scenario: ")
    data = sir.init_data(scenario=scen)
    lag = int(input("Lag: "))
    data = calculate_death_rate(data, lag=lag)

    sir.plotting(data, ["death_rate_list_smooth"], scale="linear")






