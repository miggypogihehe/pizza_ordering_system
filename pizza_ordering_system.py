import tkinter as tk
from tkinter import ttk, messagebox



pizza_prices = {
    "Pepperoni": 250,
    "Hawaiian": 280,
    "Cheese": 220,
    "Bacon": 300
}

size_prices = {
    "Small": 0,
    "Medium": 50,
    "Large": 100
}

topping_prices = {
    "Extra Cheese": 30,
    "Mushrooms": 40,
    "Bacon": 50
}




window = tk.Tk()
window.title("Pizza Ordering System")
window.geometry("720x850")
window.resizable(False, False)
window.configure(bg="#CF864A")




pizza_var = tk.StringVar(value="Pepperoni")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}



def section_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=("Arial", 11, "bold"),
        bg="#B12A2A",
        fg="#141414"
    )




header = tk.Frame(window, bg="#CE6F6F")
header.pack(fill="x", pady=(22, 14))

tk.Label(
    header,
    text="🍕",
    font=("Arial", 50),
    bg="#F3F1F1",
    fg="#181717"
).pack()

tk.Label(
    header,
    text="PIZZA ORDERING SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#F78A8A",
    fg="#3d3a38"
).pack()

tk.Label(
    header,
    text="Freshly made. Just the way you like it.",
    font=("Arial", 10, "italic"),
    bg="#E4CFCF",
    fg="#0f0606"
).pack(pady=(4, 0))




order_frame = tk.Frame(
    window,
    bg="#7A2525",
    padx=25,
    pady=18,
    highlightbackground="#AD8383",
    highlightthickness=1
)
order_frame.pack(padx=35, fill="x")



section_label(order_frame, "SELECT PIZZA FLAVOR").pack(anchor="w")

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Arial", 11)
)
pizza_dropdown.pack(fill="x", pady=(7, 13))



section_label(order_frame, "SELECT PIZZA SIZE").pack(anchor="w", pady=(0, 6))

size_frame = tk.Frame(order_frame, bg="#C5C3C3")
size_frame.pack(anchor="w", pady=(0, 12))

for size, price in size_prices.items():
    tk.Radiobutton(
        size_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 10),
        bg="#C0ABAB",
        fg="white",
        selectcolor="#AA4242",
        activebackground="#292929",
        activeforeground="#ffad42",
        cursor="hand2"
    ).pack(side="left", padx=(0, 15))


section_label(order_frame, "EXTRA TOPPINGS").pack(anchor="w", pady=(0, 6))

toppings_frame = tk.Frame(order_frame, bg="#252525")
toppings_frame.pack(anchor="w", pady=(0, 12))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        toppings_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 10),
        bg="#292929",
        fg="white",
        selectcolor="#444444",
        activebackground="#292929",
        activeforeground="#ffad42",
        cursor="hand2"
    ).pack(anchor="w")


section_label(order_frame, "QUANTITY (1–50)").pack(anchor="w", pady=(0, 6))

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 11),
    width=8,
    justify="center"
)
quantity_spinbox.pack(anchor="w")



def calculate_total():
    pizza = pizza_var.get()
    size = size_var.get()

    # Validate quantity
    try:
        quantity = int(quantity_var.get())
        if quantity < 1 or quantity > 50:
            raise ValueError
    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a whole number from 1 to 50."
        )
        return

    
    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    
    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

   
    total_per_pizza = pizza_price + size_price + topping_price
    total = total_per_pizza * quantity

    
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)

    receipt_text.insert(tk.END, "             🍕 PIZZA HOUSE\n")
    receipt_text.insert(tk.END, "           ORDER RECEIPT\n")
    receipt_text.insert(tk.END, "-" * 43 + "\n")
    receipt_text.insert(tk.END, f"Pizza Flavor : {pizza}\n")
    receipt_text.insert(tk.END, f"Pizza Size   : {size}\n")
    receipt_text.insert(tk.END, f"Base Price   : ₱{pizza_price:,.2f}\n")
    receipt_text.insert(tk.END, f"Size Add-on  : ₱{size_price:,.2f}\n")
    receipt_text.insert(tk.END, "\nEXTRA TOPPINGS\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"  {topping:<20} ₱{topping_prices[topping]:,.2f}\n"
            )
    else:
        receipt_text.insert(tk.END, "  No extra toppings\n")

    receipt_text.insert(tk.END, "-" * 43 + "\n")
    receipt_text.insert(tk.END, f"Price per pizza : ₱{total_per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity        : {quantity}\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT    : ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "-" * 43 + "\n")
    receipt_text.insert(tk.END, "       Thank you for your order!\n")

    receipt_text.config(state="disabled")


def reset_order():
    pizza_var.set("Pepperoni")
    size_var.set("Small")
    quantity_var.set(1)

    for variable in topping_vars.values():
        variable.set(False)

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.config(state="disabled")




button_frame = tk.Frame(window, bg="#F1F7D9")
button_frame.pack(pady=15)

place_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg="#ff9933",
    fg="#F5F4CC",
    activebackground="#9c5e17",
    activeforeground="#F3E8C4",
    width=18,
    relief="flat",
    cursor="hand2",
    command=calculate_total
)
place_button.grid(row=0, column=0, padx=8, ipady=7)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg="#960D0D",
    fg="white",
    activebackground="#D40C0C",
    activeforeground="white",
    width=12,
    relief="flat",
    cursor="hand2",
    command=reset_order
)
reset_button.grid(row=0, column=1, padx=8, ipady=7)




tk.Label(
    window,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg="#171717",
    fg="#ff9933"
).pack(pady=(5, 7))

receipt_text = tk.Text(
    window,
    height=13,
    width=65,
    font=("Consolas", 10),
    bg="#292929",
    fg="white",
    insertbackground="white",
    relief="flat",
    padx=12,
    pady=10
)
receipt_text.pack(padx=35, fill="x")
receipt_text.config(state="disabled")




window.mainloop()
