import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import google.generativeai as genai

genai.configure(api_key='AIzaSyB8m_g5zV1oyLB4aiOlJLz_2JYJDB2qWMw')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def select_image():
    """
    Opens a file dialog to select an image and calls the extract_text function.
    """
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    extract_text(image_path)

def extract_text(image_path):
    """
    Extracts text from the image using Tesseract OCR and prints it.
    """
    try:
        img = Image.open(image_path)
        bill_ext = pytesseract.image_to_string(img, config='--psm 6')
        #print(bill_ext)
        print("the food items here are:")
        food_items= chat.send_message('the text extracted from a food bill is' + bill_ext + '''give me only the food items and their respective prices from this 
                                    food bill with each food iteam on a seperate line.i want only the food items and their prices and strictly nothing else.
                                    The food items in this bill are given in a table format where the name of the food item is given on
                                    the left and how much that item cost is given on the right. each iteam with a seperate price is a 
                                    seperate food item.''')
        food_text = food_items.candidates[0].content.parts[0].text

        # Print only the food items (lines will be separated by \n)
        print("Food Items:")
        print(food_text)
    except FileNotFoundError:
        print("Error: File not found.")

# Initialize the Tkinter GUI (minimal for this script)
root = tk.Tk()
#root.withdraw()  # Hide the main window

# Create a button to trigger image selection
button = tk.Button(root, text="Select Image", command=select_image)
button.pack()

# Start the event loop (waits for button click)
root.mainloop()
