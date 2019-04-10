import struct
import os
import random

# Essa variável será usada para nomear os arquivos e identificar a ordem de criação do grupo de arquivos.
# Assim, não haverá arquivos com o mesmo nome.
groupCreationOrder = 0

# Variável que guarda a quantidade de arquivos gerados para a próxima intercalação.
fileQuantity = 8

lineStruct = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5

sizePerFile = lineStruct.size * 10

# Criando 10 arquivos separados dentro da pasta de buuffet para realizar a intercalação entre eles.
directoryName = "cep_file_buffer/"

if not os.path.exists(directoryName):
    os.mkdir(directoryName)

fin = open("unorganized_cep_80.dat", "r", encoding='latin-1')
for i in range(0, 8):
    ceps = []
    for y in range(0, 10):
        c = fin.read(lineStruct.size)
        ceps.append(lineStruct.unpack(bytes(c, encoding="latin-1")))
    ceps.sort(key=lambda x:x[cepColumn])

    newFileName = directoryName + str(groupCreationOrder) + "_cep_" + str(i) + ".dat"
    newFile = open(newFileName, "w+", encoding='latin-1')
    for cep in ceps:
        line = lineStruct.pack(cep[0], cep[1], cep[2], cep[3], cep[4], cep[5], cep[6])
        newFile.write(line.decode('latin-1'))
    newFile.close()
fin.close()

# Função intercala
def intercalate(fileA, fileB, newFile):
    contentA = fileA.read(lineStruct.size)
    addressA = lineStruct.unpack(bytes(contentA, encoding="latin-1"))

    contentB = fileB.read(lineStruct.size)
    addressB = lineStruct.unpack(bytes(contentB, encoding="latin-1"))

    while contentA != "" and contentB != "":
        if addressA[cepColumn] < addressB[cepColumn]:
            newFile.write(contentA)
            contentA = fileA.read(lineStruct.size)
            if contentA != "":
                addressA = lineStruct.unpack(bytes(contentA, encoding="latin-1"))
        else:
            newFile.write(contentB)
            contentB = fileB.read(lineStruct.size)
            if contentB != "":
                addressB = lineStruct.unpack(bytes(contentB, encoding="latin-1"))

    while contentA != "":
        newFile.write(contentA)
        contentA = fileA.read(lineStruct.size)
    while contentB != "":
        newFile.write(contentB)
        contentB = fileB.read(lineStruct.size)

# Intercalando de dois em dois arquivos até que reste apenas um arquivo ordenado.
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

        fileA = open(directoryName + fileNameA, "r", encoding='latin-1')
        fileB = open(directoryName + fileNameB, "r", encoding='latin-1')
        newFile = open(directoryName + newFileName, "w+", encoding='latin-1')
        fileQuantity += 1

        intercalate(fileA, fileB, newFile)

        # Fechando e deletando arquivos que já foram intercalados.
        fileA.close()
        fileB.close()
        newFile.close()
        os.remove(directoryName + fileNameA)
        os.remove(directoryName + fileNameB)
    groupCreationOrder = newGroupCreationOrder