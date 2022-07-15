import tkinter
from tkinter import messagebox
import pandas
import random
import sys

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
spanish_word = ""
english_word = ""
score = 0
high_score = 0

def press_quit():
    global high_score
    quit = messagebox.askyesno(title="Quit program", message=("Do you really want to quit?"))
    if quit:
        high_score_file = open("./data/high_score.txt", "w")
        high_score_file.write(str(high_score))
        high_score_file.close()
        sys.exit()

def next_word():
    global spanish_word, english_word
    spanish_word, english_word = random.choice(list(word_dict.items()))
    card_canvas.itemconfig(word_text, text=spanish_word)

def check_answer(event):
    global spanish_word, english_word, score, high_score
    if answer_input.get().lower() == english_word.lower():
        score += 1
        if score > high_score:
            high_score = score
            card_canvas.itemconfig(high_score_text, text=f"High Score: {high_score}")
        card_canvas.itemconfig(score_text, text=f"Score: {score}")
        del word_dict[spanish_word]
    answer_input.delete(0, 'end')
    show_answer(event=None)

def show_answer(event):
    card_canvas.itemconfig(word_text, text=english_word)
    card_canvas.itemconfig(language_text, text="English")
    card_canvas.itemconfig(image, image=card_back)
    window.after(1500, show_spanish)

def show_spanish():
    card_canvas.itemconfig(word_text, text=spanish_word)
    card_canvas.itemconfig(language_text, text="Spanish")
    card_canvas.itemconfig(image, image=card_front)
    next_word()

#--- DATA SET UP ---#
#Load data from CSV
try:
    data = pandas.read_csv("./data/spanish_words.csv")
except FileNotFoundError:
    messagebox.showerror(title="File not found!", message="No data file found")
    sys.exit()
else:
    #load data into a dictionary
    word_dict = {row.Spanish: row.English for (Spanish, row) in data.iterrows()}

#load high score
try:
    high_score_file = open("./data/high_score.txt", "r")
except FileNotFoundError:
    high_score = 0
else:
    high_score = int(high_score_file.readline().strip())
    high_score_file.close()


#----UI Set Up ----#
window = tkinter.Tk()
window.config(width=1000, height=800, padx=20, pady=20, bg=BACKGROUND_COLOR)
window.title("Spanish Flash Card Game")
window.resizable(False, False)

#load images
card_front = tkinter.PhotoImage(file="./images/card_front.png")
card_back = tkinter.PhotoImage(file="./images/card_back.png")
right_photo = tkinter.PhotoImage(file="./images/next_question.png")
wrong_photo = tkinter.PhotoImage(file="./images/quit.png")

#Put on canvas
card_canvas = tkinter.Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
image = card_canvas.create_image(400, 265, image=card_front)
language_text = card_canvas.create_text(400, 150, text="Spanish", font=(FONT_NAME, 40, "italic"))
word_text = card_canvas.create_text(400, 263, text=spanish_word, font=(FONT_NAME, 60, "bold"))
score_text = card_canvas.create_text(120, 50, text=f"Score: {score}", font=(FONT_NAME, 30, "bold"))
high_score_text = card_canvas.create_text(600, 50, text=f"High Score: {high_score}", font=(FONT_NAME, 30, "bold"))
card_canvas.grid(row=0, column=0, columnspan=3)
card_canvas.bind("<Button-1>", show_answer)

next_button = tkinter.Button(image=right_photo, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, command=lambda: show_answer(event=None))
next_button.grid(row=2, column=2)

quit_button = tkinter.Button(image=wrong_photo, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR, command=press_quit)
quit_button.grid(row=2, column=0)

answer_input = tkinter.Entry(width=20, font=(FONT_NAME, 20, "bold"))
answer_input.grid(row=2, column=1)
answer_input.bind("<Return>", check_answer)


#Start the program
next_word()

#Always at the end
window.mainloop()