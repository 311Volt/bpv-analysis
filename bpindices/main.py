import numpy as np


def power_over_freq_band(series, sample_rate, hf1, hf2):
    fft = np.fft.fft(series)
    freq = np.fft.fftfreq(len(series), 1.0 / sample_rate)

    total_power = 0.0

    for power, freq in zip(np.absolute(fft), freq):
        if hf1 <= freq < hf2:
            total_power += power

    return total_power


def idx_high_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.15, 0.40)


def idx_low_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.04, 0.15)


def idx_very_low_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.003, 0.04)


def idx_residual_variability(bp_series):
    pass


def idx_self_similarity_scale_exponents(bp_series):
    pass


def idx_entropy(bp_series):
    pass


def idx_standard_deviation(bp_series):
    return np.std(bp_series)


def idx_coeff_of_variation(bp_series):
    pass


def idx_weighted_standard_deviation(bp_series_wake, bp_series_sleep):
    sd_wake = np.std(bp_series_wake)
    sd_sleep = np.std(bp_series_sleep)
    n_wake = len(bp_series_wake)
    n_sleep = len(bp_series_sleep)

    return (sd_wake * n_wake + sd_sleep * n_sleep) / (n_wake + n_sleep)


def idx_vim(bp_series):
    pass


def idx_arv(bp_series):
    return np.average(np.abs(np.ediff1d(bp_series)))


def idx_time_rate(bp_series):
    pass


def idx_range(bp_series):
    return np.max(bp_series) - np.min(bp_series)


def idx_peak(bp_series):
    pass


def idx_through(bp_series):
    return np.mean(bp_series) - np.min(bp_series)


def idx_nocturnal_fall(bp_series):
    pass


def idx_night_day_ratio(bp_series_night, bp_series_day):
    return np.mean(bp_series_night) / np.mean(bp_series_day)


def idx_morning_surge(bp_series_morning, bp_series_sleep):
    pass


def idx_siesta_dipping(bp_series_day_w, bp_series_day_s):
    mean_w = np.mean(bp_series_day_w)
    mean_s = np.mean(bp_series_day_s)
    return (mean_w - mean_s) / mean_s


def idx_postprandial_fall(bp_series):
    pass


def entry():
    pass


if __name__ == '__main__':
    entry()
