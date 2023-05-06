from django.apps import apps
from django.contrib import admin

# Register your models here.
not_list_display = ("updated_at", "created_at", "basemodel_ptr")
# list_filter = ("created_by", "updated_by" ,)
filter_horizontal = ("user_permissions", )
class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.search_fields = ()
        self.list_display = [field.name for field in model._meta.fields if field.name not in not_list_display]
        self.list_display_links = [field.name for field in model._meta.fields if field.name not in not_list_display]
        # self.list_filter = [field.name for field in model._meta.fields if field.name in list_filter]
        self.filter_horizontal = [field.name for field in model._meta.fields if field.name in filter_horizontal]
        # self.list_editable = [field.name for field in model._meta.fields if field.name =="slug"]
        # self.list_display_links = [field.name for field in model._meta.fields if field.name !="slug"]
        super(ListAdminMixin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass