import tkinter as tk
import threading

app = tk.Tk()
button = tk.Button(text="TEST BUTTON", command=lambda: print("HELLO"))
button.pack()

trd = threading.Thread(target=app.mainloop)
trd.start()
trd.join()

def start():
    while True:
        app.update()
    
trd = threading.Thread(target=start)
trd.start()
trd.join()

# Show what it is suppposed to looklike here
#app.mainloop()
