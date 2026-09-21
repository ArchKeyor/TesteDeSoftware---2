import tkinter as tk
from tkinter import ttk, messagebox
from controller.movimento_controller import MovimentoController
from controller.pessoa_controller import PessoaController
from controller.categoria_controller import CategoriaController
from controller.forma_pagamento_controller import FormaPagamentoController

class MovimentoView(ttk.Frame):
    def __init__(self, parent, mov_ctrl: MovimentoController, pes_ctrl: PessoaController, cat_ctrl: CategoriaController, fpag_ctrl: FormaPagamentoController):
        super().__init__(parent)
        self.mov_ctrl = mov_ctrl
        self.pes_ctrl = pes_ctrl
        self.cat_ctrl = cat_ctrl
        self.fpag_ctrl = fpag_ctrl
        
        self.pes_nome_para_id = {}
        self.cat_nome_para_id = {}
        self.fpag_nome_para_id = {}
        
        self.id_selecionado = None
        
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        form_frame = ttk.Frame(self, padding=10)
        form_frame.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Responsável:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cb_responsavel = ttk.Combobox(form_frame, width=37, state="readonly")
        self.cb_responsavel.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Categoria:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.cb_categoria = ttk.Combobox(form_frame, width=37, state="readonly")
        self.cb_categoria.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Forma Pag.:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.cb_fpag = ttk.Combobox(form_frame, width=37, state="readonly")
        self.cb_fpag.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Data (DD/MM/AAAA):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.entry_data = ttk.Entry(form_frame, width=40)
        self.entry_data.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Tipo:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.cb_tipo = ttk.Combobox(form_frame, values=["Entrada", "Saída"], width=37, state="readonly")
        self.cb_tipo.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Descrição:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.entry_descricao = ttk.Entry(form_frame, width=40)
        self.entry_descricao.grid(row=6, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Valor:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.entry_valor = ttk.Entry(form_frame, width=40)
        self.entry_valor.grid(row=7, column=1, sticky=tk.W, pady=2)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Atualizar Listas", command=self._update_comboboxes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Incluir", command=self.incluir).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover).pack(side=tk.LEFT, padx=5)
        
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
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        self._update_comboboxes()

    def _update_comboboxes(self):
        pessoas = self.pes_ctrl.listar()
        self.cb_responsavel['values'] = [p.get_nome() for p in pessoas]
        self.pes_nome_para_id = {p.get_nome(): p.get_id() for p in pessoas}
        
        categorias = self.cat_ctrl.listar()
        self.cb_categoria['values'] = [c.get_nome() for c in categorias]
        self.cat_nome_para_id = {c.get_nome(): c.get_id() for c in categorias}
        
        fpags = self.fpag_ctrl.listar()
        self.cb_fpag['values'] = [f.get_nome() for f in fpags]
        self.fpag_nome_para_id = {f.get_nome(): f.get_id() for f in fpags}

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        pes_map = {p.get_id(): p.get_nome() for p in self.pes_ctrl.listar()}
        cat_map = {c.get_id(): c.get_nome() for c in self.cat_ctrl.listar()}
        fpag_map = {f.get_id(): f.get_nome() for f in self.fpag_ctrl.listar()}
            
        for m in self.mov_ctrl.listar():
            resp_nome = pes_map.get(m.get_responsavel_id(), "Desconhecido")
            cat_nome = cat_map.get(m.get_categoria_id(), "Desconhecida")
            fpag_nome = fpag_map.get(m.get_forma_pagamento_id(), "Desconhecida")
            self.tree.insert('', tk.END, values=(m.get_id(), resp_nome, cat_nome, fpag_nome, m.get_data(), m.get_tipo_movimento(), m.get_descricao(), f"{m.get_valor():.2f}"))

    def _limpar(self):
        self.id_selecionado = None
        self.cb_responsavel.set('')
        self.cb_categoria.set('')
        self.cb_fpag.set('')
        self.entry_data.delete(0, tk.END)
        self.cb_tipo.set('')
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.id_selecionado = item[0]
            
            # Select comboboxes based on Names
            resp_nome = item[1]
            if resp_nome in self.cb_responsavel['values']:
                self.cb_responsavel.set(resp_nome)
            
            cat_nome = item[2]
            if cat_nome in self.cb_categoria['values']:
                self.cb_categoria.set(cat_nome)
                    
            fpag_nome = item[3]
            if fpag_nome in self.cb_fpag['values']:
                self.cb_fpag.set(fpag_nome)
            
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, item[4])
            
            self.cb_tipo.set(item[5])
            
            self.entry_descricao.delete(0, tk.END)
            self.entry_descricao.insert(0, item[6])
            
            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, item[7])

    def incluir(self):
        resp_val = self.cb_responsavel.get()
        cat_val = self.cb_categoria.get()
        fpag_val = self.cb_fpag.get()
        data = self.entry_data.get()
        tipo = self.cb_tipo.get()
        descricao = self.entry_descricao.get()
        valor_str = self.entry_valor.get()
        
        if not all([resp_val, cat_val, fpag_val, data, tipo, descricao, valor_str]):
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
            
        try:
            valor = float(valor_str)
            resp_id = self.pes_nome_para_id.get(resp_val)
            cat_id = self.cat_nome_para_id.get(cat_val)
            fpag_id = self.fpag_nome_para_id.get(fpag_val)
            
            if not resp_id or not cat_id or not fpag_id:
                messagebox.showwarning("Aviso", "Responsável, Categoria ou Forma de Pagamento inválidos.")
                return
                
            self.mov_ctrl.adicionar(resp_id, cat_id, fpag_id, data, descricao, tipo, valor)
            self._limpar()
            self._load_data()
            messagebox.showinfo("Sucesso", "Movimento incluído com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para alterar.")
            return
            
        resp_val = self.cb_responsavel.get()
        cat_val = self.cb_categoria.get()
        fpag_val = self.cb_fpag.get()
        data = self.entry_data.get()
        tipo = self.cb_tipo.get()
        descricao = self.entry_descricao.get()
        valor_str = self.entry_valor.get()
        
        try:
            valor = float(valor_str)
            resp_id = self.pes_nome_para_id.get(resp_val)
            cat_id = self.cat_nome_para_id.get(cat_val)
            fpag_id = self.fpag_nome_para_id.get(fpag_val)
            
            if not resp_id or not cat_id or not fpag_id:
                messagebox.showwarning("Aviso", "Responsável, Categoria ou Forma de Pagamento inválidos.")
                return
                
            self.mov_ctrl.atualizar(self.id_selecionado, resp_id, cat_id, fpag_id, data, descricao, tipo, valor)
            self._limpar()
            self._load_data()
            messagebox.showinfo("Sucesso", "Movimento alterado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para remover.")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover?"):
            self.mov_ctrl.remover(self.id_selecionado)
            self._limpar()
            self._load_data()
            messagebox.showinfo("Sucesso", "Movimento removido com sucesso!")
