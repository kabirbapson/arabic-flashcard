from tkinter import *
import pandas
import random
import arabic_reshaper
from bidi.algorithm import get_display

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ----------- FIX ARABIC FUNCTION -----------
def fix_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    return bidi_text
# ------------------------------------------

# ----------- LOAD DATA -----------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/arabic_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

total_words = len(to_learn)  # 🔥 total at start
# ------------------------------------------


# ----------- PROGRESS FUNCTION -----------
def update_progress():
    learned = total_words - len(to_learn)
    percent = int((learned / total_words) * 100)

    # Update text
    canvas.itemconfig(progress_text, text=f"{learned}/{total_words} ({percent}%)")

    # Update bar
    bar_width = 400
    fill_width = int((percent / 100) * bar_width)

    canvas.coords(progress_bar_fill, 200, 480, 200 + fill_width, 500)
# ------------------------------------------


def next_card():
    global current_card, flip_timer

    if len(to_learn) == 0:
        canvas.itemconfig(card_title, text="🎉 Done!", fill="black")
        canvas.itemconfig(card_word, text="All words learned", fill="black")
        return

    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)

    arabic_word = fix_arabic(current_card["Arabic"])

    canvas.itemconfig(card_title, text="Arabic", fill="black")
    canvas.itemconfig(card_word, text=arabic_word, fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    update_progress()  # 🔥 update progress
    next_card()


# ----------- UI SETUP -----------
window = Tk()
window.title("Bappi's Flash Arabic")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(
    400, 263,
    text="",
    font=("Noto Naskh Arabic", 60, "bold")
)

# ----------- PROGRESS UI -----------

# Progress text
progress_text = canvas.create_text(
    400, 460,
    text="",
    font=("Arial", 20, "bold"),
    fill="black"
)

# Progress bar background
canvas.create_rectangle(200, 480, 600, 500, fill="#ddd", outline="")

# Progress bar fill
progress_bar_fill = canvas.create_rectangle(200, 480, 200, 500, fill="#4CAF50", outline="")

# ----------------------------------

canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# ----------- START APP -----------
update_progress()
next_card()

window.mainloop()