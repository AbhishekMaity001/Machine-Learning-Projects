""""

.       - Any Character Except New Line
\d      - Digit (0-9)
\D      - Not a Digit (0-9)
\w      - Word Character (a-z, A-Z, 0-9, _)
\W      - Not a Word Character
\s      - Whitespace (space, tab, newline)
\S      - Not Whitespace (space, tab, newline)

\b      - Word Boundary
\B      - Not a Word Boundary
^       - Beginning of a String
$       - End of a String

[]      - Matches Characters in brackets
[^ ]    - Matches Characters NOT in brackets
|       - Either Or
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


#### Sample Regexs ####

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+

"""


import re

print('\t Tab') # Normal String
print(r'\t Tab') # Raw string

text_to_search = ''''
            
    abcdefghijklmnopqrstuvwxyz
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    1234567890
    Ha HaHa
    
    MetaCharacters (Need to be escaped) :
    . ^ $ * + ? { } [ ] \ | ( )
    
    coreyms.com       
    
    321-555-4321
    123.555.1234
    123*658*6235
    800-555-4321
    900.555.1234
    34345.343-3534
    
    hist
    bist
    kist
    mist
    list
    
    Mr. Schafer
    Mr Smith
    Ms Davis
    Mrs. Robinson
    Mr. T
'''

emails = '''
CoreyMSchafer@gmail.com
corey.schafer@university.edu
corey-321-schafer@my-work.net
'''

urls = '''
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
'''

sentence = "Start a sentence and then bring it to an end"

#pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
#pattern = re.compile(r'\d\d\d[-.]\d\d\d[-.]\d\d\d\d')
#pattern = re.compile(r'[89]00[-.]\d\d\d[-.]\d\d\d\d')
#pattern = re.compile(r'[^A-Za-z]')
#pattern = re.compile(r'[^l]ist')
#pattern = re.compile(r'\d{3}.\d{3}.\d{4}')
#pattern = re.compile(r'Mrs?\.?\s[A-Z]\w*')
#pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w*')
#pattern = re.compile(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.(com|edu|net)')
#pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
#pattern = re.compile(r'https?://(www\.)?\w+\.\w+')

#pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
#sub_pattern = pattern.sub(r'\2\3',urls)

# finditer method gives the matched and non matched patterns with some extra functionality....it returns an iterable
# findall method gives the matched and in a form of a list...it returns an iterable
# match method will only return the first element at the begning and dosent returns an iterable
# search method will search the given pattern in the whole sentence and will return only the first matched else it will return None
# flags helps us to ignore cases and many more ... re.compile(r'start',re.IGNORECASE)
pattern = re.compile(r'Start')
print(pattern.match(sentence))

pattern = re.compile(r'\d{3}.\d{3}.\d{4}')
matches = pattern.findall(text_to_search)
for match in matches :
    print(match)

pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
sub_pattern = pattern.sub(r'\2\3',urls)
print(sub_pattern)


matches = pattern.finditer(urls)
for match in matches :
    print(match.group(2,3))

#print(text_to_search[50:53])
print('**********************************************\n')

with open('data.txt','r') as f:
    contents = f.read()
    pattern = re.compile(r'[89]00[.-]\d\d\d[-.]\d\d\d\d')
    matches = pattern.finditer(contents)
    for match in matches:
        print(match)



