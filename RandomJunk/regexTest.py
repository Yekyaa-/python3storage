import re

def regex(string):
    
    patternW = re.compile(r"\w+")
    pattern = re.compile(r'\d{1,}') # For brevity, this is the same as r"\d+"
    result = pattern.match(string)
    if result:
        return result.group()
    return None
    
#string = "regex is awesome!"

#result = pattern.match(string)
#print (result.group())
print (regex('007 James Bond'))

pattern = re.compile(r"\w+") # Match only alphanumeric characters
input_string = "Lorem ipsum with steroids"
result = pattern.sub("regex", input_string) # replace with the word regex
print (result)  # prints 'regex regex regex regex'


pattern = re.compile(r'\w+(?=\sfox)')
result = pattern.search("The quick brown fox")
print (result.group()) # prints 'brown'


pattern = re.compile(r"\w+(?=,)")
res = pattern.findall("Me, myself, and I")
print (res)



number = 1234567890
#input("Enter your number\n")


def monetizer(number):
    """This function adds a thousands separator using comma characters."""
    number = str(number)
    try:
        if type(int(number)) == int:
            # Format into groups of three from the right to the left
            pattern = re.compile(r'\d{1,3}(?=(\d{3})+(?!\d))')
            # substitute with a comma then return
            return pattern.sub(r'\g<0>,', number)
    except:
        return "Not a Number"

# Function call, passing in number as an argument
print (monetizer(number))
