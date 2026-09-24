import os
import shutil
import tempfile

import pytest

from controller.categoria_controller import CategoriaController
from model.categoria import Categoria
from controller.movimento_controller import MovimentoController


def test_criacao_basica():
    categoria = Categoria(nome="Alimentação")
    assert categoria.get_nome() == "Alimentação"
    assert categoria.get_id() is not None


def test_getters_e_setters():
    categoria = Categoria(nome="Alimentação")
    categoria.set_nome("Moradia")
    assert categoria.get_nome() == "Moradia"


def test_conversao_dict():
    categoria = Categoria(nome="Alimentação", id="12345")
    dados = categoria.to_dict()

    assert dados["nome"] == "Alimentação"
    assert dados["id"] == "12345"

    categoria_restaurada = Categoria.from_dict(dados)
    assert categoria_restaurada.get_nome() == "Alimentação"
    assert categoria_restaurada.get_id() == "12345"


@pytest.fixture
def controller():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)
    ctrl = CategoriaController(base_path=test_dir)
    yield ctrl
    shutil.rmtree(test_dir)


def test_adicionar_e_listar(controller):
    controller.adicionar(nome="Alimentação")
    lista = controller.listar()

    assert len(lista) == 1
    assert lista[0].get_nome() == "Alimentação"


def test_atualizar(controller):
    controller.adicionar(nome="Transporte")
    item = controller.listar()[0]

    controller.atualizar(id=item.get_id(), nome="Transporte Público")

    lista_atualizada = controller.listar()
    assert lista_atualizada[0].get_nome() == "Transporte Público"


def test_remover(controller):
    controller.adicionar(nome="Lazer")
    item = controller.listar()[0]

    controller.remover(id=item.get_id())

    assert len(controller.listar()) == 0

@pytest.fixture
def controllers():
    test_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(test_dir, "arquivos"), exist_ok=True)

    mov_ctrl = MovimentoController(base_path=test_dir)
    cat_ctrl = CategoriaController(base_path=test_dir, mov_ctrl=mov_ctrl)

    yield cat_ctrl, mov_ctrl
    shutil.rmtree(test_dir)


def test_remover_categoria_com_movimento_bloqueada(controllers):
    cat_ctrl, mov_ctrl = controllers

    cat_ctrl.adicionar(nome="Alimentação")
    categoria = cat_ctrl.listar()[0]

    mov_ctrl.adicionar(
        responsavel_id="qualquer-id",
        categoria_id=categoria.get_id(),
        forma_pagamento_id="qualquer-id",
        data="01/01/2026",
        descricao="Compra no mercado",
        tipo_movimento="Saída",
        valor=50.0,
    )

    with pytest.raises(Exception) as exc_info:
        cat_ctrl.remover(id=categoria.get_id())

    assert "movimentos atrelados" in str(exc_info.value)
    assert len(cat_ctrl.listar()) == 1