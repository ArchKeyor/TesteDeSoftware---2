from model.categoria import Categoria


def test_criacao_basica(self):
    categoria = Categoria(nome="Alimentação")
    assert categoria.get_nome() == "Alimentação"
    assert categoria.get_id is not None
