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
  global image_path, tot_usr
  image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
  extract_text(image_path)

def extract_text(image_path):
  """
  Extracts text from the image using Tesseract OCR and prints it.
  """
  try:
    img = Image.open(image_path)
    bill_ext = pytesseract.image_to_string(img, config='--psm 6')

    print("the food items here are:")
    food_items = chat.send_message('the text extracted from a food bill is' + bill_ext + '''give me only the food items and their respective prices from this 
                 food bill with each food iteam on a seperate line.i want only the food items and their prices and strictly nothing else.
                 The food items in this bill are given in a table format where the name of the food item is given on
                 the left and how much that item cost is given on the right. each iteam with a seperate price is a 
                 seperate food item.the last 2 digits of the price are decimals strictly, in case the decimal point is missing, add it''')
    food_text = food_items.candidates[0].content.parts[0].text

    total_price_inc = chat.send_message('the text extracted from the food bill is' + bill_ext + '''give me the total price of all the entire
                 bill, this is the price written after all the food items and the taxes. i want on the total price and strictly nothing else ''')
    total_price=total_price_inc.candidates[0].content.parts[0].text
    total_price=float(total_price)
    # Print only the food items (lines will be separated by \n)
    print("Food Items:")
    print(food_text)
    print("The total price for all the food items:")
    print(total_price)
    print("Money to be paid by each person:")
    split= total_price/tot_usr.get()
    print(split)

  except FileNotFoundError:
    print("Error: File not found.")

# Initialize the Tkinter GUI
root = tk.Tk()

# Create a dropdown menu for selecting a number
tot_usr = tk.IntVar()
tot_usr.set(1)  # Set a default value of 1 for number of people
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # List of available options
dropdown = tk.OptionMenu(root, tot_usr, *numbers)
dropdown.pack()

# Create a button to trigger image selection
button = tk.Button(root, text="Select Image", command=select_image)
button.pack()

# Start the event loop
root.mainloop()
