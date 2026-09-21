import tkinter as tk
from tkinter import ttk, messagebox
from controller.pessoa_controller import PessoaController
from controller.funcao_familiar_controller import FuncaoFamiliarController

class PessoaView(ttk.Frame):
    def __init__(self, parent, controller: PessoaController, ff_ctrl: FuncaoFamiliarController):
        super().__init__(parent)
        self.controller = controller
        self.ff_ctrl = ff_ctrl
        self.ff_nome_para_id = {}
        
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('TCheckbutton', background='white')
        
        self.id_selecionado = None
        
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        form_frame = ttk.Frame(self, padding=10)
        form_frame.pack(fill=tk.X)
        

        
        ttk.Label(form_frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_nome = ttk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Data Nasc (DD/MM/AAAA):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_data = ttk.Entry(form_frame, width=30)
        self.entry_data.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(form_frame, text="Função Familiar (ID):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.cb_funcao = ttk.Combobox(form_frame, width=37, state="readonly")
        self.cb_funcao.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        self.var_responsavel = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="É Responsável?", variable=self.var_responsavel).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Limpar", command=self._limpar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Incluir", command=self.incluir).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover).pack(side=tk.LEFT, padx=5)
        
        self.tree = ttk.Treeview(self, columns=('ID', 'Nome', 'Data Nasc.', 'Função', 'Responsável'), show='headings', displaycolumns=('Nome', 'Data Nasc.', 'Função', 'Responsável'))
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=100)
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Data Nasc.', text='Data Nasc.')
        self.tree.heading('Função', text='Função')
        self.tree.heading('Responsável', text='Responsável')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        self._update_comboboxes()

    def _update_comboboxes(self):
        ffs = self.ff_ctrl.listar()
        self.cb_funcao['values'] = [f.get_nome() for f in ffs]
        self.ff_nome_para_id = {f.get_nome(): f.get_id() for f in ffs}

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        ffs = self.ff_ctrl.listar()
        ff_map = {f.get_id(): f.get_nome() for f in ffs}
            
        for p in self.controller.listar():
            funcao_nome = ff_map.get(p.get_funcao_id(), "Desconhecida")
            self.tree.insert('', tk.END, values=(p.get_id(), p.get_nome(), p.get_data_nascimento(), funcao_nome, 'Sim' if p.get_is_responsavel() else 'Não'))

    def _limpar(self):
        self.id_selecionado = None
        self.entry_nome.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.cb_funcao.set('')
        self.var_responsavel.set(False)

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])['values']
            self.id_selecionado = item[0]
            
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, item[1])
            
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, item[2])
            
            ff_nome = item[3]
            if ff_nome in self.cb_funcao['values']:
                self.cb_funcao.set(ff_nome)
            
            self.var_responsavel.set(item[4] == 'Sim')

    def incluir(self):
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        funcao_val = self.cb_funcao.get()
        is_resp = self.var_responsavel.get()
        
        if not nome or not data or not funcao_val:
            messagebox.showwarning("Aviso", "Preencha nome, data e função.")
            return
            
        try:
            funcao_id = self.ff_nome_para_id.get(funcao_val)
            if not funcao_id:
                messagebox.showwarning("Aviso", "Função selecionada inválida.")
                return
            self.controller.adicionar(nome, data, funcao_id, is_resp)
            self._limpar()
            self._load_data()
            messagebox.showinfo("Sucesso", "Pessoa incluída com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))

    def alterar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para alterar.")
            return
            
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        funcao_val = self.cb_funcao.get()
        is_resp = self.var_responsavel.get()
        
        if not funcao_val:
            messagebox.showwarning("Aviso", "Preencha a função.")
            return
            
        try:
            funcao_id = self.ff_nome_para_id.get(funcao_val)
            if not funcao_id:
                messagebox.showwarning("Aviso", "Função selecionada inválida.")
                return
            self.controller.atualizar(self.id_selecionado, nome, data, funcao_id, is_resp)
            self._limpar()
            self._load_data()
            messagebox.showinfo("Sucesso", "Pessoa alterada com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))

    def remover(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para remover.")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover?"):
            try:
                self.controller.remover(self.id_selecionado)
                self._limpar()
                self._load_data()
                messagebox.showinfo("Sucesso", "Pessoa removida com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro de Integridade", str(e))
