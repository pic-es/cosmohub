def _column_list(constraint, table):
    return "__".join(constraint._pending_colargs)


naming_convention = {
    "column_list": _column_list,
    "pk": "pk__%(table_name)s",
    "fk": "fk__%(table_name)s__%(referred_table_name)s",
    "uq": "uq__%(table_name)s__%(column_list)s",
    "ix": "ix__%(table_name)s__%(column_list)s",
}
