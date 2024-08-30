import pyttsx3
import wikipedia
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def page(title: str, sentences=2):
    """
    :param title: (str) the title of the Wikipedia page to summarize
    :param sentences: (int) the number of sentences to include in the summary (optional, default is 2)
    :return: (str) the summary of the Wikipedia page
    """
    try:
        content = wikipedia.summary(title, sentences=sentences)
        return content
    except wikipedia.exceptions.PageError:
        return "Page not found. Please try another title."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation error: {e.options}"
    except Exception as e:
        return f"An error occurred: {e}"


def voicing_text(text):
    """
    Speaks the given text using the text-to-speech engine
    :param text: (str) the text to speak
    :return: (str) the input text
    """
    # Initialize the engine
    engine = pyttsx3.init()

    # Set the voice to be used
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

    # returns the input text in order to provide subtitles for the spoken audio
    return text


def summarize_and_voice():
    wiki_page = entry_page.get()
    num_of_sentences = entry_sentences.get()

    if not wiki_page:
        messagebox.showerror("Input Error", "Please enter the name of the Wikipedia page.")
        return

    if num_of_sentences:
        try:
            num_of_sentences = int(num_of_sentences)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for sentences.")
            return
    else:
        num_of_sentences = 2

    summary = page(wiki_page, num_of_sentences)
    result_text.set(summary)
    voicing_text(summary)


# Set up the main window
root = tk.Tk()
root.title("Wikipedia Summary and Voice")
root.geometry("600x450")
root.resizable(False, False)

# Create a style for ttk widgets
style = ttk.Style(root)
style.configure('TLabel', font=("Helvetica", 12))
style.configure('TButton', font=("Helvetica", 12, "bold"), padding=6)
style.configure('TEntry', font=("Helvetica", 12), padding=6)
style.configure('TFrame', padding=10)

# Create a frame for input fields
frame = ttk.Frame(root, padding=20)
frame.pack(pady=20)

# Create and place the widgets
ttk.Label(frame, text="Wikipedia Page Title:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_page = ttk.Entry(frame, width=40)
entry_page.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame, text="Number of Sentences:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_sentences = ttk.Entry(frame, width=40)
entry_sentences.grid(row=1, column=1, padx=10, pady=10)

ttk.Button(root, text="read aloud", style='TButton', command=summarize_and_voice).pack(pady=20)

result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, wraplength=550, justify="left", background="#f0f0f0", padding=10)
result_label.pack(padx=10, pady=10, fill="both", expand=True)

# Run the application
root.mainloop()
