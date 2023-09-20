import base64, binascii, zlib
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from types import NoneType
from itertools import groupby
import time
import math
from urllib.parse import unquote
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Location, Kalip, Hareket, KalipMs, DiesLocation, PresUretimRaporu, SiparisList, EkSiparis
from django.template import loader
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required, permission_required
from guardian.shortcuts import get_objects_for_user
from django.db.models import Q, Sum, Max, Count, Case, When, ExpressionWrapper, fields, OuterRef, Subquery
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction 
from aes_cipher import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import locale

# Create your views here.


locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

class IndexView(generic.TemplateView):
    template_name = 'ArslanTakipApp/index.html'

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

def calculate_pagination(page, size):
    offset = (page - 1) * size
    limit = page * size
    return (offset, limit)

def compare(s, t):
    return sorted(s) == sorted(t)

def guncelle(i, b, u):
    for j in b:
        if i == 'KalipNo':
            k = KalipMs.objects.using('dies').get(KalipNo = j[0])
            kalip = Kalip()
            kalip.KalipNo = k.KalipNo
            kalip.ProfilNo = k.ProfilNo
            kalip.Kimlik = k.Kimlik
            kalip.FirmaKodu = k.FirmaKodu
            kalip.FirmaAdi = k.FirmaAdi
            kalip.Cinsi = k.Cinsi
            kalip.Miktar = k.Miktar
            kalip.Capi = k.Capi
            kalip.UretimTarihi = k.UretimTarihi
            kalip.GozAdedi = k.GozAdedi
            kalip.Silindi = k.Silindi
            kalip.SilinmeSebebi =k.SilinmeSebebi
            kalip.Bolster = k.Bolster
            kalip.KalipCevresi = k.KalipCevresi
            kalip.KaliteOkey = k.KaliteOkey
            kalip.UreticiFirma = k.UreticiFirma
            kalip.TeniferOmruMt = k.TeniferOmruMt
            kalip.TeniferOmruKg = k.TeniferOmruKg
            kalip.TeniferKalanOmurKg = k.TeniferKalanOmurKg
            kalip.TeniferNo = k.TeniferNo
            kalip.SonTeniferTarih = k.SonTeniferTarih
            kalip.SonTeniferKg = k.SonTeniferKg
            kalip.SonTeniferSebebi = k.SonTeniferSebebi
            kalip.SonUretimTarih = k.SonUretimTarih
            kalip.SonUretimGr = k.SonUretimGr
            kalip.UretimTenSonrasiKg = k.UretimTenSonrasiKg
            kalip.UretimToplamKg = k.UretimToplamKg
            kalip.ResimGramaj = k.ResimGramaj
            kalip.KalipAciklama = k.KalipAciklama
            kalip.SikayetVar = k.SikayetVar
            kalip.KaliteAciklama = k.KaliteAciklama
            kalip.AktifPasif = k.AktifPasif
            kalip.Hatali = k.Hatali
            kalip.PresKodu  = k.PresKodu
            kalip.PaketBoyu = k.PaketBoyu
            kalip.ResimDizini = k.ResimDizini
            kalip.kalipLocation_id = 48
            
            kalip.save()
            print("kalip saved")
        else:
            print(i)
            u[i] = j[1]
            Kalip.objects.filter(KalipNo = j[0]).update(**u)
            print("updated")
    return True

@login_required #user must be logged in
#@permission_required("ArslanTakipApp.view_location") #izin yoksa login sayfasına yönlendiriyor
def location(request):
    loc = get_objects_for_user(request.user, "ArslanTakipApp.dg_view_location", klass=Location) #Location.objects.all() 
    loc_list = list(loc.values().order_by('id'))

    # Create a dictionary for O(1) lookups
    loc_dict = {item['id']: item for item in loc_list}
    root_nodes = []

    for item in loc_list:
        parent_id = item['locationRelationID_id']
        if parent_id:
            parent = loc_dict.get(parent_id)
            if parent:
                parent.setdefault('_children', []).append(item)
        else:
            root_nodes.append(item)

    data = json.dumps(root_nodes)
    gonderData = location_list(request.user)

    """ loc_list_rev = list(reversed(loc_list))
    for item in loc_list_rev:
        for i in loc_list:
            if item['locationRelationID_id'] == i['id']:
                try:
                    i['_children'].append(item)
                except:
                    i['_children'] = [item]
                loc_list.remove(item)

    childData = loc_list
    gonderData = location_list(request.user) """

    if request.method == "POST":
        dieList = request.POST.get("dieList")
        dieList = dieList.split(",")
        dieTo = request.POST.get("dieTo")
        lRec = Location.objects.get(id = dieTo)
        for i in dieList:
            k = DiesLocation.objects.get(kalipNo = i)
            if k.kalipVaris.id != lRec.id:
                hareket = Hareket()
                hareket.kalipKonum_id = k.kalipVaris.id
                hareket.kalipVaris_id = dieTo
                hareket.kalipNo = i
                hareket.kimTarafindan_id = request.user.id
                hareket.save()
                print("Hareket saved")
            else:
                print("Hareket not saved")
                
    #data = json.dumps(childData)
    return render(request, 'ArslanTakipApp/location.html', {'location_json':data, 'gonder_json':gonderData})

def location_list(a):
    gonderLoc = get_objects_for_user(a, "ArslanTakipApp.gonder_view_location", klass=Location)
    gonderLoc_list = list(gonderLoc.values().order_by('id'))

    gonder_dict = {item['id']: item for item in gonderLoc_list}
    root_nodes = []

    for item in gonderLoc_list:
        parent_id = item['locationRelationID_id']
        if parent_id:
            parent = gonder_dict.get(parent_id)
            if parent:
                parent.setdefault('_children', []).append(item)
        else:
            root_nodes.append(item)

    childData = root_nodes
    data = json.dumps(childData)
    return data

    """ gonderLoc = get_objects_for_user(a, "ArslanTakipApp.gonder_view_location", klass=Location)
    gonderLoc_list = list(gonderLoc.values().order_by('id'))
    gonderLoc_list_rev = list(reversed(gonderLoc_list))
    for item in gonderLoc_list_rev:
        for i in gonderLoc_list:
            if item['locationRelationID_id'] == i['id']:
                try:
                    i['_children'].append(item)
                except:
                    i['_children'] = [item]
                gonderLoc_list.remove(item)

    childData = gonderLoc_list
    data = json.dumps(childData)
    return data """

def kalip_liste(request):
    #Kalıp Listesi Detaylı
    params = json.loads(unquote(request.GET.get('params')))
    for i in params:
        value = params[i]
        #print("Key and Value pair are ({}) = ({})".format(i, value))
    size = params["size"]
    page = params["page"]
    offset, limit = calculate_pagination(page, size)
    filter_list = params["filter"]
    query = KalipMs.objects.using('dies').all()
    location_list = Location.objects.values()
    q = {} 
    
    if len(filter_list)>0:
        for i in filter_list:
            if i['field'] != 'ProfilNo':
                if i["type"] == "like":
                    q[i['field']+"__startswith"] = i['value']
                elif i["type"] == "=":
                    if i['field'] == 'AktifPasif':
                        if i['value'] == True:
                            i['value'] = 'Aktif'
                        else: i['value'] = 'Pasif'
                    q[i['field']] = i['value']
            else:
                q[i['field']] = i['value']
    
    query = query.filter(**q).order_by('-UretimTarihi') 

    g = list(query.values()[offset:limit])

    for c in g:
        if c['UretimTarihi'] != None:
            c['UretimTarihi'] = c['UretimTarihi'].strftime("%d-%m-%Y")
            c['SonTeniferTarih'] =c['SonTeniferTarih'].strftime("%d-%m-%Y %H:%M:%S")
            c['SonUretimTarih'] =c['SonUretimTarih'].strftime("%d-%m-%Y")
        if c['AktifPasif'] == "Aktif":
            c['AktifPasif'] = True
        elif c['AktifPasif'] == "Pasif":
            c['AktifPasif'] = False
        if c['Hatali'] == 1:
            c['Hatali'] = 0
        elif c['Hatali'] == 0:
            c['Hatali'] = 1
        try: 
            b = DiesLocation.objects.get(kalipNo = c['KalipNo']).kalipVaris_id
        except:
            b = 48
            hareket = Hareket()
            hareket.kalipVaris_id = 48
            hareket.kalipNo = c['KalipNo']
            hareket.kimTarafindan_id = 1
            hareket.save()
            print("Hareket saved")
        #print(b)
        try:
            c['kalipLocation'] = list(location_list.filter(id=list(location_list.filter(id=b))[0]["locationRelationID_id"]))[0]["locationName"] + " <BR>└ " + list(location_list.filter(id=b))[0]["locationName"]
        except:
            try:
                c['kalipLocation'] = list(location_list.filter(id=b))[0]["locationName"]
            except:
                c['kalipLocation'] = ""
        #print(c)
    kalip_count = query.count()
    lastData= {'last_page': math.ceil(kalip_count/size), 'data': []}
    lastData['data'] = g
    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def kalip_rapor(request):
    params = json.loads(unquote(request.GET.get('params')))
    for i in params:
        value = params[i]
        print("Key and Value pair are ({}) = ({})".format(i, value))
    size = params["size"]
    page = params["page"]
    offset, limit = calculate_pagination(page, size)
    filter_list = params["filter"]
    q = {} 
    kalip_count = 0
    lastData= {'last_page': math.ceil(kalip_count/size), 'data': []}

    if len(filter_list)>0:
        print(filter_list)
        for i in filter_list:
            if i["type"] == "like":
                q[i['field']+"__startswith"] = i['value']
            elif i["type"] == "=":
                q[i['field']] = i['value']
    
        query = PresUretimRaporu.objects.using('dies').all()
        query = query.filter(**q).order_by('-Tarih') 

        g = list(query.values()[offset:limit])
        for c in g:
            if c['Tarih'] != None:
                c['Tarih'] = c['Tarih'].strftime("%d-%m-%Y") + " <BR>└ " + c['BaslamaSaati'].strftime("%H:%M") + " - " + c['BitisSaati'].strftime("%H:%M")
                c['BaslamaSaati'] =c['BaslamaSaati'].strftime("%H:%M")
                c['BitisSaati'] =c['BitisSaati'].strftime("%H:%M")
            #print(c)
        kalip_count = query.count()
        lastData= {'last_page': math.ceil(kalip_count/size), 'data': []}
        lastData['data'] = g

    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)

#gelen id başka konumların parenti ise altındakileri listele??
def location_hareket(request):
    params = json.loads(unquote(request.GET.get('params')))
    size = params["size"]
    page = params["page"]
    filter_list = params["filter"]

    hareket_count = 0
    lastData= {'last_page': math.ceil(hareket_count/size), 'data': []}

    if len(filter_list)>0:
        hareketK = filter_list[0]['value']
        hareketQuery = Hareket.objects.all()
        location_list = Location.objects.values()
        hareketQuery = list(hareketQuery.values().filter(kalipNo=hareketK))
        kalip_l = list(DiesLocation.objects.filter(kalipNo=hareketK).values())
        users = User.objects.values()
        harAr = []
        for h in hareketQuery:
            har ={}
            har['id'] = h['id']
            har['kalipNo'] = kalip_l[0]['kalipNo']
            try:
                har['kalipKonum'] =list(location_list.filter(id=list(location_list.filter(id=h['kalipKonum_id']))[0]["locationRelationID_id"]))[0]["locationName"] + " <BR>└ " + list(location_list.filter(id=h['kalipKonum_id']))[0]["locationName"]
            except:
                try:
                    har['kalipKonum'] = list(location_list.filter(id=h['kalipKonum_id']))[0]["locationName"]
                except:
                    har['kalipKonum'] = ""
            try:
                har['kalipVaris'] =list(location_list.filter(id=list(location_list.filter(id=h['kalipVaris_id']))[0]["locationRelationID_id"]))[0]["locationName"] + " <BR>└ " + list(location_list.filter(id=h['kalipVaris_id']))[0]["locationName"]
            except:
                har['kalipVaris'] = list(location_list.filter(id=h['kalipVaris_id']))[0]["locationName"]
            har['kimTarafindan'] = list(users.filter(id=int(h['kimTarafindan_id'])))[0]["first_name"] + " " + list(users.filter(id=int(h['kimTarafindan_id'])))[0]["last_name"] 
            har['hareketTarihi'] = h['hareketTarihi'].strftime("%d-%m-%Y %H:%M:%S")
            harAr.append(har)
        hareket_count = len(harAr)

        lastData= {'last_page': math.ceil(hareket_count/size), 'data': []}
        lastData['data'] = list(harAr[(page-1)*size:page*size])
                
    #print(lastData)
    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def kalip(request):
    """ with transaction.atomic():
        listFields = {'AktifPasif', 'Silindi',  'Hatali', 'KalipNo', 'SilinmeSebebi', 'TeniferKalanOmurKg', 'KaliteOkey', 'TeniferOmruMt', 'TeniferOmruKg', 'TeniferNo', 'SonTeniferTarih', 
                        'SonTeniferKg', 'SonTeniferSebebi', 'SonUretimTarih', 'SonUretimGr', 'UretimTenSonrasiKg', 'UretimToplamKg', 'KalipAciklama', 'SikayetVar', 'KaliteAciklama', 
                        'PresKodu', 'PaketBoyu'}
        for i in listFields:
            print(i)
            u = {}
            rows1 = list(KalipMs.objects.using('dies').order_by('-KalipNo').values_list('KalipNo', i))
            rows2 = list(Kalip.objects.order_by('-KalipNo').values_list('KalipNo', i))
            a = compare(rows1,rows2)
            if a == False:
                print (a)
                b= set(rows1) - set(rows2)
                #print (b)
                #guncelle(i,b,u)
                for j in b:
                    print(j[0])
                    if i == 'KalipNo':
                        k = KalipMs.objects.using('dies').get(KalipNo = j[0])
                        print(k.ProfilNo)
                        kalip = Kalip()
                        kalip.KalipNo = k.KalipNo
                        kalip.ProfilNo = k.ProfilNo
                        kalip.Kimlik = k.Kimlik
                        kalip.FirmaKodu = k.FirmaKodu
                        kalip.FirmaAdi = k.FirmaAdi
                        kalip.Cinsi = k.Cinsi
                        kalip.Miktar = k.Miktar
                        kalip.Capi = k.Capi
                        kalip.UretimTarihi = k.UretimTarihi
                        kalip.GozAdedi = k.GozAdedi
                        kalip.Silindi = k.Silindi
                        kalip.SilinmeSebebi =k.SilinmeSebebi
                        kalip.Bolster = k.Bolster
                        kalip.KalipCevresi = k.KalipCevresi
                        kalip.KaliteOkey = k.KaliteOkey
                        kalip.UreticiFirma = k.UreticiFirma
                        kalip.TeniferOmruMt = k.TeniferOmruMt
                        kalip.TeniferOmruKg = k.TeniferOmruKg
                        kalip.TeniferKalanOmurKg = k.TeniferKalanOmurKg
                        kalip.TeniferNo = k.TeniferNo
                        kalip.SonTeniferTarih = k.SonTeniferTarih
                        kalip.SonTeniferKg = k.SonTeniferKg
                        kalip.SonTeniferSebebi = k.SonTeniferSebebi
                        kalip.SonUretimTarih = k.SonUretimTarih
                        kalip.SonUretimGr = k.SonUretimGr
                        kalip.UretimTenSonrasiKg = k.UretimTenSonrasiKg
                        kalip.UretimToplamKg = k.UretimToplamKg
                        kalip.ResimGramaj = k.ResimGramaj
                        kalip.KalipAciklama = k.KalipAciklama
                        kalip.SikayetVar = k.SikayetVar
                        kalip.KaliteAciklama = k.KaliteAciklama
                        kalip.AktifPasif = k.AktifPasif
                        kalip.Hatali = k.Hatali
                        kalip.PresKodu  = k.PresKodu
                        kalip.PaketBoyu = k.PaketBoyu
                        kalip.ResimDizini = k.ResimDizini
                        kalip.kalipLocation_id = 48
                        
                        kalip.save()
                        print("kalip saved")
                    else:
                        print(i)
                        u[i] = j[1]
                        Kalip.objects.filter(KalipNo = j[0]).update(**u) """
                        #print("updated")
    return render(request, 'ArslanTakipApp/kalip.html')

class KalipView(generic.TemplateView):
    template_name = 'ArslanTakipApp/kalip.html'

def location_kalip(request):
    #kalıp arşivi sayfasındaki kalıplar
    if request.method == "GET":
        path = request.get_full_path()
        print(path)
        params = json.loads(unquote(request.GET.get('params')))
        for i in params:
            value = params[i]
            print("Key and Value pair are ({}) = ({})".format(i, value))
        size = params["size"]
        page = params["page"]
        filter_list = params["filter"]
        q = {}

        loc = get_objects_for_user(request.user, "ArslanTakipApp.dg_view_location", klass=Location) #Location.objects.all() 
        loc_list = list(loc.values())
        locs = [l['id'] for l in loc_list]
        query = DiesLocation.objects.filter(kalipVaris_id__in = locs).order_by('kalipNo')
        lfil =[]
        if request.user.is_superuser:
            query = DiesLocation.objects.all().order_by('kalipNo')
        
        if len(filter_list)>0:
            for i in filter_list:
                if i["type"] == "like":
                    q[i['field']+"__startswith"] = i['value']
                elif i["type"] == "=":
                    #q[i['field']] = i['value']
                    loca = loc.values().get(id = i['value'])
                    if loca['isPhysical']: 
                        q[i['field']] = i['value']
                    else :
                        lo = loc.values().filter(locationRelationID_id = i['value'])
                        for j in list(lo):
                            if j['isPhysical']:
                                lfil.append(j['id'])
                            else:
                                filo = loc.values().filter(locationRelationID_id = j['id'])
                                for f in list(filo):
                                    if f['isPhysical']:
                                        lfil.append(f['id'])
                                    else :
                                        filo2 = loc.values().filter(locationRelationID_id = f['id'])
                                        #print(filo2)
                                        for b in list(filo2):
                                            if b['isPhysical']:
                                                lfil.append(b['id'])
                        #print(lfil)
                        query = DiesLocation.objects.filter(kalipVaris_id__in=lfil)

        query = query.filter(**q) 
        kal = KalipMs.objects.using('dies').all()
        a = list(query.values()[(page-1)*size:page*size])
        for b in a:
            s = kal.get(KalipNo=b['kalipNo'])
            if s.Silindi == 1 or s.AktifPasif == 'Pasif':
                #print(b)
                a.remove(b)
                #print("silindi")
            c = kal.get(KalipNo=b['kalipNo']).Hatali
            if c==1:
                b['Hatali'] = 1
        #print(a)
        kalip_count = query.count()
        lastData= {'last_page': math.ceil(kalip_count/size), 'data': []}
        lastData['data'] = a #list(query.values()[(page-1)*size:page*size])
        data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        return HttpResponse(data)


key = b'arslandenemebyz1'

def encrypt_aes_ecb(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def decrypt_aes_ecb(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode('utf-8')

def qrKalite(request):
    if request.method == "GET":
        print("qr sayfası")
        """ path = request.get_full_path()
        print(path)
        print(path.rsplit('/', 1)[-1]) """

        # Şifre çözme
        unhexli = binascii.unhexlify('b23d7cad6447841b177fe5610114b374')
        print(unhexli)
        decrypted_text = decrypt_aes_ecb(key, unhexli)
        print("Çözülmüş Veri:", decrypted_text)        

        ty = request.GET.get('type', '')
        no = request.GET.get('no', '')
        print(ty + " " + no)
        
        context = {
            "type" : unhexli,
            "no" : decrypted_text,
        }

        """ olmayan = []
        notsaved = []
        query = KalipMs.objects.using('dies').all() #['SIRA 5','11497'], ['SIRA 6','402-3'], ['SIRA 8','12773-3'],['SIRA 9','4405-31'],['SIRA 9','4471-33'],
        sira1 = [
                 ]
        for i in sira1:
            try:
                print(i[1])
                a = list(KalipMs.objects.using('dies').filter(KalipNo__startswith = i[1]).values())
                if not a:
                    olmayan.append(i)
                for j in a:
                    kno = j['KalipNo']
                    if kno.strip()==i[1]:
                        if DiesLocation.objects.get(kalipNo = kno).kalipVaris_id != Location.objects.get(locationName = i[0]).id:
                            hareket = Hareket()
                            print(kno+'if ici')
                            hareket.kalipKonum_id = DiesLocation.objects.get(kalipNo = kno).kalipVaris_id
                            #print(DiesLocation.objects.get(kalipNo = kno).kalipVaris_id)
                            hareket.kalipVaris_id = Location.objects.get(locationName = i[0]).id
                            #print(hareket.kalipVaris_id)
                            hareket.kalipNo = query.get(KalipNo = kno).KalipNo
                            hareket.kimTarafindan_id = request.user.id
                            hareket.save()
                            print("Hareket saved")
                            print()
            except:
                print(KalipMs.objects.using('dies').get(KalipNo = i[1]).KalipNo)
                notsaved.append(i)
                print("Hareket not saved")
    
    print(olmayan)
    print(notsaved) """
    return render(request, 'ArslanTakipApp/qrKalite.html', context)

class qrKaliteView(generic.TemplateView):
    template_name = 'ArslanTakipApp/qrKalite.html'


class HareketView(generic.TemplateView):
    template_name = 'ArslanTakipApp/hareket.html'

def qrDeneme(request):
    return

class SiparisView(generic.TemplateView):
    template_name = 'ArslanTakipApp/siparisList.html'


    
# Helper function for aggregation and formatting
def aggregate_and_format(queryset, field):
    max_val = math.ceil(queryset.aggregate(Max(field))[f'{field}__max'])
    return locale.format_string("%.0f", max_val, grouping=True)

def aggregate_multiple_and_format(queryset, fields):
    annotations = {f"{field}__max": Max(field) for field in fields}
    aggregated = queryset.aggregate(**annotations)
    
    formatted = {}
    for field in fields:
        max_key = f"{field}__max"
        max_val = math.ceil(aggregated[max_key])
        formatted[field] = locale.format_string("%.0f", max_val, grouping=True)
        
    return formatted
# Helper function for annotation and initial query
def annotate_siparis():
    return SiparisList.objects.using('dies').filter(Q(Adet__gt=0) & ((Q(KartAktif=1) | Q(BulunduguYer='DEPO')) & Q(Adet__gte=1)) & Q(BulunduguYer='TESTERE')
                                                 ).annotate(
    TopTenKg=Subquery(
        KalipMs.objects.using('dies').filter(
            ProfilNo=OuterRef('ProfilNo'),
            AktifPasif='Aktif',
            Hatali=0,
            TeniferKalanOmurKg__gte=0
        ).values('ProfilNo').annotate(
            total=Sum('TeniferKalanOmurKg')
        ).values('total')[:1]
    ),
    AktifKalipSayisi=Subquery(
        KalipMs.objects.using('dies').filter(
            ProfilNo=OuterRef('ProfilNo'),
            AktifPasif='Aktif',
            Hatali=0,
            TeniferKalanOmurKg__gte=0
        ).values('ProfilNo').annotate(
            cnt=Count('*')
        ).values('cnt')[:1]
    ),
    ToplamKalipSayisi=Subquery(
        KalipMs.objects.using('dies').filter(
            ProfilNo=OuterRef('ProfilNo'),
            AktifPasif='Aktif',
            Hatali=0
        ).values('ProfilNo').annotate(
            cnt=Count('*')
        ).values('cnt')[:1]
    )
    )

def format_item(a):
    #append to the end of the tuple
    #a[20] girenkg, 21 kalankg, 22 sontermin, 23 topten
    ttk = 0
    if a[15]: #aktifkalipsayısı
        ttk = math.ceil(a[14])
    b = (locale.format_string("%.0f", math.ceil(a[3]), grouping=True), 
            locale.format_string("%.0f", math.ceil(a[5]), grouping=True),
            a[12].strftime("%d-%m-%Y"),
            locale.format_string("%.0f", ttk, grouping=True))
    a += b
    return a
    
    """ ttk = 0
    if a['AktifKalipSayisi']:
        ttk = math.ceil(a['TopTenKg'])
    a['SonTermin'] = a['SonTermin'].strftime("%d-%m-%Y")
    a['GirenKg'] = locale.format_string("%.0f", math.ceil(a["GirenKg"]), grouping=True)
    a['Kg'] = locale.format_string("%.0f", math.ceil(a["Kg"]), grouping=True)
    a['TopTenKg'] = locale.format_string("%.0f", ttk, grouping=True)
    return a """

def aggregate_in_parallel(queryset, fields):
    with ThreadPoolExecutor() as executor:
        future_to_field = {executor.submit(aggregate_and_format, queryset, field): field for field in fields}
        return {future_to_field[future]: future.result() for future in concurrent.futures.as_completed(future_to_field)}

def apply_filters(s, filter_list):
    q = {}
    exclude_conditions = {}

    for i in filter_list:
        field = i['field']
        value = i['value']
        filter_type = i['type']

        if field == 'TopTenKg':
            q["ProfilNo__in"] = siparis_TopTenFiltre(i)
        elif filter_type == 'like':
            q[field + "__startswith" if field != 'FirmaAdi' else field + "__contains"] = value
        elif filter_type == '=':
            condition = handle_siparis_tamam_filter(field, value)
            if condition:
                if condition[0] == 'exclude':
                    exclude_conditions[condition[1]] = condition[2]
                else:
                    q[condition[0]] = condition[1]
        elif filter_type != value:
            q[field + "__gte"] = filter_type
            q[field + "__lt"] = value
        else:
            q[field] = value

    return (q, exclude_conditions)

def handle_siparis_tamam_filter(field, value):
    if field == 'SiparisTamam':
        if value == 'BLOKE':
            return (field, value)
        elif value == 'degil':
            return ('exclude', field, 'BLOKE')
    else:
        return (field, value)

def siparis_list(request):
    #validation for when params is missing or malformatted
    params = json.loads(unquote(request.GET.get('params', '{}')))
    for i in params:
        value = params[i]
        print("Key and Value pair are ({}) = ({})".format(i, value))
    size = params.get("size", 10)  # Default size to 10
    offset, limit = calculate_pagination(params.get("page", 1), size)
    filter_list = params.get("filter", [])
    sorter_List = params.get("sL", [])
    hesap = params.get("h", {})
    
    # Step 1: Initial Query and Annotation
    s = annotate_siparis()
    
    q={}
    e ={}

    if len(filter_list)>0:
        q, exclude_cond = apply_filters(s, filter_list)
        if exclude_cond:
            s = s.exclude(**exclude_cond)

        s = s.filter(**q).order_by('-SonTermin')
    else:
        s = s.exclude(SiparisTamam='BLOKE')

    sor =[]
    if len(sorter_List)>0:
        for j in sorter_List:
            if j['field'] != 'TopTenKg':
                if j['type'] == 'Azalan':
                    sor.append( "-"+j['field'])
                else: sor.append(j['field'])
            else: 
                if j['type'] == 'Azalan':
                    sor.append( "-TopTenKg")
                else: sor.append("TopTenKg")
        s = s.order_by(*sor)
    else: s= s.order_by('-SonTermin')

    e['TopTenSum'] = ""

    if hesap == 1:
        TenVList = list(s.values_list('TopTenKg',flat=True).order_by('-TopTenKg'))
        out = [sum(g) for t, g in groupby(TenVList, type)if t is not NoneType]
        e['TopTenSum'] =locale.format_string("%.0f", math.ceil(out[0]), grouping=True)
    
    sval = s.values('KartNo','ProfilNo','FirmaAdi', 'GirenKg', 'GirenAdet', 'Kg', 'Adet', 'PlanlananMm', 'Siparismm', 'KondusyonTuru', 'PresKodu','SiparisTamam','SonTermin','BilletTuru', 'TopTenKg', 'AktifKalipSayisi', 'ToplamKalipSayisi', 'Kimlik', 'Profil_Gramaj')[offset:limit]
    svalueslist = s.values_list('KartNo','ProfilNo','FirmaAdi', 'GirenKg', 'GirenAdet', 'Kg', 'Adet', 'PlanlananMm', 'Siparismm', 'KondusyonTuru', 'PresKodu','SiparisTamam','SonTermin','BilletTuru', 'TopTenKg', 'AktifKalipSayisi', 'ToplamKalipSayisi', 'Kimlik', 'Profil_Gramaj')[offset:limit]

    with ThreadPoolExecutor() as executor:
        svalueslist = list(executor.map(format_item, svalueslist))

    sip_count = s.count()
    lastData= {'last_page': math.ceil(sip_count/size), 'data': [], 'e':e}
    lastData['data'] = svalueslist
    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def siparis_TopTenFiltre(i):
    sProfil = list(SiparisList.objects.using('dies').filter(Q(Adet__gt=0) & ((Q(KartAktif=1) | Q(BulunduguYer='DEPO')) & Q(Adet__gte=1)) & Q(BulunduguYer='TESTERE')).values_list('ProfilNo', flat=True).distinct())
    k= KalipMs.objects.using('dies').filter(ProfilNo__in = sProfil, AktifPasif="Aktif", Hatali=0)
    kal = k.values('ProfilNo').filter(TeniferKalanOmurKg__gte = 0).annotate(pcount=Sum('TeniferKalanOmurKg'))
    kPList = set(list(kal.values_list('ProfilNo', flat=True).distinct()))
    if i['type'] != i['value']:
        profilList = list(kal.filter(pcount__gte = i['type'], pcount__lt = i['value']).values_list('ProfilNo', flat=True))
    else: profilList = list(kal.filter(pcount__gte = i['type']-1, pcount__lt = i['value']+1).values_list('ProfilNo', flat=True))
    diff = [x for x in sProfil if x not in kPList]
    if len(diff)>0 :
        profilList += diff #azalan sıralarken böyle artan sıralarken diff +=profilList return diff
    
    return profilList

def siparis_max(request):
    params = json.loads(unquote(request.GET.get('params', '{}')))
    filter_list = params.get("filter", [])

    base_s = SiparisList.objects.using('dies').filter(Q(Adet__gt=0) & ((Q(KartAktif=1) | Q(BulunduguYer='DEPO')) & Q(Adet__gte=1)) & Q(BulunduguYer='TESTERE'))
    k= KalipMs.objects.using('dies').filter(TeniferKalanOmurKg__gte = 0, AktifPasif="Aktif", Hatali=0)
    
    if len(filter_list)>0:
        q, exclude_cond = apply_filters(base_s, filter_list)
        if exclude_cond:
            base_s = base_s.exclude(**exclude_cond)

        base_s = base_s.filter(**q).order_by('-SonTermin')
    else:
        base_s = base_s.exclude(SiparisTamam='BLOKE')
    
    # Perform aggregation once and access values
    aggr = base_s.aggregate(
        giren_max = Max('GirenKg'),
        kg_max = Max('Kg'),
        giren_sum = Sum('GirenKg'),
        kg_sum = Sum('Kg')
    )
    
    e = {
        'GirenMax':  locale.format_string("%.0f", math.ceil(aggr['giren_max'] or 0), grouping=True),
        'KgMax':  locale.format_string("%.0f", math.ceil(aggr['kg_max'] or 0), grouping=True),
        'GirenSum':  locale.format_string("%.0f", math.ceil(aggr['giren_sum'] or 0), grouping=True),
        'KgSum':  locale.format_string("%.0f", math.ceil(aggr['kg_sum'] or 0), grouping=True),
    }
    
    sProfil = list(base_s.values_list('ProfilNo', flat=True).distinct())
    proTop = k.filter(ProfilNo__in = sProfil).values('ProfilNo').annotate(psum = Sum('TeniferKalanOmurKg'))
    sonuc = proTop.aggregate(Max('psum'))['psum__max']
    e['TopTenMax']  = math.ceil(sonuc)
    
    return JsonResponse(e)

def siparis_child(request, pNo):
    #Kalıp Listesi Detaylı
    kalip = KalipMs.objects.using('dies').values('KalipNo','UreticiFirma', 'TeniferKalanOmurKg', 'UretimToplamKg', 'PresKodu', 'Capi')
    child = kalip.filter(ProfilNo=pNo, AktifPasif="Aktif", Hatali=0)
    location_list = Location.objects.values()
    #print()
    gonder = list(child)
    for c in gonder:
        pkodu = PresUretimRaporu.objects.using('dies').filter(KalipNo=c["KalipNo"]).order_by("-Tarih", "-BitisSaati").values("PresKodu","Tarih", "BitisSaati")
        k = DiesLocation.objects.get(kalipNo = c['KalipNo']).kalipVaris_id
        if pkodu:
            c['SonPresKodu'] = pkodu[0]['PresKodu']
        try:
            c['Konum'] = list(location_list.filter(id=list(location_list.filter(id=k))[0]["locationRelationID_id"]))[0]["locationName"] + " <BR>└ " + list(location_list.filter(id=k))[0]["locationName"]
        except:
            try:
                c['Konum'] = list(location_list.filter(id=k))[0]["locationName"]
            except:
                c['Konum'] = ""

    data = json.dumps(gonder)
    return HttpResponse(data)

def siparis_presKodu(request, pNo):
    kalip = KalipMs.objects.using('dies').values('KalipNo', 'PresKodu', 'Capi')
    child = kalip.filter(ProfilNo=pNo, AktifPasif="Aktif", Hatali=0)
    kodlar = {}
    kalipNoList = list(child.order_by().values_list('KalipNo', flat=True).distinct())

    kalipPresKodu = list(child.order_by().values_list('PresKodu', flat=True).distinct())
    uRaporuPresKodu = list(PresUretimRaporu.objects.using('dies').filter(KalipNo__in = kalipNoList).order_by().values_list('PresKodu', flat=True).distinct())
    uRaporuPresKodu = [x.strip(' ') for x in uRaporuPresKodu]

    diff = [x for x in uRaporuPresKodu if x not in kalipPresKodu]

    kodlar = kalipPresKodu + diff
    return JsonResponse(kodlar, safe=False)

def siparis_ekle(request):
    if request.method == "POST":
        print(request.POST)
        e = EkSiparis.objects.all()
        siparis = SiparisList.objects.using('dies').all()
        ekSiparis = EkSiparis()
        ekSiparis.SipKimlik = request.POST['sipKimlik']
        ekSiparis.SipKartNo = siparis.get(Kimlik = request.POST['sipKimlik']).KartNo
        ekSiparis.EkAdet = request.POST['planlananAdet']
        ekSiparis.EkPresKodu = request.POST['presKodu']
        ekSiparis.EkTermin = request.POST['ekTermin']
        ekSiparis.EkKg = request.POST['sipEkleKg']
        ekSiparis.KimTarafindan_id = request.user.id
        ekSiparis.Silindi = False
        ekSiparis.MsSilindi = False
        ekSiparis.Sira = e.count()+1

        if not e.filter(SipKartNo = ekSiparis.SipKartNo):
            ekSiparis.EkNo = 1
        else: 
            lastEk = e.filter(SipKartNo = ekSiparis.SipKartNo).order_by('EkNo').latest('EkNo')
            ekSiparis.EkNo = lastEk.EkNo +1

        ekSiparis.save()

    return HttpResponseRedirect("/siparis")

class EkSiparisView(generic.TemplateView):
    template_name = 'ArslanTakipApp/eksiparis.html'

def eksiparis_list(request):
    params = json.loads(unquote(request.GET.get('params')))
    for i in params:
        value = params[i]
        print("Key and Value pair are ({}) = ({})".format(i, value))
    size = params["size"]
    page = params["page"]
    users = User.objects.values()
    
    siparis = SiparisList.objects.using('dies').filter(Q(Adet__gt=0) & ((Q(KartAktif=1) | Q(BulunduguYer='DEPO')) & Q(Adet__gte=1)) & Q(BulunduguYer='TESTERE')).extra(
        select={
            "TopTenKg": "(SELECT SUM(TeniferKalanOmurKg) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0 AND View020_KalipListe.TeniferKalanOmurKg>= 0))",
            "AktifKalipSayisi":"(SELECT COUNT(KalipNo) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0 AND View020_KalipListe.TeniferKalanOmurKg>= 0))",
            "ToplamKalipSayisi":"(SELECT COUNT(KalipNo) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0))"
        },
    )

    ekSiparis = EkSiparis.objects.order_by("Sira").exclude(MsSilindi = True)
    ekSiparisList = list(ekSiparis.values())

    for e in ekSiparisList:
        if siparis.filter(Kimlik = e['SipKimlik']).exists() == False :
            a = ekSiparis.get(SipKimlik = e['SipKimlik'], EkNo = e['EkNo'])
            if a.MsSilindi != True:
                a.MsSilindi = True
                a.save()
            ekSiparisList.remove(e)
        else:
            siparis1 = siparis.get(Kimlik = e['SipKimlik'])
            e['EkTermin'] = e['EkTermin'].strftime("%d-%m-%Y")
            e['SipKartNo'] = str(e['SipKartNo']) + "-" +str(e['EkNo'])
            e['KimTarafindan'] = list(users.filter(id=int(e['KimTarafindan_id'])))[0]["first_name"] + " " + list(users.filter(id=int(e['KimTarafindan_id'])))[0]["last_name"] 
            if siparis1:
                e['ProfilNo'] = siparis1.ProfilNo
                e['FirmaAdi'] = siparis1.FirmaAdi
                e['GirenKg'] = siparis1.GirenKg
                e['Kg'] = siparis1.Kg
                e['GirenAdet'] = siparis1.GirenAdet
                e['Adet'] = siparis1.Adet
                e['PlanlananMm'] = siparis1.PlanlananMm
                e['Mm'] = siparis1.Siparismm
                e['KondusyonTuru'] = siparis1.KondusyonTuru
                e['SiparisTamam'] = siparis1.SiparisTamam
                e['SonTermin'] = siparis1.SonTermin.strftime("%d-%m-%Y")
                e['BilletTuru'] = siparis1.BilletTuru
                e['TopTenKg'] = siparis1.TopTenKg
            

    ek_count = ekSiparis.count()
    lastData= {'last_page': math.ceil(ek_count/size), 'data': []}
    lastData['data'] = ekSiparisList
    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)

def eksiparis_acil(request):
    siparis = SiparisList.objects.using('dies').filter(Q(Adet__gt=0) & ((Q(KartAktif=1) | Q(BulunduguYer='DEPO')) & Q(Adet__gte=1)) & Q(BulunduguYer='TESTERE')).extra(
        select={
            "TopTenKg": "(SELECT SUM(TeniferKalanOmurKg) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0 AND View020_KalipListe.TeniferKalanOmurKg>= 0))",
            "AktifKalipSayisi":"(SELECT COUNT(KalipNo) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0 AND View020_KalipListe.TeniferKalanOmurKg>= 0))",
            "ToplamKalipSayisi":"(SELECT COUNT(KalipNo) FROM View020_KalipListe WHERE (View020_KalipListe.ProfilNo = View051_ProsesDepoListesi.ProfilNo AND View020_KalipListe.AktifPasif='Aktif' AND View020_KalipListe.Hatali=0))"
        },
    )

    users = User.objects.values()
    ekSiparis = EkSiparis.objects.order_by("Sira").exclude(MsSilindi = True)
    ekSiparisList = list(ekSiparis.values())

    for e in ekSiparisList:
        if siparis.filter(Kimlik = e['SipKimlik']).exists() == False :
            a = ekSiparis.get(SipKimlik = e['SipKimlik'], EkNo = e['EkNo'])
            if a.MsSilindi != True:
                a.MsSilindi = True
                a.save()
            ekSiparisList.remove(e)
        else:
            siparis1 = siparis.get(Kimlik = e['SipKimlik'])
            e['EkTermin'] = e['EkTermin'].strftime("%d-%m-%Y")
            e['SipKartNo'] = str(e['SipKartNo']) + "-" +str(e['EkNo'])
            e['KimTarafindan'] = list(users.filter(id=int(e['KimTarafindan_id'])))[0]["first_name"] + " " + list(users.filter(id=int(e['KimTarafindan_id'])))[0]["last_name"] 
            if siparis1:
                e['ProfilNo'] = siparis1.ProfilNo
                e['FirmaAdi'] = siparis1.FirmaAdi
                e['GirenKg'] = siparis1.GirenKg
                e['Kg'] = siparis1.Kg
                e['GirenAdet'] = siparis1.GirenAdet
                e['Adet'] = siparis1.Adet
                e['PlanlananMm'] = siparis1.PlanlananMm
                e['Mm'] = siparis1.Siparismm
                e['KondusyonTuru'] = siparis1.KondusyonTuru
                e['SiparisTamam'] = siparis1.SiparisTamam
                e['SonTermin'] = siparis1.SonTermin.strftime("%d-%m-%Y")
                e['BilletTuru'] = siparis1.BilletTuru
                e['TopTenKg'] = siparis1.TopTenKg

    if request.method == "GET":
        lastData= []
        lastData = ekSiparisList
        data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        return HttpResponse(data)
    elif request.method == "POST":
        print(request.POST['fark'])
        fark = request.POST['fark']
        fark = json.loads(fark)
        print(fark)
        for f in fark:
            print(f['id'])
            ek = EkSiparis.objects.get(id=f['id'])
            ek.Sira = f['Sira']
            ek.save()
        return HttpResponseRedirect("/eksiparis")


#sayfayı açma yetkisi sadece belli kullanıcıların olsun
class KalipFirinView(PermissionRequiredMixin, generic.TemplateView):
    permission_required = "ArslanTakipApp.kalipEkran_view_location"
    template_name = 'ArslanTakipApp/kalipFirinEkrani.html'

def kalipfirini_goz(request):
    #hangi kalıp fırın giriş yapan kullanıcıya göre belirlenecek
    #şimdilik gözlerin kalıp sınırı yokmuş gibi ama daha sonra bir sınır verilecek
    #HTMLe döndürülecek data kalıp no ve fırında geçirdiği süre ya da fırına atılış zamanı
    #ona bağlı olarak kaç saat olduğu htmlde hesaplanabilir
    #fırına atıldığı süre almak daha mantıklı, kalıbın o lokasyona yapıldan hareket saati 
    if not request.user.is_superuser:
        loc = get_objects_for_user(request.user, "ArslanTakipApp.goz_view_location", klass=Location) #Location.objects.all() 
        goz_count = loc.filter(locationName__contains = ". GÖZ").count()
        #print(goz_count)

        if request.method == "GET":
            loc_list = list(loc.values())
            locs = [l['id'] for l in loc_list]
            gozKalip = DiesLocation.objects.filter(kalipVaris_id__in = locs).order_by('kalipNo')
            if gozKalip:
                gozData = list(gozKalip.values('kalipNo', 'hareketTarihi', 'kalipVaris__locationName'))
                gozData.append({'gozCount': goz_count})
                data = json.dumps(gozData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
                #print(gozData)
            else:
                gozData = [{'gozCount': goz_count}]
                data = json.dumps(gozData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
            response = JsonResponse(data, safe=False) #error döndürmedim çümkü fırınların boş olma durumu bir gerçek bir hal
            #return HttpResponse(data)
        
        elif request.method == "POST":
            #print(request.POST)
            kalipNo = request.POST['kalipNo']
            firinGoz = request.POST['firinNo'][:-5]
            #firinId = userın yetkisinin olduğu presin kalıp fırını + firingoz
            #locationName contains firinGoz şeklinde olabilir.

            gonder = loc.get(locationName__contains = firinGoz)
            gonderId = gonder.id

            firinKalipSayisi = DiesLocation.objects.filter(kalipVaris_id = gonderId).count()
            if firinKalipSayisi != 3:
                k = DiesLocation.objects.get(kalipNo = kalipNo)
                if k.kalipVaris.id != gonder:
                    hareket = Hareket()
                    hareket.kalipKonum_id = k.kalipVaris.id
                    hareket.kalipVaris_id = gonderId
                    hareket.kalipNo = kalipNo
                    hareket.kimTarafindan_id = request.user.id
                    hareket.save()
                    #print("Hareket saved")
                    response = JsonResponse({"message": "Kalıp Fırına Eklendi!"})
                else:
                    #print("Hareket not saved")
                    response = JsonResponse({"error": "Kalıp fırına gönderilemedi."})
                    response.status_code = 500 #server error
            else:
                response = JsonResponse({"error": "Fırın 3 kalıp kapasitesini doldurdu, kalıp eklenemez!"})
                response.status_code = 500

    else:
        #print("superuser")
        response = JsonResponse({"error": "Superuserların sayfayı kullanımı yasaktır."})
        response.status_code = 403 #forbidden access

    return response

        
def kalipfirini_meydan(request):
    #giris yapan usera bagli pres meydanlarındaki kalıplar
    #her pres kalıp fırını için kullanıcı oluştur, pres meydanlarına yetki ver

    params = json.loads(unquote(request.GET.get('params')))
    size = params["size"]
    page = params["page"]
    offset, limit = calculate_pagination(page, size)

    loc = get_objects_for_user(request.user, "ArslanTakipApp.meydan_view_location", klass=Location) #Location.objects.all() 
    
    if not request.user.is_superuser:
        loc_id = loc.get(locationName__contains = "MEYDAN").id
        meydanKalip = DiesLocation.objects.filter(kalipVaris_id = loc_id).order_by('kalipNo')
    else:
        loc_list = list(loc.values())
        locs = [l['id'] for l in loc_list]
        meydanKalip = DiesLocation.objects.filter(kalipVaris_id__in = locs).order_by('kalipNo')
    
    #print(meydanKalip.values('kalipNo'))
    meydanData = list(meydanKalip.values('kalipNo')[offset:limit])

    meydan_count = meydanKalip.count()
    lastData= {'last_page': math.ceil(meydan_count/size), 'data': []}
    lastData['data'] = meydanData
    data = json.dumps(lastData, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
    return HttpResponse(data)
