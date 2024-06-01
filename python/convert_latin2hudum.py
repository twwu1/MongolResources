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
#Aside from the t/d and o/u/ü/ö of foreign loanwords, this font file automatically converts letters to their correct forms without the need of FVS keys.
#For example, without the dedicated font file, the word "bičig" would need the unicode character FVS2 (U+180C) affixed to the end to change the 'g' to its front vowel form, but with mnglwhiteotf.ttf this is not necessary.

#The t/d and o/u/ü/ö of recent (mostly European) loanwords have special forms:
#   't' must always be in its usual initial form.
#   'd' cannot be in its usual initial form, nor in its usual final form.
#   o/u cannot be in its usual final form.
#   ü/ö must always have a yod in its non-final form. 
#       In its final form, ü/ö is writtenlike the medial form of o/u, and the spine then forms a small hook pointing towards the lower-left.

#To display the special forms of t/d and o/u/ü/ö, print an asterix (*), which toggles the loanword forms, and all subsequent t/d and o/u/ü/ö are printed in their loanword forms until the toggle turns off.
#The loanword toggle turns off at the end of the word, when a punctuation mark or whitespace is encountered, or when another asterix '*' is encountered.

#For example, the loanword 'radio' would be displayed incorrectly without an asterix, because the 'o' would appear in its usual final form.
#Printed as *radio, however, this would be displayed correctly.
#This python program would automatically affix an FVS1 after the 'o' when the asterix toggle is on.

#Another example would be 'kompiütēr', which would be romanized as *kompiütēr in this program.
#The program would automatically insert FVS1 after the 'ü' and the 't' when the asterix toggle is on.

#Since the asterix '*' serves as a toggle, words with mixed foreign and native roots are also allowed, by putting an asterix between the native roots and recent foreign roots.
#For example, suppose that for some reason the word 'kompiütērqagantu', made up of the two roots kompiütēr and qagantu, enters the mongol vocabulary.
#In this case, 'kompiütērqagantu' can be romanized as *kompiütēr*qagantu.
#Likewise, the hypothetical word 'qagantukompiütēr' can also be handled by romanizing it as qagantu*kompiütēr

#At the moment, this program has the following limitations:
#The number of MVS exceptions is still very small; only two: ene, tere.
#This program does not account for font styles not dedicated to hudum

#Please save the Romanized text in a file called romanized_file.txt and store it next to this python file within the same folder.

f = open('romanized_file.txt', 'r', encoding="utf8")
text = f.read()
f.close()

dict = {'g': '\u182D', 'q': '\u182C', 't': '\u1832', 'd': '\u1833', 's': '\u1830', 'š': '\u1831', 'č': '\u1834', 'ǰ': '\u1835', 'l': '\u182F', 'r': '\u1837', 'n': '\u1828', 'm': '\u182E', 'ŋ': '\u1829', 'b': '\u182A', 'y': '\u1836', 'a': '\u1820', 'o': '\u1823', 'u': '\u1824', 'e': '\u1821', 'ö': '\u1825', 'ü': '\u1826', 'i': '\u1822', 'w': '\u1838',
        
        #Foreign Sounds
        'ē':'\u1827', 'p': '\u182B', 'f':'\u1839', 'k': '\u183A', 'ǩ':'\u183B', '\u02A6': '\u183C', 'z': '\u183D', 'h': '\u183E', 'ẑ': '\u183F', 'ł': '\u1840', 'ĵ':'\u1841', 'ĉ': '\u1842',
        #asterix for toggling loanword forms
        '*': ''
        }
letter_inventory = dict.keys()
#The hyphen '-' is always converted to NNBSP (U+202f)
punctuation_dict = {'-': '\u202f', '....': '\u1801', ',': '\u1802', ';': '\u1803', '.': '\u1803', ':': '\u1804'}
punctuations = punctuation_dict.keys()

#MVS is the unicode character U+180E inserted between the detached vowel and the rest of the word.
MVS_consonants = {'n', 'g', 'q', 'r', 'l', 'm', 'y'}
MVS_exceptions = {'ene', 'tere'}
vowels = {'a', 'o', 'u', 'e', 'ü', 'ö', 'i', 'ē'}

#remove trailing whitespace in each line
lines = text.split('\n')
text = ""
num_lines = len(lines)
for i in range(0, num_lines):
    line = lines[i]
    line_len = len(line)
    if line_len > 0:
        line.rstrip()
        line_len = len(line)
        if i < num_lines - 1 or line_len > 0:
            text = text + line + '\n'

#split text into array of words
#each newline character is treated as a separate word
new_text = ""
text_len = len(text)
for i in range(0, text_len):
    char = text[i]
    if not char in letter_inventory and not char == '\u0000':
        new_text_len = len(new_text)
        if new_text_len > 0 and not new_text[new_text_len - 1] == '\u0000':
            new_text = new_text + '\u0000'
        new_text = new_text + char + '\u0000'
    else:
        new_text = new_text + char
       
words = new_text.split('\u0000')

print(words)

output = ""
for word in words:
    word_len = len(word)
    prev_char = ""

    isRecent_loanword = False  
    foreign_root_beginning_index = 0    

    for i in range(0, word_len):
        char = word[i]
        
        if char == '*':
            if not isRecent_loanword:
                foreign_root_beginning_index = i
                isRecent_loanword = True
            else:
                if prev_char == 'd':
                    output = output + '\u180B'
                isRecent_loanword = False
             
        elif char in letter_inventory:
            
            #if char is the last letter in a word
            if i == word_len - 1 or not word[i + 1] in letter_inventory:
                follows_MVS_cons = prev_char in MVS_consonants and (char == 'a' or char == 'e')
                isGEorQEending = (prev_char == 'g' or prev_char == 'q') and char == 'e'
                
                if follows_MVS_cons and (not isGEorQEending) and not (word in MVS_exceptions):
                    output = output + '\u180E' #add MVS character for rendering detached vowels          
            output = output + dict[char]
        
        elif char in punctuations:
            output = output + punctuation_dict[char]
        
        else:
            output = output + char
            
        #Handle the special forms of recent loanwords
        #'\u180B' is FVS1
        #for ease of reading, if statements might be nested even when nesting is not necessary
        if (not char == '*') and isRecent_loanword:
            if char == 'd':
                if i == foreign_root_beginning_index + 1:
                    output = output + '\u180B'
                elif i == word_len - 1 or not word[i + 1] in vowels:
                    output = output + '\u180B'
            elif char == 't':
                if i > foreign_root_beginning_index + 1:
                    output = output + '\u180B'
            elif char == 'ö' or char == 'ü':
                if i > foreign_root_beginning_index + 2:
                    output = output + '\u180B'
            elif char == 'o' or char == 'u' and i == word_len - 1:
                output = output + '\u180B'

        prev_char = char
        
        
output_file = open('hudum_file.txt', 'w', encoding="utf8")
output_file.write(output)
output_file.close()
