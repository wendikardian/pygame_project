import random

print("""Winning Rules of the Rock Paper Scissor game as follows:
1. Rock vs Paper -> Paper wins
2. Rock vs Scissor -> Rock wins
3. Paper vs Scissor -> Scissor wins
""")

while True:
    print("""Enter choice :
    1. Rock
    2. Scissor
    3. Paper """)

    choice = int(input("User turn: "))
    while choice > 3 or choice < 1:
        choice = int(input("Enter valid input: "))

    if choice == 1:
        choice_name = "Rock"
    elif choice == 2:
        choice_name = "Scissor"
    else:
        choice_name = "Paper"

    print("User choice is : " + choice_name)

    print("\nNow its computer turn")
    comp_choice = random.randint(1,3)
    if comp_choice == 1:
        comp_choice_name = "Rock"
    elif comp_choice == 2:
        comp_choice_name = "Scissor"
    else:
        comp_choice_name = "Paper"

    print("Computer choice is : " + comp_choice_name)

    if(comp_choice != choice):
        if((choice == 1 and comp_choice == 2) or (choice == 2 and comp_choice ==1 )):
            print("Rock Wins")
            result = "Rock"
        elif((choice == 1 and comp_choice == 3) or (choice == 3 and comp_choice == 1)):
            print("Paper Wins")
            result = "Paper"
        else:
            print("Scissor Wins")
            result = "Scissor"


        if result == choice_name:
            print("<== User wins ==>")
        else:
            print("<== Computer wins ==>")
    else:
        print("<== Tie ==>")

    response = input("\nDo you want to play again ? (Y/N)")

    if response == "n" or response == "N":
        break

print("Thanks for playing !")
