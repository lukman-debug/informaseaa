from django.db import models
from django.core.validators import FileExtensionValidator
import os

def kapal_document_upload_path(instance, filename):
    """Generate upload path for kapal documents"""
    return f'kapal_documents/{instance.id}_{filename}'

class Kapal(models.Model):
    """Model for ship data with document management"""
    nama_kapal = models.CharField(max_length=200, verbose_name="Nama Kapal")
    nomor_registrasi = models.CharField(max_length=100, unique=True, verbose_name="Nomor Registrasi")
    pemilik = models.CharField(max_length=200, verbose_name="Pemilik")
    jenis_kapal = models.CharField(max_length=100, verbose_name="Jenis Kapal")
    tonase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tonase (GT)")
    panjang = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Panjang (m)")
    lebar = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Lebar (m)")
    tahun_pembuatan = models.IntegerField(verbose_name="Tahun Pembuatan")
    pelabuhan_asal = models.CharField(max_length=200, verbose_name="Pelabuhan Asal")
    
    # Document field for storing document file paths/URLs
    dokumen = models.FileField(
        upload_to=kapal_document_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name="Dokumen Kapal",
        help_text="Upload dokumen kapal (PDF, JPG, PNG). Maksimal 5 MB."
    )
    
    # Additional metadata fields
    status_dokumen = models.CharField(
        max_length=20,
        choices=[
            ('lengkap', 'Lengkap'),
            ('tidak_lengkap', 'Tidak Lengkap'),
            ('dalam_proses', 'Dalam Proses'),
        ],
        default='tidak_lengkap',
        verbose_name="Status Dokumen"
    )
    
    tanggal_upload_dokumen = models.DateTimeField(null=True, blank=True, verbose_name="Tanggal Upload Dokumen")
    keterangan = models.TextField(blank=True, verbose_name="Keterangan")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kapal"
        verbose_name_plural = "Kapal"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nama_kapal} ({self.nomor_registrasi})"
    
    @property
    def has_document(self):
        """Check if kapal has a document uploaded"""
        return bool(self.dokumen and self.dokumen.name)
    
    @property
    def document_url(self):
        """Get document URL if exists"""
        if self.has_document:
            return self.dokumen.url
        return None
    
    @property
    def document_name(self):
        """Get document filename if exists"""
        if self.has_document:
            return os.path.basename(self.dokumen.name)
        return None
