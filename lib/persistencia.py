import json 
from lib.oficio import Oficio
class Persistencia:
    oficios = []
    caminho = None
    def __init__(self, arquivo_persistencia) -> None:
        try:
            self.caminho = arquivo_persistencia
            self.carregar(arquivo_persistencia)

        except FileNotFoundError:
            with open(arquivo_persistencia, "w") as oficios_store:
                print("Criando persistĂȘncia")
                json.dump({"oficios" : []}, oficios_store)

    def verificar_hash(self, hash):
        for o in self.oficios:
            if o.Hash == hash:
                return True
        return False

    def inserir(self, dados):
        if isinstance(dados, Oficio):
            if not self.verificar_hash(dados.Hash):
                self.oficios.append(dados)
                return True
        return False

    def persistir(self):
        oficios_json = []
        print(len(self.oficios))
        print(self.oficios)
        if len(self.oficios)>0:
            for o in self.oficios:
                oficios_json.append(o.to_json())
            with open(self.caminho, "w") as armazenamento:
                json.dump({"oficios" : oficios_json}, armazenamento, indent=4)

    def carregar(self, arquivo):
        with open(arquivo) as armazenamento:
            tmp_oficios = json.load(armazenamento)
            print(len(tmp_oficios["oficios"]))
            if len(tmp_oficios["oficios"])>0:
                for o in tmp_oficios['oficios']:
                    tmp_oficio = Oficio(oficio_json = o)
                    self.inserir(tmp_oficio)