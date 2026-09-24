import os
import shutil
import tempfile

import pytest

from controller.forma_pagamento_controller import FormaPagamentoController
from controller.movimento_controller import MovimentoController
from model.forma_pagamento import FormaPagamento


def test_criacao_basica():
    forma_pagamento = FormaPagamento(nome="Cartão de Crédito")
    assert forma_pagamento.get_nome() == "Cartão de Crédito"
    assert forma_pagamento.get_id() is not None


def test_getters_e_setters():
    forma_pagamento = FormaPagamento(nome="Cartão de Crédito")
    forma_pagamento.set_nome("Pix")
    assert forma_pagamento.get_nome() == "Pix"


def test_conversao_dict():
    forma_pagamento = FormaPagamento(nome="Pix", id="12345")
    dados = forma_pagamento.to_dict()

    assert dados["nome"] == "Pix"
    assert dados["id"] == "12345"

    forma_pagamento_restaurada = FormaPagamento.from_dict(dados)
    assert forma_pagamento_restaurada.get_nome() == "Pix"
    assert forma_pagamento_restaurada.get_id() == "12345"


@pytest.fixture
def controller():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)
    ctrl = FormaPagamentoController(base_path=test_dir)
    yield ctrl
    shutil.rmtree(test_dir)


def test_adicionar_e_listar(controller):
    controller.adicionar(nome="Boleto")
    lista = controller.listar()

    assert len(lista) == 1
    assert lista[0].get_nome() == "Boleto"


def test_atualizar(controller):
    controller.adicionar(nome="Dinheiro")
    item = controller.listar()[0]

    controller.atualizar(id=item.get_id(), nome="Dinheiro Vivo")

    lista_atualizada = controller.listar()
    assert lista_atualizada[0].get_nome() == "Dinheiro Vivo"


def test_remover(controller):
    controller.adicionar(nome="Transferência")
    item = controller.listar()[0]

    controller.remover(id=item.get_id())

    assert len(controller.listar()) == 0


@pytest.fixture
def controllers():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)

    mov_ctrl = MovimentoController(base_path=test_dir)
    fp_ctrl = FormaPagamentoController(base_path=test_dir, mov_ctrl=mov_ctrl)

    yield fp_ctrl, mov_ctrl
    shutil.rmtree(test_dir)


def test_remover_forma_pagamento_com_movimento_bloqueada(controllers):
    fp_ctrl, mov_ctrl = controllers

    fp_ctrl.adicionar(nome="Cartão de Débito")
    forma_pagamento = fp_ctrl.listar()[0]

    mov_ctrl.adicionar(
        responsavel_id="qualquer-id",
        categoria_id="qualquer-id",
        forma_pagamento_id=forma_pagamento.get_id(),
        data="01/01/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=50.0,
    )

    with pytest.raises(Exception) as exc_info:
        fp_ctrl.remover(id=forma_pagamento.get_id())

    assert "movimentos atrelados" in str(exc_info.value)
    assert len(fp_ctrl.listar()) == 1