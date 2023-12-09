import csv
import typing
import datetime

import dateutils
from txrsession import TxrSession
from txrsessionmetadata import TxrSessionMetadata


def read_txr_sessions_metadata(filename: str, dir_rt: str = "RESP_TXR") -> typing.List[TxrSessionMetadata]:
    results = []
    with open(filename, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            begin_date = row["Rozpoczecie_skanowania"]
            day = begin_date[0:2]
            month = begin_date[3:5]
            year = begin_date[6:10]
            time = begin_date[10:15]

            results.append(TxrSessionMetadata(
                id=row["Identyfikator"],
                age=int(row["Wiek"]),
                gender="male" if row["Plec"][0] == 'M' else "female",
                bmiValue=calculate_bmi(read_float_row(row["Waga"]), read_float_row(row["Wzrost"])),
                waistToHip=0,
                drugsQuantity=read_int_row(row["Leki"]),
                illnessDuration=read_int_row(row["Czas_podawania"]),
                beginTime="{}-{}-{} {}".format(year, month, day, time),
                originalFile=f"{dir_rt}/Raw_data_ABP_{row['Identyfikator']}.csv"
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


def import_txr_session(metadata: TxrSessionMetadata) -> TxrSession:
    ts_systolic = []
    ts_diastolic = []
    ts_bpm = []
    mins_since_start = []
    timestamps = []

    with open(metadata.originalFile, "r") as rawdatafile:

        reader = csv.DictReader(rawdatafile)
        for row in reader:
            if "Skurczowe" in row and len(row["Skurczowe"].strip()) > 0:
                ts_systolic.append(int(row["Skurczowe"]))
                ts_diastolic.append(int(row["Rozkurczowe"]))
                ts_bpm.append(int(row["Czestosc pracy serca"]))

                datestr = date_string(row)
                mins_since_start.append(minutes_between(metadata.beginTime, datestr))
                timestamps.append(datestr)

    return TxrSession(
        meta=metadata,
        series_systolic=ts_systolic,
        series_diastolic=ts_diastolic,
        series_bpm=ts_bpm,
        mins_since_start=mins_since_start,
        timestamps=timestamps
    )


def batch_import_txr_sessions(metadata_filename: str, dir_rt: str = "RESP_TXR") -> typing.List[TxrSession]:
    return [import_txr_session(meta) for meta in read_txr_sessions_metadata(metadata_filename, dir_rt)]

def read_float_row(row):
    if row == "nan":
        return 0
    return float(row)

def read_int_row(row):
    if row == "nan":
        return 0
    return int(row)

def calculate_bmi(weight, height):
    if height == 0:
        return 0
    return weight / pow(height, 2)