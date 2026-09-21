from model.categoria import Categoria
from model.repositorio import RepositorioCSV
from controller.movimento_controller import MovimentoController
import os

class CategoriaController:
    def __init__(self, base_path: str, mov_ctrl: MovimentoController = None):
        self.repo = RepositorioCSV(os.path.join(base_path, 'arquivos', 'categorias.csv'), Categoria)
        self.mov_ctrl = mov_ctrl

    def set_movimento_controller(self, mov_ctrl: MovimentoController):
        self.mov_ctrl = mov_ctrl

    def adicionar(self, nome: str):
        t = Categoria(nome=nome)
        self.repo.salvar(t)

    def listar(self):
        return self.repo.listar_todos()

    def atualizar(self, id: str, nome: str):
        t = Categoria(nome=nome, id=id)
        self.repo.atualizar(id, t)

    def remover(self, id: str):
        if self.mov_ctrl and self.mov_ctrl.existe_por_categoria(id):
            raise Exception("Não é possível remover. Existem movimentos atrelados a esta categoria.")
        self.repo.remover(id)
