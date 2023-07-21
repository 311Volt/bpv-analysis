import pandas as pd
import json


def parse_table_to_data_frame(json_file):
    with open(json_file) as f:
        data = json.load(f)
        data_frame = pd.json_normalize(data)
        return data_frame


def extract_single_metric_to_data_frame(metric, full_data_frame):
    selected_columns = ['id', 'age', 'gender', f"indices_systolic.{metric}",
                        f"indices_diastolic.{metric}", f"indices_avg.{metric}"]
    data_frame = full_data_frame[selected_columns].copy()
    return data_frame


def data_frame_to_markdown(df):
    markdown_rows = []

    markdown_row = "| " + " | ".join(str(value) for value in df.columns) + " |"
    markdown_rows.append(markdown_row)

    markdown_row = "| " + " | ".join("-" for value in df.columns) + " |"
    markdown_rows.append(markdown_row)

    # Iterate through rows of the DataFrame
    for _, row in df.iterrows():
        # Convert row values to Markdown format
        markdown_row = "| " + " | ".join(str(value) for value in row) + " |"

        # Append the Markdown row to the list
        markdown_rows.append(markdown_row)

    # Convert the list of Markdown rows to a Markdown table
    markdown_table = "\n".join(markdown_rows)
    return markdown_table


def create_md_table_from_data_frame(data_frame, metric):
    df = extract_single_metric_to_data_frame(metric, data_frame)
    max_values = df.max()
    markdown = data_frame_to_markdown(df)

    markdown_rows = markdown.split('\n')

    new_markdown = ""
    title = 0
    for row in markdown_rows:
        split_row = row.split('|')[1:-1]
        new_row = ""
        for i in range(0, len(split_row)):
            if i >= len(split_row) - 3 and title > 1:
                value = float(split_row[i])
                if max_values[i] == value:
                    split_row[i] = "**" + split_row[i].strip() + "**"
            new_row += "|" + split_row[i]
        new_markdown += new_row + "|" + "\n"
        title += 1

    return new_markdown


def create_description_for_metric(data_frame, metric):
    df = extract_single_metric_to_data_frame(metric, data_frame)
    max_values = df.max()

    markdown = data_frame_to_markdown(df)
    markdown_rows = markdown.split('\n')

    ids = ["", "", ""]

    title = 0
    for row in markdown_rows:
        split_row = row.split('|')[1:-1]
        for i in range(0, len(split_row)):
            if i >= len(split_row) - 3 and title > 1:
                value = float(split_row[i])
                if max_values[i] == value:
                    ids[i - (len(split_row) - 3)] = (split_row[0], value)
                    # split_row[i] = "**" + split_row[i].strip() + "**"
        title += 1

    return f"""
        After calculating {metric} for each patient's systolic, diastolic and average
        blood pressure we received following results (see table below).
        As we can see, 
        highest systolic blood pressure was detected for patient {ids[0][0]} and reached {ids[0][1]}.
        Highest diastolic blood pressure was detected for patient {ids[1][0]} and reached {ids[1][1]}.
        Highest average blood pressure was detected for patient {ids[2][0]} and reached {ids[2][1]}. 
    """


def create_markdown_for_metric(data_frame, metric):
    markdown_text = create_description_for_metric(data_frame, metric)
    markdown_table = create_md_table_from_data_frame(data_frame, metric)

    return markdown_text + "\n\n\n" + markdown_table


def write_markdown_for_metric_to_file(data_frame, metric, filename):
    with open(filename, "w") as file:
        file.write(create_markdown_for_metric(data_frame, metric))


write_markdown_for_metric_to_file(parse_table_to_data_frame("../params.json"), "entropy", "entropy.md")
