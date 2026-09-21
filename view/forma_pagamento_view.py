import tkinter as tk
from tkinter import ttk, messagebox
from controller.forma_pagamento_controller import FormaPagamentoController

class FormaPagamentoView(ttk.Frame):
    def __init__(self, parent, controller: FormaPagamentoController):
        super().__init__(parent)
        self.controller = controller
        
        self.id_selecionado = None
        
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        form_frame = ttk.Frame(self, padding=10)
        form_frame.pack(fill=tk.X)
        

        
        ttk.Label(form_frame, text="Forma de Pagamento:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_nome = ttk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Incluir", command=self.incluir).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover).pack(side=tk.LEFT, padx=5)
        
        self.tree = ttk.Treeview(self, columns=('ID', 'Nome'), show='headings', displaycolumns=('Nome',))
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=100)
        self.tree.heading('Nome', text='Nome')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for fp in self.controller.listar():
            self.tree.insert('', tk.END, values=(fp.get_id(), fp.get_nome()))

    def _limpar(self):
        self.id_selecionado = None
        self.entry_nome.delete(0, tk.END)

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.id_selecionado = item[0]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, item[1])

    def incluir(self):
        nome = self.entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome.")
            return
            
        self.controller.adicionar(nome)
        self._limpar()
        self._load_data()
        messagebox.showinfo("Sucesso", "Forma de pagamento incluída!")

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para alterar.")
            return
            
        nome = self.entry_nome.get()
        self.controller.atualizar(self.id_selecionado, nome)
        self._limpar()
        self._load_data()
        messagebox.showinfo("Sucesso", "Forma de pagamento alterada!")

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para remover.")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover?"):
            try:
                self.controller.remover(self.id_selecionado)
                self._limpar()
                self._load_data()
                messagebox.showinfo("Sucesso", "Forma de pagamento removida!")
            except Exception as e:
                messagebox.showerror("Erro de Integridade", str(e))
