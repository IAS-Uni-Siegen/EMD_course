import os
import fileinput
from subprocess import call

os.makedirs('built', exist_ok=True)
call_pdflatex_l = ['pdflatex', '-synctex=1',
                   '-interaction=nonstopmode', 'main.tex']


def clear_tex_binaries():
    # clean misc files
    for file in os.listdir('.'):
        if file.startswith('main'):
            if not file.endswith(('.tex', '.pdf')):
                os.remove(file)


# build main pdf
clear_tex_binaries()
with fileinput.input('main.tex', inplace=True) as f:
    for line in f:
        if 'includeonly{' in line:
            # comment out includeonly flag
            print(f'%{line}', end='')
        #check if a line include 'handout' parameter and if yes, delete it
        elif 'handout' in line:
            print(line.replace('handout', ''), end='')
        else:
            print(line, end='')
        
call(call_pdflatex_l)
call(call_pdflatex_l)
os.replace('main.pdf', os.path.join('built', 'main.pdf'))
