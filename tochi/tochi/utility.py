from datetime import datetime
import re
import spacy
import json

query_cache = {}
norConverter = []

def update_query_cache(newNaturalQuery, newProcessedQuery):
    global query_cache
    query_cache[newNaturalQuery] = newProcessedQuery

def load_query_cache():
    global query_cache
    try:
        print("Loading cache memory...")
        with open("./cache.json", "r") as file:
           query_cache =  json.load(file).get("query_cache", {})
    except Exception as e:
        print(f'Error reading query cache!! Exiting with error {e}')     

def update_close_query_cache():
    global query_cache
    try:
        print("Updating cache memory...")
        with open("./cache.json", "w") as file:
           json.dump({"query_cache": query_cache}, file, indent=4)
    except Exception as e:
        print(f'Error updating query cache!! Exiting with error {e}')    
        
def initialize_norConverter():
    global norConverter
    norConverter = spacy.load("en_core_web_sm")

import re

def extract_values(natural_query):
    values = []
    
    # Regex patterns for different types of values
    patterns = [
        (r'\b\d+\b', "number"),  # Match numbers
        (r'\b[\w\.-]+@[\w\.-]+\.\w+\b', "email"),  # Match emails
        (r'name\s*=\s*[\'"]?([a-zA-Z]+)[\'"]?', "name")  # Match names
    ]
    
    # Find all matches and maintain order
    matches = []
    for pattern, label in patterns:
        for match in re.finditer(pattern, natural_query):
            matches.append((match.start(), match.group(), label))
    
    # Sort matches by their order of appearance in text
    matches.sort(key=lambda x: x[0])
    
    # Extract values in correct order
    values = [match[1] for match in matches]

    return tuple(values)



def extract_values2(natural_query):
    values = []
    
    numbers = re.findall(r'\b\d+\b', natural_query)
    values.extend(numbers)

    emails = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', natural_query)
    values.extend(emails)

    names = re.findall(r'name\s*=\s*[\'"]?([a-zA-Z]+)[\'"]?', natural_query)
    values.extend(names)

    print(values)

    return tuple(values)

def normalize_query(text):
    # Phone numbers (various formats)
    text = re.sub(r'\b\+?[\d\-\(\)\s\.]{10,}\b', '?', text)
    
    # All numbers (including single digits)
    text = re.sub(r'\b\d+\b', '?', text)
    
    # Email addresses
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '?', text)
    
    # Dates (various formats)
    # MM/DD/YYYY or DD/MM/YYYY
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '?', text)
    # YYYY-MM-DD
    text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', '?', text)
    # Month DD, YYYY
    text = re.sub(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', '?', text)
    
    # Names - look for name patterns in field assignments
    text = re.sub(r'name\s*=\s*[\'"]?([a-zA-Z]+)[\'"]?', r'name = ?', text)
    
    return text

def tochilogo():

    now = datetime.now()
    curr_session = now.strftime("%d/%m/%Y %H:%M:%S")

    #?-------------------------------------------

    print("                                     ")
    print("████████╗ ██████╗  ██████╗██╗  ██╗██╗")
    print("╚══██╔══╝██╔═══██╗██╔════╝██║  ██║██║")
    print("   ██║   ██║   ██║██║     ███████║██║")
    print("   ██║   ██║   ██║██║     ██╔══██║██║")
    print("   ██║   ╚██████╔╝╚██████╗██║  ██║██║")
    print("   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝")
    print("                                     ")
    print(f'|    Session: [{curr_session}]    |')
    print("                                     ")