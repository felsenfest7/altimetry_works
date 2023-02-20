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
#GOKCEADA ALES
#Verinin okunması
#Verinin okunması
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/GOKCEADA/GOKCEADA_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/GOKCEADA/GOKCEADA_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/GOKCEADA/GOKCEADA_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_s3a = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/GOKCEADA/GOKCEADA_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_jason1 = rmn.sekiz_index(ales_jason1)
ales_jason2 = rmn.sekiz_index(ales_jason2)
ales_jason3 = rmn.sekiz_index(ales_jason3)
ales_s3a = rmn.iki_index(ales_s3a)

#Verilere filtrelerin uygulanması
ales_jason1 = rmn.filter_ales_05(ales_jason1)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_s3a = rmn.filter_ales_06(ales_s3a)

#Verilerin birleştirilmesi
ales_frames = [ales_jason1, ales_jason2, ales_jason3, ales_s3a]
ales_veriler = rmn.merge_df(ales_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

#Grafik çizdirme
#gunluk_ssh = pl.plot_ssh_gunluk(ales_veriler_gunluk, "Gökçeada Günlük Altimetre Verileri")
#aylik_ssh = pl.plot_ssh_aylik(ales_veriler_aylik, "Gökçeada Aylık Altimetre Verileri")
#yillik_ssh = pl.plot_ssh_yillik(ales_veriler_yillik, "Gökçeada Yıllık Altimetre Verileri")

#gunluk_sla = pl.plot_sla_gunluk(ales_veriler_gunluk, "Gökçeada Günlük Altimetre Verileri")
#aylik_sla = pl.plot_sla_aylik(ales_veriler_aylik, "Gökçeada Aylık Altimetre Verileri")
#yillik_sla = pl.plot_sla_yillik(veriler_yillik, "Gökçeada Yıllık Altimetre Verileri")
#-----------------------------------------------------------------------------------------------------------------------
#GOKCEADA LRM/SAR
lrm_saral = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/GOKCEADA/GOKCEADA_VERİLER/SARAL/SARAL_DATA/*.nc")
lrm_cryosat2 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/GOKCEADA/GOKCEADA_VERİLER/CRYOSAT2/CRYOSAT2_DATA/*.nc")
lrm_s3a = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/GOKCEADA/GOKCEADA_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")

#Verilerin değerlerinin alınması
lrm_saral = rmn.sifir_index(lrm_saral)
lrm_cryosat2 = rmn.sifir_index(lrm_cryosat2)
lrm_s3a = rmn.sifir_index(lrm_s3a)

#Verilerin birleştirilmesi
lrm_frames = [lrm_saral, lrm_cryosat2, lrm_s3a]
lrm_veriler = rmn.merge_df(lrm_frames)

#LRM verilerin filter uygulanması
lrm_veriler = rmn.lrm_sla_filter(lrm_veriler)

#Günlük, aylık ve yıllık veriler
lrm_veriler_gunluk = lrm_veriler
lrm_veriler_aylik = rmn.aylik_sla(lrm_veriler_gunluk)
lrm_veriler_yillik = rmn.yillik_sla(lrm_veriler_gunluk)

#gunluk_sla = pl.sla_gunluk(lrm_veriler_gunluk, "Gökçeada Günlük Altimetre Verileri")
#aylik_sla = pl.sla_aylik(lrm_veriler_aylik, "Gökçeada Aylık Altimetre Verileri")
#yillik_sla = pl.sla_yillik(lrm_veriler_yillik, "Gökçeada Yıllık Altimetre Verileri")

#a = pl.iki_df_sla_plot(lrm_veriler_aylik, ales_veriler_aylik, "Gökçeada Aylık SLA Verileri", "aylik")
#a = pl.iki_df_sla_plot(lrm_veriler_gunluk, ales_veriler_gunluk, "Gökçeada Günlük SLA Verileri", "gunluk")
"""
print(ales_veriler_aylik["glat.00"].mean())
print(ales_veriler_aylik["glon.00"].mean())
print(lrm_veriler_aylik["glat.00"].mean())
print(lrm_veriler_aylik["glon.00"].mean())
"""


















