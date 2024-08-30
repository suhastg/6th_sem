import pyttsx3
import tkinter as tk
from tkinter import messagebox
from huggingface_hub import InferenceClient

# Initialize Hugging Face client
client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token="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",
)

def fetch_summary(title: str, sentences=2):
    """
    Fetches summary from Hugging Face model.
    :param title: (str) the topic to summarize
    :param sentences: (int) the number of sentences to include in the summary (optional, default is 2)
    :return: (str) the summary
    """
    try:
        prompt = f"answer '{title}' in {sentences} sentences."
        response = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=500, stream=False)
        summary = response.choices[0].message['content']
        return summary
    except Exception as e:
        return f"An error occurred: {e}"

def voicing_text(text):
    """
    Speaks the given text using the text-to-speech engine.
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

    summary = fetch_summary(wiki_page, num_of_sentences)
    result_text.set(summary)
    voicing_text(summary)

# Set up the main window
root = tk.Tk()
root.title("Topic Summary and Voice")

# Create and place the widgets
tk.Label(root, text="Text:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_page = tk.Entry(root, width=50)
entry_page.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Sentences:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_sentences = tk.Entry(root, width=50)
entry_sentences.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="read aloud", command=summarize_and_voice).grid(row=2, column=0, columnspan=2, pady=20)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                                                                                      
# Run the application
root.mainloop()
