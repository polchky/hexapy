from .base_command import BaseCommand

class BLECommand(BaseCommand):
    def __init__(self, config):
        BaseCommand.__init__(config)
        self.update_interval_ms = 500
        self.command_timeout_ms = 1000
        

    def setup(self):
        return 1

    def ready(self):
        return True

    def get_command(self):
        return
