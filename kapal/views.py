from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.core.files.base import ContentFile
import json
import base64
import os
from .models import Kapal

def kapal_list(request):
    """Display list of ships with search and filtering"""
    kapal_list = Kapal.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        kapal_list = kapal_list.filter(
            Q(nama_kapal__icontains=search) |
            Q(nomor_registrasi__icontains=search) |
            Q(pemilik__icontains=search) |
            Q(jenis_kapal__icontains=search)
        )
    
    # Filter by document status
    status_filter = request.GET.get('status')
    if status_filter:
        kapal_list = kapal_list.filter(status_dokumen=status_filter)
    
    # Pagination
    paginator = Paginator(kapal_list, 10)  # Show 10 ships per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # View mode (table or card)
    view_mode = request.GET.get('view', 'table')
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'view_mode': view_mode,
        'status_choices': Kapal._meta.get_field('status_dokumen').choices,
    }
    
    return render(request, 'kapal/list.html', context)

def kapal_detail(request, pk):
    """Display detailed view of a ship"""
    kapal = get_object_or_404(Kapal, pk=pk)
    
    context = {
        'kapal': kapal,
    }
    
    return render(request, 'kapal/detail.html', context)

def kapal_add(request):
    """Add new ship"""
    if request.method == 'POST':
        try:
            kapal = Kapal(
                nama_kapal=request.POST.get('nama_kapal'),
                nomor_registrasi=request.POST.get('nomor_registrasi'),
                pemilik=request.POST.get('pemilik'),
                jenis_kapal=request.POST.get('jenis_kapal'),
                tonase=request.POST.get('tonase'),
                panjang=request.POST.get('panjang'),
                lebar=request.POST.get('lebar'),
                tahun_pembuatan=request.POST.get('tahun_pembuatan'),
                pelabuhan_asal=request.POST.get('pelabuhan_asal'),
                keterangan=request.POST.get('keterangan', '')
            )
            
            # Handle document upload
            if request.FILES.get('dokumen'):
                kapal.dokumen = request.FILES['dokumen']
                kapal.status_dokumen = 'lengkap'
                kapal.tanggal_upload_dokumen = timezone.now()
            
            kapal.save()
            messages.success(request, f'Kapal {kapal.nama_kapal} berhasil ditambahkan.')
            return redirect('kapal:detail', pk=kapal.pk)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'kapal/add.html')

def kapal_edit(request, pk):
    """Edit existing ship"""
    kapal = get_object_or_404(Kapal, pk=pk)
    
    if request.method == 'POST':
        try:
            kapal.nama_kapal = request.POST.get('nama_kapal')
            kapal.nomor_registrasi = request.POST.get('nomor_registrasi')
            kapal.pemilik = request.POST.get('pemilik')
            kapal.jenis_kapal = request.POST.get('jenis_kapal')
            kapal.tonase = request.POST.get('tonase')
            kapal.panjang = request.POST.get('panjang')
            kapal.lebar = request.POST.get('lebar')
            kapal.tahun_pembuatan = request.POST.get('tahun_pembuatan')
            kapal.pelabuhan_asal = request.POST.get('pelabuhan_asal')
            kapal.keterangan = request.POST.get('keterangan', '')
            
            # Handle document upload
            if request.FILES.get('dokumen'):
                # Delete old document if exists
                if kapal.dokumen:
                    kapal.dokumen.delete()
                
                kapal.dokumen = request.FILES['dokumen']
                kapal.status_dokumen = 'lengkap'
                kapal.tanggal_upload_dokumen = timezone.now()
            
            kapal.save()
            messages.success(request, f'Kapal {kapal.nama_kapal} berhasil diperbarui.')
            return redirect('kapal:detail', pk=kapal.pk)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    context = {
        'kapal': kapal,
    }
    
    return render(request, 'kapal/edit.html', context)

def kapal_delete(request, pk):
    """Delete ship"""
    kapal = get_object_or_404(Kapal, pk=pk)
    
    if request.method == 'POST':
        # Delete associated document file
        if kapal.dokumen:
            kapal.dokumen.delete()
        
        nama = kapal.nama_kapal
        kapal.delete()
        messages.success(request, f'Kapal {nama} berhasil dihapus.')
        return redirect('kapal:list')
    
    context = {
        'kapal': kapal,
    }
    
    return render(request, 'kapal/delete.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def upload_document(request, pk):
    """Upload document for a ship"""
    kapal = get_object_or_404(Kapal, pk=pk)
    
    if request.FILES.get('document'):
        try:
            # Delete old document if exists
            if kapal.dokumen:
                kapal.dokumen.delete()
            
            kapal.dokumen = request.FILES['document']
            kapal.status_dokumen = 'lengkap'
            kapal.tanggal_upload_dokumen = timezone.now()
            kapal.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Dokumen berhasil diupload',
                'document_url': kapal.document_url,
                'document_name': kapal.document_name
            })
            
        except Exception:
            return JsonResponse({
                'success': False,
                'error': 'Terjadi kesalahan saat mengupload dokumen'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'No document provided'
    })

@csrf_exempt
@require_http_methods(["POST"])
def delete_document(request, pk):
    """Delete document for a ship"""
    kapal = get_object_or_404(Kapal, pk=pk)
    
    if kapal.dokumen:
        kapal.dokumen.delete()
        kapal.status_dokumen = 'tidak_lengkap'
        kapal.tanggal_upload_dokumen = None
        kapal.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Dokumen berhasil dihapus'
        })
    
    return JsonResponse({
        'success': False,
        'error': 'No document to delete'
    })

@csrf_exempt
@require_http_methods(["POST"])
def camera_upload(request):
    """Handle camera image upload"""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        kapal_id = data.get('kapal_id')
        
        if not image_data or not kapal_id:
            return JsonResponse({
                'success': False,
                'error': 'Missing image data or kapal ID'
            })
        
        kapal = get_object_or_404(Kapal, pk=kapal_id)
        
        # Decode base64 image
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        
        # Create file from base64 data
        image_file = ContentFile(
            base64.b64decode(imgstr),
            name=f'camera_capture_{kapal_id}.{ext}'
        )
        
        # Delete old document if exists
        if kapal.dokumen:
            kapal.dokumen.delete()
        
        kapal.dokumen = image_file
        kapal.status_dokumen = 'lengkap'
        kapal.tanggal_upload_dokumen = timezone.now()
        kapal.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Foto dari kamera berhasil disimpan',
            'document_url': kapal.document_url,
            'document_name': kapal.document_name
        })
        
    except Exception:
        return JsonResponse({
            'success': False,
            'error': 'Terjadi kesalahan saat mengupload dokumen'
        })

@csrf_exempt
@require_http_methods(["POST"])
def validate_file(request):
    """Validate uploaded file"""
    if request.FILES.get('file'):
        file = request.FILES['file']
        
        # Check file size (max 5MB)
        if file.size > 5242880:
            return JsonResponse({
                'valid': False,
                'error': 'File terlalu besar. Maksimal 5MB.'
            })
        
        # Check file extension
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            return JsonResponse({
                'valid': False,
                'error': 'Format file tidak didukung. Gunakan PDF, JPG, atau PNG.'
            })
        
        return JsonResponse({
            'valid': True,
            'file_name': file.name,
            'file_size': file.size
        })
    
    return JsonResponse({
        'valid': False,
        'error': 'No file provided'
    })
