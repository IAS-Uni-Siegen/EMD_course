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

def build_pdf(with_solution):
    # Modify and build the main.tex file
    clear_tex_binaries()

    # Flag to ensure documentclass line is modified correctly
    docclass_modified = False
    
    with fileinput.input('main.tex', inplace=True) as f:
        for line in f:
            if 'includeonly{' in line:
                # Comment out the includeonly flag
                print(f'%{line}', end='')
            # Look for the documentclass line
            elif '\\documentclass' in line and 'exerciseClass' in line:
                docclass_modified = True  # Set the flag that we have modified the line

                # Split documentclass into its components
                preamble, class_info = line.split('{', 1)
                class_name = class_info.rstrip('}\n')  # Remove the trailing }
                
                if with_solution:
                    # Add the [solution] option if not present
                    if '[' not in preamble:
                        preamble = preamble.replace('\\documentclass', '\\documentclass[solution]')
                    else:
                        preamble = preamble.replace('[', '[solution, ')
                else:
                    # Remove the [solution] option if present
                    preamble = preamble.replace('[solution, ', '[').replace('[solution]', '')

                # Reassemble the documentclass line
                print(f'{preamble}{{{class_name}}}', end='\n')
            else:
                print(line, end='')
    
    # If we didn't modify the documentclass, raise an exception for debugging
    if not docclass_modified:
        raise ValueError("documentclass line with 'exerciseClass' not found or not modified.")

    # Run pdflatex twice for proper compilation
    call(call_pdflatex_l)
    call(call_pdflatex_l)


# go into the parent directory
os.chdir('..')
os.makedirs('built', exist_ok=True)


# build main pdf (without solutions)
os.chdir('exercise')

build_pdf(with_solution=True)
#os.makedirs('../built', exist_ok=True)
os.replace('main.pdf', os.path.join('../built', 'exercise_with_solution.pdf'))
    
    # Build without solutions
build_pdf(with_solution=False)
os.replace('main.pdf', os.path.join('../built', 'exercise.pdf'))

