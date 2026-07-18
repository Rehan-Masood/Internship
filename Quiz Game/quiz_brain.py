import sys

class QuizBrain:

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = self.get_valid_answer(current_question.text)
        self.check_answer(user_answer, current_question.answer)

    def get_valid_answer(self, question_text):
        valid_true = ["true", "t"]
        valid_false = ["false", "f"]

        while True:
            print(f"Q.{self.question_number}: {question_text} (True/False)?: ", end="")
            sys.stdout.flush()
            user_answer = input().strip().lower()

            if user_answer in valid_true:
                return "true"
            elif user_answer in valid_false:
                return "false"
            else:
                print("Invalid input. Please enter True/T or False/F.")

    def check_answer(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")

        print(f"The correct answer was: {correct_answer.capitalize()}.")
        print(f"Your current score is: {self.score}/{self.question_number}.\n")
