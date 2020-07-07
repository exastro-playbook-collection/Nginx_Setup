import os
import re
import sys

nginxConfPath = sys.argv[1]
confPathList_file = sys.argv[2]
nginxfile = nginxConfPath
file_tmp = confPathList_file + 'confPathList.txt'

def getConfPath(confFile,confFile_tmp):
    if os.path.isfile(confFile):
        fo = open(confFile)
        readlines = fo.readlines()
        for strline in readlines:
            if re.match('\s*#.*', strline) is not None:
                continue
            includePath = None
            if re.match("\s*include\s+'\s*(.*)\s*'\s*;", strline) is not None:
                includeMatch = re.match("\s*include\s+'\s*(.*)\s*'\s*;", strline)
                includePath = includeMatch.group(1).strip()
            elif re.match('\s*include\s+"\s*(.*)\s*"\s*;', strline) is not None:
                includeMatch = re.match('\s*include\s+"\s*(.*)\s*"\s*;', strline)
                includePath = includeMatch.group(1).strip()
            elif re.match('\s*include\s+(.*)\s*;', strline) is not None:
                includeMatch = re.match('\s*include\s+(.*)\s*;', strline)
                includePath = includeMatch.group(1).strip()
            if includePath is not None:
                if includePath.startswith('/') == False:
                    includePath = nginxfile.rpartition('/')[0] + '/' + includePath
                searchFileList = searchFile(includePath)
                search_readlines = searchFileList.readlines()
                for search_read in search_readlines:
                    confFile_tmp.write(search_read.strip() + '\n')
                    getConfPath(search_read.strip(), confFile_tmp)
        fo.close()

def searchFile(path):
    cmd = "find / -regextype 'posix-egrep' -regex " + "'" + path.replace('*','.*') + "'"
    cmdResult = os.popen(cmd)
    return cmdResult

if os.path.isfile(nginxfile):
    fo_tmp = open(file_tmp, 'w+')
    getConfPath(nginxfile, fo_tmp)
    fo_tmp.close()