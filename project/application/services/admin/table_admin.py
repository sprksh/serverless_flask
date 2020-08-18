from flask_admin.contrib.sqla import ModelView

from application import Table


class TableAdminView(ModelView):
    _model = Table
    _category = ""
