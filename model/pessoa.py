import uuid
from datetime import datetime

class Pessoa:
    def __init__(self, nome: str, data_nascimento: str, funcao_id: str, is_responsavel: bool, id: str = None):
        self.set_nome(nome)
        self.set_data_nascimento(data_nascimento)
        self.set_funcao_id(funcao_id)
        self.set_is_responsavel(is_responsavel)
        if id is None:
            self.__id = str(uuid.uuid4())
        else:
            self.__id = id

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str):
        self.__nome = nome

    def get_data_nascimento(self) -> str:
        return self.__data_nascimento

    def set_data_nascimento(self, data_nascimento: str):
        try:
            datetime.strptime(data_nascimento, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Data de nascimento '{data_nascimento}' inválida. Use o formato DD/MM/AAAA.")
        self.__data_nascimento = data_nascimento

    def get_funcao_id(self) -> str:
        return self.__funcao_id

    def set_funcao_id(self, funcao_id: str):
        self.__funcao_id = funcao_id

    def get_is_responsavel(self) -> bool:
        return self.__is_responsavel

    def set_is_responsavel(self, is_responsavel: bool):
        self.__is_responsavel = is_responsavel

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def to_dict(self):
        return {
            'nome': self.get_nome(),
            'data_nascimento': self.get_data_nascimento(),
            'funcao_id': self.get_funcao_id(),
            'is_responsavel': self.get_is_responsavel(),
            'id': self.get_id()
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nome=data['nome'],
            data_nascimento=data.get('data_nascimento', ''),
            funcao_id=data.get('funcao_id', data.get('funcao', '')), # fallback para migração
            is_responsavel=data['is_responsavel'] == 'True' if isinstance(data['is_responsavel'], str) else data['is_responsavel'],
            id=data.get('id')
        )

    @staticmethod
    def get_fields():
        return ['nome', 'data_nascimento', 'funcao_id', 'is_responsavel', 'id']
