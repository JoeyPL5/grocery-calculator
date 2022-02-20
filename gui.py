import traceback
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from calculator import Calculator


class GUI:
    # start gui
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry("400x450")
        self.win.title("Grocery Calculator")

        # calculate button
        self.calc_button = tk.Button(self.win, text='Calculate', command=self.calculate)
        self.calc_button.pack(side=tk.BOTTOM, pady=20)

        # who ordered label and text box
        self.who_ordered_label = tk.Label(self.win, text='Who ordered? Separate with spaces (ex. \"Andrew Joey\")')
        self.who_ordered_label.pack(side=tk.TOP, pady=10)
        self.who_ordered_text_box = tk.Entry(self.win, width=50, bg="white", fg="black", justify='center')
        self.who_ordered_text_box.pack(side=tk.TOP)

        # who paid label and text box
        self.who_paid_label = tk.Label(self.win, text='Who paid? (ex. "Andrew")')
        self.who_paid_label.pack(side=tk.TOP, pady=10)
        self.who_paid_text_box = tk.Entry(self.win, width=20, bg="white", fg="black", justify='center')
        self.who_paid_text_box.pack(side=tk.TOP)

        # total cost label and text box
        self.cost_label = tk.Label(self.win, text='Total cost? (ex. "190.42")')
        self.cost_label.pack(side=tk.TOP, pady=10)
        self.cost_text_box = tk.Entry(self.win, width=10, bg="white", fg="black", justify='center')
        self.cost_text_box.pack(side=tk.TOP)

        self.personal_items_label = tk.Label(self.win, text='Personal items? Format: "[cost] [name1] [name2] ..."'
                                                            '\nSeparate by line (ex. "16.59 Andrew Joey")')
        self.personal_items_label.pack(side=tk.TOP, pady=10)
        self.personal_item_text_box = ScrolledText(self.win, width=25, height=20)
        self.personal_item_text_box.pack(side=tk.TOP)
        self.win.mainloop()

    # calculate
    def calculate(self):
        # start results popup
        results_popup = tk.Toplevel()
        results_popup.geometry("300x300")
        results_popup.title("Results")

        results_string = ""
        who_ordered = self.who_ordered_text_box.get()
        who_paid = self.who_paid_text_box.get()
        # catch float conversion error
        try:
            cost = float(self.cost_text_box.get())
        except ValueError:
            # custom error popup
            results_string = "Invalid cost input, try again."
            results_label = tk.Label(results_popup, text=results_string)
            results_label.pack(side=tk.TOP, pady=10)
        personal_items = self.personal_item_text_box.get('1.0', tk.END).split(sep='\n')
        calc = Calculator(who_ordered, who_paid, cost, personal_items)

        # try running calculations, catch any error it throws and prompt to try again
        try:
            calc.run()
            results_string = calc.final_amounts() + '\n' + calc.venmo_amounts()
        except Exception as e:
            results_string = "ERROR: " + str(e) + ", try again."
            traceback.print_exc()
        results_label = tk.Label(results_popup, text=results_string)
        results_label.pack(side=tk.TOP, pady=10)


if __name__ == "__main__":
    gui = GUI()


