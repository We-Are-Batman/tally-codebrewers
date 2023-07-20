import tkinter as tk

def show_page(page_name):
    # Hide all frames
    for frame in frames.values():
        frame.grid_forget()
    
    # Show the selected page
    frames[page_name].grid(row=0, column=0, padx=10, pady=10)

root = tk.Tk()
root.title("Page Navigation Example")

# Create multiple frames, each representing a separate page
frames = {}
for page_name in ["Page 1", "Page 2"]:
    frame = tk.Frame(root)
    label = tk.Label(frame, text=f"This is {page_name}")
    label.pack(pady=20)
    frames[page_name] = frame

# Show the first page initially
show_page("Page 1")

# Create buttons to navigate between pages
button_page1 = tk.Button(root, text="Page 1", command=lambda: show_page("Page 1"))
button_page1.grid(row=1, column=0, padx=10, pady=5)

button_page2 = tk.Button(root, text="Page 2", command=lambda: show_page("Page 2"))
button_page2.grid(row=2, column=0, padx=10, pady=5)

root.mainloop()
