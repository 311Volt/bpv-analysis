import csv
from BPSeries import BPSeries
from BPSeriesMetadata import BPSeriesMetadata
import typing
import dateutils


def read_bpv_metadata(filename: str) -> typing.List[BPSeriesMetadata]:
    results = []
    with open(filename, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            begin_date = row["Rozpoczecie_skanowania"]
            day = begin_date[0:2]
            month = begin_date[3:5]
            year = begin_date[6:10]
            time = begin_date[10:15]
            results.append(BPSeriesMetadata(
                id=row["Identyfikator"],
                age=int(row["Wiek"]),
                gender="male" if row["Plec"][0] == 'M' else "female",
                beginTime="{}-{}-{} {}".format(year, month, day, time),
                originalFile=f"RESP_TXR/Raw_data_ABP_{row['Identyfikator']}.csv"
            ))
    return results


def date_string(point_dict) -> str:
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(
        int(point_dict["Rok"]), int(point_dict["Miesiace"]), int(point_dict["Dzien"]),
        int(point_dict["Godzina"]), int(point_dict["Minuta"])
    )


def minutes_between(t1: str, t2: str) -> int:
    t1d = dateutils.str_to_datetime(t1)
    t2d = dateutils.str_to_datetime(t2)

    delta = t2d - t1d
    return int(delta.total_seconds() / 60)


def import_bpv_data(metadata: BPSeriesMetadata) -> BPSeries:
    ts_systolic = []
    ts_diastolic = []
    ts_avg = []
    mins_since_start = []
    timestamps = []

    with open(metadata.originalFile, "r") as rawdatafile:

        reader = csv.DictReader(rawdatafile)
        for row in reader:
            if "Skurczowe" in row and len(row["Skurczowe"].strip()) > 0:
                ts_systolic.append(int(row["Skurczowe"]))
                ts_diastolic.append(int(row["Rozkurczowe"]))
                ts_avg.append(int(row["SCT"]))
                mins_since_start.append(minutes_between(metadata.beginTime, date_string(row)))
                timestamps.append(date_string(row))

    return BPSeries(
        meta=metadata,
        series_systolic=ts_systolic,
        series_diastolic=ts_diastolic,
        series_avg=ts_avg,
        mins_since_start=mins_since_start,
        timestamps=timestamps,
        indices_systolic={},
        indices_diastolic={},
        indices_avg={}
    )
