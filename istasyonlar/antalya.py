#-----------------------------------------------------------------------------------------------------------------------
#Tüm verinin okunması için (dataframe'in gözükmesi için) gerekli kodlar
import pandas as pd
import numpy as np

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',5000)

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

#Verinin okunması için kütüphaneler
import read_merge_nc as rmn
import plot as pl
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA ALES
#Verinin okunması
ales_envisat = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/ENVISAT/ENVISAT_DATA/*.nc")
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_s3a = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")
ales_s3b = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/ANTALYA_VERİLER/SENTINEL3B/SENTINEL3B_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_envisat = rmn.sifir_index(ales_envisat)
ales_jason1 = rmn.dort_index(ales_jason1)
ales_jason2 = rmn.dort_index(ales_jason2)
ales_jason3 = rmn.dort_index(ales_jason3)
ales_s3a = rmn.bir_index(ales_s3a)
ales_s3b = rmn.bir_index(ales_s3b)

#Veriye filter uygulanması
ales_envisat = rmn.filter_ales_05(ales_envisat)
ales_jason1 = rmn.filter_ales_05(ales_jason1)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_s3a = rmn.filter_ales_06(ales_s3a)
ales_s3b = rmn.filter_ales_06(ales_s3b)

#Verilerin birleştirilmesi
ales_frames = [ales_envisat, ales_jason1, ales_jason2, ales_jason3, ales_s3a, ales_s3b]
ales_veriler = rmn.merge_df(ales_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

#Grafik çizdirme
#gunluk_ssh = pl.plot_ssh_gunluk(ales_veriler_gunluk, "Antalya Günlük Altimetre Verileri")
#aylik_ssh = pl.plot_ssh_aylik(ales_veriler_aylik, "Antalya Aylık Altimetre Verileri")
#yillik_ssh = pl.plot_ssh_yillik(ales_veriler_yillik, "Antalya Yıllık Altimetre Verileri")

#gunluk_sla = pl.plot_sla_gunluk(ales_veriler_gunluk, "Antalya Günlük Altimetre Verileri")
#aylik_sla = pl.plot_sla_aylik(ales_veriler_aylik, "Antalya Aylık Altimetre Verileri")
#yillik_sla = pl.plot_sla_yillik(ales_veriler_yillik, "Antalya Yıllık Altimetre Verileri")
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA LRM/SAR/SARIN
#Verinin okunması
lrm_topex_em = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/TOPEX_EM/TOPEX_EM_DATA/*.nc")
lrm_envisat = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/ENVISAT/ENVISAT_DATA/*.nc")
lrm_gfo = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/GFO/GFO_DATA/*.nc")
lrm_cryosat2 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/CRYOSAT2/CRYOSAT2_DATA/*.nc")
lrm_s3a = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")
lrm_s3b = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/ANTALYA/ANTALYA_VERİLER/SENTINEL3B/SENTINEL3B_DATA/*.nc")

#Verilerin değerlerinin alınması
lrm_topex_em = rmn.sifir_index(lrm_topex_em)
lrm_envisat = rmn.ondort_index(lrm_envisat)
lrm_gfo = rmn.on_index(lrm_gfo)
lrm_cryosat2 = rmn.yedi_index(lrm_cryosat2)
lrm_s3a = rmn.bes_index(lrm_s3a)
lrm_s3b = rmn.sifir_index(lrm_s3b)

#Verilerin birleştirilmesi
lrm_frames = [lrm_topex_em, lrm_envisat, lrm_gfo, lrm_cryosat2, lrm_s3a, lrm_s3b]
lrm_veriler = rmn.merge_df(lrm_frames)

#LRM verilerin filter uygulanması
lrm_veriler = rmn.lrm_sla_filter(lrm_veriler)

#Günlük, aylık ve yıllık veriler
lrm_veriler_gunluk = lrm_veriler
lrm_veriler_aylik = rmn.aylik_sla(lrm_veriler_gunluk)
lrm_veriler_yillik = rmn.yillik_sla(lrm_veriler_gunluk)

#gunluk_sla = pl.sla_gunluk(lrm_veriler_gunluk, "Antalya Günlük Altimetre Verileri")
#aylik_sla = pl.sla_aylik(lrm_veriler_aylik, "Antalya Aylık Altimetre Verileri")
#yillik_sla = pl.sla_yillik(lrm_veriler_yillik, "Antalya Yıllık Altimetre Verileri")

#a = pl.iki_df_sla_plot(lrm_veriler_aylik, ales_veriler_aylik, "Antalya Aylık SLA Verileri", "aylik")
#a = pl.iki_df_sla_plot(lrm_veriler_gunluk, ales_veriler_gunluk, "Antalya Günlük SLA Verileri", "gunluk")
"""
table = rmn.df2excel(ales_veriler_gunluk)
print(table)
"""
#print(ales_veriler_gunluk["glat.00"].mean())
#print(ales_veriler_gunluk["glon.00"].mean())