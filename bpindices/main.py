
import indices
import datareader
import json


def entry_point():
    meta = datareader.read_metadata("RESP_metadata.csv")
    meta1 = list()
    for entry in meta:
        raw = datareader.read_raw_data(entry)
        if len(raw["seriesSystolic"]) == 0:
            continue

        entry1 = entry
        entry1["indices_systolic"] = indices.all_indices(raw["seriesSystolic"])
        entry1["indices_diastolic"] = indices.all_indices(raw["seriesSystolic"])
        entry1["indices_avg"] = indices.all_indices(raw["seriesAverage"])
        meta1.append(entry1)
        # print(json.dumps(datareader.read_raw_data(entry), indent=4))
        #break
    print(json.dumps(meta1, indent=4))


if __name__ == '__main__':
    entry_point()
