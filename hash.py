#!/usr/bin/env python3
import hashlib, sys, qrcode, PyPDF2, json
from datetime import date

def count_pages(filename):
    count = 0
    with open(filename,"rb") as file:
       data = PyPDF2.PdfFileReader(file)
       count = data.getNumPages()
    return count

def print_data(dados):
   if isinstance(dados, dict):
      print("Descrição: {}".format(dados['descrição']))
      print("Emissor: {}".format(dados['emissor']))
      print("Arquivo: {}".format(dados['arquivo']))
      print("Numero de páginas: {}".format(dados['nr_paginas']))	
      print("Protocolado em: {}".format(dados['dataProtocolo']))	
      print("Hash: {}".format(dados['hash']))	
   else:
      print("Formato inválido")


def hashfile(file): 
   sha256 = hashlib.sha256()
   BUF_SIZE = 65536  
   try:
      with open(file ,"rb") as infile:
         while True: 
            data = infile.read(BUF_SIZE)
            if not data:
               break
            sha256.update(data)

            return(sha256.hexdigest())
   except:
      print("Arquivo vazio ou inexistente")

if __name__=="__main__":
   try:
      with open("oficios.json") as oficios_store:
         oficios_db = json.load(oficios_store)   
   except FileNotFoundError:
      with open("oficios.json", "w") as oficios_store:
         print("Criando persistência")
         json.dump({"oficios":[]},oficios_store)


   if len(sys.argv)==2:

      descricao = input("Insira a descrição do arquivo: ") 
      emissor = input("Informe o emissor do documento: ")
      filehash = hashfile(sys.argv[1])
      contagem = count_pages(sys.argv[1])
         
      if filehash:
         dados = {
               "descrição": descricao,
               "emissor": emissor,
               "arquivo": sys.argv[1],
               "nr_paginas": contagem, 
               "dataProtocolo": date.today().strftime("%d/%m/%Y"),
               "hash": filehash
               }


         print_data(dados)
         repetido = False
         for o in oficios_db['oficios']:
           if dados['hash'] == o['hash']:
              repetido = True
              break
         if repetido:
            print("Este oficio já foi protocolado anteriormente")
         else: 
            oficios_db['oficios'].append(dados)
            img = qrcode.make(dados)
            img.save("{}.png".format(sys.argv[1]))
            print("QR Code {}.png exportado".format(sys.argv[1]))

         with open("oficios.json", "w") as oficios_store:
            json.dump(oficios_db, oficios_store)
            oficios_store.close()   
   else:
      print("O numero de argumentos deve ser igual a um")
