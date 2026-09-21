from model.pessoa import Pessoa
from model.repositorio import RepositorioCSV
from controller.movimento_controller import MovimentoController
import os

class PessoaController:
    def __init__(self, base_path: str, mov_ctrl: MovimentoController = None):
        self.repo = RepositorioCSV(os.path.join(base_path, 'arquivos', 'pessoas.csv'), Pessoa)
        self.mov_ctrl = mov_ctrl

    def set_movimento_controller(self, mov_ctrl: MovimentoController):
        self.mov_ctrl = mov_ctrl

    def adicionar(self, nome: str, data_nascimento: str, funcao_id: str, is_responsavel: bool):
        p = Pessoa(nome=nome, data_nascimento=data_nascimento, funcao_id=funcao_id, is_responsavel=is_responsavel)
        self.repo.salvar(p)

    def listar(self):
        return self.repo.listar_todos()

    def atualizar(self, id: str, nome: str, data_nascimento: str, funcao_id: str, is_responsavel: bool):
        p = Pessoa(nome=nome, data_nascimento=data_nascimento, funcao_id=funcao_id, is_responsavel=is_responsavel, id=id)
        self.repo.atualizar(id, p)

    def remover(self, id: str):
        if self.mov_ctrl and self.mov_ctrl.existe_por_pessoa(id):
            raise Exception("Não é possível remover. Existem movimentos atrelados a esta pessoa.")
        self.repo.remover(id)

    def existe_por_funcao(self, funcao_id: str) -> bool:
        return any(p.get_funcao_id() == funcao_id for p in self.listar())
