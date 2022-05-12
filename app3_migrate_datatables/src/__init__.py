from flask_restful import Resource
from datetime import datetime
from sqlalchemy import or_
from respect_validation import FormValidator, Validator as v


class ResourceCustom(Resource):

    @classmethod
    def fv(cls) -> 'FormValidator':
        return FormValidator()

    @classmethod
    def validate_datatables(cls, data, columns=None) -> 'FormValidator':

        rules = {
            "draw": v.intType().min(0),
            "start": v.intType().min(0),
            "length": v.intType().min(0),
            "search": v.keySet(
                v.key("value", v.stringType()),
                v.key("regex", v.boolType())
            ),
            "order": v.listType().length(1, 1).each(v.keySet(
                v.key("column", v.intType().min(0)),
                v.key("dir", v.stringType().include(['asc', 'desc']))
            )),
            "column": v.listType().each(v.keySet(
                v.key("data", v.stringType()),
                v.key("name", v.optional(v.stringType())),
                v.key("searchable", v.boolType()),
                v.key("orderable", v.boolType()),
                v.key("search", v.dictType().keySet(
                    v.key("value", v.stringType()),
                    v.key("regex", v.boolType()),
                ))
            ))
        }

        if columns:
            #
            #  I have to add new rule to check column name
            #  in "order". Optionaly add check for "column" (data or name)
            #
            pass

        return cls.fv().validate(data, rules)

    @classmethod
    def datatables(cls, model, req):
        model_columns = model.__table__.columns.keys()

        validation = cls.validate_datatables(data=req, columns=model_columns)
        if validation.failed():
            return {"validation": validation.get_messages()}, 400

        order_by = getattr(model, req["column"][req["order"][0]["column"]]["data"]) if req["order"][0]["dir"] == 'asc'\
            else getattr(model, req["column"][req["order"][0]["column"]]["data"]).desc()

        table_query = model.query.order_by(order_by)

        select_columns = []
        for c in req["column"]:
            select_columns.append(getattr(model, c["data"]).label(c["data"]))
        table_query = table_query.with_entities(*select_columns)

        total_count = table_query.count()

        search = []
        if req["search"]["value"]:
            for c in select_columns:
                search.append(getattr(model, c.name).like('%{}%'.format(req["search"]["value"])))

        if search:
            table_query = table_query.filter(or_(*search))

        records_filtered = table_query.count()

        table_query = table_query.limit(req["length"])
        if req["start"]:
            table_query = table_query.offset(req["start"])

        output = []
        for row in table_query.all():
            _row = {}
            for i, cell in enumerate(row):
                if isinstance(row[i], datetime):
                    _row[select_columns[i].name] = row[i].strftime("%Y-%m-%d %H:%M:%S")
                    continue
                _row[select_columns[i].name] = row[i]
            output.append(_row)

        return {
            "recordsTotal": total_count,
            "recordsFiltered": records_filtered,
            "data": output,
            "draw": req["draw"] + 1
        }
