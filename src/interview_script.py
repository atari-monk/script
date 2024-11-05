import json

class InterviewSimulator:
    def __init__(self, data_file, scenario):
        # Load interview data
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        
        self.scenario = self.data['scenarios'][scenario]
        self.questions = self.scenario['questions']
        self.score = 0
        self.total_questions = len(self.questions)

    def conduct_interview(self):
        print("Starting the interview for the position: Grocery Store Manager\n")
        
        for idx, question_data in enumerate(self.questions):
            panel_member = question_data["panel_member"]
            question = question_data["question"]
            choices = question_data["choices"]
            correct_answer = question_data["correct_answer"]
            
            # Display the question and choices
            print(f"{panel_member}: {question}")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            
            # Get the applicant's answer
            answer_index = int(input("Select your answer (1, 2, or 3): ")) - 1
            applicant_answer = choices[answer_index]
            
            # Check if the answer is correct
            if applicant_answer == correct_answer:
                print("Correct!\n")
                self.score += 1
            else:
                print(f"Incorrect. The correct answer was: {correct_answer}\n")
        
        # Final score
        print(f"Interview completed! Your score: {self.score}/{self.total_questions}")

# Set up the interview scenario
data_file = '../data/interview_data.json'
scenario = 'grocery_store_manager'

# Run the interview
interview = InterviewSimulator(data_file, scenario)
interview.conduct_interview()
