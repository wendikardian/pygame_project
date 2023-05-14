# def order_pizza():
#     quantity = 1
#     price = 10
#     total_order = quantity * price
#     print(total_order)

# order_pizza()

# def order_pizza(quantity):
#     price = 10
#     total_order = quantity * price
#     print(total_order)

# order_pizza(7)

def order_pizza(quantity):
    price = 10
    total_order = quantity * price
    print(total_order)
order = input("How many pizzas do you want to order ? ")
pizza = int(order)
order_pizza(pizza)