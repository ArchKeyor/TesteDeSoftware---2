from model.forma_pagamento import FormaPagamento
from model.repositorio import RepositorioCSV
from controller.movimento_controller import MovimentoController
import os

class FormaPagamentoController:
    def __init__(self, base_path: str, mov_ctrl: MovimentoController = None):
        self.repo = RepositorioCSV(os.path.join(base_path, 'arquivos', 'formas_pagamento.csv'), FormaPagamento)
        self.mov_ctrl = mov_ctrl

    def set_movimento_controller(self, mov_ctrl: MovimentoController):
        self.mov_ctrl = mov_ctrl

    def adicionar(self, nome: str):
        fp = FormaPagamento(nome=nome)
        self.repo.salvar(fp)

    def listar(self):
        return self.repo.listar_todos()

    def atualizar(self, id: str, nome: str):
        fp = FormaPagamento(nome=nome, id=id)
        self.repo.atualizar(id, fp)

    def remover(self, id: str):
        if self.mov_ctrl and self.mov_ctrl.existe_por_forma_pagamento(id):
            raise Exception("Não é possível remover. Existem movimentos atrelados a esta forma de pagamento.")
        self.repo.remover(id)
