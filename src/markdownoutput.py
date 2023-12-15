import hashlib
import typing

import pandas
import numpy as np
import os
import matplotlib.pyplot as plt

from PIL import Image

from dataclasses import dataclass


def render_current_figure() -> np.ndarray:
    canvas = plt.gcf().canvas
    canvas.draw()
    return np.array(canvas.buffer_rgba())


@dataclass
class MarkdownImage:
    content: np.ndarray
    hash: str
    alt: str

    def src(self) -> str:
        return "img/{}.png".format(self.hash)

    def save(self, root):
        os.makedirs(os.path.join(root, "img"), exist_ok=True)
        path = os.path.join(root, self.src())
        if not os.path.exists(path):
            Image.fromarray(self.content).save(path)

    def render(self) -> str:
        return "\n[{}]({})\n".format(self.alt, self.src())


@dataclass
class MarkdownText:
    text: str

    def render(self) -> str:
        return self.text


class MarkdownOutput:

    def __init__(self, output_directory: str, filename: str = "report.md", file_mode: str = "a"):
        self.output_directory = output_directory
        self.filename = filename
        self.file_mode = file_mode
        self.buffer = []

        os.makedirs(self.output_directory, exist_ok=True)
        self._open_output_file()
        pass

    def _open_output_file(self):
        self.file = open(os.path.join(self.output_directory, self.filename), self.file_mode)

    def __enter__(self):
        self._open_output_file()
        return self

    def __exit__(self, *args):
        self.write_to_filesystem()
        self.file.close()

    def close(self):
        self.file.close()

    def write_to_filesystem(self):
        for obj in self.buffer:
            self.file.write(obj.render())
            if isinstance(obj, MarkdownImage):
                obj.save(self.output_directory)

    def write(self, text: str):
        self.buffer.append(MarkdownText(text=text))

    def writeln(self, text: str = ""):
        self.write(text + "\n")

    def write_paragraph(self, text: str = ""):
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

    def write_bullet_points(self, items: typing.List[str]):
        for item in items:
            self.writeln(" - " + item)
        self.write_paragraph("")

    def write_ordered_list(self, items: typing.List[str]):
        for idx, item in enumerate(items):
            self.writeln("{}. ".format(idx+1) + item)
        self.write_paragraph("")

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
        self._write_tbl_heading(["index"] + list(dataframe.columns))
        # TODO emphasis for max/min elements
        for row in dataframe.itertuples():
            self._write_tbl_row(row, float_format)
        self.writeln("")

    def _get_img_resource_abs_path(self, name):
        return os.path.join(self.output_directory, self._get_img_resource_rel_path(name))

    def insert_current_pyplot_figure(self, image_id: str, alt: str = None, **kwargs):
        if alt is None:
            alt = "Figure"

        img = render_current_figure()
        hash = hashlib.sha1(img).hexdigest()

        obj = MarkdownImage(
            content=img,
            hash=hash,
            alt=alt
        )

        self.buffer.append(obj)
