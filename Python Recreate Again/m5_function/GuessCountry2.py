def check_guess(guess, answer):
    global score
    still_guessing = True
    attemp = 0
    while still_guessing and attemp < 3:
        if guess.lower() == answer.lower():
            print("Correct answer!")
            score += 1
            still_guessing = False
        else:
            if attemp < 2:
                print("Wrong answer!")
            attemp += 1

score = 0
print("Guess the Country !")

guess1 = input("By Size, what is the largest country in the world ? ")
check_guess(guess1, "russia")
guess2 = input("Which country has a unicorn as its national animal ? ")
check_guess(guess2, "Scotland")
guess3 = input("In which country would you find the currency Bath ? ")
check_guess(guess3, "thailand")

print("Your score is " + str(score))