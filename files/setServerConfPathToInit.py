import os
import re
import sys

filename = sys.argv[1]
tmpPath = sys.argv[2]
if os.path.isfile(filename):
    lines_tmp = []
    confOpen = open(filename)
    confAlllines = confOpen.readlines()
    for lines in confAlllines:
        lines_tmp.append(lines)
        confOpen.close()
    if len(lines_tmp) > 0:
        for index in range(len(lines_tmp)):
            includeMatch = re.match("\s*include\s+'\s*(.*)\s*'\s*;", lines_tmp[index])
            if includeMatch is not None:
                includePath = includeMatch.group(1).strip()
                if includePath.startswith('/') == True:
                    lines_tmp[index] = '  include   ' + "'" + lines_tmp[index].split(tmpPath, 1)[1]
            elif re.match('\s*include\s+"\s*(.*)\s*"\s*;', lines_tmp[index]) is not None:
                includeMatch = re.match('\s*include\s+"\s*(.*)\s*"\s*;', lines_tmp[index])
                includePath = includeMatch.group(1).strip()
                if includePath.startswith('/') == True:
                    lines_tmp[index] = '  include   ' + '"' + lines_tmp[index].split(tmpPath, 1)[1]
            elif re.match('\s*include\s+(.*)\s*;', lines_tmp[index]) is not None:
                includeMatch = re.match('\s*include\s+(.*)\s*;', lines_tmp[index])
                includePath = includeMatch.group(1).strip()
                if includePath.startswith('/') == True:
                    lines_tmp[index] = '  include   ' + lines_tmp[index].split(tmpPath, 1)[1]
    write_str = ''.join(lines_tmp)
    fp = open(filename, 'w+')
    fp.write(write_str)
    fp.close()
