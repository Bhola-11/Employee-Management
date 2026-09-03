from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.permissions import role_required
from .models import CompanyDocument, DocumentCategory
from .forms import CompanyDocumentForm

@login_required
def document_vault_view(request):
    org = request.tenant_org
    categories = DocumentCategory.objects.filter(organization=org)
    documents = CompanyDocument.objects.filter(organization=org).select_related('category')
    return render(request, 'documents/vault.html', {
        'categories': categories,
        'documents': documents
    })

@login_required
@role_required('SUPER_ADMIN', 'ORG_ADMIN', 'HR_MANAGER')
def document_upload_view(request):
    org = request.tenant_org
    if request.method == 'POST':
        form = CompanyDocumentForm(request.POST, request.FILES, organization=org)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.organization = org
            doc.save()
            messages.success(request, f"Document '{doc.title}' published to vault.")
            return redirect('documents:vault')
    else:
        form = CompanyDocumentForm(organization=org)
    return render(request, 'documents/upload_form.html', {'form': form, 'title': 'Publish Policy Document'})
