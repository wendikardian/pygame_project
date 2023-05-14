apple = 3
fox = 4


print(apple == fox)
print(apple != fox)
print(apple < fox)
print(apple > fox)

print((apple == 3) and (fox == 2))
print((apple == 3) and (fox == 4))
print((apple == 3) or (fox == 2))


is_dark = input("Is it dark outside ? y/n")
if is_dark == "y":
    print("Good night! Zzz....")
else:
    print("Good morning !")

weather = input("What is the weather for today ? (rainy/snowy/sunny)")
if weather == "rainy":
    print("Remember to bring your umbrella!")
elif weather == "snowy":
    print("Remember to bring your gloves!")
else:
    print("Remember to bring your sunglasses!")

age = int(input("How old are you ?"))
height = int(input("How tall are you?"))
if age > 10 and height > 100:
    print("Congratulation, You can ride the roller coaster!")
else:
    print("Sorry, You can't ride the roller coaster!")

