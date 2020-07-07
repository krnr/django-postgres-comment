from django.http.response import JsonResponse
from .models import Ticket


def all_tickets(request):
    qs = Ticket.objects.all().set_label("count all tickets")
    total = qs.count()
    return JsonResponse({"total": total})
