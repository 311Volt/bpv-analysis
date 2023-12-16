import hashlib
import typing

import pandas
import numpy as np
import os
import io
import matplotlib.pyplot as plt

from abc import ABCMeta, abstractmethod
from PIL import Image
from dataclasses import dataclass


class MarkdownNode(metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def hash(self) -> str:
        pass

    def save(self, root_dir):
        pass


class MarkdownImage(MarkdownNode):
    pngdata: bytes
    imghash: str
    alt: str

    def __init__(self, content: np.ndarray, alt: str):
        self.alt = alt
        with io.BytesIO() as bio:
            Image.fromarray(content).save(bio, format='png')
            self.pngdata = bio.getvalue()
        self.imghash = hashlib.sha1(self.pngdata).hexdigest()

    @staticmethod
    def of_current_pyplot_figure():
        canvas = plt.gcf().canvas
        canvas.draw()
        return MarkdownImage(np.array(canvas.buffer_rgba()), plt.gcf().axes[0].get_title())

    def src(self) -> str:
        return "img/{}.png".format(self.imghash)

    def hash(self) -> str:
        return self.imghash

    def get_png_data(self):
        return self.pngdata

    def save(self, root_dir):
        os.makedirs(os.path.join(root_dir, "img"), exist_ok=True)
        path = os.path.join(root_dir, self.src())

        if not os.path.exists(path):
            with open(path, "wb") as outfile:
                outfile.write(self.pngdata)

    def render(self) -> str:
        return "\n![{}]({})\n".format(self.alt, self.src())


@dataclass
class MarkdownText(MarkdownNode):
    text: str

    def render(self) -> str:
        return self.text

    def hash(self) -> str:
        return hashlib.sha1(self.text.encode('utf-8')).hexdigest()


class MarkdownDocument(MarkdownNode):

    def __init__(self):
        self.block_dict: typing.Dict[str, MarkdownNode] = dict()
        self.block_hash_seq: typing.List[str] = []
        pass

    def _blocks(self):
        return [self.block_dict[blk_hash] for blk_hash in self.block_hash_seq]

    def render(self):
        result = ""
        for blk in self._blocks():
            result += blk.render()
        return result

    def hash(self) -> str:
        h = hashlib.new('sha1')
        for blk in self._blocks():
            h.update(blk.hash())
        return h.hexdigest()

    def save_to_directory(self, output_dir):
        for blk_hash in self.block_hash_seq:
            self.block_dict[blk_hash].save(output_dir)
        with open(os.path.join(output_dir, "report.md")) as out_md_file:
            out_md_file.write(self.render())

    def add_block(self, block: MarkdownNode):
        blk_hash = block.hash()
        self.block_dict[blk_hash] = block
        self.block_hash_seq.append(blk_hash)

    def write(self, text: str):
        self.add_block(MarkdownText(text=text))

    def writeln(self, text: str = ""):
        self.write(text+"\n")

    def write_paragraph(self, text: str = ""):
        self.write(text+"\n\n")

    def write_heading(self, text: str, order: int):
        self.write_paragraph("#"*order+" "+text)

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
            self.writeln(" - "+item)
        self.write_paragraph("")

    def write_ordered_list(self, items: typing.List[str]):
        for idx, item in enumerate(items):
            self.writeln("{}. ".format(idx+1)+item)
        self.write_paragraph("")

    def _write_tbl_row(self, values, float_format: str = ".4g"):
        values_str = [
            ("{:"+float_format+"}").format(value)
            if isinstance(value, float) else value
            for value in values
        ]
        self.writeln("| {} |".format(" | ".join(values_str)))

    def _write_tbl_heading(self, column_names):
        self._write_tbl_row(column_names)
        self.writeln("|-"*len(column_names)+"|")

    def write_dataframe(self, dataframe: pandas.DataFrame, max_of_col_emphasis=True, float_format=".4g"):
        self._write_tbl_heading(["index"]+list(dataframe.columns))
        # TODO emphasis for max/min elements
        for row in dataframe.itertuples():
            self._write_tbl_row(row, float_format)
        self.writeln("")

    def write_subdocument(self, document: MarkdownNode):
        self.add_block(document)

    def insert_current_pyplot_figure(self):
        self.add_block(MarkdownImage.of_current_pyplot_figure())
