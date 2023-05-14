
while True:
    print("Body mass index (BMI)")
    weight = float(input("How much do you weight in Kilograms ? "))
    height = float(input("How tall are you in meters ? "))
    BMI = weight / (height * height)

    if BMI < 18.5:
        print("Less Weight")
    elif 18.5 < BMI < 24.9:
        print("Normal Weight")
    elif 25 < BMI < 29.9:
        print("Over Weight")
    else:
        print("Obesity")

    print("Your BMI = " + str(BMI))

    ans = input("Do you want to input again ? y/n --> ")
    if ans == "n":
        break