import numpy as np

import indices
import datareader
import json
import scipy
import scipy.stats
import matplotlib.pyplot as plt
import pandas as pd


def series_for_param(metadata, lparam):
    ret = []
    for row in metadata:
        ret.append(lparam(row))
    return ret


def normality_test(series):
    return scipy.stats.shapiro(series).pvalue >= 0.05


def meta_where_gender(meta, gender):
    return [row for row in meta if row["gender"] == gender]

def meta_where_age_valid(meta):
    return [row for row in meta if row["age"] < 100]


def entry_point():
    meta = datareader.read_metadata("RESP_metadata.csv")
    meta1 = list()
    for entry in meta:
        raw = datareader.read_raw_data(entry)
        if len(raw["seriesSystolic"]) == 0:
            continue

        entry1 = entry
        entry1["indices_systolic"] = indices.all_indices(raw["seriesSystolic"])
        entry1["indices_diastolic"] = indices.all_indices(raw["seriesDiastolic"])
        entry1["indices_avg"] = indices.all_indices(raw["seriesAverage"])
        meta1.append(entry1)
        # print(json.dumps(datareader.read_raw_data(entry), indent=4))
        # break
    print(json.dumps(meta1, indent=4))

    metaf = meta_where_gender(meta1, "female")
    metam = meta_where_gender(meta1, "male")
    metaa = meta_where_age_valid(meta1)

    keys = ["mean", "entropy", "stddev", "coeff_of_variation", "arv", "range", "peak", "through"]

    pvalue_test = {
        "female": dict(),
        "male": dict()
    }
    mean = {
        "female": dict(),
        "male": dict()
    }
    for key in keys:
        pvalue_test["female"][key] = scipy.stats.shapiro(
            series_for_param(metaf, lambda row: row["indices_avg"][key])).pvalue
        pvalue_test["male"][key] = scipy.stats.shapiro(
            series_for_param(metam, lambda row: row["indices_avg"][key])).pvalue
        mean["female"][key] = float(np.mean(
            np.array(series_for_param(metaf, lambda row: row["indices_avg"][key]))))
        mean["male"][key] = float(np.mean(
            np.array(series_for_param(metam, lambda row: row["indices_avg"][key]))))
    # mean = time_series_for_param(meta1, lambda row: row["indices_avg"]["mean"])

    arv_f = series_for_param(metaf, lambda row: row["indices_avg"]["arv"])
    arv_m = series_for_param(metam, lambda row: row["indices_avg"]["arv"])

    print(json.dumps({"pvalue": pvalue_test, "mean": mean}, indent=4))

    fig, axs = plt.subplots(1, 2)

    axs[0].set_title("arv histogram for females")
    axs[0].hist(arv_f, bins=20)
    axs[1].set_title("arv histogram for males")
    axs[1].hist(arv_m, bins=20)

    plt.figure()
    dfdata = []
    for gender in ["male", "female"]:
        for key in keys:
            dfdata.append([key, gender, mean[gender][key]])
    df = pd.DataFrame(dfdata, columns=["Index", "Gender", "Value"])
    df.pivot("Index", "Gender", "Value").plot(kind='bar')

    q3age = series_for_param(metaa, lambda row: row["age"])
    q3arv = series_for_param(metaa, lambda row: row["indices_avg"]["arv"])

    plt.figure()
    plt.title("Age vs ARV (corr: Pearson = {:.2f}, Spearman = {:.2f})".format(
        float(scipy.stats.pearsonr(q3age, q3arv)[0]),
        float(scipy.stats.spearmanr(q3age, q3arv)[0])
    ))
    plt.xlabel("Age")
    plt.ylabel("ARV")
    plt.scatter(q3age, q3arv)

    plt.figure()
    plt.title()

    plt.show()


if __name__ == '__main__':
    entry_point()
