import re

def get_words(filename):
    f = open(filename, 'r')
    lines = list(f)
    lines = [line for line in lines if not is_comment(line)]
    s = ''.join(lines)
    w = re.split("\W+", s)
    return [x for x in w if x] # filter empty strings

def is_comment(line):
   # if a line starts with %, its a comment line
   s = line.lstrip()
   if len(s) == 0:
       return  True
   if s[0] == '#':
       return True
   else:
       return False

    
