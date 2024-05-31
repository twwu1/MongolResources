#Convert Romanized alphabet of literary Mongol into traditional Mongol letters (hudum bicig).
#This program handles the traditional spellings, not those of the Cyrillic script in the Khalkha dialect.
#A converter between Cyrillic and hudum can be found here: http://trans.mglip.com/EnglishC2T.aspx

#Supported letters are the following:
#   vowels: a, o, u, e, ü, ö, i
#   consonants: g, q, b, m, n, ŋ, ǰ, č, š, s, l, r, w, y
#   foreign sounds: ē, p, f, k, ǩ, ʦ (U+02A6), z, h, ĵ, ł, ĉ, ẑ
#A modified form of the German keyboard or Turkish keyboard might be best for typing these letters.
#Modified keyboards could be made with Keyman, at https://keyman.com/developer/

#Unicode has the same code for both the back vowel g sound and the front vowel g sound, so this python program only uses the letter 'g' to represent both sounds; likewise for q.
#The character 'U+183A' (like a backwards 'C' with two or three prongs sticking out of its upper tip) was borrowed directly from the old Uyghur alphabet, and originally served as the front vowel K in the medieval Mongol alphabet, but then in later times it came to be only used for foreign loanwords.
#Outside of foreign loanwords, the front vowel K came to be written with only one prong on its upper tip; this character has the same unicode as the back vowel q.
 
#For noun case endings, a hyphen '-', which is converted to NNBSP (U+202f), must be in between the noun and the case ending for it to be rendered properly.
#In order to be rendered properly, the resulting hudum text must be printed in font styles dedicated to the traditional Mongol script.

#A recommended font file is supplied in the same folder as this program called mnglwhiteotf.ttf
#Aside from the t/d and o/u/ü/ö of foreign loanwords, this font file automatically converts letters to their correct forms without the need of FVS keys
#For example, without the dedicated font file, the word "bičig" would need the unicode character FVS2 (U+180C) affixed to the end to change the 'g' to its front vowel form, but with mnglwhiteotf.ttf this is not necessary

#The t/d and o/u/ü/ö of recent (mostly European) loanwords have special forms:
#   't' must always be in its initial form 
#   'd' cannot be in its initial form, nor in its final form
#   o/u cannot be in its final form
#   ü/ö must always have a yod
#To display these special forms, print an asterix (*) as the first symbol of the word 

#For example, the loanword 'radio' would be displayed incorrectly without an asterix, because the 'o' would appear in its final form.
#Printed as *radio, however, this would be displayed correctly.
#This python program would automatically affix an FVS1 after the 'o'
#Another example would be 'kompiütēr', which would be printed as *kompiütēr in this program.
#The program would automatically insert FVS1 after the 'ü' and the 't'

#At the moment, this program has the following limitations:
#The number of MVS exceptions is still very small; only two: ene, tere.
#This program does not account for font styles not dedicated to hudum

#Please save the Romanized text in a file called romanized_file.txt and store it next to this python file within the same folder.

f = open('romanized_file.txt', 'r', encoding="utf8")
text = f.read()
f.close()

dict = {'g': '\u182D', 'q': '\u182C', 't': '\u1832', 'd': '\u1833', 's': '\u1830', 'š': '\u1831', 'č': '\u1834', 'ǰ': '\u1835', 'l': '\u182F', 'r': '\u1837', 'n': '\u1828', 'm': '\u182E', 'ŋ': '\u1829', 'b': '\u182A', 'y': '\u1836', 'a': '\u1820', 'o': '\u1823', 'u': '\u1824', 'e': '\u1821', 'ö': '\u1825', 'ü': '\u1826', 'i': '\u1822', 'w': '\u1838',
        
        #Foreign Sounds
        'ē':'\u1827', 'p': '\u182B', 'f':'\u1839', 'k': '\u183A', 'ǩ':'\u183B', '\u02A6': '\u183C', 'z': '\u183D', 'h': '\u183E', 'ẑ': '\u183F', 'ł': '\u1840', 'ĵ':'\u1841', 'ĉ': '\u1842'
        }
letter_inventory = dict.keys()
#The hyphen '-' is always converted to NNBSP
punctuation_dict = {'-': '\u202f', '....': '\u1801', ',': '\u1802', ';': '\u1803', ':': '\u1804'}
punctuations = punctuation_dict.keys()

#MVS is the unicode character U+180E inserted between the detached vowel and the rest of the word.
MVS_consonants = {'n': '', 'g': '', 'q': '', 'r': '', 'l': '', 'm': '', 'y': ''}.keys()
MVS_exceptions = {'ene': '', 'tere': ''}.keys()
hudum_chars = dict.keys()
vowels = {'a', 'o', 'u', 'e', 'ü', 'ö', 'i', 'ē'}

#remove trailing whitespace in each line
lines = text.split('\n')
text = ""
num_lines = len(lines)
for i in range(0, num_lines):
    line = lines[i]
    line_len = len(line)
    if line_len > 0:
        line.strip(' ')
        line.strip('\t')
        line_len = len(line)
        if i < num_lines - 1 or line_len > 0:
            text = text + line + '\n'

#split text into array of words
#each newline character is treated as a separate word
text = text.replace('\n', ' \n ')
words = text.split(' ')

print(words)

output = ""
for word in words:
    word_len = len(word)
    prev_char = " "
    
    word_beginning_index = 0
    isRecent_loanword = False

    if word_len > 0 and word[0] == '*': #if the first character of word is an asterix
        isRecent_loanword = True
        word_beginning_index = 1

    for i in range(word_beginning_index, word_len):
        char = word[i]
        if char in hudum_chars:
            
            last_char = i == word_len - 1 or not word[i + 1] in letter_inventory
            follows_MVS_cons = prev_char in MVS_consonants and (char == 'a' or char == 'e')
            isMVSexception = word in MVS_exceptions

            if last_char and follows_MVS_cons and not isMVSexception:
                output = output + '\u180E' #add MVS character for rendering detached vowels
            
            output = output + dict[char]
            prev_char = char
        elif char in punctuations:
            output = output + punctuation_dict[char]
        else:
            output = output + char

        #Handle the special forms of recent loanwords
        #'\u180B' is FVS1
        if isRecent_loanword:
            if char == 'd':
                if i == word_beginning_index:
                    output = output + '\u180B'
                elif i == word_len - 1 or not word[i + 1] in vowels:
                    output = output + '\u180B'
            elif char == 't':
                if i > word_beginning_index:
                    output = output + '\u180B'
            elif char == 'ö' or char == 'ü':
                if i > word_beginning_index + 1:
                    output = output + '\u180B'
            elif char == 'o' or char == 'u' and i == word_len - 1:
                output = output + '\u180B'
    
    if word_len > 0 and not word.isspace():
        output = output + " "

output_file = open('hudum_file.txt', 'w', encoding="utf8")
output_file.write(output)
output_file.close()
