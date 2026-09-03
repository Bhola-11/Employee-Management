import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import HelpdeskTicket, TicketComment, TicketCategory
from .forms import HelpdeskTicketForm, TicketCommentForm

@login_required
def helpdesk_dashboard_view(request):
    org = request.tenant_org
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    
    my_tickets = []
    if employee:
        my_tickets = HelpdeskTicket.objects.filter(employee=employee).select_related('category')
        
    all_tickets = HelpdeskTicket.objects.filter(organization=org).select_related('category', 'employee', 'assigned_to')[:20]
    return render(request, 'helpdesk/dashboard.html', {
        'my_tickets': my_tickets,
        'all_tickets': all_tickets,
        'employee': employee
    })

@login_required
def ticket_create_view(request):
    org = request.tenant_org
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        messages.error(request, "Employee profile required to raise helpdesk tickets.")
        return redirect('helpdesk:dashboard')
        
    if request.method == 'POST':
        form = HelpdeskTicketForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.organization = org
            ticket.employee = employee
            ticket.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
            ticket.save()
            messages.success(request, f"Helpdesk Ticket #{ticket.ticket_number} created.")
            return redirect('helpdesk:ticket_detail', ticket.id)
    else:
        form = HelpdeskTicketForm(organization=org)
    return render(request, 'helpdesk/ticket_form.html', {'form': form, 'title': 'Create Support Ticket'})

@login_required
def ticket_detail_view(request, ticket_id):
    org = request.tenant_org
    ticket = get_object_or_404(HelpdeskTicket, id=ticket_id, organization=org)
    comments = ticket.comments.select_related('author').all()
    
    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.ticket = ticket
            c.author = request.user
            c.save()
            messages.success(request, "Response posted to ticket.")
            return redirect('helpdesk:ticket_detail', ticket.id)
    else:
        comment_form = TicketCommentForm()
        
    return render(request, 'helpdesk/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form
    })
