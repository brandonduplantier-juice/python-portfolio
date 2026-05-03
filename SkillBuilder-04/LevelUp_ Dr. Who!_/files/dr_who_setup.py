# Dictionaries needed for Dr Who Quiz

question_bank = {
    'Which is better on a pizza?': ['OLIVES', 'PINEAPPLE'],
    'Where would you rather be?': ['MOUNTAIN', 'BEACH'],
    'Night Owl or Morning Lark?': ['NIGHT', 'MORNING'],
    'Best way to eat an ice cream?': ['CONE', 'CUP'],
    'What do you prefer to wear?': ['SWEATPANTS', 'JEANS']
}

answer_bank = {
    'Dr. Alvarez':['PINEAPPLE', 'BEACH', 'NIGHT', 'CONE', 'JEANS'],
    'Dr. Crider':['OLIVES', 'MOUNTAIN', 'MORNING', 'CUP', 'SWEATPANTS']
}

# functions
def get_input(options):
    response = input(f'Type your answer: {options[0]} OR {options[1]}?').upper()
    
    return response


def get_user_response_solution(answer_choices):
    # Do NOT follow this function, it explicitly uses
    # concepts not in the course to prevent copy-paste cheating.
    # Follow the guide provide in the notebook
    needs_response = True
    
    while needs_response:
        response = get_input(answer_choices)
        
        needs_response = False if response in answer_choices else print("Didn't get a valid response. Try again!")
            
    return response