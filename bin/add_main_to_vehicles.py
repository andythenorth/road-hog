import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import codecs

filenames = []
for filename in os.listdir(os.path.join('src','vehicles')):
    if '__' not in filename and '.DS_Store' not in filename:
        filenames.append(filename)

def insert_main(filename):
    content = codecs.open(os.path.join('src','vehicles',filename),'r', encoding='utf-8').read()
    if not 'consist =' in content:
        print(filename, 'is not a vehicle, skipping')
        return
    else:
        lines = codecs.open(os.path.join('src','vehicles',filename),'r', encoding='utf-8').readlines()
        modified_lines = []
        for index, line in enumerate(lines):
            if "consist =" in line:
                base_line_num_for_reformat = index
                break
        for index, line in enumerate(lines):
            if index <=base_line_num_for_reformat:
                modified_lines.append(line)
            if index > base_line_num_for_reformat:
                line = '    ' + line
                modified_lines.append(line)
        modified_lines.insert(base_line_num_for_reformat, '\n')
        modified_lines.insert(base_line_num_for_reformat + 1, 'def main(roster):\n    ')
        modified_lines.insert(base_line_num_for_reformat + 3, '        roster=roster,\n')
        modified_lines.append('\n    return consist')
        file = open(os.path.join('src','vehicles',filename),'w')
        file.write(''.join(modified_lines))
        file.close

for filename in filenames:
    insert_main(filename)
