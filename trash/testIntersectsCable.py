from modeles.entites_systeme_minlight import Cable,Vec3

cable1 = Cable(Vec3(5000,0,0),"a",Vec3(4500,4500,4500),1)
cable2 = Cable(Vec3(0,0,0),"b",Vec3(3500,4500,4500),1)

if(cable1.intersects_cable(cable2)):
  print("deu ruim, teve intersecao")
else:
  print("deu bom, nao se cruzaram")
