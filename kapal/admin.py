from django.contrib import admin
from .models import Kapal

@admin.register(Kapal)
class KapalAdmin(admin.ModelAdmin):
    list_display = ['nama_kapal', 'nomor_registrasi', 'pemilik', 'jenis_kapal', 'status_dokumen', 'has_document', 'created_at']
    list_filter = ['status_dokumen', 'jenis_kapal', 'created_at']
    search_fields = ['nama_kapal', 'nomor_registrasi', 'pemilik']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Kapal', {
            'fields': ('nama_kapal', 'nomor_registrasi', 'pemilik', 'jenis_kapal')
        }),
        ('Spesifikasi Teknis', {
            'fields': ('tonase', 'panjang', 'lebar', 'tahun_pembuatan', 'pelabuhan_asal')
        }),
        ('Dokumen', {
            'fields': ('dokumen', 'status_dokumen', 'tanggal_upload_dokumen')
        }),
        ('Keterangan', {
            'fields': ('keterangan',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
