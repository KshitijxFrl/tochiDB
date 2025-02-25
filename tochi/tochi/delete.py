import re

def normalize_text(text):
    """
    Normalize text by replacing sensitive information with question marks.
    
    Args:
        text (str): Input text to normalize
        
    Returns:
        str: Normalized text with sensitive information replaced
    """
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
print(normalize_text("create a user in the table nuc with fields name = Alan, number = 1 and email = alan@gmail.com and date = 2025-5-1"))
print(normalize_text("create a user in the table nuc with fields name = Wade, number = 2 and email = wade@gmail.com"))
print(normalize_text("create a user in the table nuc with fields name = Todd, number = 3 and email = todd@gmail.com"))
print(normalize_text("create a user in the table nuc with fields name = Goku, number = 3 and email = goku@gmail.com"))