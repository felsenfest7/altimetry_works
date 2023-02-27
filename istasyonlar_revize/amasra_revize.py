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
import trend_analysis as ta
import plot_revize as pr
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA ALES
#Verinin okunması
ales_envisat = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/AMASRA/AMASRA_VERİLER/ENVISAT/ENVISAT_DATA/*.nc")
ales_saral = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/AMASRA/AMASRA_VERİLER/SARAL/SARAL_DATA/*.nc")
ales_saraldp = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/AMASRA/AMASRA_VERİLER/SARAL_DP/SARAL_DP_DATA/*.nc")
ales_s3b_698 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/AMASRA/AMASRA_VERİLER/SENTINEL3B/SENTINEL3B_698_DATA/*.nc")
ales_s3b_625 = rmn.merge_nc("/home/furkan/deus/ALTIMETRY/processler/ALES/AMASRA/AMASRA_VERİLER/SENTINEL3B/SENTINEL3B_625_DATA/*.nc")

#Verilerin değerlerinin alınması
ales_envisat = rmn.sifir_index(ales_envisat)
ales_saral = rmn.sifir_index(ales_saral)
ales_saraldp = rmn.sifir_index(ales_saraldp)
ales_s3b_698 = rmn.sifir_index(ales_s3b_698)
ales_s3b_625 = rmn.sifir_index(ales_s3b_625)
"""
#Veriye filter uygulanması
ales_envisat = rmn.filter_ales_05(ales_envisat)
ales_saral = rmn.filter_ales_05(ales_saral)
ales_saraldp = rmn.filter_ales_05(ales_saraldp)
ales_s3b_698 = rmn.filter_ales_06(ales_s3b_698)
ales_s3b_625 = rmn.filter_ales_06(ales_s3b_625)
"""
#Verilerin birleştirilmesi
#Tüm veriler
ales_frames = [ales_envisat, ales_saral, ales_saraldp, ales_s3b_698, ales_s3b_625]
ales_veriler = rmn.merge_df(ales_frames)

#LRM verileri
lrm_frames = [ales_envisat, ales_saral, ales_saraldp]
lrm_veriler = rmn.merge_df(lrm_frames)

#SAR verileri
sar_frames = [ales_s3b_698, ales_s3b_625]
sar_veriler = rmn.merge_df(sar_frames)

#ALES verilerin filter uygulanması
#ales_veriler = rmn.ales_sla_filter(ales_veriler)
#lrm_veriler = rmn.ales_sla_filter(lrm_veriler)
#sar_veriler = rmn.ales_sla_filter(sar_veriler)

#Günlük, aylık ve yıllık veriler
ales_veriler_gunluk = ales_veriler
ales_veriler_aylik = rmn.aylik(ales_veriler_gunluk)
ales_veriler_yillik = rmn.yillik(ales_veriler_gunluk)

lrm_veriler_gunluk = lrm_veriler
lrm_veriler_aylik = rmn.aylik(lrm_veriler_gunluk)
lrm_veriler_yillik = rmn.yillik(lrm_veriler_gunluk)

sar_veriler_gunluk = sar_veriler
sar_veriler_aylik = rmn.aylik(sar_veriler_gunluk)
sar_veriler_yillik = rmn.yillik(sar_veriler_gunluk)

#NaN değerlerinin olma ihtimaline karşı önlem
lrm_veriler_aylik.replace(' ', np.nan, inplace=True)

ales_veriler_aylik = ales_veriler_aylik.dropna(1)
lrm_veriler_aylik = lrm_veriler_aylik.dropna()
sar_veriler_aylik = sar_veriler_aylik.dropna(1)

#Ortalama koordinat değerinin hesabı
hesaba_girecek_veriler = [ales_s3b_698]
ort_koordinatlar = rmn.ort_koord(hesaba_girecek_veriler, 8.5)

enlem = ort_koordinatlar[0]
boylam = ort_koordinatlar[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
lrm_agirliklar = rmn.agirlik_hesabi(lrm_veriler_gunluk, enlem, boylam)
sar_agirliklar = rmn.agirlik_hesabi(sar_veriler_gunluk, enlem, boylam)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
idw_lrm = rmn.idw(lrm_agirliklar)
idw_sar = rmn.idw(sar_agirliklar)

#Zamansal ve verisel olarak interpolasyonların yapılması
idw_lrm = rmn.dates_interpolation(idw_lrm)
idw_lrm = rmn.interpolation_ales(idw_lrm)

idw_sar = rmn.dates_interpolation(idw_sar)
idw_sar = rmn.interpolation_ales(idw_sar)

#Excel tabloları
#lrm_aylik_veriler_excel = rmn.df2excel(idw_lrm, "ALES", "AMASRA", "amasra_lrm_idw")
#sar_aylik_veriler_excel = rmn.df2excel(idw_sar, "ALES", "AMASRA", "amasra_sar_idw")

#Verilerin çizdirilmesi
#aylik_ssh_plot = pr.plot_ssh_aylik(idw_lrm, idw_sar, "Amasra Aylık Ağırlıklandırılmış Altimetre Verileri")

#-----------------------------------------------------------------------------------------------------------------------
#AMASRA GELENEKSEL VERİLER
#Verinin okunması
gel_envisat = rmn.merge_nc_ssh("/home/furkan/deus/ALTIMETRY/processler/SSH_VERİLERİ/AMASRA/AMASRA_VERİLER/ENVISAT/ENVISAT_DATA/*.nc")
gel_cryosat2 = rmn.merge_nc_ssh("/home/furkan/deus/ALTIMETRY/processler/SSH_VERİLERİ/AMASRA/AMASRA_VERİLER/CRYOSAT2/CRYOSAT2_DATA/*.nc")
gel_s3b_698 = rmn.merge_nc_ssh("/home/furkan/deus/ALTIMETRY/processler/SSH_VERİLERİ/AMASRA/AMASRA_VERİLER/SENTINEL3B/SENTINEL3B_698_DATA/*.nc")
gel_s3b_625 = rmn.merge_nc_ssh("/home/furkan/deus/ALTIMETRY/processler/SSH_VERİLERİ/AMASRA/AMASRA_VERİLER/SENTINEL3B/SENTINEL3B_625_DATA/*.nc")

#Verilerin değerlerinin alınması
gel_envisat = rmn.sifir_index(gel_envisat)
gel_cryosat2 = rmn.sifir_index(gel_cryosat2)
gel_s3b_698 = rmn.bir_index(gel_s3b_698)
gel_s3b_625 = rmn.sifir_index(gel_s3b_625)

#Verilerin birleştirilmesi
#Tüm veriler
gel_frames = [gel_envisat, gel_cryosat2, gel_s3b_698, gel_s3b_625]
gel_veriler = rmn.merge_df(gel_frames)

#LRM verileri
gel_lrm_frames = [gel_envisat, gel_cryosat2]
gel_lrm_veriler = rmn.merge_df(gel_lrm_frames)

#SAR verileri
gel_sar_frames = [gel_s3b_698, gel_s3b_625]
gel_sar_veriler = rmn.merge_df(gel_sar_frames)

#Günlük, aylık ve yıllık veriler
gel_veriler_gunluk = gel_veriler
gel_veriler_aylik = rmn.aylik(gel_veriler_gunluk)
gel_veriler_yillik = rmn.yillik(gel_veriler_gunluk)

gel_lrm_veriler_gunluk = gel_lrm_veriler
gel_lrm_veriler_aylik = rmn.aylik(gel_lrm_veriler_gunluk)
gel_lrm_veriler_yillik = rmn.yillik(gel_lrm_veriler_gunluk)

gel_sar_veriler_gunluk = gel_sar_veriler
gel_sar_veriler_aylik = rmn.aylik(gel_sar_veriler_gunluk)
gel_sar_veriler_yillik = rmn.yillik(gel_sar_veriler_gunluk)

#NaN değerlerinin olma ihtimaline karşı önlem
gel_lrm_veriler_aylik.replace(' ', np.nan, inplace=True)
gel_sar_veriler_aylik.replace(' ', np.nan, inplace=True)

gel_veriler_aylik = gel_veriler_aylik.dropna(1)
gel_lrm_veriler_aylik = gel_lrm_veriler_aylik.dropna()
gel_sar_veriler_aylik = gel_sar_veriler_aylik.dropna(1)

#Ortalama koordinat değerinin hesabı
gel_hesaba_girecek_veriler = [gel_envisat]
gel_ort_koordinatlar = rmn.gel_ort_koord(gel_hesaba_girecek_veriler)

gel_enlem = gel_ort_koordinatlar[0]
gel_boylam = gel_ort_koordinatlar[1]

#Ağırlık hesabı ile verilerin yeniden düzenlenmesi
gel_lrm_agirliklar = rmn.agirlik_hesabi(gel_lrm_veriler_gunluk, enlem, boylam)
gel_sar_agirliklar = rmn.agirlik_hesabi(gel_sar_veriler_gunluk, enlem, boylam)

#IDW değerlerinin hesaplanması ile son dataframelerin elde edilmesi
gel_idw_lrm = rmn.gel_idw(gel_lrm_agirliklar)
gel_idw_sar = rmn.gel_idw(gel_sar_agirliklar)

#Zamansal ve verisel olarak interpolasyonların yapılması
gel_idw_lrm = rmn.dates_interpolation(gel_idw_lrm)
gel_idw_lrm = rmn.interpolation_ssh(gel_idw_lrm)

gel_idw_sar = rmn.dates_interpolation(gel_idw_sar)
gel_idw_sar = rmn.interpolation_ssh(gel_idw_sar)

#Excel tabloları
#gel_lrm_aylik_veriler_excel = rmn.df2excel_ssh(gel_idw_lrm, "SSH_VERİLERİ", "AMASRA", "amasra_lrm_idw")
#gel_sar_aylik_veriler_excel = rmn.df2excel_ssh(gel_idw_sar, "SSH_VERİLERİ", "AMASRA", "amasra_sar_idw")

#Verilerin çizdirilmesi
#gel_aylik_ssh_plot = pr.plot_ssh_aylikv2(gel_idw_lrm, gel_idw_sar, "Amasra Aylık Ağırlıklandırılmış Altimetre Verileri")

#KARŞILAŞTIRMA PLOTUNUN ÇİZDİRİLMESİ

#karsilastirma = pr.iki_df_ssh_plot(idw_lrm, idw_sar, gel_idw_lrm, gel_idw_sar, "Amasra Aylık Ağırlıklandırılmış ALES ve Altimetri Verileri")




