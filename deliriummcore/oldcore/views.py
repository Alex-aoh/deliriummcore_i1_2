import os
from webbrowser import get
import imgkit
import mimetypes

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from main.methods import checkCoreAccess, getCoreRole
from oldcore.models import Event, TicketRequest, Ticket, Seller, Fase
from django.conf import settings
from oldcore.methods import checkSeller
from django.db.models import Q
from django.contrib.auth.models import User


from hashlib import md5, sha256

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        return render(request, 'oldcore/index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)

        requests_ap = TicketRequest.objects.filter(Q(user=request.user) &  Q(status="AP"))
        ap_cash = 0
        for ticket in requests_ap:
            ap_cash = ap_cash + ticket.total


        requests_cash = TicketRequest.objects.filter(Q(payment_method="CASH") &  Q(status="AP") & Q(user=request.user))
        all_cash = 0
        requests_debt = requests_cash.filter(cash_pay=False)
        debt_cash = 0

        for ticket in requests_cash:
            all_cash = all_cash + ticket.total

        for ticket in requests_debt:
            debt_cash = debt_cash + ticket.total
        
        

        return render(request, 'oldcore/dashboard.html', {
            "requests_cash": TicketRequest.objects.filter(user=request.user, payment_method="CASH"),
            "all_cash": all_cash,
            "debt_cash": debt_cash,
            "paid_cash": all_cash - debt_cash,
            "ap_cash": ap_cash,
            "boletos": len(Ticket.objects.filter(user=request.user)),
            "comision": int(ap_cash*0.1),

            

        })

def admin_index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:

            requests_ap = TicketRequest.objects.filter(Q(user=request.user) &  Q(status="AP"))
            ap_cash = 0
            for ticket in requests_ap:
                ap_cash = ap_cash + ticket.total


            requests_cash = TicketRequest.objects.filter(Q(payment_method="CASH") &  Q(status="AP") & Q(user=request.user))
            all_cash = 0
            requests_debt = requests_cash.filter(cash_pay=False)
            debt_cash = 0

            for ticket in requests_cash:
                all_cash = all_cash + ticket.total

            for ticket in requests_debt:
                debt_cash = debt_cash + ticket.total
            
            

            return render(request, 'oldcore/admin_index.html', {
                "requests_cash": TicketRequest.objects.filter(user=request.user, payment_method="CASH"),
                "all_cash": all_cash,
                "debt_cash": debt_cash,
                "paid_cash": all_cash - debt_cash,
                "ap_cash": ap_cash,
                "boletos": len(Ticket.objects.filter(user=request.user)),
                "comision": int(ap_cash*0.1),

                

            })
        else:
            return HttpResponseRedirect(reverse("main:home"))

def rp_check_select(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:
            if request.method == "POST":
                if request.POST["us"]:
                    username = request.POST["us"]
                    return HttpResponseRedirect(reverse("oldcore:rp_check_main", args=(username,)))
            
            else:
                return render(request, 'oldcore/rp_check_select.html', {
                    "users": Seller.objects.all(),
                })


        else:
            return HttpResponseRedirect(reverse("main:home"))

def rp_check_main(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:
            user_selected = get_object_or_404(User, username=username)

            return render(request, 'oldcore/rp_check_main.html', {
                    "requests": TicketRequest.objects.filter(user=user_selected),
                    "user_selected": user_selected,
                })
        else:
            return HttpResponseRedirect(reverse("main:home"))   

def lista_requests(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)

        user_selected = get_object_or_404(User, username=request.user)

        return render(request, 'oldcore/tools/ticketsrequest/lista_requests.html', {
                "requests": TicketRequest.objects.filter(user=user_selected),
                "user_selected": user_selected,
                })   

def admin_lista_requests(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:

            requests = TicketRequest.objects.all()

            return render(request, 'oldcore/tools/ticketsrequest/admin_lista_requests.html', {
                "requests": requests
            })
        else:
            return HttpResponseRedirect(reverse("main:home"))


def my_requests(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:    
        return render(request, "oldcore/tools/ticketsrequest/my_requests.html",{
            "ticketspe": request.user.ticketrequest_set.all().filter(status="PE"),
            "ticketsap": request.user.ticketrequest_set.all().filter(status="AP"),
            "ticketsre": request.user.ticketrequest_set.all().filter(status="RE"),

        })

def create_request(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        event_on_sell = get_object_or_404(Event, status="EV")
        fase = event_on_sell.fase_set.get(is_active=True)
        return render(request, "oldcore/tools/ticketsrequest/create_request.html", {
            "event": event_on_sell,
            "fase": fase,
        })

def new_ticket_request(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        event = get_object_or_404(Event, status="EV")
        fase = event.fase_set.get(is_active=True)
        if request.POST["q_tickets"]:
            totalp = int(request.POST["q_tickets"])*fase.price
        else:
            totalp=0
        try:
            t = ticket_request_create(request=request, event=event, totalp=totalp, fase=fase)

        except (BaseException):
            return render(request, "oldcore/tools/ticketsrequest/create_request.html", {
            "event": event,
            "fase": fase,
            "message": "¡Error al crear a la Request!",
            "message_type": "danger"
            })
        else:
            t.save()
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(t.pk,)))
            
def delete_ticket_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if request.POST:
            if request.POST.get('yes', False):
                tr = get_object_or_404(TicketRequest, pk=requestid)
                for ticket in tr.ticket_set.all():
                    if os.path.exists(settings.MEDIA_ROOT + "/tickets/" + ticket.hash + '.jpg'):
                        os.remove(settings.MEDIA_ROOT + "/tickets/" + ticket.hash +'.jpg')
                if tr.comprobante:
                    if os.path.exists(settings.MEDIA_ROOT + str(tr.comprobante)):
                        os.remove(settings.MEDIA_ROOT + str(tr.comprobante))

                get_object_or_404(TicketRequest, pk=requestid).delete()
                return HttpResponseRedirect(reverse("oldcore:index"), {
                    "message": "Request Borrada",
                    "message_type": "success",
                })
            if request.POST.get('not', False):
                return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))
        return render(request, "oldcore/tools/ticketsrequest/delete_ticket_request.html", {
            "requestid": requestid
        })

def request_view(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)

        status_display = ticketrequest.get_status_display()

        ticketcount = range(len(Ticket.objects.filter(ticketrequest=requestid)))
        if ticketrequest.user == request.user or request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff"):
            return render(request, "oldcore/tools/ticketsrequest/request_view.html", {
                "requestid": requestid,
                "ticketrequest": ticketrequest,
                "status_display": status_display,
                "ticketslist": Ticket.objects.filter(ticketrequest=requestid),
                "ticketcount": ticketcount,
                "comments": ticketrequest.commentticketrequest_set.all()
            }) 

def admin_request_view(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)

        status_display = ticketrequest.get_status_display()

        if request.user.has_perm("oldcore.can_view_admin") or request.user.has_perm("oldcore.can_view_staff") :
            return render(request, "oldcore/tools/ticketsrequest/admin_request_view.html", {
                "requestid": requestid,
                "ticketrequest": ticketrequest,
                "status_display": status_display,
                "ticketslist": Ticket.objects.filter(ticketrequest=requestid),
                "comments": ticketrequest.commentticketrequest_set.all()
            })
        else:
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

def aprobar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
        status_display = ticketrequest.get_status_display()

        if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
            ticketrequest.status = "AP"
            ticketrequest.save()


            if ticketrequest.ticket_set.all():
                return HttpResponseRedirect(reverse("tickets:request_view", args=(requestid,)))
            if not ticketrequest.ticket_set.all():
                #NO HAY TICKETS CREADOS
                for t in range(ticketrequest.q_tickets):

                    hash = hashTicket(event=ticketrequest.event.name, user=ticketrequest.user.username, request=ticketrequest.pk,id=Ticket.objects.count())
                    ticketnew = Ticket(
                    hash=hash,
                    client=ticketrequest.client,
                    ticketrequest=ticketrequest,
                    user=ticketrequest.user,
                    seller=Seller.objects.get(user=ticketrequest.user),
                    event=ticketrequest.event,

                    fase = ticketrequest.fase,
                    price= ticketrequest.fase.price,
                    status_export = True)
                    ticketnew.save()

                    options = {
                        'xvfb': '',
                        'crop-y': '4',

                    }
                    #export html
                    #options={}
                    imgkit.from_url('0.0.0.0/oldcore/t/export/' + hash, settings.MEDIA_ROOT + "tickets/" + hash +'.jpg', options=options)



                return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

            
            # return render(request, "tickets/request_view.html", {
            #     "error_message": hash,
            #     "requestid": requestid
            # })
            # return HttpResponseRedirect(reverse("tickets:admin_request_view", args=(requestid,)))
        else:
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

def temp_ticket_export(request, hash):
    status_export = Ticket.objects.get(hash=hash)
    if status_export.status_export == True:
        return render(request, "oldcore/ticket_export.html", {
            "hash": hash
        })
    else:
        return reverse("oldcore:index")

def image_tickets(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid) 
        tickets = Ticket.objects.filter(ticketrequest=ticketrequest)
        return render(request, "oldcore/image_tickets_request.html", {
            "requestid": requestid,
            "tickets": tickets,
            "ticketrequest": ticketrequest,
        })

def image_ticket(request, hash):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        ticket = get_object_or_404(Ticket, hash=hash)
        return render(request, "oldcore/image_tickets.html", {
            "ticket": ticket,
        })

def download_ticket(request, tickethash):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:

        # Define text file name
        filename = str(tickethash) + ".jpg"
        # Define the full file path
        filepath = settings.MEDIA_ROOT + 'tickets/' + filename
        # Open the file for reading content
        with open(filepath, 'rb') as f:
            path = f.read()
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response

def rechazar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
        status_display = ticketrequest.get_status_display()

        if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
            ticketrequest.status = "RE"
            ticketrequest.save()
            return HttpResponseRedirect(reverse("oldcore:admin_request_view", args=(requestid,)))
        else:
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

def archivar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
        status_display = ticketrequest.get_status_display()

        if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
            ticketrequest.status = "AR"
            ticketrequest.save()
            return HttpResponseRedirect(reverse("oldcore:admin_request_view", args=(requestid,)))
        else:
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

def asignar_request(request, requestid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        if requestid == 0:
            return HttpResponseRedirect(reverse("oldcore:index"))
        ticketrequest = get_object_or_404(TicketRequest, pk=requestid)
        status_display = ticketrequest.get_status_display()

        if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :
            ticketrequest.staff_asigned = request.user.username
            ticketrequest.save()
            return HttpResponseRedirect(reverse("oldcore:admin_request_view", args=(requestid,)))
        else:
            return HttpResponseRedirect(reverse("oldcore:request_view", args=(requestid,)))

def hashTicket(event, user, request, id):
    request = str(request)
    id = str(id)
    h = md5()
    h.update(event.encode('utf-8'))
    h.update(user.encode('utf-8'))
    h.update(request.encode('utf-8'))
    h.update(id.encode('utf-8'))

    return h.hexdigest()

def ticket_request_create(request, event, totalp, fase):
    if not request.POST["payment_method"] == "CASH":
        t = TicketRequest(
            user=request.user,
            seller=Seller.objects.get(user=request.user),
            event=event,
            context=request.POST["context"],
            q_tickets=int(request.POST["q_tickets"]),
            reference=request.POST["reference"],
            client=request.POST["client"],
            fase=fase,
            total=totalp,
            payment_method=request.POST["payment_method"],
            comprobante=request.FILES["comprobante"])
        return t

    elif request.POST["payment_method"] == "CASH":
        t = TicketRequest(
            user=request.user,
            seller=Seller.objects.get(user=request.user),
            event=event,
            context=request.POST["context"],
            q_tickets=int(request.POST["q_tickets"]),
            reference=request.POST["reference"],
            client=request.POST["client"],
            fase=fase,
            total=totalp,
            payment_method=request.POST["payment_method"],
            cash_pay = False)
        return t

def log_websocket(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:

        if request.user.has_perm("users.can_view_admin") or request.user.has_perm("users.can_view_staff") :

            return render(request, 'oldcore/log_websocket.html', {
                'room_name': room_name
            })
        else:
            return HttpResponseRedirect(reverse("main:home"))


def cashpaytoggle(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)
        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:
            r = get_object_or_404(TicketRequest, id=id)
            if r.cash_pay == False:
                r.cash_pay = True
                r.save()
            else:
                r.cash_pay = False
                r.save()
            return HttpResponseRedirect(reverse("oldcore:cash_index"))
        else:
            return HttpResponseRedirect(reverse("main:home"))

def cash_index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    elif not checkCoreAccess(request.user):
        return HttpResponseRedirect(reverse("main:home"))

    else:
        checkSeller(request.user)

        requests = TicketRequest.objects.filter(payment_method="CASH")

        if getCoreRole(request.user) == 6 or getCoreRole(request.user) == 5:
            return render(request, 'oldcore/cash/cash_index.html', {
                "requests": requests
            })
        else:
            return HttpResponseRedirect(reverse("main:home"))


    