from abc import ABCMeta, abstractmethod
import src.bpvappcontext as appctx

class AbstractAnalyzer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, ctx: appctx.BPVAppContext, config: dict):
        pass

    @staticmethod
    @abstractmethod
    def create_config_form(ctx):
        pass

    @abstractmethod
    def process(self, active_dataframe):
        pass

    @abstractmethod
    def present(self):
        pass

    @abstractmethod
    def present_as_markdown(self, output_filename: str):
        pass
