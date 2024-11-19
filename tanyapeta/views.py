import csv
from django.shortcuts import render  # type: ignore
from django.http import JsonResponse # type: ignore
import json
import os
def index(request):

    return render(request, 'oseandata.html')


def get_spl_data(request):
    spl_data = []
    with open('static/SPL (2).csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spl_data.append(row)
    return JsonResponse(spl_data, safe=False)

def get_klorofil_data(request):
    klorofil_data = []
    with open('static/SPL (2).csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            klorofil_data.append(row)
    return JsonResponse(klorofil_data, safe=False)

def get_mangrove_data(request):
    mangrove_data = []
    with open('static/mangrove (1).csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mangrove_data.append(row)
    return JsonResponse(mangrove_data, safe=False)

def get_lamun_data(request):
    lamun_data = []
    with open('static/lamun.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lamun_data.append(row)
    return JsonResponse(lamun_data, safe=False)

def get_karang_data(request):
    karang_data = []
    with open('static/terumbu_karang.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            karang_data.append(row)
    return JsonResponse(karang_data, safe=False)


# Fungsi untuk membaca file data
def load_data():
    # Baca data SPL
    spl_data = []
    with open('static/SPL (2).csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spl_data.append(row)

    # Baca data Klorofil
    klorofil_data = []
    with open('static/Klo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            klorofil_data.append(row)

    return spl_data, klorofil_data

# Fungsi untuk menampilkan data zona tangkapan ikan
def fishing_zone(request):
    spl_data, klorofil_data = load_data()

    # Gabungkan data SPL dan Klorofil berdasarkan latitude dan longitude
    fishing_zones = []
    for spl in spl_data:
        for chla in klorofil_data:
            if spl['latitude'] == chla['latitude'] and spl['longitude'] == chla['longitude']:
                # Logika untuk menentukan zona tangkapan ikan
                if 26 <= float(spl['spl']) <= 30 and 0.5 <= float(chla['chla']) <= 2.0:
                    fishing_zones.append({
                        "latitude": spl['latitude'],
                        "longitude": spl['longitude'],
                        "spl": spl['spl'],
                        "chla": chla['chla']
                    })

    return JsonResponse(fishing_zones, safe=False)
