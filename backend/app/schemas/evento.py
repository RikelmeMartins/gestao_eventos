from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class EventoSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    descricao = fields.Str(allow_none=True)
    data_inicio = fields.DateTime(required=True)
    data_fim = fields.DateTime(required=True)
    local = fields.Str(allow_none=True, validate=validate.Length(max=200))
    vagas = fields.Int(load_default=0, validate=validate.Range(min=0))

    @validates_schema
    def validar_datas(self, dados, **kwargs):
        inicio, fim = dados.get("data_inicio"), dados.get("data_fim")
        if inicio and fim and fim < inicio:
            raise ValidationError(
                "A data de término deve ser igual ou posterior à de início.", "data_fim"
            )
