GREEN = '#B1DDC6'
from tkinter import *
import pandas as pd
import random

global random_index, english_word, random_hindi_word

# Opening Hindi CSV
daata = pd.read_csv("hindi-english - Sheet1.csv")
data_dict = daata.to_dict('split')
del data_dict["index"]
del data_dict["columns"]

studied = {'data': []}
to_learn = data_dict

# Function to generate a random Hindi word
def go_into_flashcard():
    global random_index, random_hindi_word
    random_index = random.randint(0, len(to_learn["data"]) - 1)
    random_hindi_word = to_learn["data"][random_index][0]

    canvas.itemconfig(x, text=random_hindi_word)
    canvas.itemconfig(bg_image, image=card_front)
    canvas.itemconfig(first_text, text="हिंदी", fill="black")

# Function to add the current word to the studied list and remove from to_learn
def add_to_studied():
    global english_word, random_hindi_word, random_index
    english_word = to_learn["data"][random_index][1]
    studied['data'].append([random_hindi_word, english_word])
    del to_learn['data'][random_index]
    go_into_flashcard()

# Function to flip the flashcard to show the English word for 3 seconds
def flip_the_flashcard():
    global english_word, random_hindi_word
    english_word = to_learn["data"][random_index][1]

    canvas.itemconfig(bg_image, image=bg)
    canvas.itemconfig(first_text, text="English", fill="white")
    canvas.itemconfig(x, text=english_word, fill="white")

    # Schedule the flip back to Hindi after 3 seconds
    window.after(3000, flip_back_to_hindi)

# Function to flip back to the Hindi word
def flip_back_to_hindi():
    global random_hindi_word
    random_hindi_word = to_learn["data"][random_index][0]

    canvas.itemconfig(bg_image, image=card_front)
    canvas.itemconfig(first_text, text="हिंदी", fill="black")
    canvas.itemconfig(x, text=random_hindi_word, fill="black")

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=GREEN)

# Tick button
tick_image = PhotoImage(file="right.png")
tick = Button(image=tick_image, bg=GREEN, highlightthickness=0, command=add_to_studied)
tick.grid(row=1, column=0)

# Cross button
cross_image = PhotoImage(file="wrong.png")
wrong = Button(image=cross_image, bg=GREEN, highlightthickness=0, command=go_into_flashcard)
wrong.grid(row=1, column=2)

# Show backside button
flip_image = PhotoImage(file="flip.png")
flip = Button(image=flip_image, command=flip_the_flashcard)
flip.grid(row=1, column=1)

# Canvas setup
canvas = Canvas(window, width=800, height=526, highlightthickness=0, bg=GREEN)
canvas.grid(row=0, column=0, columnspan=3, sticky="ew")
card_front = PhotoImage(file="card_front.png")
bg = PhotoImage(file="card_back.png")

bg_image = canvas.create_image(400, 263, image=card_front)
first_text = canvas.create_text(400, 150, text="हिंदी", font=("Arial", 40, "italic"))
x = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.update()

go_into_flashcard()  # Initialize with the first word
print(len(data_dict['data']))
window.mainloop()
