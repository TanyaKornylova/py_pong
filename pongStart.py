import Tkinter as tk


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, buttons to start
        self.prompt = tk.Label(self, text="Choose how to play:", anchor="w")
        self.entry = tk.Entry(self)
        self.createServer = tk.Button(self, text="Create a server", command = create_game)
        self.joinServer = tk.Button(self, text="Join a server", command = connect_game(self.entry.get()))
        self.output = tk.Label(self, text="")

        # lay the widgets out on the screen. 
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.createServer.pack(side="right")
        self.joinServer.pack(side="left")



root = tk.Tk()
Example(root).pack(fill="both", expand=True)
root.mainloop()
