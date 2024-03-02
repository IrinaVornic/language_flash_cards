from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------------- Working with CSV file ----------------------------------------------------#
random_pair = {}
# to_learn = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    words_data = pandas.read_csv('./data/french_words.csv')
    to_learn = words_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')
# Variant 1
# to_learn = [{row.French: row.English} for (index, row) in words_data.iterrows()]
# Variant 2


def generate_random_word():
    global random_pair, flip_timer
    window.after_cancel(flip_timer)
    random_pair = random.choice(to_learn)
    canvas.itemconfig(language, text="French", fill='black')
    canvas.itemconfig(word, text=random_pair["French"], fill='black')
    canvas.itemconfig(canvas_image, image=flash_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=green_image)
    canvas.itemconfig(language, text="English", fill='white')
    canvas.itemconfig(word, text=random_pair['English'], fill='white')


def is_known():
    to_learn.remove(random_pair)
    generate_random_word()
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)




#
# ---------------------------------- UI SETUP -----------------------------------------------------------------#

window = Tk()

window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# Canvas
canvas = Canvas(width=800, height=526)
green_image = PhotoImage(file='./images/card_back.png')
flash_image = PhotoImage(file='./images/card_front.png')
canvas_image = canvas.create_image(400, 263, image=flash_image)
language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill='#000000')
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "italic"), fill='#000000')
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
# Buttons
ok_btn_img = PhotoImage(file='./images/right.png')
ok_button = Button(image=ok_btn_img, highlightbackground=BACKGROUND_COLOR, highlightthickness=0,
                   command=is_known)
ok_button.grid(column=1, row=1)

wrong_btn_img = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_btn_img, highlightbackground=BACKGROUND_COLOR, highlightthickness=0,
                      command=generate_random_word)
wrong_button.grid(column=0, row=1)

generate_random_word()

window.mainloop()
