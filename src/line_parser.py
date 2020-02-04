import argparse
import json
import cv2
import random
import numpy as np
import re


class LineParser:
    def __init__(self, hashes):
        self.hashes = hashes

    # Generates and image of a line of text
    def parse_line(self, line):
        
        assert(len(line) > 0)
        
        counter = 1

        # initialze finalImage to the image of first word before appending other words
        letter = line[0]
        if check_inv(letter):
            letter = 'inv'
        elif check_dinv(letter):
            letter = 'dinv'

        key = letter + str(counter) + '.jpg'
        
        if letter == ' ':
            letter = 'whitespace'
            key = letter + '.jpg'
        finalImage = np.array(self.hashes[key], dtype = np.uint8)

        for i in range(1, len(line)):
            # In every iteration of counter is a random number between 1..5
            counter = random.randrange(1, 6, 1)
            letter = line[i]
            
            # JSON file contains dictionary where key is like A3.jpg and value is image array
            # Keys are accordingly generated
            if check_inv(letter):
                letter = 'inv'
            elif check_dinv(letter):
                letter = 'dinv'
            
            key = letter + str(counter) + '.jpg'

            if letter == ' ':
                letter = 'whitespace'
                key = letter + '.jpg'
            finalImage = np.hstack((finalImage, np.array(self.hashes[key], dtype = np.uint8)))

        return finalImage      

    # Generates image of a line of text where output image length is fixed
    # Can be thought of as a wrapper around parse_line
    def parse_line_constrained(self, line, MAX_CHARS): 
        
        assert(MAX_CHARS > 0)
        
        totalChars = len(line)
        wordlist = line.split()
        leftover = ''

        partialLength = 0
        charsCovered = 0
        finalImage = np.array([[]], dtype = np.uint8)
        starting = True

        # 2 characters on left edge are used up for blankspaces
        if MAX_CHARS > 2:
            finalImage = self.parse_line('  ')
            MAX_CHARS -= 2

        # line image is generated word by word
        for word in wordlist:
            partialLength += len(word) + 2 # in every iteration one word and two spaces are added
            charsCovered += len(word) + 1 # in every iteration one word and a space are covered from text line
            
            if partialLength > MAX_CHARS:
                charsCovered -= (len(word) + 1)
                partialLength -= (len(word) + 2)
                leftover = line[charsCovered:] + ' '
                break
            
            finalImage = np.hstack((finalImage, self.parse_line(word)))
            finalImage = np.hstack((finalImage, self.parse_line('  ')))

            starting = False
        
        # Add spaces to the end of line
        n_spaces = MAX_CHARS - partialLength
        if starting:
            finalImage = self.parse_line(' ')
            n_spaces -= 1
        spaces = ' '*(n_spaces)
        if(len(spaces) > 0):
            finalImage = np.hstack((finalImage, self.parse_line(spaces)))
        # leftover is the text that did not fit in line
        return finalImage, leftover 


    def show(self, window_name, image):
        cv2.imshow(window_name, image)
        cv2.waitKey()
        cv2.destroyWindow(window_name)

def check_inv(letter):
    if ord(letter) == 8216 or ord(letter) == 8217:
        return True
    else:
        return False

def check_dinv(letter):
    if ord(letter) == 8220 or ord(letter) == 8221:
        return True
    else:
        return False

def main():
    # Used to decide which image of letter will be used. Goes from 1 to 5
    counter = 1 

    with open('hashes.json') as f:
        hashes = json.load(f)
    # JSON file contains dictionary where key is like A3.jpg and value is image array
    word = args.word[0]
    letter = word[0]
    if letter == ' ':
        letter = 'whitespace'
    key = letter + str(counter) + '.jpg'
    finalImage = np.array(hashes[key], dtype = np.uint8)

    for i in range(1, len(word)):
        # In every iteration of counter is a random number between 1..5
        counter = random.randrange(1, 6, 1)
        letter = word[i]
        key = letter + str(counter) + '.jpg'
        if letter == ' ':
            letter = 'whitespace'
            key = letter + '.jpg'
        finalImage = np.hstack((finalImage, np.array(hashes[key], dtype = np.uint8)))

    show(args.word[0], finalImage)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Output image for word')
    parser.add_argument('word', type=str, nargs=1)
    args = parser.parse_args()
    main()