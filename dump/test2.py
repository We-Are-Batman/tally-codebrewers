import tkinter as tk

root = tk.Tk()

# Create three buttons
button1 = tk.Button(root, text="Button 1", width=10)
button2 = tk.Button(root, text="Button 2", width=10)
button3 = tk.Button(root, text="Button 3", width=10)

# Pack the buttons side by side
button1.pack(side="left")
button2.pack(side="left")
button3.pack(side="left")

root.mainloop()
