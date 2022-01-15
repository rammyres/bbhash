class Oficio:
    descricao = ''
    emissor = ''
    arquivo = ''
    nr_paginas = 0
    data_protocolo = ''
    Hash = ''

    def __init__(self, oficio_json = None, 
                        descricao = None, 
                        emissor = None ,
                        arquivo = None ,
                        nr_paginas = None ,
                        data_protocolo = None ,
                        Hash = None ) -> None:
        if oficio_json:
            self.descricao = oficio_json["descricao"]
            self.emissor = oficio_json["emissor"]
            self.arquivo = oficio_json["arquivo"]
            self.nr_paginas = oficio_json["nr_paginas"]
            self.data_protocolo = oficio_json["data_protocolo"]
            self.Hash = oficio_json["hash"]
        else:
            self.descricao = descricao
            self.emissor = emissor
            self.arquivo = arquivo
            self.nr_paginas = nr_paginas
            self.data_protocolo = data_protocolo
            self.Hash = Hash

    def to_json(self):
        return(
            {
                "descricao": self.descricao,
                "emissor": self.emissor,
                "arquivo": self.arquivo,
                "nr_paginas": self.nr_paginas, 
                "data_protocolo": self.data_protocolo,
                "hash": self.Hash

            }
        )

    def print_data(self):
        print("Descrição: {}".format(self.descricao))
        print("Emissor: {}".format(self.emissor))
        print("Arquivo: {}".format(self.arquivo))
        print("Numero de páginas: {}".format(self.nr_paginas))	
        print("Protocolado em: {}".format(self.data_protocolo))	
        print("Hash: {}".format(self.Hash))
