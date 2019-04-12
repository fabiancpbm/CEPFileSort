import struct
import os
import shutil
import random

# Essa variável será usada para nomear os arquivos e identificar a ordem de criação do grupo de arquivos.
# Assim, não haverá arquivos com o mesmo nome.
groupCreationOrder = 0

# Estrutura do arquivo.
lineStruct = struct.Struct("72s72s72s72s2s8s2s")

# Tamanhos do arquivo.
fileSize = os.path.getsize("unorganized_cep_80.dat")
registerQtd = fileSize // lineStruct.size
registerPerFile = 10
fileQuantity = registerQtd // registerPerFile

cepColumn = 5

# Criando 10 arquivos separados dentro da pasta de buuffet para realizar a intercalação entre eles.
directoryName = "cep_file_buffer/"

if not os.path.exists(directoryName):
    os.mkdir(directoryName)

fin = open("unorganized_cep_80.dat", "rb")
for i in range(0, fileQuantity):
    ceps = []
    for y in range(0, registerPerFile):
        c = fin.read(lineStruct.size)
        ceps.append(lineStruct.unpack(bytes(c)))
    ceps.sort(key=lambda x:x[cepColumn])

    newFileName = directoryName + str(groupCreationOrder) + "_cep_" + str(i) + ".dat"
    newFile = open(newFileName, "wb+")
    for cep in ceps:
        line = lineStruct.pack(cep[0], cep[1], cep[2], cep[3], cep[4], cep[5], cep[6])
        newFile.write(line)
    newFile.close()
fin.close()

# Função intercala
def intercalate(fileA, fileB, newFile):
    contentA = fileA.read(lineStruct.size)
    addressA = lineStruct.unpack(contentA)

    contentB = fileB.read(lineStruct.size)
    addressB = lineStruct.unpack(contentB)

    while len(contentA) != 0 and len(contentB) != 0:
        if addressA[cepColumn] < addressB[cepColumn]:
            newFile.write(contentA)
            contentA = fileA.read(lineStruct.size)
            if len(contentA) == lineStruct.size:
                addressA = lineStruct.unpack(contentA)
        else:
            newFile.write(contentB)
            contentB = fileB.read(lineStruct.size)
            if len(contentB) == lineStruct.size:
                addressB = lineStruct.unpack(contentB)

    while len(contentA) != 0:
        newFile.write(contentA)
        contentA = fileA.read(lineStruct.size)
    while len(contentB) != 0:
        newFile.write(contentB)
        contentB = fileB.read(lineStruct.size)

# Intercalando de dois em dois arquivos até que reste apenas um arquivo ordenado.
newFileName = ""
while fileQuantity > 1:
    randomOrder = random.sample(range(fileQuantity), fileQuantity)
    iterations = fileQuantity
    print("Quantidade de arquivos para intercalar: " + str(fileQuantity))
    fileQuantity = 0
    newGroupCreationOrder = groupCreationOrder + 1
    for i in range(0, iterations, 2):
        # Capturando os arquivos que serão intercalados e criando novo arquivo para armazelar o resultado
        # da intercalação.
        fileNameA = str(groupCreationOrder) + "_cep_" + str(randomOrder[i]) + ".dat"
        fileNameB = str(groupCreationOrder) + "_cep_" + str(randomOrder[i + 1]) + ".dat"
        newFileName = str(newGroupCreationOrder) + "_cep_" + str(fileQuantity) + ".dat"
        print("Intercalando os arquivos: '" + fileNameA + "' e '" + fileNameB + "'.")

        fileA = open(directoryName + fileNameA, "rb")
        fileB = open(directoryName + fileNameB, "rb")
        newFile = open(directoryName + newFileName, "wb+")
        fileQuantity += 1

        intercalate(fileA, fileB, newFile)

        # Fechando e deletando arquivos que já foram intercalados.
        fileA.close()
        fileB.close()
        newFile.close()
        os.remove(directoryName + fileNameA)
        os.remove(directoryName + fileNameB)
    groupCreationOrder = newGroupCreationOrder
os.rename(directoryName + newFileName, "organized_cep_80.dat")
shutil.rmtree(directoryName)