"""
Description: A class that scrapes a specific URL to display the IP address shown.
Author: Mischa Pustogorodsky
Date: Oct 19/2024
"""

from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    def __init__(self):
        # Initialize the HTML parser and set up variables to hold data
        super().__init__()
        self.body = False  # Currently not tracking if we are in the body
        self.ip = ""       # Variable to hold the extracted IP address

    def handle_data(self, data):
        # This method is called whenever we find text data in the HTML
        if "Current IP Address:" in data:  
            # If the text includes the label for the IP address,
            # we extract the actual IP address by splitting the string at ":"
            ip_address = data.split(": ")[1].strip()  
            # Print the extracted IP address without extra spaces
            print(ip_address)  

def get_ip():
    # Create an instance of the parser
    myparser = MyHTMLParser()

    # Download the webpage that shows the current IP address
    with urllib.request.urlopen("http://checkip.dyndns.org") as response:
        html = str(response.read())  # Read the content of the webpage

    # Feed the HTML content to the parser to process it
    myparser.feed(html)

    return myparser.ip 

if __name__ == "__main__":
    print(get_ip())

    #a note to add a commit