import json 
from lib import oficio as Oficio
class pesistencia:
    oficios = []
    caminho = None
    def __init__(self, arquivo_persistencia) -> None:
        try:
            with open(arquivo_persistencia) as armazenamento:
                self.caminho = arquivo_persistencia
                self.oficios = json.load(armazenamento)   
                
        except FileNotFoundError:
            with open(arquivo_persistencia, "w") as oficios_store:
                print("Criando persistência")
                self.oficios({"oficios":[]})
                self.persistir()

    def inserir(self, oficio) -> bool:
        if isinstance(oficio, Oficio):
            self.oficios.append(oficio)
            return True
        return False

    def persistir(self):
        if self.oficios:
            with open(self.caminho) as armazenamento:
                json.dump(self.oficios, armazenamento)
