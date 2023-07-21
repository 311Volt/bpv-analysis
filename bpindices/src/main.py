import numpy as np

import datareader
import dataextractor


def entry_point():
    sessions = datareader.batch_import_txr_sessions("RESP_metadata.csv")

    mtx = dataextractor.create_data_frame(
        sessions=sessions,
        extractor_name="systolic",
        filter_names=["age_valid"],
        index_names=["mean", "stddev", "arv"]
    )

    print(mtx)

    # print(json.dumps([dataclasses.asdict(dat) for dat in sessions], indent=4))

    # keys = ["mean", "entropy", "stddev", "coeff_of_variation", "arv", "range", "peak", "through"]
    #
    # pvalue_test = {
    #     "female": dict(),
    #     "male": dict()
    # }
    # mean = {
    #     "female": dict(),
    #     "male": dict()
    # }
    # for key in keys:
    #     pvalue_test["female"][key] = scipy.stats.shapiro(series_for_param(metaf, lambda row: row["indices_avg"][key])).pvalue
    #     pvalue_test["male"][key] = scipy.stats.shapiro(series_for_param(metam, lambda row: row["indices_avg"][key])).pvalue
    #     mean["female"][key] = float(np.mean(np.array(series_for_param(metaf, lambda row: row["indices_avg"][key]))))
    #     mean["male"][key] = float(np.mean(np.array(series_for_param(metam, lambda row: row["indices_avg"][key]))))
    # # mean = time_series_for_param(meta1, lambda row: row["indices_avg"]["mean"])
    #
    # arv_f = series_for_param(metaf, lambda row: row["indices_avg"]["arv"])
    # arv_m = series_for_param(metam, lambda row: row["indices_avg"]["arv"])
    #
    # print(json.dumps({"pvalue": pvalue_test, "mean": mean}, indent=4))
    #
    # fig, axs = plt.subplots(1, 2)
    #
    # axs[0].set_title("arv histogram for females")
    # axs[0].hist(arv_f, bins=20)
    # axs[1].set_title("arv histogram for males")
    # axs[1].hist(arv_m, bins=20)
    #
    # plt.figure()
    # dfdata = []
    # for gender in ["male", "female"]:
    #     for key in keys:
    #         dfdata.append([key, gender, mean[gender][key]])
    # df = pd.DataFrame(dfdata, columns=["Index", "Gender", "Value"])
    # df.pivot("Index", "Gender", "Value").plot(kind='bar')
    #
    # q3age = series_for_param(metaa, lambda row: row["age"])
    # q3arv = series_for_param(metaa, lambda row: row["indices_avg"]["arv"])
    #
    # plt.figure()
    # plt.title("Age vs ARV (corr: Pearson = {:.2f}, Spearman = {:.2f})".format(
    #     float(scipy.stats.pearsonr(q3age, q3arv)[0]),
    #     float(scipy.stats.spearmanr(q3age, q3arv)[0])
    # ))
    # plt.xlabel("Age")
    # plt.ylabel("ARV")
    # plt.scatter(q3age, q3arv)
    #
    # plt.figure()
    # plt.title()
    #
    # plt.show()


if __name__ == '__main__':
    entry_point()
