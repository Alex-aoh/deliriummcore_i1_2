from datetime import datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Seller(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    class Meta:
         
        permissions = (
            ("can_view_admin", "To see admin pages"),
            ("can_view_staff", "To see staff pages"),
            ("can_view_rp", "To see rp PAGES"),
        )


class Event(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=30)
    datetime = models.DateTimeField()
    locationmapslink = models.CharField(max_length=300, verbose_name="Google Maps Link", blank=True)

    STATUS = ( 
        ("AN", "Anunciado"), 
        ("EV", "En Venta"), 
        ("VT", "Venta Terminada"), 
        ("AR", "Archivado"), 
    ) 
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='AN',
    )

    def __str__(self) -> str:
        return self.name

class Fase(models.Model):
    name = models.CharField(verbose_name="Nombre de Fase", max_length=20)
    event = models.ForeignKey(verbose_name="Evento", to=Event, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name="Precio")
    is_active = models.BooleanField(default=False)
    q_sells = models.IntegerField(verbose_name="Ventas", default=0)

    def __str__(self):
        return "Fase - " + self.name + " - " + self.event.name
    


class TicketRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    context = models.CharField(max_length=300, blank=True)
    q_tickets = models.IntegerField(verbose_name="Tickets")
    reference = models.CharField(max_length=150, default="none")
    client = models.CharField(max_length=50, default="none")
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    total = models.IntegerField(verbose_name="Total", default="0")
    created = models.DateTimeField(auto_now=True)
    staff_asigned = models.CharField(max_length=30, default="none")
    comprobante = models.FileField(upload_to='uploads/comprobantes/quimera/', blank=True)

    PAYMENTS = ( 
        ("CASH", "Efectivo"), 
        ("TRANSFER", "Transferencía"), 
        ("DEPOSIT", "Deposíto"), 
    ) 
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENTS,
        default='CASH',
    )

    STATUS = ( 
        ("PE", "Pendiente"), 
        ("RE", "Rechazado"), 
        ("AP", "Aprobado"), 
        ("AR", "Archivado"), 
    ) 
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='PE',
    )

    cash_pay = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return "#" + str(self.pk) + " - " + self.user.username + " " + self.status 



class Ticket(models.Model):

    hash = models.CharField(primary_key=True, verbose_name="Hash Id", max_length=200)
    client = models.CharField(max_length=50, default="none")
    ticketrequest = models.ForeignKey(TicketRequest, on_delete=models.CASCADE)


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(to=Seller, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name="Price")

    status_export = models.BooleanField(default=True)

    use = models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s" % (self.hash, self.ticketrequest.pk)

class CommentTicketRequest(models.Model):
    ticketrequest = models.ForeignKey(TicketRequest, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.CharField(max_length=600)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)


class RegToken(models.Model):
    token = models.CharField(max_length=20)

class Entrada(models.Model):
    name = models.CharField(max_length=40, default="name_default")
    price = models.IntegerField(verbose_name="Price")
    created = models.DateTimeField(auto_now=True)
    isCortesia = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.price) + "$ - " + str(self.isCortesia)
    
    