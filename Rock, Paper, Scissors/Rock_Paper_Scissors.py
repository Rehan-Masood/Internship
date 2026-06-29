import random

Rock = '''
    88                
    88                
    88                
8b,dPPYba,  ,adPPYba,  88   ,d8  ,adPPYba,  
88P'   "Y8 a8"     "8a 88 ,a8"  a8P_____88  
88         8b       d8 8888[    8PP"""""""  
88         "8a,   ,a8" 88`"Yba, "8b,   ,aa  
88          `"YbbdP"'  88   `Y8a `"Ybbd8"' 
'''
Paper = ''' 
8b,dPPYba,  ,adPPYYba, 8b,dPPYba,   ,adPPYba, 8b,dPPYba,  
88P'    "8a ""     `Y8 88P'    "8a a8P_____88 88P'   "Y8  
88       d8 ,adPPPPP88 88       d8 8PP""""""" 88          
88b,   ,a8" 88,    ,88 88b,   ,a8" "8b,   ,aa 88          
88`YbbdP"'  `"8bbdP"Y8 88`YbbdP"'   `"Ybbd8"' 88          
'''
Scissors = ''' 
,adPPYba,  ,adPPYba, 88 ,adPPYba, ,adPPYba,  ,adPPYba,  8b,dPPYba, ,adPPYba,  
I8[    "" a8"    "" 88 I8[    "" I8[    "" a8"    "8a 88P'   "Y8 I8[    ""  
 `"Y8ba,  8b         88  `"Y8ba,   `"Y8ba,  8b       d8 88         `"Y8ba,  
aa    ]8I "8a,   ,aa 88 aa    ]8I aa    ]8I "8a,   ,a8" 88        aa    ]8I  
`"YbbdP"'  `"Ybbd8"' 88 `"YbbdP"' `"YbbdP"'  `"YbbdP"'  88        `"YbbdP"'  
'''

Game_images = [Rock, Paper, Scissors]

user_choice = int(input('What do you choose? Type 0 for "Rock", 1 for "Paper" or 2 for "Scissors":\n'))

if user_choice >= 3 or user_choice < 0:
    print("You typed an invalid number, you lose!")
else:
    print("You chose:")
    print(Game_images[user_choice])

    computer_choice = random.randint(0, 2)
    print("Computer chose:")
    print(Game_images[computer_choice])

    if user_choice == computer_choice:
        print("It's a draw!")
    elif (user_choice == 0 and computer_choice == 2) or \
         (user_choice == 1 and computer_choice == 0) or \
         (user_choice == 2 and computer_choice == 1):
        print("You win!")
    else:
        print("You lose!")