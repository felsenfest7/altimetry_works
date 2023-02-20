#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR/istasyonlar")

#Verinin okunması için kütüphaneler
import read_merge_nc as rmn
import plot as pl

#Uydu verilerinin konumları
import antalya as antl
import arsuz as arsz
import bozyazi as bzyz
import erdemli as erdm
import gokceada as gada
import igneada as iada
import marmara_ereglisi as merg
import marmaris as aksa
import mentes as mnts
import trabzon as trbz
import yalova as ylva

"""
#ALES VERİLERİ
#Günlük Veriler
ales_antl_gunluk = antl.ales_veriler_gunluk
ales_arsz_gunluk = arsz.ales_veriler_gunluk
ales_bzyz_gunluk = bzyz.ales_veriler_gunluk
ales_erdm_gunluk = erdm.ales_veriler_gunluk
ales_gada_gunluk = gada.ales_veriler_gunluk
ales_iada_gunluk = iada.ales_veriler_gunluk
ales_merg_gunluk = merg.ales_veriler_gunluk
ales_aksa_gunluk = aksa.ales_veriler_gunluk
ales_mnts_gunluk = mnts.ales_veriler_gunluk
ales_trbz_gunluk = trbz.ales_veriler_gunluk
ales_ylva_gunluk = ylva.ales_veriler_gunluk

#Excel tablosunun oluşturulması
table_gunluk = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/tum_gunluk_ales_verileri.xlsx",
                                   ales_antl_gunluk, ales_arsz_gunluk, ales_bzyz_gunluk, ales_erdm_gunluk, ales_gada_gunluk,
                                   ales_iada_gunluk, ales_merg_gunluk, ales_aksa_gunluk, ales_mnts_gunluk, ales_trbz_gunluk,
                                   ales_ylva_gunluk)

#Aylık Veriler
ales_antl_aylik = antl.ales_veriler_aylik
ales_arsz_aylik = arsz.ales_veriler_aylik
ales_bzyz_aylik = bzyz.ales_veriler_aylik
ales_erdm_aylik = erdm.ales_veriler_aylik
ales_gada_aylik = gada.ales_veriler_aylik
ales_iada_aylik = iada.ales_veriler_aylik
ales_merg_aylik = merg.ales_veriler_aylik
ales_aksa_aylik = aksa.ales_veriler_aylik
ales_mnts_aylik = mnts.ales_veriler_aylik
ales_trbz_aylik = trbz.ales_veriler_aylik
ales_ylva_aylik = ylva.ales_veriler_aylik

#Excel tablosunun oluşturulması
table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/tum_aylik_ales_verileri.xlsx",
                                   ales_antl_aylik, ales_arsz_aylik, ales_bzyz_aylik, ales_erdm_aylik, ales_gada_aylik,
                                   ales_iada_aylik, ales_merg_aylik, ales_aksa_aylik, ales_mnts_aylik, ales_trbz_aylik,
                                   ales_ylva_aylik)
"""

#LRM VERİLERİ
#Günlük Veriler
lrm_antl_gunluk = antl.lrm_veriler_gunluk
lrm_arsz_gunluk = arsz.lrm_veriler_gunluk
lrm_bzyz_gunluk = bzyz.lrm_veriler_gunluk
lrm_erdm_gunluk = erdm.lrm_veriler_gunluk
lrm_gada_gunluk = gada.lrm_veriler_gunluk
lrm_iada_gunluk = iada.lrm_veriler_gunluk
lrm_merg_gunluk = merg.lrm_veriler_gunluk
lrm_aksa_gunluk = aksa.lrm_veriler_gunluk
lrm_mnts_gunluk = mnts.lrm_veriler_gunluk
lrm_trbz_gunluk = trbz.lrm_veriler_gunluk
lrm_ylva_gunluk = ylva.lrm_veriler_gunluk

#Excel tablosunun oluşturulması
table_gunluk = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/tum_gunluk_lrm_verileri.xlsx",
                                   lrm_antl_gunluk, lrm_arsz_gunluk, lrm_bzyz_gunluk, lrm_erdm_gunluk, lrm_gada_gunluk,
                                   lrm_iada_gunluk, lrm_merg_gunluk, lrm_aksa_gunluk, lrm_mnts_gunluk, lrm_trbz_gunluk,
                                   lrm_ylva_gunluk)

#Aylık Veriler
lrm_antl_aylik = antl.lrm_veriler_aylik
lrm_arsz_aylik = arsz.lrm_veriler_aylik
lrm_bzyz_aylik = bzyz.lrm_veriler_aylik
lrm_erdm_aylik = erdm.lrm_veriler_aylik
lrm_gada_aylik = gada.lrm_veriler_aylik
lrm_iada_aylik = iada.lrm_veriler_aylik
lrm_merg_aylik = merg.lrm_veriler_aylik
lrm_aksa_aylik = aksa.lrm_veriler_aylik
lrm_mnts_aylik = mnts.lrm_veriler_aylik
lrm_trbz_aylik = trbz.lrm_veriler_aylik
lrm_ylva_aylik = ylva.lrm_veriler_aylik

#Excel tablosunun oluşturulması
table_aylik = rmn.ales_data_merge("/home/furkan/deus/ALTIMETRY/processler/tum_aylik_lrm_verileri.xlsx",
                                   lrm_antl_aylik, lrm_arsz_aylik, lrm_bzyz_aylik, lrm_erdm_aylik, lrm_gada_aylik,
                                   lrm_iada_aylik, lrm_merg_aylik, lrm_aksa_aylik, lrm_mnts_aylik, lrm_trbz_aylik,
                                   lrm_ylva_aylik)


