import random
import string

print("Welcome to password maker !")

adjectives=["sleepy", "slow", "red", "orange", "yellow", "green", "blue", "purple", "fluffy", "white"]

nouns = ["Apple", "Dinosaur", "Ball", "Toaster", "goat", "dragon", "hammer", "duck", "panda"]

def password_maker():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(0, 100)
    special_char = random.choice(string.punctuation)
    password = adjective + noun + str(number) + special_char
    print("Your new password is : "+ password)

while True:
    password_maker()
    response = input("Would you like another password Type y or n : ")
    if response == "n":
        break
    elif response != "y" and "n":
        print("What do you mean ?")
        break