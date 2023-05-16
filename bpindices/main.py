
import indices
import datareader
import json


def entry_point():
    meta = datareader.read_metadata("RESP_metadata.csv")
    for entry in meta:
        print(json.dumps(datareader.read_raw_data(entry), indent=4))
        break



if __name__ == '__main__':
    entry_point()
