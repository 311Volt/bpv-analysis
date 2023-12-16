import logging

import flask
import threading
import os
import io
from markupsafe import Markup
import markdown
from bpvappcontext import BPVAppContext
from markdowndocument import MarkdownDocument, MarkdownImage


class LivePreviewServer:
    def __init__(self, name, ctx: BPVAppContext, host="127.0.0.1", port=7999):
        self.app = flask.Flask(name)
        self.ctx = ctx
        self.needs_update = False
        self.host = host
        self.port = port

        @self.app.route("/")
        def report_view():
            md = self.ctx.get_current_report().render_to_html()
            preview = ""
            if self.ctx.get_current_analysis_preview() is not None:
                preview = '<div class="current-analysis-preview">{}</div>'\
                    .format(self.ctx.get_current_analysis_preview().render_to_html())
            return flask.render_template("report.html", content=Markup(md), preview=Markup(preview))

        @self.app.route("/img/<imgpath>")
        def imgview(imgpath: str):
            imghash = imgpath.split(".")[0]
            md_img = None
            cur_prev = self.ctx.get_current_analysis_preview()
            if imghash in self._doc().block_dict:
                md_img = self._doc().block_dict[imghash]
            elif cur_prev is not None and imghash in cur_prev.block_dict:
                md_img = cur_prev.block_dict[imghash]
            if md_img is not None:
                return flask.send_file(
                    io.BytesIO(md_img.get_png_data()),
                    download_name=imgpath,
                    mimetype='image/png'
                )
            return flask.Response(status=404)

        @self.app.route("/needs-update")
        def needs_update():
            result = "true" if self.needs_update else "false"
            self.needs_update = False
            return result

    def _doc(self):
        return self.ctx.get_current_report()

    def trigger_update(self):
        self.needs_update = True

    def get_addr(self):
        return "http://{}:{}".format(self.host, self.port)

    def run(self, **kwargs):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        self.app.run(host=self.host, port=self.port, **kwargs)

    def run_async(self, **kwargs):
        threading.Thread(target=lambda: self.run(**kwargs)).start()


