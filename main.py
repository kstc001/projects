from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    dic = original_data.to_dict(orient="records")
else:
    # dic = [{"French": v.French, "English": v.English} for (k, v) in data.iterrows()]
    dic = data.to_dict(orient="records")
current_card = {}


def next_flashcards():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dic)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(img, image=front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(img, image=back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")


def check_mark():
    dic.remove(current_card)
    data = pandas.DataFrame(dic)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_flashcards()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front = PhotoImage(file="images/card_front.png")
back = PhotoImage(file="images/card_back.png")
img = canvas.create_image(400, 263, image=front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text=f"", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_flashcards)
unknown_button.grid(row=1, column=0)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=check_mark)
known_button.grid(row=1, column=1)

next_flashcards()

window.mainloop()
