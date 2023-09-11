
from abc import ABCMeta, abstractmethod


class BPVAppContext(metaclass=ABCMeta):
    @abstractmethod
    def run_app(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def get_selected_index_paths(self):
        pass

    @abstractmethod
    def get_selected_filters(self):
        pass

    @abstractmethod
    def create_active_dataframe(self):
        pass

    @abstractmethod
    def get_txr_sessions(self):
        pass

    @abstractmethod
    def get_master_window(self):
        pass

    @abstractmethod
    def _on_slave_window_close(self, name):
        pass

    @abstractmethod
    def slave_window_op(self, name, op):
        pass

    @abstractmethod
    def spawn_slave_window(self, name, window):
        pass
