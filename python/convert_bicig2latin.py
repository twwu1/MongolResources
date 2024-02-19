#Convert traditional Mongol letters (Mongol bicig) into the Roman alphabet.
#This program is meant for the literary Mongol spelling rules, not for those of the Cyrillic script in the Khalkha dialect.
#A converter between Cyrillic and bicig can be found here: http://trans.mglip.com/EnglishC2T.aspx

#Unicode has the same code for both the back vowel g sound and the front vowel g sound, so this python program only uses the letter 'g' to represent both sounds; likewise for the q/k sounds. 
#Sounds for transcribing sounds in foreign loanwords such as p are not included in this program.

# Please save the bicig text in a file called bicig_file.txt and store it next to this python file within the same folder.

f = open('bicig_file.txt', 'r')
text = f.read()
f.close()

dict = {'\u182D': 'g', '\u182C': 'k', '\u1832': 't', '\u1833': 'd', '\u1830': 's', '\u1831': 'š', '\u1834': 'č', '\u1835': 'ǰ', '\u182F': 'l', '\u1837': 'r', '\u1828': 'n', '\u182E': 'm', '\u1829': 'ŋ', '\u182A': 'b', '\u1836': 'y', '\u1820': 'a', '\u1823': 'o', '\u1824': 'u', '\u1821': 'e', '\u1825': 'ö', '\u1826': 'ü', '\u1822': 'i'}
bicig_chars = dict.keys()

punctuation_dict = {'\u1801': '....', '\u1802': ',', '\u1803': ';', '\u1804': ':', '\u1805': '\n', '\u003F':'\u003F', '\n': '\n', '\u202F': '-'}
punctuations = punctuation_dict.keys()

text = text.replace('\n', ' \n')
words = text.split(' ')

print(words)

output = ""
for word in words:
    for char in word:
        if char in bicig_chars:
            output = output + dict[char]
        elif char in punctuations:
            output = output + punctuation_dict[char]
    output = output + " "

output_file = open('romanized_file.txt', 'w')
output_file.write(output)
output_file.close()