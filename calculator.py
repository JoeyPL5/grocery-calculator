from typing import List


class Calculator:
    # initialize calculator, take in a list of names for who bought, a name for who paid, and a list of personal item
    # strings in the format "[cost] [name1] [name2] ..."
    def __init__(self, who_bought: str, who_paid: str, cost: float, items: List[str]):
        self.buyers = who_bought.split()
        self.num_buyers = len(self.buyers)
        self.payer = who_paid
        self.personal_items = items
        self.receipt_costs = [cost]
        self.receipt_payers = [who_paid]
        self.amount_paid = []
        self.amount_owed = []

    # takes in integer 'length' and returns a list of length 'length' with all values as zero
    def initialize_zeros(self, length):
        empty_list = []
        for i in range(length):
            empty_list.append(0.00)
        return empty_list

    # Adds the costs of the receipts to the amount payed by the person who payed for it
    def initial_payments(self):
        self.amount_paid = self.initialize_zeros(self.num_buyers)
        self.amount_owed = self.initialize_zeros(self.num_buyers)
        for cost_index, cost in enumerate(self.receipt_costs):
            index = self.buyers.index(self.receipt_payers[cost_index])
            self.amount_paid[index] += cost

    # takes in input for items only part of the group purchased
    def partial_payments(self):
        for item in self.personal_items:
            if not item:
                continue
            pay_input = item.split(" ")
            pay_input[0] = pay_input[0].strip()
            cost = float(pay_input[0])
            splitters = len(pay_input) - 1
            marginal_cost = cost / splitters
            i = 1
            while i < len(pay_input):
                if pay_input[i] in self.buyers:
                    index = self.buyers.index(pay_input[i])
                    self.amount_owed[index] += marginal_cost
                i += 1

    # calculates the cost of the items purchased as a group
    def group_payments(self):
        total_payed = self.sum_list(self.amount_paid)
        total_owed = self.sum_list(self.amount_owed)
        total_left = total_payed - total_owed
        marginal_cost = total_left / self.num_buyers
        for i in range(self.num_buyers):
            self.amount_owed[i] += marginal_cost

    # adds every element of a number list
    def sum_list(self, num_list):
        total = 0
        for num in num_list:
            total += num
        return total

    # returns a string the final amounts each person pays and owes
    def final_amounts(self) -> str:
        info = ""
        for i in range(self.num_buyers):
            payed = self.amount_paid[i]
            owed = self.amount_owed[i]
            if payed > owed:
                info += self.buyers[i] + " receives $" + str(round(abs(payed - owed), 2)) + "\n"
            else:
                info += self.buyers[i] + " owes $" + str(round(abs(payed - owed), 2)) + "\n"
        return info

    # returns a string with how much each person should venmo
    def venmo_amounts(self) -> List[str]:
        balances = []
        venmos = []
        for i in range(self.num_buyers):
            balances.append(round(self.amount_paid[i] - self.amount_owed[i], 2))
        for i in range(self.num_buyers):
            j = 0
            while balances[i] > 0 and j < self.num_buyers:
                if not i == j:
                    if balances[j] < 0:
                        amount_to_venmo = min(abs(balances[i]), abs(balances[j]))
                        venmos.append(self.buyers[j] + " venmos " + self.buyers[i] + " $" + str(amount_to_venmo))
                        balances[i] -= amount_to_venmo
                        balances[j] += amount_to_venmo
                j += 1
        info = ""
        for message in venmos:
            info += message + "\n"
        return info

    # run calculations
    def run(self):
        self.initial_payments()
        self.partial_payments()
        self.group_payments()
