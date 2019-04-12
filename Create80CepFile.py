import struct

lineStruct = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5

f = open("cep.dat", "rb")
content = f.read(lineStruct.size * 80)
f.close()

newFile = open("unorganized_cep_80.dat", "wb+")
newFile.write(content)