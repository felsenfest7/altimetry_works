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
#SİNOP
#Verinin okunması
ales_envisat42 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/ENVISAT/ENVISAT_DATA_0042/*.nc")
ales_envisat255 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/ENVISAT/ENVISAT_DATA_0255/*.nc")
ales_jason2 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/JASON2/JASON2_DATA/*.nc")
ales_jason3 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/JASON3/JASON3_DATA/*.nc")
ales_s3a_0195 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/SENTINEL3A/SENTINEL3A_0195_DATA/*.nc")
ales_s3a_0270 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/SİNOP/SİNOP_VERİLER/SENTINEL3A/SENTINEL3A_0270_DATA/*.nc")
print(ales_jason2)
#Verilerin değerlerinin alınması
ales_envisat42 = rmn.on_index(ales_envisat42)
ales_envisat255 = rmn.sifir_index(ales_envisat255)
ales_jason2 = rmn.dort_index(ales_jason2)
ales_jason3 = rmn.dort_index(ales_jason3)
ales_s3a_0195 = rmn.alti_index(ales_s3a_0195)
ales_s3a_0270 = rmn.bes_index(ales_s3a_0270)

#Veriye filtrelerin uygulanması
ales_envisat42 = rmn.filter_ales_05(ales_envisat42)
ales_envisat255 = rmn.filter_ales_05(ales_envisat255)
ales_jason2 = rmn.filter_ales_05(ales_jason2)
ales_jason3 = rmn.filter_ales_05(ales_jason3)
ales_s3a_0195 = rmn.filter_ales_06(ales_s3a_0195)
ales_s3a_0270 = rmn.filter_ales_06(ales_s3a_0270)

#Verilerin birleştirilmesi
ales_frames = [ales_envisat42, ales_envisat255, ales_jason2, ales_jason3, ales_s3a_0195, ales_s3a_0270]
ales_veriler = rmn.merge_df(ales_frames)

#ALES verilerin filter uygulanması
ales_veriler = rmn.ales_sla_filter(ales_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

#Grafik çizdirme
#gunluk_ssh = pl.plot_ssh_gunluk(ales_veriler_gunluk, "Sinop Günlük Altimetre Verileri")
#aylik_ssh = pl.plot_ssh_aylik(ales_veriler_aylik, "Sinop Aylık Altimetre Verileri")
#yillik_ssh = pl.plot_ssh_yillik(ales_veriler_yillik, "Sinop Yıllık Altimetre Verileri")

#gunluk_sla = pl.plot_sla_gunluk(ales_veriler_gunluk, "Sinop Günlük Altimetre Verileri")
#aylik_sla = pl.plot_sla_aylik(ales_veriler_aylik, "Sinop Aylık Altimetre Verileri")
#yillik_sla = pl.plot_sla_yillik(ales_veriler_yillik, "Sinop Yıllık Altimetre Verileri")



























































