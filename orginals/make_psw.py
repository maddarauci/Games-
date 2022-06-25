#python
from random import randint
#import pyperclip

allSymbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
		'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
		'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 
		'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
		'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', 
		'5', '6', '7', '8', '9', '0', '- ', '=', '`', '~', '!', '@', '#', '$', 
		'%', '^', '&', '*', ' (', ' )', ' ¹', '²', '³', '⁴', '⁵', '⁶', '⁷', 
		'⁸', '⁹', '⁰', '¡', '¤', '€', '¼', '½', ' ¾', '‘', '’', 'æ', '©', 
		'®', 'þ', '«', '»', '"', "'", 'ß', '§', 'ð', 'œ', 'Æ', 'Œ', 'ø', 
		'¶', 'Ø', '°', '¿', '£', '‘¥', '÷', '×', '/', '?' ]

password = ' '
lenSymbols = len(allSymbols)
recycleMe = int(input("how much characters do you want your password to be?     "))

for i in range(recycleMe):
    password = password + allSymbols[randint(0, lenSymbols)]
print(password)
##pyperclip.copy(password)
##print("copied to clipboard")
print(password)