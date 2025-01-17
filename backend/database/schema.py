from schematics.models import Model
from schematics.types import (
    StringType,
    IntType,
    DateTimeType,
    TimestampType,
    FloatType,
)


class Cliente(Model):
    nome = StringType(required=True)
    cpf = StringType(required=True)
    telefone = StringType(default="")


class Comanda(Model):
    cliente_id = IntType(required=True)
    inicio = TimestampType(required=True)
    fim = TimestampType(serialize_when_none=True)
    data_comanda = DateTimeType(required=True)


class Produto(Model):
    produto = StringType(required=True)
    valor = FloatType(required=True)
    unidade = StringType(required=True)


def validate_document(data, cls):
    model = cls(data)
    model.validate()

    return model
