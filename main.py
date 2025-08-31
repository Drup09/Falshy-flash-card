from tkinter import *
from pandas import *
from random import *
import os

# ----------------- Logic ------------------

# Load data: use words_to_learn.csv if it exists, otherwise use french_words.csv
try:
    df = read_csv("Flashy-flash card app/data/words_to_learn.csv")
except FileNotFoundError:
    df = read_csv("Flashy-flash card app/data/french_words.csv")

to_learn = df.to_dict(orient="records")
current_card = {}

def french_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  # cancel previous timer

    current_card = choice(to_learn)   # pick a new word
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")

    flip_timer = window.after(3000, func=english_card)  # set new timer
  

def english_card():
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# ----------------- Saving progress -----------------
def is_known():
    to_learn.remove(current_card)  # remove current word
    data = DataFrame(to_learn)
    data.to_csv("Flashy-flash card app/data/words_to_learn.csv", index=False)
    french_card()  # show next word


# ----------------- UI SETUP -----------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg="#B1DDC6")

BACKGROUND_COLOR = "#B1DDC6"

flip_timer = window.after(3000, func=english_card)

# ----------------- CARD IMAGE -----------------
card_front_img = PhotoImage(file="Flashy-flash card app/images/card_front.png")
card_back_img = PhotoImage(file="Flashy-flash card app/images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# ----------------- BUTTONS -----------------
wrong_img = PhotoImage(file="Flashy-flash card app/images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=french_card)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="Flashy-flash card app/images/correct.png")
right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)

# Start with a French card
french_card()

window.mainloop()
