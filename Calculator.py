# takes inputs from user regarding total receipt costs and who payed for each one
def receipt_info(count):
    global receipt_costs
    global receipt_payers
    receipt_costs = []
    receipt_payers = []
    for i in range(count):
        while True:
            try:
                receipt_costs.append(float(input("What was the total cost of receipt " + str(i + 1) + "?\n")))
                break
            except ValueError:
                print('Invalid value. Please re-input.\n')
                pass
        while True:
            payer = input("Who payed for receipt " + str(i + 1) + "?\n")
            if payer in buyers:
                receipt_payers.append(payer)
                break
            else:
                print("Invalid name. Please re-input.\n")


# takes in integer 'length' and returns a list of length 'length' with all values as zero
def initializeZeros(length):
    empty_list = []
    for i in range(length):
        empty_list.append(0.00)
    return empty_list


# Adds the costs of the receipts to the amount payed by the person who payed for it
def initialPayments():
    global amount_payed
    global amount_owed
    amount_payed = initializeZeros(num_buyers)
    amount_owed = initializeZeros(num_buyers)
    for cost_index, cost in enumerate(receipt_costs):
        index = buyers.index(receipt_payers[cost_index])
        amount_payed[index] += cost


# takes in input for items only part of the group purchased
def partialPayments():
    print("Input an item that isn't for the whole group...\n Format: Cost Name1 Name2... \n Examples: (a) 10.35 "
          "Joey \n (b) 45.1 Ethan Andrew Joe \n"
          "'q' when all inputs complete \n")
    while True:
        payment = input("Input:\n")
        pay_input = payment.split()
        if pay_input[0].lower() == 'q':
            break
        else:
            try:
                cost = float(pay_input[0])
                splitters = len(pay_input) - 1
                marginal_cost = cost / splitters
                i = 1
                while i < len(pay_input):
                    if pay_input[i] in buyers:
                        index = buyers.index(pay_input[i])
                        amount_owed[index] += marginal_cost
                    i += 1
            except ValueError:
                print(
                    "Error with inputs... make sure first value is cost and following names are buyers.\n Please "
                    "re-input.\n")
                pass


# calculates the cost of the items purchased as a group
def groupPayments():
    total_payed = sumList(amount_payed)
    total_owed = sumList(amount_owed)
    total_left = total_payed - total_owed
    marginal_cost = total_left / num_buyers
    for i in range(num_buyers):
        amount_owed[i] += marginal_cost


# adds every element of a number list
def sumList(num_list):
    total = 0
    for num in num_list:
        total += num
    return total


# prints the final amounts each person pays and owes
def finalAmounts():
    print("")
    for i in range(num_buyers):
        payed = amount_payed[i]
        owed = amount_owed[i]
        if payed > owed:
            print(buyers[i] + " receives $" + str(round(abs(payed - owed), 2)))
        else:
            print(buyers[i] + " owes $" + str(round(abs(payed - owed), 2)))
    print("")


# prints how much each person should venmo
def venmoAmounts():
    balances = []
    venmos = []
    for i in range(num_buyers):
        balances.append(round(amount_payed[i] - amount_owed[i], 2))
    for i in range(num_buyers):
        j = 0
        while balances[i] > 0:
            if not i == j:
                if balances[j] < 0:
                    amount_to_venmo = min(abs(balances[i]), abs(balances[j]))
                    venmos.append(buyers[j] + " venmos " + buyers[i] + " $" + str(amount_to_venmo))
                    balances[i] -= amount_to_venmo
                    balances[j] += amount_to_venmo
            j += 1
    for message in venmos:
        print(message)


who_bought = input("Who bought groceries? (spaces between names)\n")
global buyers
global num_buyers
buyers = who_bought.split()
num_buyers = len(buyers)
num_receipts = int(input("How many receipts?\n"))
receipt_info(num_receipts)
initialPayments()
partialPayments()
groupPayments()
finalAmounts()
venmoAmounts()
