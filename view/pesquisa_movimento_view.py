import tkinter as tk
from tkinter import ttk, messagebox
from controller.movimento_controller import MovimentoController
from controller.forma_pagamento_controller import FormaPagamentoController
from controller.pessoa_controller import PessoaController
from controller.categoria_controller import CategoriaController
from controller.funcao_familiar_controller import FuncaoFamiliarController

class PesquisaMovimentoView(ttk.Frame):
    def __init__(self, parent, mov_ctrl: MovimentoController, fpag_ctrl: FormaPagamentoController, pes_ctrl: PessoaController, cat_ctrl: CategoriaController, ff_ctrl: FuncaoFamiliarController):
        super().__init__(parent)
        self.mov_ctrl = mov_ctrl
        self.fpag_ctrl = fpag_ctrl
        self.pes_ctrl = pes_ctrl
        self.cat_ctrl = cat_ctrl
        self.ff_ctrl = ff_ctrl
        
        self.fpag_nome_para_id = {}
        self.pes_nome_para_id = {}
        self.cat_nome_para_id = {}
        self.ff_nome_para_id = {}
        
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        
        self._create_widgets()

    def _create_widgets(self):
        # Filtro Frame
        filtro_frame = ttk.LabelFrame(self, text="Filtros Opcionais", padding=10)
        filtro_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Row 0
        ttk.Label(filtro_frame, text="Data Início (Opcional):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_inicio = ttk.Entry(filtro_frame, width=15)
        self.entry_inicio.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filtro_frame, text="Data Fim (Opcional):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_fim = ttk.Entry(filtro_frame, width=15)
        self.entry_fim.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filtro_frame, text="Forma Pag.:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.cb_fpag = ttk.Combobox(filtro_frame, width=20, state="readonly")
        self.cb_fpag.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        # Row 1
        ttk.Label(filtro_frame, text="Responsável:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cb_responsavel = ttk.Combobox(filtro_frame, width=20, state="readonly")
        self.cb_responsavel.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filtro_frame, text="Função Familiar:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.cb_ff = ttk.Combobox(filtro_frame, width=20, state="readonly")
        self.cb_ff.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(filtro_frame, text="Categoria:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.cb_categoria = ttk.Combobox(filtro_frame, width=20, state="readonly")
        self.cb_categoria.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
        
        self._load_combobox()
        
        # Row 2
        btn_pesquisar = ttk.Button(filtro_frame, text="Pesquisar", command=self.pesquisar)
        btn_pesquisar.grid(row=2, column=0, columnspan=6, pady=10)
        
        # Treeview para resultados
        self.tree = ttk.Treeview(self, columns=('ID', 'Responsável', 'Categoria', 'F. Pag', 'Data', 'Tipo', 'Descrição', 'Valor'), show='headings', displaycolumns=('Responsável', 'Categoria', 'F. Pag', 'Data', 'Tipo', 'Descrição', 'Valor'))
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=80)
        self.tree.heading('Responsável', text='Responsável')
        self.tree.heading('Categoria', text='Categoria')
        self.tree.heading('F. Pag', text='F. Pag')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Valor', text='Valor')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Totais Frame
        totais_frame = ttk.Frame(self, padding=10)
        totais_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.lbl_ganhos = ttk.Label(totais_frame, text="Total Ganhos (Entradas): R$ 0.00", font=('Arial', 12, 'bold'), foreground='green')
        self.lbl_ganhos.pack(side=tk.TOP, anchor=tk.W, pady=2)
        
        self.lbl_gastos = ttk.Label(totais_frame, text="Total Gastos (Saídas): R$ 0.00", font=('Arial', 12, 'bold'), foreground='red')
        self.lbl_gastos.pack(side=tk.TOP, anchor=tk.W, pady=2)
        
        self.lbl_saldo = ttk.Label(totais_frame, text="Saldo no Período: R$ 0.00", font=('Arial', 12, 'bold'), foreground='blue')
        self.lbl_saldo.pack(side=tk.TOP, anchor=tk.W, pady=2)

    def _load_combobox(self):
        fpags = self.fpag_ctrl.listar()
        self.cb_fpag['values'] = ["Todas"] + [f.get_nome() for f in fpags]
        self.fpag_nome_para_id = {f.get_nome(): f.get_id() for f in fpags}
        self.cb_fpag.set("Todas")
        
        pessoas = self.pes_ctrl.listar()
        self.cb_responsavel['values'] = ["Todos"] + [p.get_nome() for p in pessoas]
        self.pes_nome_para_id = {p.get_nome(): p.get_id() for p in pessoas}
        self.cb_responsavel.set("Todos")
        
        categorias = self.cat_ctrl.listar()
        self.cb_categoria['values'] = ["Todas"] + [c.get_nome() for c in categorias]
        self.cat_nome_para_id = {c.get_nome(): c.get_id() for c in categorias}
        self.cb_categoria.set("Todas")
        
        funcoes = self.ff_ctrl.listar()
        self.cb_ff['values'] = ["Todas"] + [f.get_nome() for f in funcoes]
        self.ff_nome_para_id = {f.get_nome(): f.get_id() for f in funcoes}
        self.cb_ff.set("Todas")

    def pesquisar(self):
        inicio = self.entry_inicio.get()
        fim = self.entry_fim.get()
        
        if (inicio and not fim) or (fim and not inicio):
            messagebox.showwarning("Aviso", "Preencha ambas as datas ou deixe ambas em branco.")
            return
            
        fpag_val = self.cb_fpag.get()
        resp_val = self.cb_responsavel.get()
        cat_val = self.cb_categoria.get()
        ff_val = self.cb_ff.get()
        
        try:
            fpag_id = self.fpag_nome_para_id.get(fpag_val) if fpag_val not in ("Todas", "") else None
            resp_id = self.pes_nome_para_id.get(resp_val) if resp_val not in ("Todos", "") else None
            cat_id = self.cat_nome_para_id.get(cat_val) if cat_val not in ("Todas", "") else None
            ff_id = self.ff_nome_para_id.get(ff_val) if ff_val not in ("Todas", "") else None
            
            valid_responsavel_ids = None
            if ff_id and not resp_id:
                # Filtrar as pessoas que têm essa função familiar
                pessoas = self.pes_ctrl.listar()
                valid_responsavel_ids = [p.get_id() for p in pessoas if p.get_funcao_id() == ff_id]
                
            movimentos, ganhos, gastos, saldo = self.mov_ctrl.pesquisar_avancado(
                data_inicio=inicio,
                data_fim=fim,
                forma_pagamento_id=fpag_id,
                responsavel_id=resp_id,
                categoria_id=cat_id,
                valid_responsavel_ids=valid_responsavel_ids
            )
            
            # Atualiza Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            pes_map = {p.get_id(): p.get_nome() for p in self.pes_ctrl.listar()}
            cat_map = {c.get_id(): c.get_nome() for c in self.cat_ctrl.listar()}
            fpag_map = {f.get_id(): f.get_nome() for f in self.fpag_ctrl.listar()}
                
            for m in movimentos:
                resp_nome = pes_map.get(m.get_responsavel_id(), "Desconhecido")
                cat_nome = cat_map.get(m.get_categoria_id(), "Desconhecida")
                fpag_nome = fpag_map.get(m.get_forma_pagamento_id(), "Desconhecida")
                self.tree.insert('', tk.END, values=(m.get_id(), resp_nome, cat_nome, fpag_nome, m.get_data(), m.get_tipo_movimento(), m.get_descricao(), f"{m.get_valor():.2f}"))
                
            # Atualiza Totais
            self.lbl_ganhos.config(text=f"Total Ganhos (Entradas): R$ {ganhos:.2f}")
            self.lbl_gastos.config(text=f"Total Gastos (Saídas): R$ {gastos:.2f}")
            
            cor_saldo = 'green' if saldo >= 0 else 'red'
            self.lbl_saldo.config(text=f"Saldo no Período: R$ {saldo:.2f}", foreground=cor_saldo)
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", "As datas informadas são inválidas. Use DD/MM/AAAA.")
