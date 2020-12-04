from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from django.utils.translation import gettext as _


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # self.available_children.append(modules.LinkList)
        super(CustomIndexDashboard, self).init_with_context(context)
        self.children.append(
            modules.LinkList(
                _("DB Backups"),
                children=[
                    {
                        "title": _("Make backup"),
                        "url": "/api/v0/backup/",
                        "external": False,
                    },
                    {
                        "title": _("Restore database"),
                        "url": "/api/v0/restore/",
                        "external": False,
                    },
                    {
                        "title": _("Update cert"),
                        "url": "/api/v0/update-cert/",
                        "external": False,
                    }
                ],
                column=0,
                order=0,
            )
        )
