import tkinter as tk
from tkinter import ttk
import os
import sys

# Adiciona o diretório atual ao sys.path para importações absolutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.pessoa_controller import PessoaController
from controller.categoria_controller import CategoriaController
from controller.movimento_controller import MovimentoController
from controller.forma_pagamento_controller import FormaPagamentoController
from controller.funcao_familiar_controller import FuncaoFamiliarController

from view.pessoa_view import PessoaView
from view.categoria_view import CategoriaView
from view.movimento_view import MovimentoView
from view.pesquisa_movimento_view import PesquisaMovimentoView
from view.forma_pagamento_view import FormaPagamentoView
from view.funcao_familiar_view import FuncaoFamiliarView

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Gastos Familiares")
        self.root.geometry("800x600")
        self.root.state('zoomed') # Maximiza a tela no Windows
        self.root.configure(bg='white')
        
        # Estilo Global
        style = ttk.Style()
        style.theme_use('clam') # Tema limpo
        style.configure('.', background='white')
        style.configure('Dashboard.TButton', font=('Arial', 12, 'bold'), padding=15)
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Inicializa Controllers
        self.mov_ctrl = MovimentoController(base_path)
        self.pes_ctrl = PessoaController(base_path, self.mov_ctrl)
        self.ff_ctrl = FuncaoFamiliarController(base_path, self.pes_ctrl)
        self.cat_ctrl = CategoriaController(base_path, self.mov_ctrl)
        self.fpag_ctrl = FormaPagamentoController(base_path, self.mov_ctrl)
        
        # Container Principal
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.frames = {}
        
        # Cria Dashboard
        self._create_dashboard()
        
        # Inicializa Views com Wrappers
        self.view_ff = self._create_module_wrapper("Funções Familiares", FuncaoFamiliarView, self.ff_ctrl)
        self.view_pessoas = self._create_module_wrapper("Pessoas", PessoaView, self.pes_ctrl, self.ff_ctrl)
        self.view_categorias = self._create_module_wrapper("Categorias", CategoriaView, self.cat_ctrl)
        self.view_fpag = self._create_module_wrapper("Formas de Pagamento", FormaPagamentoView, self.fpag_ctrl)
        self.view_movimentos = self._create_module_wrapper("Movimentos", MovimentoView, self.mov_ctrl, self.pes_ctrl, self.cat_ctrl, self.fpag_ctrl)
        self.view_pesquisa = self._create_module_wrapper("Pesquisa e Relatórios", PesquisaMovimentoView, self.mov_ctrl, self.fpag_ctrl, self.pes_ctrl, self.cat_ctrl, self.ff_ctrl)
        
        self.show_dashboard()

    def _create_dashboard(self):
        self.dashboard_frame = ttk.Frame(self.container)
        
        lbl_title = ttk.Label(self.dashboard_frame, text="Controle de Gastos Familiares", font=('Arial', 24, 'bold'))
        lbl_title.pack(pady=40)
        
        btn_frame = ttk.Frame(self.dashboard_frame)
        btn_frame.pack()
        
        modulos = [
            ("Funções Familiares", 0, 0),
            ("Pessoas", 0, 1),
            ("Categorias", 1, 0),
            ("Formas de Pagamento", 1, 1),
            ("Movimentos", 2, 0),
            ("Pesquisa e Relatórios", 2, 1)
        ]
        
        for nome, row, col in modulos:
            btn = ttk.Button(btn_frame, text=nome, style='Dashboard.TButton', width=25,
                             command=lambda n=nome: self.show_view(n))
            btn.grid(row=row, column=col, padx=15, pady=15)
            
        self.frames["Dashboard"] = self.dashboard_frame

    def _create_module_wrapper(self, title, view_class, *args):
        frame = ttk.Frame(self.container)
        
        header = ttk.Frame(frame, padding=10)
        header.pack(fill=tk.X)
        
        btn_voltar = ttk.Button(header, text="< Voltar", command=self.show_dashboard)
        btn_voltar.pack(side=tk.LEFT)
        
        lbl_title = ttk.Label(header, text=title, font=('Arial', 16, 'bold'))
        lbl_title.pack(side=tk.LEFT, padx=20)
        
        # Instancia a View real dentro do frame principal e desempacota logo abaixo
        view_instance = view_class(frame, *args)
        view_instance.pack(fill=tk.BOTH, expand=True)
        
        self.frames[title] = frame
        return view_instance

    def show_dashboard(self):
        for f in self.frames.values():
            f.pack_forget()
        self.frames["Dashboard"].pack(fill=tk.BOTH, expand=True)

    def show_view(self, name):
        # Dispara os recarregamentos necessários antes de exibir a tela
        if name == "Pessoas":
            self.view_pessoas._update_comboboxes()
            self.view_pessoas._load_data()
        elif name == "Movimentos":
            self.view_movimentos._update_comboboxes()
            self.view_movimentos._load_data()
        elif name == "Pesquisa e Relatórios":
            self.view_pesquisa._load_combobox()
        elif name == "Funções Familiares":
            self.view_ff._load_data()
        elif name == "Categorias":
            self.view_categorias._load_data()
        elif name == "Formas de Pagamento":
            self.view_fpag._load_data()
            
        # Alterna para o Frame
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
