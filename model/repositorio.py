import csv
import os
import shutil
import tempfile
from typing import TypeVar

T = TypeVar("T")


class RepositorioCSV:
    def __init__(self, filepath: str, model_class: type[T]):
        self.filepath = filepath
        self.model_class = model_class

        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        if not os.path.exists(self.filepath):
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = self.model_class.get_fields()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

    def salvar(self, entidade: T):
        with open(self.filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.model_class.get_fields())
            writer.writerow(entidade.to_dict())

    def listar_todos(self) -> list[T]:
        entidades = []
        if not os.path.exists(self.filepath):
            return entidades

        with open(self.filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entidades.append(self.model_class.from_dict(row))
        return entidades

    def buscar_por_id(self, id: str) -> T | None:
        for entidade in self.listar_todos():
            if entidade.get_id() == id:
                return entidade
        return None

    def atualizar(self, id: str, nova_entidade: T):
        temp_fd, temp_path = tempfile.mkstemp()
        fieldnames = self.model_class.get_fields()

        with os.fdopen(temp_fd, "w", newline="", encoding="utf-8") as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()

            with open(self.filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["id"] == id_entity:
                        writer.writerow(nova_entidade.to_dict())
                    else:
                        writer.writerow(row)

        shutil.move(temp_path, self.filepath)

    def remover(self, id: str):
        temp_fd, temp_path = tempfile.mkstemp()
        fieldnames = self.model_class.get_fields()

        with os.fdopen(temp_fd, "w", newline="", encoding="utf-8") as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()

            with open(self.filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["id"] != id_entity:
                        writer.writerow(row)

        shutil.move(temp_path, self.filepath)
