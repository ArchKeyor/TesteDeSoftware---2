import unittest
import os
import tempfile
import shutil

from model.funcao_familiar import FuncaoFamiliar
from controller.funcao_familiar_controller import FuncaoFamiliarController
from controller.pessoa_controller import PessoaController

class TestFuncaoFamiliarUnitario(unittest.TestCase):
    """
    TESTES DE UNIDADE
    Focados exclusivamente em testar os comportamentos internos do modelo FuncaoFamiliar (a entidade).
    Verificamos se a classe inicializa corretamente, valida seus atributos e formata seus dicionários.
    Nenhuma interação com banco de dados ou controllers é feita aqui.
    """
    def test_criacao_basica(self):
        # Testa se a entidade é criada com um ID automático e o nome correto
        ff = FuncaoFamiliar(nome="Pai")
        self.assertEqual(ff.get_nome(), "Pai")
        self.assertIsNotNone(ff.get_id())

    def test_getters_e_setters(self):
        # Testa os métodos de encapsulamento
        ff = FuncaoFamiliar(nome="Mãe")
        ff.set_nome("Avó")
        self.assertEqual(ff.get_nome(), "Avó")

    def test_conversao_dict(self):
        # Testa se a exportação/importação de dicionários (usada pelo CSV) está consistente
        ff_original = FuncaoFamiliar(nome="Tio", id="12345")
        dados = ff_original.to_dict()
        
        self.assertEqual(dados['nome'], "Tio")
        self.assertEqual(dados['id'], "12345")
        
        ff_restaurada = FuncaoFamiliar.from_dict(dados)
        self.assertEqual(ff_restaurada.get_nome(), "Tio")
        self.assertEqual(ff_restaurada.get_id(), "12345")

class TestFuncaoFamiliarComponente(unittest.TestCase):
    """
    TESTES DE COMPONENTES
    Focados no Controller (FuncaoFamiliarController) isolado de outros controllers,
    mas interagindo com seu Repositório (arquivos CSV reais gerados em uma pasta temporária).
    Testamos o fluxo CRUD (Criar, Ler, Atualizar, Deletar) do componente.
    """
    def setUp(self):
        # Cria um diretório temporário para não sujar o sistema de arquivos real do usuário
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, 'arquivos'), exist_ok=True)
        # Inicializa o controller apontando para a pasta temporária
        self.controller = FuncaoFamiliarController(base_path=self.test_dir)

    def tearDown(self):
        # Limpa o diretório temporário após cada teste
        shutil.rmtree(self.test_dir)

    def test_adicionar_e_listar(self):
        # Verifica se ao adicionar uma Função Familiar, o repositório a persiste e a lista corretamente
        self.controller.adicionar(nome="Filho")
        lista = self.controller.listar()
        
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].get_nome(), "Filho")

    def test_atualizar(self):
        # Adiciona e depois atualiza o nome, verificando a persistência
        self.controller.adicionar(nome="Sobrinho")
        item = self.controller.listar()[0]
        
        self.controller.atualizar(id=item.get_id(), nome="Sobrinho(a)")
        
        lista_atualizada = self.controller.listar()
        self.assertEqual(lista_atualizada[0].get_nome(), "Sobrinho(a)")

    def test_remover(self):
        # Testa a exclusão de um registro isolado
        self.controller.adicionar(nome="Irmão")
        item = self.controller.listar()[0]
        
        self.controller.remover(id=item.get_id())
        self.assertEqual(len(self.controller.listar()), 0)


class TestFuncaoFamiliarIntegracao(unittest.TestCase):
    """
    TESTES DE INTEGRAÇÃO
    Verificam como o FuncaoFamiliarController interage e respeita as regras de negócio
    impostas por outros módulos (como o PessoaController). 
    A principal regra de integração é: "Não se pode apagar uma função familiar se houver uma pessoa atrelada a ela".
    """
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, 'arquivos'), exist_ok=True)
        
        # Inicializamos controllers de Pessoa (que precisa de Movimento, mas podemos passar None pois não testaremos movimentos aqui)
        # e Função Familiar
        self.pes_ctrl = PessoaController(base_path=self.test_dir, mov_ctrl=None)
        self.ff_ctrl = FuncaoFamiliarController(base_path=self.test_dir, pes_ctrl=self.pes_ctrl)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_remover_com_dependencia_bloqueada(self):
        # 1. Adicionamos a Função Familiar
        self.ff_ctrl.adicionar(nome="Pai")
        ff_criada = self.ff_ctrl.listar()[0]
        
        # 2. Atrelamos uma Pessoa a essa função (Simulando uma integração real)
        self.pes_ctrl.adicionar(nome="João", data_nascimento="01/01/1980", is_responsavel=True, funcao_id=ff_criada.get_id())
        
        # 3. Tentamos remover a Função Familiar, o que deve levantar uma exceção por conta da dependência (Pessoa atrelada)
        with self.assertRaises(Exception) as context:
            self.ff_ctrl.remover(id=ff_criada.get_id())
            
        # 4. Verificamos se a mensagem de erro da integração está correta
        self.assertTrue("pessoas atreladas" in str(context.exception))
        
        # 5. Confirmamos que o item não foi apagado
        self.assertEqual(len(self.ff_ctrl.listar()), 1)

if __name__ == '__main__':
    unittest.main()
