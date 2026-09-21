from model.funcao_familiar import FuncaoFamiliar
from model.repositorio import RepositorioCSV
from controller.pessoa_controller import PessoaController
import os

class FuncaoFamiliarController:
    def __init__(self, base_path: str, pes_ctrl: PessoaController = None):
        self.repo = RepositorioCSV(os.path.join(base_path, 'arquivos', 'funcoes_familiares.csv'), FuncaoFamiliar)
        self.pes_ctrl = pes_ctrl

    def set_pessoa_controller(self, pes_ctrl: PessoaController):
        self.pes_ctrl = pes_ctrl

    def adicionar(self, nome: str) -> FuncaoFamiliar:
        ff = FuncaoFamiliar(nome=nome)
        self.repo.salvar(ff)
        return ff

    def listar(self):
        return self.repo.listar_todos()

    def atualizar(self, id: str, nome: str):
        ff = FuncaoFamiliar(nome=nome, id=id)
        self.repo.atualizar(id, ff)

    def remover(self, id: str):
        if self.pes_ctrl and self.pes_ctrl.existe_por_funcao(id):
            raise Exception("Não é possível remover. Existem pessoas atreladas a esta função.")
        self.repo.remover(id)
