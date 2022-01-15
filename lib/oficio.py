class oficio:
    descricao = ''
    emissor = ''
    arquivo = ''
    nr_paginas = 0
    data_protocolo = ''
    Hash = ''

    def __init__(self, descricao, emissor, arquivo, nr_paginas, data_protocolo, Hash) -> None:
        self.descricao = descricao
        self.emissor = emissor
        self.arquivo = arquivo
        self.nr_paginas = nr_paginas
        self.data_protocolo = data_protocolo
        self.Hash = Hash

    def to_json(self):
        return(
            {
                "descrição": self.descricao,
                "emissor": self.emissor,
                "arquivo": self.arquivo,
                "nr_paginas": self.nr_pagins, 
                "dataProtocolo": self.data_protocolo,
                "hash": self.Hash

            }
        )


