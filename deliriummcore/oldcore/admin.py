from django.contrib import admin
from oldcore.models import Event, Fase, Seller, TicketRequest, Ticket, CommentTicketRequest, RegToken, Entrada
# Register your models here.

admin.site.register(Seller)
admin.site.register(Event)
admin.site.register(Fase)
admin.site.register(TicketRequest)
admin.site.register(Ticket)
admin.site.register(CommentTicketRequest)
admin.site.register(RegToken)
admin.site.register(Entrada)