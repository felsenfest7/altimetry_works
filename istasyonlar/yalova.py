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
#YALOVA ALES
#Verinin okunması
ales_jason1 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/YALOVA/YALOVA_VERİLER/JASON1/JASON1_DATA/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/YALOVA/YALOVA_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/YALOVA/YALOVA_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_s3a_242 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/YALOVA/YALOVA_VERİLER/SENTINEL3A/SENTINEL3A_242_DATA/*.nc")
ales_s3a_55 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/YALOVA/YALOVA_VERİLER/SENTINEL3A/SENTINEL3A_55_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_jason1 = rmn.uc_index(ales_jason1)
ales_jason2 = rmn.uc_index(ales_jason2)
ales_jason3 = rmn.uc_index(ales_jason3)
ales_s3a_242 = rmn.iki_index(ales_s3a_242)
ales_s3a_55 = rmn.bir_index(ales_s3a_55)

#Verilere filtrelerin uygulanması
ales_jason1 = rmn.filter_ales_05(ales_jason1)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_s3a_242 = rmn.filter_ales_06(ales_s3a_242)
ales_s3a_55 = rmn.filter_ales_06(ales_s3a_55)

#Verilerin birleştirilmesi
ales_frames = [ales_jason1, ales_jason2, ales_jason3, ales_s3a_242, ales_s3a_55]
ales_veriler = rmn.merge_df(ales_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

#Grafik çizdirme
#gunluk_ssh = pl.plot_ssh_gunluk(ales_veriler_gunluk, "Yalova Günlük Altimetre Verileri")
#aylik_ssh = pl.plot_ssh_aylik(ales_veriler_aylik, "Yalova Aylık Altimetre Verileri")
#yillik_ssh = pl.plot_ssh_yillik(ales_veriler_yillik, "Yalova Yıllık Altimetre Verileri")

#gunluk_sla = pl.plot_sla_gunluk(ales_veriler_gunluk, "Yalova Günlük Altimetre Verileri")
#aylik_sla = pl.plot_sla_aylik(ales_veriler_aylik, "Yalova Aylık Altimetre Verileri")
#yillik_sla = pl.plot_sla_yillik(ales_veriler_yillik, "Yalova Yıllık Altimetre Verileri")
#-----------------------------------------------------------------------------------------------------------------------
#YALOVA LRM/SAR/SARIN
#Verinin okunması
lrm_cryosat2 = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/YALOVA/YALOVA_VERİLER/CRYOSAT2/CRYOSAT2_DATA/*.nc")
lrm_s3b = rmn.merge_nc_sla("/home/furkan/deus/ALTIMETRY/processler/LRM/YALOVA/YALOVA_VERİLER/SENTINEL3B/SENTINEL3B_DATA/*.nc")

#Verilerin değerlerinin alınması
lrm_cryosat2 = rmn.sifir_index(lrm_cryosat2)
lrm_s3b = rmn.sifir_index(lrm_s3b)

#Verilerin birleştirilmesi
lrm_frames = [lrm_cryosat2, lrm_s3b]
lrm_veriler = rmn.merge_df(lrm_frames)

#LRM verilerin filter uygulanması
lrm_veriler = rmn.lrm_sla_filter(lrm_veriler)

#Günlük, aylık ve yıllık veriler
lrm_veriler_gunluk = lrm_veriler
lrm_veriler_aylik = rmn.aylik_sla(lrm_veriler_gunluk)
lrm_veriler_yillik = rmn.yillik_sla(lrm_veriler_gunluk)

#gunluk_sla = pl.sla_gunluk(lrm_veriler_gunluk, "Yalova Günlük Altimetre Verileri")
#aylik_sla = pl.sla_aylik(lrm_veriler_aylik, "Yalova Aylık Altimetre Verileri")
#yillik_sla = pl.sla_yillik(lrm_veriler_yillik, "Yalova Yıllık Altimetre Verileri")

#a = pl.iki_df_sla_plot(lrm_veriler_aylik, ales_veriler_aylik, "Yalova Aylık SLA Verileri", "aylik")
#a = pl.iki_df_sla_plot(lrm_veriler_gunluk, ales_veriler_gunluk, "Yalova Günlük SLA Verileri", "gunluk")









