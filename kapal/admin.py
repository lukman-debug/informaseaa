from django.contrib import admin
from .models import Kapal

@admin.register(Kapal)
class KapalAdmin(admin.ModelAdmin):
    list_display = ('nama_kapal', 'nomor_registrasi', 'jenis_kapal', 'pemilik', 'pelabuhan_asal', 'get_dokumen_count', 'created_at')
    list_filter = ('jenis_kapal', 'tahun_pembuatan', 'created_at')
    search_fields = ('nama_kapal', 'nomor_registrasi', 'pemilik', 'pelabuhan_asal')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama_kapal', 'nomor_registrasi', 'jenis_kapal', 'ukuran_kapal', 'tahun_pembuatan')
        }),
        ('Kepemilikan', {
            'fields': ('pemilik', 'pelabuhan_asal')
        }),
        ('Dokumen', {
            'fields': ('dokumen',)
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_dokumen_count(self, obj):
        return obj.get_dokumen_count()
    get_dokumen_count.short_description = 'Jumlah Dokumen'
