"""
Description: A class that scrapes a specific url to display all listed color
names and their associated hex codes.
Author: Mischa Pustogorodsky
Date: Oct 19/2024
"""

from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.in_table = False  # Flag to track if we're within a table
        self.in_row = False  # Flag to track if we're within a row
        self.colors = []  # List to store extracted colors as tuples
        self.row_count = 0  # Counter to keep track of the number of rows
        self.headers = []  # List to store header names
        self.current_row = []  # List to store current row data

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True  # Set flag when entering a table
        elif tag == 'tr' and self.in_table:
            self.in_row = True  # Mark that we're in a row
            self.current_row = []  # Reset for a new row
            self.row_count += 1  # Increment the row count

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False  # Reset flag when leaving the table
        elif tag == 'tr' and self.in_table:
            if self.row_count > 1:  # Skip the header row
                if len(self.current_row) > 1:  # Ensure we have data
                    # Store color name and hex code using header indexes
                    color_name = self.current_row[self.headers.index("Color name")]
                    color_hex = self.current_row[self.headers.index("Hex")]
                    self.colors.append((color_name, color_hex))  # Append as a tuple
            self.in_row = False  # Mark that we're out of the row

    def handle_data(self, data):
        if self.in_table and self.in_row:
            data = data.strip()  # Clean the data by stripping whitespace
            if self.row_count == 1:
                self.headers.append(data)  # Capture header names on the first row
            else:
                self.current_row.append(data)  # Store data in the current row

# Instantiate the parser
myparser = MyHTMLParser()  # Create an instance of the MyHTMLParser class

# Fetch the webpage content
with urllib.request.urlopen("https://www.colorhexa.com/color-names") as response:
    html = response.read().decode('utf-8')  # Decode the response to a string

# Feed the HTML to the parser
myparser.feed(html)  # Start parsing the HTML content

# Print out the collected colors
for color_name, color_hex in myparser.colors:
    print(f"{color_name}: {color_hex}")  

total_colors = len(myparser.colors)  # Calculate total number of colors extracted
print(f"Total Colors: {total_colors}")  # Print the total count of colors