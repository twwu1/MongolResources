#Convert Romanized alphabet of literary Mongol into traditional Mongol letters (Mongol bicig).
#This program is meant for the literary Mongol spelling rules, not for those of the Cyrillic script in the Khalkha dialect.
#A converter between Cyrillic and bicig can be found here: http://trans.mglip.com/EnglishC2T.aspx

#Supported letters are the following:
#   Vowels: a, o, u, e, ü, ö, i
#   Consonants: g, k, b, m, n, ŋ, ǰ, č, š, s, l, r, y
#A modified form of the German keyboard or Turkish keyboard might be best for typing these letters.

#Unicode has the same code for both the back vowel g sound and the front vowel g sound, so this python program only uses the letter 'g' to represent both sounds; likewise for k. 
#For noun case endings, a hyphen '-' must be in between the noun and the case ending for it to be rendered properly. 
#In order to be rendered properly, the resulting bicig text must be printed in font styles dedicated to the traditional Mongol script.

#At the moment, this program has the following limitations:
#Punctuation marks are not supported.
#Special letters for transcribing foreign loanwords are not supported.
#Vowels in foreign loanwords that do not conform to vowel harmony rules are not supported.
#The number of MVS exceptions is still very small; only two: ene, tere.

#Please save the Romanized text in a file called romanized_file.txt and store it next to this python file within the same folder.

f = open('romanized_file.txt', 'r')
text = f.read()
f.close()

dict = {'g': '\u182D', 'k': '\u182C', 't': '\u1832', 'd': '\u1833', 's': '\u1830', 'š': '\u1831', 'č': '\u1834', 'ǰ': '\u1835', 'l': '\u182F', 'r': '\u1837', 'n': '\u1828', 'm': '\u182E', 'ŋ': '\u1829', 'b': '\u182A', 'y': '\u1836', 'a': '\u1820', 'o': '\u1823', 'u': '\u1824', 'e': '\u1821', 'ö': '\u1825', 'ü': '\u1826', 'i': '\u1822', '-': '\u202f'}
#MVS is the unicode character \u180E inserted between the detached vowel and the rest of the word.
MVS_consonants = {'n': '', 'g': '', 'k': '', 'r': '', 'l': '', 'm': '', 'y': ''}.keys()
MVS_exceptions = {'ene': '', 'tere': ''}.keys()
bicig_chars = dict.keys()
words = text.split(' ')

print(words)

output = ""
for word in words:
    word_len = len(word)
    prev_char = " "
    for i in range(0, word_len):
        char = word[i]
        if char in bicig_chars:
            
            last_char = i == word_len - 1
            follows_MVS_cons = prev_char in MVS_consonants and (char == 'a' or char == 'e')
            isMVSexception = word in MVS_exceptions

            if last_char and follows_MVS_cons and not isMVSexception:
                output = output + '\u180E' #add MVS character for rendering detached vowels
            
            output = output + dict[char]
            prev_char = char
    
    output = output + " "

output_file = open('bicig_file.txt', 'w')
output_file.write(output)
output_file.close()