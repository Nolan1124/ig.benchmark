import sys


def generate_rate(fileName,variable,plotFileName):
    fileData = file(fileName,"r")
    line = fileData.readline()
    data = {}
    while len(line):
        result = eval(line)
        data[result[variable]] = result["rate"]
        line = fileData.readline()
    iVar = data.keys()
    iVar.sort()
    plotFile = file(plotFileName,"w")
    for i in iVar:
        print (str(i)+","+str(data[i]))
        print >> plotFile,(str(i)+","+str(data[i]))
    plotFile.flush()
    plotFile.close()
    pass


if __name__ == "__main__":
    generate_rate(sys.argv[1],sys.argv[2],sys.argv[3])


