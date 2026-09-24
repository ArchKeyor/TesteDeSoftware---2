import os
import shutil
import tempfile

import pytest

from controller.categoria_controller import CategoriaController
from controller.forma_pagamento_controller import FormaPagamentoController
from controller.movimento_controller import MovimentoController
from controller.pessoa_controller import PessoaController
from model.movimento import Movimento


def test_criacao_basica():
    movimento = Movimento(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
    )
    assert movimento.get_responsavel_id() == "pessoa-123"
    assert movimento.get_categoria_id() == "categoria-123"
    assert movimento.get_forma_pagamento_id() == "forma-123"
    assert movimento.get_data() == "10/06/2026"
    assert movimento.get_descricao() == "Compra no mercado"
    assert movimento.get_tipo_movimento() == "Saída"
    assert movimento.get_valor() == 150.50
    assert movimento.get_id() is not None


def test_getters_e_setters():
    movimento = Movimento(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
    )
    movimento.set_descricao("Compra no mercado - atualizado")
    assert movimento.get_descricao() == "Compra no mercado - atualizado"


def test_data_invalida_levanta_erro():
    with pytest.raises(ValueError):
        Movimento(
            responsavel_id="pessoa-123",
            categoria_id="categoria-123",
            forma_pagamento_id="forma-123",
            data="2026-06-10",  # formato errado
            descricao="Compra no mercado",
            tipo_movimento="Saída",
            valor=150.50,
        )


def test_valor_convertido_para_float():
    movimento = Movimento(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150,  # passa int, não float
    )
    assert movimento.get_valor() == 150.0
    assert isinstance(movimento.get_valor(), float)


def test_conversao_dict():
    movimento = Movimento(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
        id="12345",
    )
    dados = movimento.to_dict()

    assert dados["responsavel_id"] == "pessoa-123"
    assert dados["valor"] == 150.50
    assert dados["id"] == "12345"

    movimento_restaurado = Movimento.from_dict(dados)
    assert movimento_restaurado.get_descricao() == "Compra no mercado"
    assert movimento_restaurado.get_id() == "12345"


@pytest.fixture
def controller():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)
    ctrl = MovimentoController(base_path=test_dir)
    yield ctrl
    shutil.rmtree(test_dir)


def test_adicionar_e_listar(controller):
    controller.adicionar(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
    )
    lista = controller.listar()

    assert len(lista) == 1
    assert lista[0].get_descricao() == "Compra no mercado"


def test_adicionar_com_valor_negativo_levanta_erro(controller):
    with pytest.raises(ValueError):
        controller.adicionar(
            responsavel_id="pessoa-123",
            categoria_id="categoria-123",
            forma_pagamento_id="forma-123",
            data="10/06/2026",
            descricao="Compra no mercado",
            tipo_movimento="Saída",
            valor=-50.0,
        )


def test_atualizar(controller):
    controller.adicionar(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
    )
    item = controller.listar()[0]

    controller.atualizar(
        id=item.get_id(),
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado - atualizada",
        tipo_movimento="Saída",
        valor=200.0,
    )

    lista_atualizada = controller.listar()
    assert lista_atualizada[0].get_descricao() == "Compra no mercado - atualizada"
    assert lista_atualizada[0].get_valor() == 200.0


def test_remover(controller):
    controller.adicionar(
        responsavel_id="pessoa-123",
        categoria_id="categoria-123",
        forma_pagamento_id="forma-123",
        data="10/06/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=150.50,
    )
    item = controller.listar()[0]

    controller.remover(id=item.get_id())

    assert len(controller.listar()) == 0


@pytest.fixture
def cenario_completo():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)

    mov_ctrl = MovimentoController(base_path=test_dir)
    pes_ctrl = PessoaController(base_path=test_dir, mov_ctrl=mov_ctrl)
    cat_ctrl = CategoriaController(base_path=test_dir, mov_ctrl=mov_ctrl)
    fp_ctrl = FormaPagamentoController(base_path=test_dir, mov_ctrl=mov_ctrl)

    yield pes_ctrl, cat_ctrl, fp_ctrl, mov_ctrl
    shutil.rmtree(test_dir)


def test_fluxo_completo_pessoa_categoria_forma_pagamento_movimento(cenario_completo):
    pes_ctrl, cat_ctrl, fp_ctrl, mov_ctrl = cenario_completo

    pes_ctrl.adicionar(
        nome="Roberto",
        data_nascimento="15/04/1985",
        funcao_id="funcao-pai-123",
        is_responsavel=True,
    )
    pessoa = pes_ctrl.listar()[0]

    cat_ctrl.adicionar(nome="Alimentação")
    categoria = cat_ctrl.listar()[0]

    fp_ctrl.adicionar(nome="Cartão de Crédito")
    forma_pagamento = fp_ctrl.listar()[0]

    mov_ctrl.adicionar(
        responsavel_id=pessoa.get_id(),
        categoria_id=categoria.get_id(),
        forma_pagamento_id=forma_pagamento.get_id(),
        data="10/06/2026",
        descricao="Compras do mês",
        tipo_movimento="Saída",
        valor=350.0,
    )

    movimento_salvo = mov_ctrl.listar()[0]
    assert movimento_salvo.get_responsavel_id() == pessoa.get_id()
    assert movimento_salvo.get_categoria_id() == categoria.get_id()
    assert movimento_salvo.get_forma_pagamento_id() == forma_pagamento.get_id()