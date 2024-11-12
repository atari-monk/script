from base.base_command import BaseCommand
from commands.adaptive_systems.lib.temperature_control import TemperatureControlSystem

class TemperatureControlCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Target temperature is set to 22.0 degrees
        target_temperature = 22.0
        temperature_system = TemperatureControlSystem(target_temperature)
        temperature_system.run()

    @property
    def description(self):
        return "Temperature Control System."
    