
import csv
import datetime
import json

def read_metadata(filename):
    results = []
    with open(filename, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            begin_date = row["Rozpoczecie_skanowania"]
            day = begin_date[0:2]
            month = begin_date[3:5]
            year = begin_date[6:10]
            time = begin_date[10:15]
            results.append({
                "id": row["Identyfikator"],
                "age": int(row["Wiek"]),
                "gender": "male" if row["Plec"][0] == 'M' else "female",
                "beginTime": "{}-{}-{} {}".format(year, month, day, time),
                "datapath": "RESP_TXR/Raw_data_ABP_{}.csv".format(row["Identyfikator"])
            })
    return results


def date_string(point_dict):
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(
        int(point_dict["Rok"]), int(point_dict["Miesiace"]), int(point_dict["Dzien"]),
        int(point_dict["Godzina"]), int(point_dict["Minuta"])
    )


def minutes_between(t1, t2):
    t1d = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M")
    t2d = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M")

    delta = t2d - t1d
    return int(delta.total_seconds() / 60)


def read_raw_data(metadata):
    ts_systolic = []
    ts_diastolic = []
    ts_avg = []
    mins_since_start = []

    with open(metadata["datapath"], "r") as rawdatafile:

        reader = csv.DictReader(rawdatafile)
        for row in reader:
            if "Skurczowe" in row and len(row["Skurczowe"].strip())>0:
                ts_systolic.append(int(row["Skurczowe"]))
                ts_diastolic.append(int(row["Rozkurczowe"]))
                ts_avg.append(int(row["SCT"]))
                mins_since_start.append(minutes_between(metadata["beginTime"], date_string(row)))

    return {
        "seriesSystolic": ts_systolic,
        "seriesDiastolic": ts_diastolic,
        "seriesAverage": ts_avg,
        "minsSinceStart": mins_since_start,
        "avgSamplesPerHour": len(mins_since_start) / (mins_since_start[-1] / 60)
    }