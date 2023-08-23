import numpy as np
import numpy.typing as npt
import scipy.stats
import math


BPSeriesArray = npt.NDArray[np.float32]


def power_over_freq_band(series: BPSeriesArray, sample_rate: float, hf1: float, hf2: float) -> float:
    fft = np.fft.fft(series)
    freq = np.fft.fftfreq(len(series), 1.0 / sample_rate)

    total_power = 0.0

    for power, freq in zip(np.absolute(fft), freq):
        if hf1 <= freq <= hf2:
            total_power += power

    return float(total_power)


def cycling_components_sum(series: BPSeriesArray) -> float:
    series = np.array(series, np.float32)
    f = np.fft.fft(series)
    f_abs = np.abs(f)
    freqs = np.fft.fftfreq(len(series))

    amp_24 = 2.0 * f_abs[np.abs(freqs - 1 / 24).argmin()]
    phase_24 = 1.0 * np.angle(f[np.abs(freqs - 1 / 24).argmin()])
    amp_12 = 2.0 * f_abs[np.abs(freqs - 1 / 12).argmin()]
    phase_12 = 1.0 * np.angle(f[np.abs(freqs - 1 / 12).argmin()])

    return float(np.sum(
        amp_24 * np.cos(2 * np.pi * series / 24 + phase_24) +
        amp_12 * np.cos(2 * np.pi * series / 12 + phase_12)
    ))


def idx_high_freq_power(bp_series: BPSeriesArray, sample_rate: float) -> float:
    return power_over_freq_band(bp_series, sample_rate, 0.15, 0.40)


def idx_low_freq_power(bp_series: BPSeriesArray, sample_rate: float) -> float:
    return power_over_freq_band(bp_series, sample_rate, 0.04, 0.15)


def idx_very_low_freq_power(bp_series: BPSeriesArray, sample_rate: float) -> float:
    return power_over_freq_band(bp_series, sample_rate, 0.003, 0.04)


def idx_residual_variability(bp_series: BPSeriesArray) -> float:
    cc = cycling_components_sum(bp_series)
    rv = 0
    for bp in bp_series:
        rv += pow(bp - cc, 2)
    return rv


def idx_self_similarity_scale_exponents(bp_series: BPSeriesArray) -> float:
    pass


def idx_mean(bp_series: BPSeriesArray) -> float:
    return float(np.mean(bp_series))


def idx_entropy(bp_series: BPSeriesArray, m: int = 5, threshold: int = 12):
    n = len(bp_series)
    count = np.sum(np.abs(np.diff(bp_series[:n - m + 1], n=m)) <= threshold)
    return -math.log(np.max([10e-15, count]) / n)


def idx_standard_deviation(bp_series: BPSeriesArray) -> float:
    return float(np.std(bp_series))


def idx_coeff_of_variation(bp_series: BPSeriesArray) -> float:
    return scipy.stats.variation(bp_series)


def idx_weighted_standard_deviation(bp_series_wake: BPSeriesArray, bp_series_sleep: BPSeriesArray) -> float:
    sd_wake = np.std(bp_series_wake)
    sd_sleep = np.std(bp_series_sleep)
    n_wake = len(bp_series_wake)
    n_sleep = len(bp_series_sleep)

    return (sd_wake * n_wake + sd_sleep * n_sleep) / (n_wake + n_sleep)


def idx_vim(bp_series_matrix: npt.NDArray, idx_individual: int) -> float:
    stddevs = np.std(bp_series_matrix, axis=1)
    means = np.mean(bp_series_matrix, axis=1)
    log_sd = np.log10(stddevs)
    log_mean = np.log10(means)
    x, intercept, r_value, p_value, std_err = scipy.stats.linregress(log_sd, log_mean)
    return stddevs[idx_individual] * pow(np.mean(means), x) / pow(means[idx_individual], x)


def idx_arv(bp_series: BPSeriesArray) -> float:
    return np.average(np.abs(np.ediff1d(bp_series)))


def idx_time_rate(bp_series: BPSeriesArray, arr_mins_since_start: npt.NDArray[np.int32]) -> float:
    return np.average(np.diff(bp_series) / np.diff(arr_mins_since_start))


def idx_range(bp_series: BPSeriesArray) -> float:
    return np.max(bp_series) - np.min(bp_series)


def idx_peak(bp_series: BPSeriesArray) -> float:
    return np.max(bp_series) - np.mean(bp_series)


def idx_through(bp_series: BPSeriesArray) -> float:
    return np.mean(bp_series) - np.min(bp_series)


def idx_max(bp_series: BPSeriesArray) -> float:
    return np.max(bp_series)


def idx_min(bp_series: BPSeriesArray) -> float:
    return np.min(bp_series)


def idx_nocturnal_fall(bp_series_night: BPSeriesArray, bp_series_day: BPSeriesArray) -> float:
    return (np.mean(bp_series_day) - np.mean(bp_series_night)) / np.mean(bp_series_day)


def idx_night_day_ratio(bp_series_night: BPSeriesArray, bp_series_day: BPSeriesArray) -> float:
    return np.mean(bp_series_night) / np.mean(bp_series_day)


def idx_morning_surge(bp_series_morning: BPSeriesArray, bp_series_sleep: BPSeriesArray) -> float:
    return np.mean(bp_series_morning) - np.mean(np.argpartition(bp_series_sleep, 3)[:3])


def idx_siesta_dipping(bp_series_day_w: BPSeriesArray, bp_series_day_s: BPSeriesArray) -> float:
    mean_w = np.mean(bp_series_day_w)
    mean_s = np.mean(bp_series_day_s)
    return (mean_w - mean_s) / mean_s


def idx_postprandial_fall(reading_before_lunch: float, reading_after_lunch: float) -> float:
    return reading_before_lunch - reading_after_lunch


