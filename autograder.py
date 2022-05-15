import os

#os.getcwd()
#os.listdir() returns the contents of cwd if no argument is given
#os.mkdir()

#A function which filters a set of characters from a given string
def filter_characters_from_string(string,exemptChars):
    newString = ''
    for char in string:
        if char not in exemptChars:
            newString = newString + char
    return newString


#A function that filters characters from a set of strings
def filter_characters_from_strings(strings,exemptChars,exemptStrings = [],flag = False):
    newStrings = []
    for string in strings:
        if string not in exemptStrings:
            newString = filter_characters_from_string(string,exemptChars)
            if newString:
                newStrings.append(newString)
            elif flag == True:
                newStrings.append(False)
            #else throw an error...?
    return newStrings


def rename_file(fileName, newFileName, path = os.getcwd()):
    try:
        os.replace(path+fileName,path+newFileName)
        return True
    except:
        return False


def rename_files(files, exemptChars, exemptFiles = [], path = os.getcwd()):
    # !!! Consider order of parameters!

    newFileNames = filter_characters_from_strings(files,exemptChars,exemptFiles,True)
    #assuming len(newFileNames) == len(files)
    index = 0
    length = len(newFileNames)
    while index < length:
        if newFileNames[index]:
            success = rename_file(files[index],newFileNames[index],path)
            #error handling for success
            #probably a write to a log
        index = index + 1
    return newFileNames

def copy_file(fileName,origin,destination):
    fileContents = open(origin+fileName,'r')
    fileData = fileContents.read()
    fileContents.close()
    newFileContents = open(destination+fileName,'w')
    newFileContents.write(fileData)
    newFileContents.close()
    return True

def insert_try_import(name,source):
    tabSpace = '    '
    string = 'try:\n'
    string = string + tabSpace + 'from '+source+' import '+name+'\n'
    string = string + 'except:\n'
    string = string + tabSpace + 'print("Error in loading '+name+'")'+'\n'
    return string


def grade_submissions(testFunctions, path = os.getcwd(), testsFile = 'tests.py', outputLog = 'output.txt', shellScripts = 'files.sh', exemptChars = [], exemptFiles = []):
    # !!! Make file renaming an option! Implicit by default empty lists for exemptions

    files = os.listdir(path)

    # --- Rename files in directory --- #
    if exemptChars:
        # !!! Make sure path is properly propagated!
        newFiles = rename_files(files, exemptChars, exemptFiles, path)
        files = newFiles
    # --- Otherwise make sure factor exemptFiles --- #
    elif exemptFiles:
        for file in exemptFiles:
            files.remove(file)

    # --- Sort impending file read for the sake of output --- #
    files.sort()

    # --- Prime test files --- #
    f = open(testsFile,'r')
    testData = f.read()
    f.close()

    tabSpace = '    '
    shellScriptString = ''

    try:
        os.mkdir('feedback')
    except:
        print('feedback folder already created!')

    '''try:
        os.mkdir('tests')
    except:
        print('tests folder already created!')'''

    for file in files:
        nameVar = file.split('.')[0]
        if file != shellScripts and file != outputLog and file != testsFile:
            newData = 'name = "'+nameVar+'"\n'
            for function in testFunctions:
                newData = newData + insert_try_import(function,nameVar)
            newData = newData + '\nprint("'+file+'")\n'
            newData = newData + testData
            newData = newData + '\nprint("---------------")\n'
            newFile = open('test.'+file,'w')
            newFile.write(newData)
            newFile.close()

            shellScriptString = shellScriptString + 'python3 test.'+file+' > feedback/'+nameVar+outputLog+'\n'
            shellScriptString = shellScriptString + 'cat feedback/'+nameVar+outputLog+' >> '+outputLog+'\n'
            shellScriptString = shellScriptString + 'rm test.'+file+'\n'
            print(file)


    f = open(shellScripts,'w')
    f.write(shellScriptString)
    f.close()

    return True

#def grade_submissions(testFunctions, path = os.getcwd(), testsFile = 'tests.py', outputLog = 'output.txt', shellScripts = 'files.sh', exemptChars = [], exemptFiles = []):

grade_submissions(['manageWindows','newWeek'],os.getcwd(),'tests.py','output.txt','files.sh',['-',' ','(',')'],['tests.py','autograder.py','files.sh','output.txt','__pycache__','.git','tests','feedback'])


