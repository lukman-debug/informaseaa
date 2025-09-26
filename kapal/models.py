from django.db import models
import json

class Kapal(models.Model):
    nama_kapal = models.CharField(max_length=200, verbose_name="Nama Kapal")
    nomor_registrasi = models.CharField(max_length=100, unique=True, verbose_name="Nomor Registrasi")
    jenis_kapal = models.CharField(max_length=100, verbose_name="Jenis Kapal")
    ukuran_kapal = models.CharField(max_length=50, verbose_name="Ukuran Kapal")
    tahun_pembuatan = models.IntegerField(verbose_name="Tahun Pembuatan")
    pemilik = models.CharField(max_length=200, verbose_name="Pemilik")
    pelabuhan_asal = models.CharField(max_length=200, verbose_name="Pelabuhan Asal")
    dokumen = models.JSONField(default=list, blank=True, verbose_name="Dokumen")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kapal"
        verbose_name_plural = "Kapal"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nama_kapal} ({self.nomor_registrasi})"
    
    def get_dokumen_count(self):
        """Get count of documents"""
        if isinstance(self.dokumen, list):
            return len(self.dokumen)
        return 0
    
    def has_dokumen(self):
        """Check if kapal has any documents"""
        return self.get_dokumen_count() > 0
