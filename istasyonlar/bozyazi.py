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
#BOZYAZI ALES

#Verinin okunması
ales_envisat = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/ENVISAT/ENVISAT_DATA/*.nc")
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason1em = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/JASON1_EM/JASON1_EM_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_s3a = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/BOZYAZI/BOZYAZI_VERİLER/SENTINEL3A/SENTINEL3A_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_envisat = rmn.bir_index(ales_envisat)
ales_jason1 = rmn.dort_index(ales_jason1)
ales_jason1em = rmn.sifir_index(ales_jason1em)
ales_jason2 = rmn.bir_index(ales_jason2)
ales_jason3 = rmn.bir_index(ales_jason3)
ales_s3a = rmn.sifir_index(ales_s3a)

#Veriye filter uygulanması
ales_envisat = rmn.filter_ales_05(ales_envisat)
ales_jason1 = rmn.filter_ales_05(ales_jason1)
ales_jason1em = rmn.filter_ales_05(ales_jason1em)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_s3a = rmn.filter_ales_06(ales_s3a)

#Verilerin birleştirilmesi
ales_frames = [ales_envisat, ales_jason1, ales_jason1em, ales_jason2, ales_jason3, ales_s3a]
ales_veriler = rmn.merge_df(ales_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

#Grafik çizdirme
#gunluk_ssh = pl.plot_ssh_gunluk(ales_veriler_gunluk, "Bozyazı Günlük Altimetre Verileri")
#aylik_ssh = pl.plot_ssh_aylik(ales_veriler_aylik, "Bozyazı Aylık Altimetre Verileri")
#yillik_ssh = pl.plot_ssh_yillik(ales_veriler_yillik, "Bozyazı Yıllık Altimetre Verileri")

#gunluk_sla = pl.plot_sla_gunluk(ales_veriler_gunluk, "Bozyazı Günlük Altimetre Verileri")
#aylik_sla = pl.plot_sla_aylik(ales_veriler_aylik, "Bozyazı Aylık Altimetre Verileri")
#yillik_sla = pl.plot_sla_yillik(ales_veriler_yillik, "Bozyazı Yıllık Altimetre Verileri")
#-----------------------------------------------------------------------------------------------------------------------
#BOZYAZI LRM/SAR/SARIN

#Verilerin okunması
lrm_envisat_586 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/ENVISAT/ENVISAT_586_42_DATA/*.nc")
lrm_envisat_513 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/ENVISAT/ENVISAT_513_DATA/*.nc")
lrm_cryosat2 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/CRYOSAT2/CRYOSAT2_DATA/*.nc")
lrm_saral = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/SARAL/SARAL_DATA/*.nc")
lrm_s3a_397 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/SENTINEL3A/SENTINEL3A_397_DATA/*.nc")
lrm_s3a_156 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/BOZYAZI/BOZYAZI_VERİLER/SENTINEL3A/SENTINEL3A_156_DATA/*.nc")

#Verilerin değerlerinin alınması
lrm_envisat_586 = rmn.sifir_index(lrm_envisat_586)
lrm_envisat_513 = rmn.dort_index(lrm_envisat_513)
lrm_cryosat2 = rmn.sifir_index(lrm_cryosat2)
lrm_saral = rmn.sifir_index(lrm_saral)
lrm_s3a_397 = rmn.uc_index(lrm_s3a_397)
lrm_s3a_156 = rmn.sifir_index(lrm_s3a_156)

#Verilerin birleştirilmesi
lrm_frames = [lrm_envisat_586, lrm_envisat_513, lrm_cryosat2, lrm_saral, lrm_s3a_397, lrm_s3a_156]
lrm_veriler = rmn.merge_df(lrm_frames)

#LRM verilerin filter uygulanması
lrm_veriler = rmn.lrm_sla_filter(lrm_veriler)

#Günlük, aylık ve yıllık veriler
lrm_veriler_gunluk = lrm_veriler
lrm_veriler_aylik = rmn.aylik_sla(lrm_veriler_gunluk)
lrm_veriler_yillik = rmn.yillik_sla(lrm_veriler_gunluk)

#gunluk_sla = pl.sla_gunluk(lrm_veriler_gunluk, "Bozyazı Günlük Altimetre Verileri")
#aylik_sla = pl.sla_aylik(lrm_veriler_aylik, "Bozyazı Aylık Altimetre Verileri")
#yillik_sla = pl.sla_yillik(lrm_veriler_yillik, "Bozyazı Yıllık Altimetre Verileri")
#-----------------------------------------------------------------------------------------------------------------------
#a = pl.iki_df_sla_plot(lrm_veriler_aylik, ales_veriler_aylik, "Bozyazı Aylık SLA Verileri", "aylik")
#a = pl.iki_df_sla_plot(lrm_veriler_gunluk, ales_veriler_gunluk, "Bozyazı Günlük SLA Verileri", "gunluk")
"""
print(ales_veriler_aylik["glat.00"].mean())
print(ales_veriler_aylik["glon.00"].mean())
print(lrm_veriler_aylik["glat.00"].mean())
print(lrm_veriler_aylik["glon.00"].mean())
"""