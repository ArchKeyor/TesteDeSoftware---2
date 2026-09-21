import uuid
from datetime import datetime

class Movimento:
    def __init__(self, responsavel_id: str, categoria_id: str, forma_pagamento_id: str, data: str, descricao: str, tipo_movimento: str, valor: float, id: str = None):
        self.set_responsavel_id(responsavel_id)
        self.set_categoria_id(categoria_id)
        self.set_forma_pagamento_id(forma_pagamento_id)
        self.set_data(data)
        self.set_descricao(descricao)
        self.set_tipo_movimento(tipo_movimento)
        self.set_valor(valor)
        if id is None:
            self.__id = str(uuid.uuid4())
        else:
            self.__id = id

    def get_responsavel_id(self) -> str:
        return self.__responsavel_id

    def set_responsavel_id(self, responsavel_id: str):
        self.__responsavel_id = responsavel_id

    def get_categoria_id(self) -> str:
        return self.__categoria_id

    def set_categoria_id(self, categoria_id: str):
        self.__categoria_id = categoria_id

    def get_forma_pagamento_id(self) -> str:
        return self.__forma_pagamento_id

    def set_forma_pagamento_id(self, forma_pagamento_id: str):
        self.__forma_pagamento_id = forma_pagamento_id

    def get_data(self) -> str:
        return self.__data

    def set_data(self, data: str):
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Data '{data}' inválida. Use o formato DD/MM/AAAA.")
        self.__data = data

    def get_descricao(self) -> str:
        return self.__descricao

    def set_descricao(self, descricao: str):
        self.__descricao = descricao

    def get_tipo_movimento(self) -> str:
        return self.__tipo_movimento

    def set_tipo_movimento(self, tipo_movimento: str):
        self.__tipo_movimento = tipo_movimento

    def get_valor(self) -> float:
        return self.__valor

    def set_valor(self, valor: float):
        self.__valor = float(valor)

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def to_dict(self):
        return {
            'responsavel_id': self.get_responsavel_id(),
            'categoria_id': self.get_categoria_id(),
            'forma_pagamento_id': self.get_forma_pagamento_id(),
            'data': self.get_data(),
            'descricao': self.get_descricao(),
            'tipo_movimento': self.get_tipo_movimento(),
            'valor': self.get_valor(),
            'id': self.get_id()
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            responsavel_id=data['responsavel_id'],
            categoria_id=data.get('categoria_id', data.get('tipo_conta_id')),
            forma_pagamento_id=data.get('forma_pagamento_id', ''),
            data=data.get('data', ''),
            descricao=data.get('descricao', data.get('categoria', '')), # Fallback for old data
            tipo_movimento=data['tipo_movimento'],
            valor=float(data['valor']),
            id=data.get('id')
        )

    @staticmethod
    def get_fields():
        return ['responsavel_id', 'categoria_id', 'forma_pagamento_id', 'data', 'descricao', 'tipo_movimento', 'valor', 'id']
