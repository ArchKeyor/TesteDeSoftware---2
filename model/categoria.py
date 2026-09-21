import uuid

class Categoria:
    def __init__(self, nome: str, id: str = None):
        self.set_nome(nome)
        if id is None:
            self.__id = str(uuid.uuid4())
        else:
            self.__id = id

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str):
        self.__nome = nome

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def to_dict(self):
        return {
            'nome': self.get_nome(),
            'id': self.get_id()
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nome=data['nome'],
            id=data.get('id')
        )

    @staticmethod
    def get_fields():
        return ['nome', 'id']
