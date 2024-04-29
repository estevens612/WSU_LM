from tkinter import Tk, Label, Entry, Text, Button, Scrollbar, END, Frame, TOP, X
import author_matcher
import threading
import time

def main():
    root = Tk()
    root.title("Matchmaker")
    root.geometry('800x600')  # Set default window size

    # Set dark mode colors
    background_color = '#333'
    text_color = '#DDD'
    input_bg = '#555'
    input_fg = '#EEE'

    root.configure(bg=background_color)

    # Title
    title_frame = Frame(root, bg=background_color)
    title_frame.pack(side=TOP, fill=X)
    title_label = Label(title_frame, text="WSU Matchmaker", font=("Helvetica", 24, "bold"), fg=text_color, bg=background_color)
    title_label.pack(pady=10)

    # Text display
    text = Text(root, height=15, width=75, bg=background_color, fg=text_color, insertbackground=text_color)
    scrollbar = Scrollbar(root, command=text.yview, bg='#666')
    text.configure(yscrollcommand=scrollbar.set)
    text.pack(side='top', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Search instruction
    Label(root, text="Enter your search query about research topics or faculty:", fg=text_color, bg=background_color).pack(pady=(0, 5))

    # Search bar
    entry = Entry(root, width=50, font=("Helvetica", 14), bg=input_bg, fg=input_fg, insertbackground=text_color)
    entry.pack(side='bottom', fill='x', padx=5, pady=5)

    data, vectorizer, text_vectors = author_matcher.load_data()

    def display_results(results):
        seen_results = set()  # Set to track seen results and avoid duplicates
        if not results:
            text.insert(END, "No matches found.\n", 'noresults')
        else:
            for result in results:
                if result not in seen_results:  # Check if the result has been seen
                    text.insert(END, result, 'results')
                    seen_results.add(result)  # Mark this result as seen
                    time.sleep(0.5)  # Pause for effect like chat rolling out
            if not seen_results:  # Check if all results were duplicates
                text.insert(END, "All results were duplicates.\n", 'noresults')
        text.insert(END, "\n")
        text.see(END)

    def on_search():
        query = entry.get()
        if not query:
            return
        entry.delete(0, END)
        text.insert(END, f"You: {query}\n", 'you')
        text.insert(END, "Finding matches...\n", 'loading')
        results = author_matcher.search_database(query, data, vectorizer, text_vectors)
        threading.Thread(target=display_results, args=(results,)).start()

    entry.bind('<Return>', lambda event: on_search())
    button = Button(root, text="Search", command=on_search, bg=input_bg, fg=input_fg)
    button.pack(side='bottom', fill='x')

    # Define text tags for coloring
    text.tag_configure('you', foreground='#0b0')
    text.tag_configure('results', foreground='#bb0')
    text.tag_configure('noresults', foreground='#b00')
    text.tag_configure('loading', foreground='#888')

    root.mainloop()

if __name__ == "__main__":
    main()
