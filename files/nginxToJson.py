import json
import os
import re
import sys

allConfPath = sys.argv[1]
nginxfile = allConfPath + '/nginx.json'
dir = allConfPath
# get config block
def getConfigInfo(jsonData, configList):
    if 'config' in jsonData:
        configList = jsonData['config']
    return configList

# get http block
def getHttpInfo(configList, httpINJson, filename):
    httpInfo = None
    config_index = None
    parsed_index = None
    configIndex = 0
    for configIndex in range(len(configList)):
        if configIndex == len(configList):
            break
        config = configList[configIndex]
        isBreak = False
        if 'file' in config:
            filename = '.*/' + filename
            if re.match(filename, config['file']) is not None:
                isBreak = True
        if isBreak == True:
            if 'parsed' in config:
                parsedList = config['parsed']
                parsedIndex = 0
                for parsedIndex in range(len(parsedList)):
                    if parsedIndex == len(parsedList):
                        break
                    parsed = parsedList[parsedIndex]
                    if 'directive' in parsed:
                        if parsed['directive'] == 'http':
                            parsed_index = parsedIndex
                            httpInfo = parsed
            config_index = configIndex
            break
    httpINJson['httpInfo'] = httpInfo
    httpINJson['config_index'] = config_index
    httpINJson['parsed_index'] = parsed_index
    return httpINJson

# get all conf files in dir
def file_name(file_dir):
    filesList = []
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                if 'nginx.json' not in os.path.join(root, file):
                    filesList.append(os.path.join(root, file))
    return filesList

# get nginx.conf server info nginxServerList
def getNginxConfServerInfo(nginxHttpInfoBlock, nginxServerList):
    for index in range(len(nginxHttpInfoBlock)):
        if index == len(nginxHttpInfoBlock):
            break
        # get sub conf file
        if 'server' in nginxHttpInfoBlock[index]['directive']:
            serverMap = {}
            serverMap['serverInNginxconfIndex'] = index
            serverMap['serverBlock'] = nginxHttpInfoBlock[index]
            nginxServerList.append(serverMap)
    return nginxServerList

def getIncludeInServerLocation(serverBlock, includeList):
    if len(serverBlock) > 0:
        for server_block in serverBlock:
            if 'location' in server_block['directive']:
                locationBlock = server_block['block']
                for location_block in locationBlock:
                    if 'include' in location_block['directive']:
                        if len(location_block['includes']) > 0:
                            includeList.append(location_block['includes'])

def getIncludeInParsed(parsed, includeList):
    if len(parsed) > 0:
        for parsed_index in parsed:
            if 'include' in parsed_index['directive']:
                if len(parsed_index['includes']) > 0:
                    includeList.append(parsed_index['includes'])
            if 'server' in parsed_index['directive']:
                getIncludeInServerLocation(parsed_index['block'], includeList)

# get sub conf serverInfo subServerList
def getSubConfServerInfo(none,subServerList):
    nginxConfigList = []
    nginxConfigList = getConfigInfo(nginxJsonData, nginxConfigList)
    if len(nginxConfigList) > 1:
        index = 1
        for index in range(len(nginxConfigList)):
            if 'parsed' in nginxConfigList[index]:
                parsedList = nginxConfigList[index]['parsed']
                for parsedIndex in range(len(parsedList)):
                    if parsedIndex == len(parsedList):
                        break
                    if 'server' == parsedList[parsedIndex]['directive']:
                        subServerMap = {}
                        subServerMap['file'] = nginxConfigList[index]['file']
                        subServerMap['serverBlock'] = parsedList[parsedIndex]['block']
                        subServerMap['serverInParsed'] = parsedIndex
                        subServerMap['includeIndex'] = index
                        subServerList.append(subServerMap)
    return subServerList
# change args
def changeServerBlock(beforeServerBlockList,afterServerBlockList):
    #for afterServerBlock in afterServerBlockList:
    afterServerBlockIndex = 0
    afterServerBlockListLength = len(afterServerBlockList)
    while afterServerBlockIndex < afterServerBlockListLength:
        afterServerBlockIndex_isChange = False
        afterDirective = afterServerBlockList[afterServerBlockIndex]['directive']
        if 'location' != afterDirective:
            isAdd = True
            for beforeServerBlockIndex in range(len(beforeServerBlockList)):
                if beforeServerBlockIndex == len(beforeServerBlockList):
                    break
                beforeDirective = beforeServerBlockList[beforeServerBlockIndex]['directive']
                if afterDirective == beforeDirective:
                    beforeServerBlockList[beforeServerBlockIndex]['args'] = afterServerBlockList[afterServerBlockIndex]['args']
                    isAdd = False
                    break
            if isAdd == True:
                beforeServerBlockList.append(afterServerBlockList[afterServerBlockIndex])
        if 'location' == afterDirective:
            addLocation = True
            afterLocationNameList = afterServerBlockList[afterServerBlockIndex]['args']
            afterLocationName = ''
            for args in afterLocationNameList:
                afterLocationName = afterLocationName + ',' + args
            beforeServerBlockIndex = 0
            beforeServerBlockListLength = len(beforeServerBlockList)
            while beforeServerBlockIndex < beforeServerBlockListLength:
                beforeServerBlockIndex_isChange = False
                if 'directive' in beforeServerBlockList[beforeServerBlockIndex]:
                    beforeDirective = beforeServerBlockList[beforeServerBlockIndex]['directive']
                    if afterDirective == beforeDirective:
                        beforeLocationNameList = beforeServerBlockList[beforeServerBlockIndex]['args']
                        beforeLocationName = ''
                        for args in beforeLocationNameList:
                            beforeLocationName = beforeLocationName + ',' + args
                        if beforeLocationName == afterLocationName:
                            addLocation = False
                            afterServerBlockBlockIndex = 0
                            afterServerBlockList_block_Length = len(afterServerBlockList[afterServerBlockIndex]['block'])
                            while afterServerBlockBlockIndex < afterServerBlockList_block_Length:
                                afterServerBlockBlockIndex_isChange = False
                                if 'isDelete' == afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]['directive']:
                                    if afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]['args'][0].lower() == 'true':
                                        del beforeServerBlockList[beforeServerBlockIndex]
                                        beforeServerBlockIndex_isChange = True
                                        break
                                    else:
                                        del afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]
                                        afterServerBlockBlockIndex_isChange = True
                                        beforeServerBlockList[beforeServerBlockIndex] = afterServerBlockList[afterServerBlockIndex]
                                        break
                                if beforeServerBlockIndex_isChange == False:
                                    afterServerBlockBlockIndex = afterServerBlockBlockIndex + 1
                                afterServerBlockList_block_Length = len(afterServerBlockList[afterServerBlockIndex]['block'])
                if beforeServerBlockIndex_isChange == False:
                    beforeServerBlockIndex = beforeServerBlockIndex + 1
                beforeServerBlockListLength = len(beforeServerBlockList)
            if addLocation == True:
                afterServerBlockBlockIndex = 0
                afterServerBlockList_blockblock_Length = len(afterServerBlockList[afterServerBlockIndex]['block'])
                while afterServerBlockBlockIndex < afterServerBlockList_blockblock_Length:
                    afterServerBlockBlockIndex_isChange = False
                    if 'isDelete' == afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]['directive']:
                        if afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]['args'][0].lower() == 'true':
                            del afterServerBlockList[afterServerBlockIndex]
                            afterServerBlockIndex_isChange = True
                            break
                        if afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]['args'][0].lower() == 'false':
                            del afterServerBlockList[afterServerBlockIndex]['block'][afterServerBlockBlockIndex]
                            afterServerBlockBlockIndex_isChange = True
                            beforeServerBlockList.append(afterServerBlockList[afterServerBlockIndex])
                            break
                    if afterServerBlockBlockIndex_isChange == False:
                        afterServerBlockBlockIndex = afterServerBlockBlockIndex + 1
                    afterServerBlockList_blockblock_Length = len(afterServerBlockList[afterServerBlockIndex]['block'])
        if afterServerBlockIndex_isChange == False:
            afterServerBlockIndex = afterServerBlockIndex + 1
        afterServerBlockListLength = len(afterServerBlockList)
    return beforeServerBlockList
nginxJsonData = None
nginxConfigList = []
nginxHttpINJson = {}
if os.path.isfile(nginxfile):
    fo = open(nginxfile)
    alllines = fo.read()
    nginxJsonData = json.loads(alllines)
    #print json.dumps(nginxJsonData)
    nginxConfigList = getConfigInfo(nginxJsonData, nginxConfigList)
    nginxHttpINJson = getHttpInfo(nginxConfigList, nginxHttpINJson, 'nginx.conf')
    fo.close()
# get param file server
filesList = []
filesList = file_name(dir)
deleteServerList = []
addServerList = []
if len(filesList) > 0:
    for file in filesList:
        fo = open(file)
        alllines = fo.read()
        paramJsonData = json.loads(alllines)
        paramHttpInJson = getHttpInfo(getConfigInfo(paramJsonData, []), {}, '*.conf' )
        paramHttpInfo = paramHttpInJson['httpInfo']
        if paramHttpInfo is not None and 'block' in paramHttpInfo:
            blockList = paramHttpInfo['block']
            for block in blockList:
                if 'server' in block['directive']:
                    isDelete = False
                    if 'block' in block:
                        serverParamList = block['block']
                     #   for blockblock in serverParamList:
                        for blockblockIndex in range(len(serverParamList)):
                            if blockblockIndex == len(serverParamList):
                                break
                            if serverParamList[blockblockIndex]['directive'] == 'isDelete':
                                if serverParamList[blockblockIndex]['args'][0].lower() == 'true':
                                    isDelete = True
                                    del serverParamList[blockblockIndex]
                                if serverParamList[blockblockIndex]['args'][0].lower() == 'false':
                                    addServerList.append(block)

                                    del serverParamList[blockblockIndex]
                                    break
                            if serverParamList[blockblockIndex]['directive'] == 'server_name':
                                if isDelete == True:
                                    deleteServerName = {}
                                    deleteServerName['server_name'] = serverParamList[blockblockIndex]['args']
                                    deleteServerList.append(deleteServerName)
                                    break
        fo.close()
# delete server from nginx.conf and sub conf file
nginxHttpInfoBlock = nginxHttpINJson['httpInfo']['block']
nginxServerList = getNginxConfServerInfo(nginxHttpInfoBlock, [])
subServerList = getSubConfServerInfo(nginxHttpInfoBlock, [])
if len(deleteServerList) > 0:
    for deleteServer in deleteServerList:
        nginxServerList = getNginxConfServerInfo(nginxHttpInfoBlock, [])
        subServerList = getSubConfServerInfo(nginxHttpInfoBlock, [])
        for server_name in deleteServer['server_name']:
            for nginxServer in nginxServerList:
                blockblock = nginxServer['serverBlock']['block']
                for block in blockblock:
                    if 'server_name' == block['directive']:
                        serverNameList = block['args']
                        if server_name in serverNameList:
                            nginxHttpInfoBlock.pop(nginxServer['serverInNginxconfIndex'])
                            nginxHttpINJson['httpInfo']['block'] = nginxHttpInfoBlock
                            break
            for subServer in subServerList:
                blockblock = subServer['serverBlock']
                for block in blockblock:
                    if 'server_name' == block['directive']:
                        serverNameList = block['args']
                        if server_name in serverNameList:
                            nginxConfigList[subServer['includeIndex']]['parsed'].pop(subServer['serverInParsed'])
                            nginxJsonData['config'] = nginxConfigList
                            break
# change or add server from nginx.conf and sub conf file
subServerList = getSubConfServerInfo(nginxHttpInfoBlock, [])
if len(addServerList) > 0:
    for addServer in addServerList:
        isChange = False
        filePath = None
        blockIndex = 0
        addServer_block_length = len(addServer['block'])
        while blockIndex < addServer_block_length:
            blockIndex_isChange = False
            if 'serverFilePath' == addServer['block'][blockIndex]['directive']:
                filePath = addServer['block'][blockIndex]['args'][0]
                del addServer['block'][blockIndex]
                blockIndex_isChange = True
            if 'server_name' == addServer['block'][blockIndex]['directive']:
                argsList = addServer['block'][blockIndex]['args']
                for HttpblockIndex in range(len(nginxHttpInfoBlock)):
                    if HttpblockIndex == len(nginxHttpInfoBlock):
                        break
                    if 'server' == nginxHttpInfoBlock[HttpblockIndex]['directive']:
                        blockblocklist = nginxHttpInfoBlock[HttpblockIndex]['block']
                        for blockblockIndex in range(len(blockblocklist)):
                            if blockblockIndex == len(blockblocklist):
                                break
                            if 'server_name' == blockblocklist[blockblockIndex]['directive']:
                                nginxHttpagrsList = blockblocklist[blockblockIndex]['args']
                                for args in argsList:
                                    if args in nginxHttpagrsList:
                                        isChange = True
                                        nginxHttpInfoBlock[HttpblockIndex]['block'] = changeServerBlock(nginxHttpInfoBlock[HttpblockIndex]['block'], addServer['block'])
                                        break
                #for subServer in subServerList:
                for serverBlockIndex in range(len(subServerList)):
                    if 'serverBlock' in subServerList[serverBlockIndex]:
                        subServerList_serverBlock = subServerList[serverBlockIndex]['serverBlock']
                        for subServerList_serverBlockIndex in range(len(subServerList_serverBlock)):
                            if subServerList_serverBlockIndex == len(subServerList_serverBlock):
                                break
                            if ('directive' in subServerList_serverBlock[subServerList_serverBlockIndex]) and ('server_name' == subServerList_serverBlock[subServerList_serverBlockIndex]['directive']):
                                serverNameList = subServerList_serverBlock[subServerList_serverBlockIndex]['args']
                                for args in argsList:
                                    if args in serverNameList:
                                        isChange = True
                                        serverInParsed = subServerList[serverBlockIndex]['serverInParsed']
                                        configIndex = subServerList[serverBlockIndex]['includeIndex']
                                        subServerList[serverBlockIndex]['serverBlock'] = changeServerBlock(subServerList[serverBlockIndex]['serverBlock'], addServer['block'])
                                        nginxConfigList[configIndex]['parsed'][serverInParsed]['block'] = subServerList[serverBlockIndex]['serverBlock']
                                        break
            if blockIndex_isChange == False:
                blockIndex = blockIndex + 1
            addServer_block_length = len(addServer['block'])
        if isChange == False:
            blockIndex_blockIndex = 0
            addServer_block_addServerblock_length = len(addServer['block'])
            while blockIndex_blockIndex < addServer_block_addServerblock_length:
                blockIndex_isChange = False
                if 'location' == addServer['block'][blockIndex_blockIndex]['directive']:
                    locationBlockIndex = 0
                    addServer_blockblock_length = len(addServer['block'][blockIndex_blockIndex]['block'])
                    while locationBlockIndex < addServer_blockblock_length:
                        locationBlockIndex_isChange = False
                        if 'isDelete' == addServer['block'][blockIndex_blockIndex]['block'][locationBlockIndex]['directive']:
                            if addServer['block'][blockIndex_blockIndex]['block'][locationBlockIndex]['args'][0].lower() == 'true':
                                del addServer['block'][blockIndex_blockIndex]
                                blockIndex_isChange = True
                                break
                            del addServer['block'][blockIndex_blockIndex]['block'][locationBlockIndex]
                            locationBlockIndex_isChange = True
                            break
                        if locationBlockIndex_isChange == False:
                            locationBlockIndex = locationBlockIndex + 1
                        addServer_blockblock_length = len(addServer['block'][blockIndex_blockIndex]['block'])
                if blockIndex_isChange == False:
                    blockIndex_blockIndex = blockIndex_blockIndex + 1
                addServer_block_addServerblock_length = len(addServer['block'])
            addConfigServer = {}
            addConfigServer['status'] = 'ok'
            addConfigServer['errors'] = []
            addConfigServer['file'] = filePath
            addConfigServer['parsed'] = []
            parsedMap = {}
            parsedMap['line'] = 1
            parsedMap['args'] = []
            parsedMap['directive'] = 'server'
            parsedMap['block'] = addServer['block']
            addConfigServer['parsed'].append(parsedMap)
            nginxConfigList.append(addConfigServer)
            addInclude = {}
            addInclude['args'] = [filePath]
            addInclude['directive'] = 'include'
            addInclude['includes'] = [len(nginxConfigList)-1]
            nginxHttpInfoBlock.append(addInclude)
            '''
            addInclude = len(nginxConfigList) - 1
            for nginxHttpInfoBlockIndex in range(len(nginxHttpInfoBlock)):
                if nginxHttpInfoBlockIndex == len(nginxHttpInfoBlock):
                    break
                if nginxHttpInfoBlock[nginxHttpInfoBlockIndex]['directive'] == 'include':
                    nginxHttpInfoBlock[nginxHttpInfoBlockIndex]['args'].append(filePath)
                    nginxHttpInfoBlock[nginxHttpInfoBlockIndex]['includes'].append(addInclude)
                    break
           '''
nginxHttpINJson['httpInfo']['block'] = nginxHttpInfoBlock
parsed_index = nginxHttpINJson['parsed_index']
config_index = nginxHttpINJson['config_index']
nginxConfigList[config_index]['parsed'][parsed_index] = nginxHttpINJson['httpInfo']
nginxJsonData['config'] = nginxConfigList
file_tmp = allConfPath + '/nginx_tmp.json'
fo = open(file_tmp, 'w+')
fo.write(json.dumps(nginxJsonData))
#json.dump(nginxJsonData, fo)
fo.close()
