from django.db.models import Q

def format_search_string(fields, keyword):
    Qr = None
    for field in fields:        
        q = Q(**{"%s__icontains" % field: keyword })
        if Qr:
            Qr = Qr | q
        else:
            Qr = q
    
    return Qr

def get_fields(model, fieldnames):
    return [model._meta.get_field(field) for field in fieldnames]