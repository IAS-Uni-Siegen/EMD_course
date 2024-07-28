import os
import fileinput
from subprocess import call

call_pdflatex_l = ['pdflatex', '-synctex=1',
                   '-interaction=nonstopmode', 'main.tex']


def clear_tex_binaries():
    # clean misc files
    for file in os.listdir('.'):
        if file.startswith('main'):
            if not file.endswith(('.tex', '.pdf')):
                os.remove(file)


# build main pdf (with solutions)
clear_tex_binaries()
with fileinput.input('main.tex', inplace=True) as f:
    for line in f:
        if 'includeonly{' in line:
            # comment out includeonly flag
            print(f'%{line}', end='')
        #check if the line including '\documentclass' has the parameter 'solution' - if not add it
        elif '{exerciseClass}' in line:
            if 'solution' not in line:
                print(line.replace('{exerciseClass}', ', [solution]{exerciseClass}'), end='')
            else:
                print(line, end='')    
        else:
            print(line, end='')
        
call(call_pdflatex_l)
call(call_pdflatex_l)


# go into the parent directory
os.chdir('..')
os.makedirs('built', exist_ok=True)
#take main.pdf from the exercise folder and move it to the parent folder
os.replace('exercise/main.pdf', os.path.join('built', 'exercise_with_solution.pdf'))


# build main pdf (without solutions)
os.chdir('exercise')
clear_tex_binaries()
with fileinput.input('main.tex', inplace=True) as f:
    for line in f:
        if 'includeonly{' in line:
            # comment out includeonly flag
            print(f'%{line}', end='')
        #check if the line including '\documentclass' has the parameter 'solution' - if yes remove it
        elif '{exerciseClass}' in line:
            if 'solution' in line:
                print(line.replace(', [solution]{exerciseClass}', '{exerciseClass}'), end='')
            else:
                print(line, end='')    
        else:
            print(line, end='')
        
call(call_pdflatex_l)
call(call_pdflatex_l)


# go into the parent directory
os.chdir('..')
os.makedirs('built', exist_ok=True)
#take main.pdf from the exercise folder and move it to the parent folder
os.replace('exercise/main.pdf', os.path.join('built', 'exercise.pdf'))