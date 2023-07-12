import typing

import numpy as np
import scipy.stats
import math


def power_over_freq_band(series, sample_rate, hf1, hf2):
    fft = np.fft.fft(series)
    freq = np.fft.fftfreq(len(series), 1.0 / sample_rate)

    total_power = 0.0

    for power, freq in zip(np.absolute(fft), freq):
        if hf1 <= freq <= hf2:
            total_power += power

    return total_power


def cycling_components_sum(series):
    f = np.fft.fft(series)
    f_abs = np.abs(f)
    freqs = np.fft.fftfreq(len(series))

    amp_24 = 2 * f_abs[np.abs(freqs - 1 / 24).argmin()]
    phase_24 = np.angle(f[np.abs(freqs - 1 / 24).argmin()])
    amp_12 = 2 * f_abs[np.abs(freqs - 1 / 12).argmin()]
    phase_12 = np.angle(f[np.abs(freqs - 1 / 12).argmin()])

    return np.sum(
        amp_24 * np.cos(2 * np.pi * series / 24 + phase_24) + amp_12 * np.cos(2 * np.pi * series / 12 + phase_12))


def idx_high_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.15, 0.40)


def idx_low_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.04, 0.15)


def idx_very_low_freq_power(bp_series, sample_rate):
    return power_over_freq_band(bp_series, sample_rate, 0.003, 0.04)


def idx_residual_variability(bp_series):
    cc = cycling_components_sum(bp_series)
    rv = 0
    for bp in bp_series:
        rv += pow(bp - cc, 2)
    return rv


def idx_self_similarity_scale_exponents(bp_series):
    pass


def idx_mean(bp_series):
    return np.mean(bp_series)


def idx_entropy(bp_series, m=5, threshold=12):
    n = len(bp_series)
    count = np.sum(np.abs(np.diff(bp_series[:n - m + 1], n=m)) <= threshold)
    return -math.log(np.max([10e-15, count]) / n)


def idx_standard_deviation(bp_series):
    return np.std(bp_series)


def idx_coeff_of_variation(bp_series):
    return scipy.stats.variation(bp_series)


def idx_weighted_standard_deviation(bp_series_wake, bp_series_sleep):
    sd_wake = np.std(bp_series_wake)
    sd_sleep = np.std(bp_series_sleep)
    n_wake = len(bp_series_wake)
    n_sleep = len(bp_series_sleep)

    return (sd_wake * n_wake + sd_sleep * n_sleep) / (n_wake + n_sleep)


def idx_vim(bp_series_multiple, individual):
    sds = [np.std(bp_series) for bp_series in bp_series_multiple]
    means = [np.mean(bp_series) for bp_series in bp_series_multiple]
    log_sd = np.log10(sds)
    log_mean = np.log10(means)
    x, intercept, r_value, p_value, std_err = scipy.stats.linregress(log_sd, log_mean)
    return sds[individual] * pow(np.mean(means), x) / pow(means[individual], x)


def idx_arv(bp_series):
    return np.average(np.abs(np.ediff1d(bp_series)))


def idx_time_rate(bp_series, time_series):
    n = len(bp_series) - 1
    total = 0
    for i in range(n - 1):
        total += np.abs(bp_series[i + 1] - bp_series[i]) / (time_series[i + 1] - time_series[i])
    return total / n


def idx_range(bp_series):
    return np.max(bp_series) - np.min(bp_series)


def idx_peak(bp_series):
    return np.max(bp_series) - np.mean(bp_series)


def idx_through(bp_series):
    return np.mean(bp_series) - np.min(bp_series)


def idx_nocturnal_fall(bp_series_night, bp_series_day):
    return (np.mean(bp_series_day) - np.mean(bp_series_night)) / np.mean(bp_series_day)


def idx_night_day_ratio(bp_series_night, bp_series_day):
    return np.mean(bp_series_night) / np.mean(bp_series_day)


def idx_morning_surge(bp_series_morning, bp_series_sleep):
    return np.mean(bp_series_morning) - np.mean(np.argpartition(bp_series_sleep, 3)[:3])


def idx_siesta_dipping(bp_series_day_w, bp_series_day_s):
    mean_w = np.mean(bp_series_day_w)
    mean_s = np.mean(bp_series_day_s)
    return (mean_w - mean_s) / mean_s


def idx_postprandial_fall(reading_before_lunch, reading_after_lunch):
    return reading_before_lunch - reading_after_lunch


bpv_index_functions = {
    "residual_variability": idx_residual_variability,
    "mean": idx_mean,
    "entropy": idx_entropy,
    "stddev": idx_standard_deviation,
    "coeff_of_variation": idx_coeff_of_variation,
    "arv": idx_arv,
    "range": idx_range,
    "peak": idx_peak,
    "through": idx_through
}

bpv_all_indices: typing.List[str] = list(bpv_index_functions.keys())


def calculate_index(bp_series: typing.List[float], idxname: str) -> float:
    series_np = np.array(bp_series, dtype=np.float32)
    return float(bpv_index_functions[idxname](series_np))


def all_indices(bp_series):
    return {idx: calculate_index(bp_series, idx) for idx in bpv_index_functions}
