#Convert traditional Mongol letters (hudum bicig) into the Roman alphabet.
#This program is meant to assign a Latin letter to each hudum letter, not for converting to the Cyrillic spellings in the Khalkha dialect.
#A converter between Cyrillic and hudum can be found here: http://trans.mglip.com/EnglishC2T.aspx

#Unicode has the same code for both the back vowel g sound and the front vowel g sound, so this python program only uses the letter 'g' to represent both sounds; likewise for q. 

# Please save the hudum text in a file called hudum_file.txt and store it next to this python file within the same folder.

f = open('hudum_file.txt', 'r')
text = f.read()
f.close()

dict = {'\u182D': 'g', '\u182C': 'q', '\u1832': 't', '\u1833': 'd', '\u1830': 's', '\u1831': 'š', '\u1834': 'č', '\u1835': 'ǰ', '\u182F': 'l', '\u1837': 'r', '\u1828': 'n', '\u182E': 'm', '\u1829': 'ŋ', '\u182A': 'b', '\u1820': 'a', '\u1823': 'o', '\u1824': 'u', '\u1821': 'e', '\u1825': 'ö', '\u1826': 'ü', '\u1822': 'i', '\u1836': 'y',
        #Foreign Sounds
        '\u1827': 'ē', '\u182B': 'p', '\u1839': 'f', '\u183A': 'k', '\u183B': 'ǩ', '\u183C': '\u02A6', '\u183D': 'z', '\u183E': 'h', '\u183F': 'ẑ', '\u1841': 'ĵ', '\u1842': 'ĉ'
        }
hudum_chars = dict.keys()

punctuation_dict = {'\u1801': '....', '\u1802': ',', '\u1803': ';', '\u1804': ':', '\u202F': '-'}
punctuations = punctuation_dict.keys()

text = text.replace('\n', ' \n ')
words = text.split(' ')

print(words)

output = ""
for word in words:
    if '\u180B' in word: #if a recent foreign loanword needing special letter forms
        output = output + '*'
    for char in word:
        if char in hudum_chars:
            output = output + dict[char]
        elif char in punctuations:
            output = output + punctuation_dict[char]
        else:
            output = output + char
    
    if not word.isspace():
        output = output + " "

output_file = open('romanized_file.txt', 'w')
output_file.write(output)
output_file.close()