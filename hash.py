#!/usr/bin/env python3
import hashlib, PyPDF2, json
from PyPDF2.utils import PdfReadError
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
      print("1 - Protocolar novo ofício")
      
      if len(oficios_db.oficios)>0:
         print("2 - Listar ofícios protolados")
         print("3 - Exportar QR Code de ofícios protolados")
      print("9 - Sair")
      e = input("Digite a escolha: ")

      if e == "1":
           while(True):
            descricao = input("Digite a descrição do documento: ")
            emissor = input("Digite o emissor do documento: ")
            arquivo = input("Informe o arquivo PDF do documento digitalizado: ")

            try:
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
               if oficios_db.inserir(o):
                  oficios_db.persistir()
                  print("Base de oficios atualizada")
                  o.exportar_qrcode()
               else:
                  print("Oficio já consta na base de protocolos")
               break
            except PdfReadError:
               print("Arquivo no formato invalido ou inexistente\nPor hora esse script só processa arquivos PDF")
      elif e == '2':
         while(True):
            try:
               for i in range(len(oficios_db.oficios)):
                  print("{} - {}".format(i+1, oficios_db.oficios[i].descricao))
               ex = input("Digite o numero para detalhar o ofício ou 'sair' para retornar ao menu anterior: ")
               if ex == 'sair':
                  break
               else: 
                  oficios_db.oficios[int(ex)-1].print_data()
            except ValueError:
               print("Digite um numero válido ou 'sair'")
            except IndexError:
               print("Número de oficio inexistente")
      elif e == '3':
         while(True):
            try:
               for i in range(len(oficios_db.oficios)):
                  print("{} - {}".format(i+1, oficios_db.oficios[i].descricao))
               ex = input("Digite o numero para exportar o QR Code ou 'sair' para retornar ao menu anterior: ")
               if ex == 'sair':
                  break
               else: 
                  oficios_db.oficios[int(ex)-1].exportar_qrcode()
            except ValueError:
               print("Digite um numero válido ou 'sair'")


      elif e == '9':
         break
      else:
         print("Opção inválida")
       
