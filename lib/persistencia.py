import json 
from lib import oficio
class persistencia:
    oficios = [oficio]
    caminho = None
    def __init__(self, arquivo_persistencia) -> None:
        try:
            self.caminho = arquivo_persistencia
            self.carregar()

        except FileNotFoundError:
            with open(arquivo_persistencia, "w") as oficios_store:
                print("Criando persistência")
                self.persistir()

    def inserir(self, dados) -> bool:
        if isinstance(dados, oficio):
            self.oficios.append(dados)
            return True
        return False

    def persistir(self):
        oficios_json = []
        if len(self.oficios)>0:
            for o in self.oficios:
                oficios_json.append(o.to_json())
            with open(self.caminho) as armazenamento:
                json.dump({"oficios" : oficios_json}, armazenamento)
        else:
            with open(self.caminho) as armazenamento:
                json.dump({"oficios" : []}, armazenamento)

    def carregar(self, arquivo):
        with open(arquivo) as armazenamento:
            tmp_oficios = json.load(armazenamento)
            if len(tmp_oficios["oficios"])>0:
                for o in tmp_oficios['oficios']:
                    tmp_oficio = oficio(oficion_json = o)
                    self.oficios.inserir(o)