import struct

lineStruct = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5

f = open("cep.dat", "r", encoding='latin-1')
content = f.read(lineStruct.size * 80)
f.close()

newFile = open("unorganized_cep_80.dat", "w+", encoding='latin-1')
newFile.write(content)