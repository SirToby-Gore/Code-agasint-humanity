import random
import time
import card_pack
import tkinter as tk
from tkinter import ttk
import screeninfo # pip install
import pyttsx3 # pip install

class Cards:
    def __init__(self, colour : str):
        self.cards = colour.split("\n")
        random.shuffle(self.cards)
            
    def draw(self, amount : int):
        pick = []
        indexs = sorted(random.sample(range(len(self.cards)), amount))
        for off_set, i in enumerate(indexs):
            pick.append(self.cards[i-off_set])
            self.cards.pop(i-off_set)
        return pick

class player:
    def __init__(self, index :int, name : str):
        self.hand = white_cards.draw(5)
        self.name = name
        self.index = index
        self.score = 0
    
    def play(self):
        for i,h in enumerate(self.hand): print(f"{i+1} : {h}"); time.sleep(0.01)
        try:
            inp = int(input(f"Select you best card {self.name} (1-5): "))
            if inp < 0 or inp > 6:
                inp = random.randint(1,5)
        except ValueError:
            inp = random.randint(1,5)
        choice = self.hand[inp-1]
        self.hand.pop(inp-1)
        self.hand.append(white_cards.draw(1))
        return [choice,self.index]
    
    def add_score(self):
        self.score += 1


monitor  = screeninfo.get_monitors()[0]
divition = 5

def stringer(string, char_limit=43):
    if not string:
        return ""
    words = string.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > char_limit:
            lines.append(current_line)
            current_line = ""
        current_line += word + " "

    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)

class Window:
    def __init__(self, window_name=__file__.strip(".py"), cl_bg = "#212121", cl_pri = "green", cl_sec = "navy", cl_er = "red", cl_bt=None, 
                 geo=f"800x500+{monitor.width // divition}+{monitor.height // divition}", x=0, y=0, full=False, fnt = "Neue Helvetica BQ"):
        self.colour_bg=cl_bg
        self.colour_error = cl_er
        self.colour_primairy = cl_pri
        self.colour_secondairy = cl_sec
        self.font = fnt
        self.cache = []
        self.error_lables = []
        self.colour_button = cl_bt or cl_pri
        self.root = tk.Tk()
        
        if full: self.root.attributes("-fullscreen", True)
        else: self.root.geometry(geo)
        self.root.resizable(False, False)
        self.root.title(window_name)
        self.root.configure(bg=self.colour_bg)
        self.style = tk.ttk.Style(self.root)
        self.style.theme_use("classic")
        
    def header_text(self, string : str, change=True):
        if change: string=stringer(string)
        question_label = tk.Label(self.root, text=string.title(), font=(self.font, 30),bg=self.colour_bg, foreground=self.colour_primairy)
        question_label.pack(pady=10)
        
        self.root.update()
    
    def sub_text(self, string : str, change=True):
        if change: string=stringer(string)
        player_name_label = tk.Label(self.root, text=string.capitalize(), font=(self.font, 24),bg=self.colour_bg, foreground=self.colour_secondairy)
        player_name_label.pack(pady=5)
        
        self.root.update()

    def selection_list(self, hand: list, player_index=0, wideness=45):
        chosen_card = tk.StringVar()
        combobox = tk.ttk.Combobox(self.root, textvariable=chosen_card, values=hand, state="readonly", font=(self.font, 14), foreground=self.colour_primairy, width=wideness)
        combobox.pack(pady=5)

        def handle_confirm_click():
            if chosen_card.get():
                self.cache.append(chosen_card.get())
                self.end()
            else:
                self.error_message()

        confirm_button = tk.Button(self.root, text="Confirm", command=handle_confirm_click,
                                   bg=self.colour_bg, fg=self.colour_button)
        confirm_button.pack(pady=5)

        self.root.update()
    
    def continue_button(self, text="continue"):
        tk.Button(self.root, text=text.upper(), command=lambda: self.root.destroy(), bg=self.colour_bg, fg=self.colour_button, font=(self.font, 10)).pack(pady=5)
        
    def text_box(self, button_text="Submit_text", player_index=0):
        def handle_text(text, player_index):
            if not text: self.error_message("type into box")
            else:
                self.cache.append(text)
                self.root.destroy()

        self.entry_var = tk.StringVar(self.root)
        self.entry_box = tk.Entry(self.root, textvariable=self.entry_var, bg=self.colour_bg, fg=self.colour_button, font=(self.font, 14))
        self.entry_box.pack(pady=5)

        self.entry_button = tk.Button(self.root, text=button_text, command=lambda: handle_text(self.entry_var.get(), self.entry_box), bg=self.colour_bg, fg=self.colour_button, font=(self.font, 10))
        self.entry_button.pack(pady=5)

    def start(self):
        self.root.mainloop()
        
    def end(self):
        self.root.destroy()
    
    def error_message(self, message="Invalid, please select an option."):
        try:
            self.err_lab.destroy()
        except:
            self.err_lab = tk.Label(self.root, text=message.capitalize(), font=(self.font, 12), bg=self.colour_bg, foreground=self.colour_error).pack(pady=5)
        else:
            self.err_lab = tk.Label(self.root, text=message.capitalize(), font=(self.font, 12), bg=self.colour_bg, foreground=self.colour_error).pack(pady=5)


def get_name():
    extra = ""
    while True:
        choice = Window("Choose a name", cl_pri="yellow", cl_sec="yellow")
        choice.header_text("Pick a good name")
        choice.sub_text("Remember your name!!!", change=False)
        choice.selection_list([f"{prefs.draw(1)[0]} {nouns.draw(1)[0]}" for _ in range(4)], 0, 19)
        choice.text_box("Have your custom name")
        choice.start()
        if choice.cache[0]: break
    return choice.cache[0]
   
def text_to_speech(text, speed=200, voice_id=random.sample([
    'Microsoft Hazel Desktop - English (Great Britain)',
    'Microsoft David Desktop - English (United States)',
    'Microsoft Zira Desktop - English (United States)'],1)[0]):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    
    voices = engine.getProperty('voices')
    selected_voice = None
    
    for v in voices:
        if voice_id.lower() in v.id.lower():
            selected_voice = v
            break

    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == "__main__":
    
    white_cards = Cards(card_pack.retrurn_white())
    black_cards = Cards(card_pack.retrurn_black())
    nouns = Cards(card_pack.retrurn_nouns())
    prefs = Cards(card_pack.retrurn_prefs())
    
    audio_window = Window(window_name="Options", cl_pri="violet")  # Instantiate Window object
    audio_window.header_text("Audio?")
    audio_window.selection_list(["True", "False"], 0, 5)
    audio_window.start()
    audio_check = audio_window.cache[0]
    audio = None
    if audio_check == "True": audio = True
    else: audio = False
    
    max_players =  11
    player_window = Window(window_name="set players", cl_pri="orange")
    player_window.header_text("Select the number of players")
    player_window.selection_list([i for i in range(3, max_players+1)], 0, 5)
    player_window.start()
    No_players = int(player_window.cache[0])

    players = [
         player(i, get_name().title())
        for i in range(No_players)
        ]
    
    card_reader = random.randint(0,No_players)
    for round_number, question_card in enumerate(black_cards.cards):
        #changes the players over
        if card_reader+1 < No_players: card_reader += 1
        else: card_reader = 0
        
        data_window = Window("scores", cl_pri="blue", cl_sec="blue")
        data_window.header_text("scores so far")
        data_window.sub_text("\n".join([f"{player.name} : {player.score}" for player in players]), change=False)
        data_window.continue_button()
        data_window.start()
        
        #takes in answeres form players
        answeres = []
        if audio: text_to_speech(question_card.format(*["blank" for _ in range(question_card.count("{}"))]))
        for player in players:
            if player.index == card_reader: continue 
            else:
                player_ans = []
                for count in range(question_card.count("{}")):
                    if audio: text_to_speech(player.name)
                    answere_window = Window(f"take you pick {player.name}", cl_pri="silver", cl_sec="green")
                    answere_window.header_text(question_card.format(*["______" for _ in range(question_card.count("{}"))]))
                    answere_window.sub_text(f"{player.name} pick your best card, picking card number {count+1}/{question_card.count('{}')}")
                    answere_window.selection_list(player.hand, player.index)
                    answere_window.start()
                    for index, card in enumerate(player.hand):
                        if answere_window.cache == card: player.hand[index] = white_cards.draw(1)[0]
                    if answere_window.cache[0].lower() == "[Write your own card]".lower():
                        answere_window = Window("custom card", cl_sec="cyan", cl_bt="cyan", cl_pri="silver")
                        answere_window.header_text(question_card)
                        answere_window.sub_text("write your own card")
                        answere_window.text_box(button_text="submit custom card", player_index=player.index)
                        answere_window.start()
                        
                    player_ans.append(answere_window.cache[0])
                    for idx, pl_cr in enumerate(player.hand):
                        if pl_cr == answere_window.cache[0]:
                            player.hand.pop(idx)
                            break
                        
                answeres.append([player_ans, player.index])                    
                
                while len(player.hand)<5:
                    player.hand.append(white_cards.draw(1)[0])
        
        for idx, ans in enumerate(answeres):
            string = f"{idx+1} : {question_card.format(*[i for i in ans[0]])}"
            ans.append(string)
            if audio: text_to_speech(string)

        if audio: text_to_speech(players[card_reader].name)
        card_reader_window = Window("Read these in full", cl_pri="silver", cl_sec="indigo")
        card_reader_window.header_text(question_card.format(*["______" for _ in range(question_card.count("{}"))]))
        card_reader_window.sub_text(f"pick the best card {players[card_reader].name}")
        card_reader_window.selection_list([" + ".join(x[0]) for x in answeres])
        card_reader_window.start()
        
        #awards points to the winner
        try:
            index = "T"
            for ans in answeres:
                if card_reader_window.cache == ans[0]: index = ans[1]; break
            players[int(index)].add_score()
        except ValueError:
            players[random.sample(answeres, 1)[0][1]].add_score()
    
    win = Window("Winners", cl_pri="gold")
    sorted_data = sorted([(i.name, i.score) for i in players], key=lambda x: x[1], reverse=True)
    win.header_text("\n".join([f"{name} : {score}" for name, score in sorted_data]), change=False)
    win.start()
