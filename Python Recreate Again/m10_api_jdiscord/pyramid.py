def pyramid(star):
    for rows in range(0, star):
        for columns in range(0, rows+1):
            print("*", end=" ")
        print("\r")

def pyramid_down(star):
    for rows in range(star + 1, 0, -1):
        for columns in range(0, rows-1):
            print("*", end=" ")
        print("\r")

pyramid(3)
pyramid_down(3)