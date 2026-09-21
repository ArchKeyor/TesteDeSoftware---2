from model.movimento import Movimento
from model.repositorio import RepositorioCSV
import os
from datetime import datetime

class MovimentoController:
    def __init__(self, base_path: str):
        self.repo = RepositorioCSV(os.path.join(base_path, 'arquivos', 'movimentos.csv'), Movimento)

    def adicionar(self, responsavel_id: str, categoria_id: str, forma_pagamento_id: str, data: str, descricao: str, tipo_movimento: str, valor: float):
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        m = Movimento(responsavel_id=responsavel_id, categoria_id=categoria_id, forma_pagamento_id=forma_pagamento_id, data=data, descricao=descricao, tipo_movimento=tipo_movimento, valor=valor)
        self.repo.salvar(m)

    def listar(self):
        return self.repo.listar_todos()

    def atualizar(self, id: str, responsavel_id: str, categoria_id: str, forma_pagamento_id: str, data: str, descricao: str, tipo_movimento: str, valor: float):
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        m = Movimento(responsavel_id=responsavel_id, categoria_id=categoria_id, forma_pagamento_id=forma_pagamento_id, data=data, descricao=descricao, tipo_movimento=tipo_movimento, valor=valor, id=id)
        self.repo.atualizar(id, m)

    def remover(self, id: str):
        self.repo.remover(id)

    def existe_por_pessoa(self, pessoa_id: str) -> bool:
        return any(m.get_responsavel_id() == pessoa_id for m in self.listar())

    def existe_por_categoria(self, categoria_id: str) -> bool:
        return any(m.get_categoria_id() == categoria_id for m in self.listar())

    def existe_por_forma_pagamento(self, fp_id: str) -> bool:
        return any(m.get_forma_pagamento_id() == fp_id for m in self.listar())

    def pesquisar_avancado(self, data_inicio: str = "", data_fim: str = "", forma_pagamento_id: str = None, responsavel_id: str = None, categoria_id: str = None, valid_responsavel_ids: list = None):
        if data_inicio and data_fim:
            inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            fim = datetime.strptime(data_fim, "%d/%m/%Y")
        else:
            inicio = None
            fim = None
            
        movimentos_filtrados = []
        total_entradas = 0.0
        total_saidas = 0.0
        
        for m in self.listar():
            if forma_pagamento_id and m.get_forma_pagamento_id() != forma_pagamento_id:
                continue
            if responsavel_id and m.get_responsavel_id() != responsavel_id:
                continue
            if categoria_id and m.get_categoria_id() != categoria_id:
                continue
            if valid_responsavel_ids is not None and m.get_responsavel_id() not in valid_responsavel_ids:
                continue
                
            if inicio and fim:
                data_mov = datetime.strptime(m.get_data(), "%d/%m/%Y")
                if not (inicio <= data_mov <= fim):
                    continue
                    
            movimentos_filtrados.append(m)
            if m.get_tipo_movimento() == "Entrada":
                total_entradas += m.get_valor()
            elif m.get_tipo_movimento() == "Saída":
                total_saidas += m.get_valor()
                
        saldo = total_entradas - total_saidas
        return movimentos_filtrados, total_entradas, total_saidas, saldo
