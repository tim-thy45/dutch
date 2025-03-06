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
    Extracts text from the image using Tesseract OCR, parses it with the AI model,
    and displays food items and prices with checkboxes in a Tkinter window.
    """
    try:
        img = Image.open(image_path)
        bill_text = pytesseract.image_to_string(img, config='--psm 6')

        # Get food items and prices from the AI model
        food_items = chat.send_message('the text extracted from a food bill is' + bill_text + '''give me only the food items and their respective prices from this 
                                         food bill with each food iteam on a seperate line.i want only the food items and their prices and strictly nothing else.
                                         The food items in this bill are given in a table format where the name of the food item is given on
                                         the left and how much that item cost is given on the right. each iteam with a seperate price is a 
                                         seperate food item.''')
        food_data = food_items.candidates[0].content.text.splitlines()

        # Create Tkinter window
        window = tk.Tk()
        window.title("Food Items and Prices")

        # Initialize variables for checkboxes and prices
        checkboxes = {}
        prices = {}

        # Loop through each food item line
        for line in food_data:
            # Separate food item and price (assuming simple format)
            try:
                item, price = line.split(":")
                item = item.strip()  # Remove leading/trailing whitespace
                price = float(price.strip())  # Convert price to float
            except ValueError:
                # Skip lines that don't follow the expected format
                continue

            # Create checkbox and price label
            checkboxes[item] = tk.IntVar()
            price_label = tk.Label(window, text=f"{item}: ${price:.2f}")
            checkbox = tk.Checkbutton(
                window, text=item, variable=checkboxes[item], onvalue=1, offvalue=0
            )

            # Pack widgets
            checkbox.pack(anchor=tk.W)
            price_label.pack(anchor=tk.W)

        # Process selected items later (optional)
        def process_selection():
            selected_items = [item for item, var in checkboxes.items() if var.get()]
            # Do something with selected items (e.g., calculate total price)
            print(f"Selected items: {', '.join(selected_items)}")

        # Button to trigger selection processing (optional)
        process_button = tk.Button(window, text="Process Selection", command=process_selection)
        # process_button.pack()  # Uncomment to add a button

        window.mainloop()

    except FileNotFoundError:
        print("Error: File not found.")


# Initialize Tkinter GUI
root = tk.Tk()
#root.withdraw()  # Hide the main window

# Create a button to trigger image selection
button = tk.Button(root, text="Select Image", command=select_image)
button.pack()

# Start the event loop (waits for button click)
root.mainloop()
