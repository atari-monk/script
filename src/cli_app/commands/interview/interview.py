from base.base_command import BaseCommand
from .lib.interview import InterviewSimulator

class InterviewCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def execute(self, *args):
        # Set up the interview scenario
        data_file = '../../data/interview_data.json'
        scenario = 'grocery_store_manager'

        # Run the interview
        interview = InterviewSimulator(data_file, scenario)
        interview.conduct_interview()

    @property
    def description(self):
        return "Interview sim."