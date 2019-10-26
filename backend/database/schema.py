from schematics.models import Model
from schematics.types import (
    StringType,
)


class Cliente(Model):
    nome = StringType(required=True)
    cpf = StringType(required=True)
    telefone = StringType(default="")


def validate_document(data, cls):
    model = cls(data)
    model.validate()

    return model
