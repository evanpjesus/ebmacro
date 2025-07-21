from pynput.keyboard import Key, Controller, Listener
import threading
import time
import tkinter as tk

kb = Controller()
should_exit = False
macro_active = False
listener_thread = None

function_key_words = {
    Key.f1: [
        "owned", "renown", "wonder", "owner", "drown", "drone", "downer", "newer", "wed",
        "row", "now", "rod", "nod", "new", "den", "own", "worn", "word", "wore", "owed",
        "neon", "done", "redo", "redone", "renew", "won", "ender", "deer", "nerd", "drew",
        "need", "rode", "were", "owe", "red"
    ],
    Key.f2: [
        "mystic", "salt", "claim", "claims", "calm", "mail", "macs", "aim", "cam", "cams", "mat",
        "sob", "casts", "last", "mist", "clay", "scam", "stay", "slim", "cat", "cats", "city", "mic",
        "mics", "act", "icy", "lit", "slam", "list", "slit", "slimy", "sake"
    ],
    Key.f3: [
        "slope", "slopes", "boss", "loss", "lips", "lisp", "spoil", "slip", "bless", "bop", "bops",
        "pole", "poles", "boil", "blips", "soil", "pie", "oil", "bios", "boils", "lies", "possible",
        "bio", "bliss", "blip", "pile"
    ],
    Key.f4: [
        "validate", "invalid", "valid", "anvil", "divine", "dental", "invite", "invade", "live",
        "lived", "deal", "data", "vital", "naive", "naval", "ant", "delta", "dealt", "lie", "lied",
        "tie", "net", "laid", "deli", "aid", "lane", "invited", "date", "alive", "denial", "advent",
        "vent", "van", "alien", "devil", "late", "land"
    ],
    Key.f5: [
        "optical", "apricot", "captor", "patrol", "tropical", "capital", "portal", "ratio", "topic",
        "lit", "cap", "rap", "trap", "crop", "lot", "pic", "pal", "pat", "crap", "tailor", "part",
        "car", "cat", "cart", "tail", "optic", "clap", "clip", "tip", "trip", "pit", "capitol", "air"
    ],
    Key.f6: [
        "seat", "east", "ate", "set", "sea", "tea", "eat", "sat", "eats"
    ],
    Key.f7: [
        "enlarge", "enrage", "angel", "eagle", "set", "agree", "learn", "anger", "ample", "large",
        "genre", "rage", "range", "green", "glare", "gene", "lean", "real", "gel", "leg", "lag",
        "nag", "age", "angle", "angler", "general", "earn", "gear", "regal", "near", "rag"
    ]
}

def type_list(word_list):
    global should_exit
    amt = len(word_list)
    if amt == 0:
        return
    timeBreak = .05
    for word in word_list:
        if should_exit:
            break
        for char in word:
            kb.press(char)
            kb.release(char)
            time.sleep(0.05)
        kb.press(Key.space)
        kb.release(Key.space)
        time.sleep(timeBreak)

def on_press(key):
    global macro_active
    if key == "j":
        start_macro()
    elif key == Key.esc:
        stop_macro()
    elif macro_active and key in function_key_words:
        threading.Thread(target=type_list, args=(function_key_words[key],)).start()

def on_release(key):
    pass  # not used

def macro_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def start_macro():
    global should_exit, macro_active
    should_exit = False
    macro_active = True
    status_label.config(text="Status: Macro Listening (F1–F7)", fg="green")

def stop_macro():
    global should_exit, macro_active
    should_exit = True
    macro_active = False
    status_label.config(text="Status: Macro Stopped", fg="red")

# --- GUI ---
root = tk.Tk()
root.title("East Brickton Swiping Macro")
root.geometry("900x600")
root.configure(bg="#f9f9f9")

# Header
title_label = tk.Label(root, text="East Brickton Swiping Macro", font=("Helvetica", 20, "bold"), bg="#f9f9f9")
title_label.pack(pady=15)

# Status
status_label = tk.Label(root, text="Status: Macro Stopped", fg="red", font=("Helvetica", 13), bg="#f9f9f9")
status_label.pack()

# Buttons
btn_frame = tk.Frame(root, bg="#f9f9f9")
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="Start (j)", command=start_macro, width=15, bg="#d0f0d0", font=("Helvetica", 12))
start_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(btn_frame, text="Stop (ESC)", command=stop_macro, width=15, bg="#f0d0d0", font=("Helvetica", 12))
stop_btn.grid(row=0, column=1, padx=10)

# Scrollable word list
container = tk.Frame(root, bg="#f9f9f9")
container.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(container, bg="#f9f9f9", highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Word list display
for key, words in function_key_words.items():
    label = tk.Label(scrollable_frame,
                     text=f"{key.name.upper()} ➜ {', '.join(sorted(set(words)))}",
                     anchor="w", justify="left", wraplength=800,
                     font=("Helvetica", 11), bg="#f9f9f9", padx=10, pady=5)
    label.pack(anchor="w", fill="x")

# Start keyboard listener in background
threading.Thread(target=macro_listener, daemon=True).start()

root.mainloop()