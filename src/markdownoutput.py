import pandas
import os
import matplotlib.pyplot as plt


class MarkdownOutput:
    RESOURCES_DIR_NAME = "resources"

    def __init__(self, output_directory: str, filename: str = "report.md", file_mode: str = "a"):
        self.output_directory = output_directory
        self.resource_directory = os.path.join(self.output_directory, MarkdownOutput.RESOURCES_DIR_NAME)
        self.filename = filename
        self.file_mode = file_mode

        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs(self.resource_directory, exist_ok=True)
        self._open_output_file()
        pass

    def _open_output_file(self):
        self.file = open(os.path.join(self.output_directory, self.filename), self.file_mode)

    def __enter__(self):
        self._open_output_file()
        return self

    def __exit__(self, *args):
        self.file.close()

    def close(self):
        self.file.close()

    def write(self, text: str):
        self.file.write(text)

    def writeln(self, text: str):
        self.write(text + "\n")

    def write_paragraph(self, text: str):
        self.write(text + "\n\n")

    def write_heading(self, text: str, order: int):
        self.write_paragraph("#" * order + " " + text)

    def write_h1(self, text: str):
        self.write_heading(text, 1)

    def write_h2(self, text: str):
        self.write_heading(text, 2)

    def write_h3(self, text: str):
        self.write_heading(text, 3)

    def write_h4(self, text: str):
        self.write_heading(text, 4)

    def _write_tbl_row(self, values, float_format: str = ".4g"):
        values_str = [
            ("{:" + float_format + "}").format(value)
            if isinstance(value, float) else value
            for value in values
        ]
        self.writeln("| {} |".format(" | ".join(values_str)))

    def _write_tbl_heading(self, column_names):
        self._write_tbl_row(column_names)
        self.writeln("|-" * len(column_names) + "|")

    def write_dataframe(self, dataframe: pandas.DataFrame, max_of_col_emphasis=True, float_format=".4g"):
        self._write_tbl_heading([" "] + dataframe.columns)
        # TODO emphasis for max/min elements
        for row in dataframe.itertuples():
            self._write_tbl_row(row, float_format)
        self.writeln("")

    def insert_current_pyplot_figure(self, image_id: str, alt: str = None, **kwargs):
        if alt is None:
            alt = "Figure"
        img_rel_path = os.path.join(MarkdownOutput.RESOURCES_DIR_NAME, "{}.png".format(image_id))
        imgpath = os.path.join(self.output_directory, img_rel_path)
        plt.savefig(fname=imgpath, **kwargs)

        self.write_paragraph("![{}]({})".format(alt, img_rel_path))
