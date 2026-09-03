from django.contrib import admin
from .models import TicketCategory, HelpdeskTicket, TicketComment

admin.site.register(TicketCategory)
admin.site.register(HelpdeskTicket)
admin.site.register(TicketComment)
