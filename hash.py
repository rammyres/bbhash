#!/usr/bin/env python3
import hashlib, sys, qrcode, PyPDF2, json
from datetime import date
from lib.persistencia import Persistencia
from lib.oficio import Oficio

def count_pages(filename):
    count = 0
    with open(filename,"rb") as file:
       data = PyPDF2.PdfFileReader(file)
       count = data.getNumPages()
       file.close()
    return count

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
   oficios_db = Persistencia("oficios.json")
   print("Script de protocolo de oficios")
   while(True):
      print("Escolha uma opção: ")
      print("1 - Protoclar novo ofício")
      print("2 - Listar ofícios protolados")
      print("9 - Sair")
      e = input("Digite a escolha: ")

      if e == "1":
           while(True):
            descricao = input("Digite a descrição do documento: ")
            emissor = input("Digite o emissor do documento: ")
            arquivo = input("Informe o arquivo PDF do documento digitalizado: ")

            # try:
            Hash = hashfile(arquivo)
            nr_paginas = count_pages(arquivo)
            o = Oficio(
               descricao = descricao,
               emissor = emissor,
               arquivo = arquivo,
               nr_paginas = nr_paginas,
               data_protocolo = date.today().strftime("%d/%m/%Y"),
               Hash = Hash
            )
            o.print_data()
            oficios_db.inserir(o)
            oficios_db.persistir()
            break
            # except:
               #  print("Arquivo no formato invalido ou inexistente")
      elif e == '9':
         break
      else:
         print("Opção inválida")
       