import os
import shutil
import tempfile

import pytest

from controller.movimento_controller import MovimentoController
from controller.pessoa_controller import PessoaController
from model.pessoa import Pessoa


def test_criacao_basica():
    pessoa = Pessoa(
        nome="João",
        data_nascimento="15/03/1990",
        funcao_id="funcao-123",
        is_responsavel=True,
    )
    assert pessoa.get_nome() == "João"
    assert pessoa.get_data_nascimento() == "15/03/1990"
    assert pessoa.get_funcao_id() == "funcao-123"
    assert pessoa.get_is_responsavel() is True
    assert pessoa.get_id() is not None


def test_getters_e_setters():
    pessoa = Pessoa(
        nome="João",
        data_nascimento="15/03/1990",
        funcao_id="funcao-123",
        is_responsavel=True,
    )
    pessoa.set_nome("João Silva")
    assert pessoa.get_nome() == "João Silva"


def test_data_nascimento_invalida_levanta_erro():
    with pytest.raises(ValueError):
        Pessoa(
            nome="João",
            data_nascimento="1990-03-15",  # formato errado, deveria ser DD/MM/AAAA
            funcao_id="funcao-123",
            is_responsavel=True,
        )


def test_data_nascimento_texto_invalido_levanta_erro():
    with pytest.raises(ValueError):
        Pessoa(
            nome="João",
            data_nascimento="data-invalida",
            funcao_id="funcao-123",
            is_responsavel=True,
        )


def test_conversao_dict():
    pessoa = Pessoa(
        nome="Maria",
        data_nascimento="20/07/1985",
        funcao_id="funcao-456",
        is_responsavel=False,
        id="12345",
    )
    dados = pessoa.to_dict()

    assert dados["nome"] == "Maria"
    assert dados["data_nascimento"] == "20/07/1985"
    assert dados["funcao_id"] == "funcao-456"
    assert dados["is_responsavel"] is False
    assert dados["id"] == "12345"

    pessoa_restaurada = Pessoa.from_dict(dados)
    assert pessoa_restaurada.get_nome() == "Maria"
    assert pessoa_restaurada.get_id() == "12345"


@pytest.fixture
def controller():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)
    ctrl = PessoaController(base_path=test_dir)
    yield ctrl
    shutil.rmtree(test_dir)


def test_adicionar_e_listar(controller):
    controller.adicionar(
        nome="Ana",
        data_nascimento="10/05/1995",
        funcao_id="funcao-789",
        is_responsavel=True,
    )
    lista = controller.listar()

    assert len(lista) == 1
    assert lista[0].get_nome() == "Ana"


def test_atualizar(controller):
    controller.adicionar(
        nome="Carlos",
        data_nascimento="01/01/2000",
        funcao_id="funcao-001",
        is_responsavel=False,
    )
    item = controller.listar()[0]

    controller.atualizar(
        id=item.get_id(),
        nome="Carlos Eduardo",
        data_nascimento="01/01/2000",
        funcao_id="funcao-001",
        is_responsavel=False,
    )

    lista_atualizada = controller.listar()
    assert lista_atualizada[0].get_nome() == "Carlos Eduardo"


def test_remover(controller):
    controller.adicionar(
        nome="Beatriz",
        data_nascimento="12/12/1992",
        funcao_id="funcao-002",
        is_responsavel=True,
    )
    item = controller.listar()[0]

    controller.remover(id=item.get_id())

    assert len(controller.listar()) == 0


@pytest.fixture
def controllers():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)

    mov_ctrl = MovimentoController(base_path=test_dir)
    pes_ctrl = PessoaController(base_path=test_dir, mov_ctrl=mov_ctrl)

    yield pes_ctrl, mov_ctrl
    shutil.rmtree(test_dir)


def test_remover_pessoa_com_movimento_bloqueada(controllers):
    pes_ctrl, mov_ctrl = controllers

    pes_ctrl.adicionar(
        nome="Fernanda",
        data_nascimento="25/09/1988",
        funcao_id="funcao-003",
        is_responsavel=True,
    )
    pessoa = pes_ctrl.listar()[0]

    mov_ctrl.adicionar(
        responsavel_id=pessoa.get_id(),
        categoria_id="qualquer-id",
        forma_pagamento_id="qualquer-id",
        data="01/01/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=50.0,
    )

    with pytest.raises(Exception) as exc_info:
        pes_ctrl.remover(id=pessoa.get_id())

    assert "movimentos atrelados" in str(exc_info.value)
    assert len(pes_ctrl.listar()) == 1