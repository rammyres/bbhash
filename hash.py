#!/usr/bin/env python3
import hashlib, PyPDF2, json
from PyPDF2.utils import PdfReadError
from datetime import date
from lib.persistencia import Persistencia
from lib.oficio import Oficio
import textwrap
from PIL import Image, ImageDraw, ImageFont

def count_pages(filename):
   filename = filename.replace(" ", "")
   count = 0
   with open(filename,"rb") as file:
      data = PyPDF2.PdfFileReader(file)
      count = data.getNumPages()
      file.close()
   return count

def hashfile(file):
   file = file.replace(" ", "") 
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


def exportar_protocolo(filehash, qr, data):
   fundo = Image.open("img/base.png")
   qr = Image.open('img/qr.png')
   qr.thumbnail((120, 120))

   fundo.paste(qr, (5, 112))

   im_w = 140
   im_h = 100
   im_y = 5

   im = Image.new(mode="RGB", size=(im_w, im_h), color=(255,255,255,0))
   fonte = ImageFont.truetype("fonts/BancoDoBrasilTextos-Regular.ttf", 14)
   desenho = ImageDraw.Draw(im)

   lines = textwrap.wrap(filehash, width=14)

   y_text = im_y

   for line in lines:
      width, height = fonte.getsize(line)
      desenho.text((2 / 2, y_text), line, font=fonte, fill=(0,0,0,0))
      y_text += height

   fundo.paste(im, (2, 3))

   texto_data = "Recebido em 22 de novembro de 2022"
   fonte_data = ImageFont.truetype("fonts/BancoDoBrasilTextos-Regular.ttf", 18)
   largura, altura = desenho.textsize(texto_data, fonte_data)
   print(largura)
   
   im_data = Image.new(mode="RGB", size=(largura+4, altura), color=(255,255,255,0))
   desenho = ImageDraw.Draw(im_data)  
   
   desenho.text((2, 0), text=texto_data, font=fonte_data, fill=(0, 0, 0, 0))

   fundo.paste(im_data, (140, 130))
   fundo.show()
   # fundo.save("protocolo.png")

if __name__=="__main__":
   oficios_db = Persistencia("oficios.json")

   print("Script de protocolo de oficios")
   while(True):
      print("Escolha uma opção: ")
      print("1 - Protocolar novo ofício")
      
      if len(oficios_db.oficios)>0:
         print("2 - Listar ofícios protolados")
         print("3 - Exportar QR Code de ofícios protocolados")
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
                  exportar_protocolo(o.Hash, 'img/qr.png', o.data_protocolo)
               else:
                  print("Oficio já consta na base de protocolos")
               break
            except PdfReadError:
               print("Arquivo no formato invalido ou inexistente\nPor hora esse script só processa arquivos PDF")
      elif e == '2':
         if len(oficios_db.oficios)>0:
            while(True):
               try:
                  for i in range(len(oficios_db.oficios)):
                     print("{} - {}".format(i+1, oficios_db.oficios[i].descricao))
                  ex = input("Digite o numero para detalhar o ofício ou 'sair' para retornar ao menu anterior: ")
                  if ex.lower() == 'sair':
                     break
                  else: 
                     oficios_db.oficios[int(ex)-1].print_data()
               except ValueError:
                  print("Digite um numero válido ou 'sair'")
               except IndexError:
                  print("Número de oficio inexistente")
         else:
            print("Opção inválida")
      elif e == '3':
         if len(oficios_db.oficios)>0:
            while(True):
               try:
                  for i in range(len(oficios_db.oficios)):
                     print("{} - {}".format(i+1, oficios_db.oficios[i].descricao))
                  ex = input("Digite o numero para exportar o QR Code ou 'sair' para retornar ao menu anterior: ")
                  if ex.lower() == 'sair':
                     break
                  else: 
                     # oficios_db.oficios[int(ex)-1].exportar_qrcode()
                     exportar_protocolo(oficios_db.oficios[int(ex)-1].Hash, 'img/qr.png', oficios_db.oficios[int(ex)-1].data_protocolo)
               except ValueError:
                  print("Digite um numero válido ou 'sair'")
         else:
            print("Opção inválida")

      elif e == '9':
         break
      else:
         print("Opção inválida")
       
