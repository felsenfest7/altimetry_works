import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from netCDF4 import Dataset as dt
import glob
import xarray as xr
import pandas as pd
import cartopy as ca
import os
import juliandate as jd
from datetime import datetime
import math as m
from dateutil.relativedelta import relativedelta

#Dosyaların okunarak dataframe haline getirilmesi

def merge_nc(files):
    """
        --> Bu fonksiyonun ana amacı indirilen nc dosyalarının path'inin fonksiyona girdi olarak girilmesidir.
        --> Ardından pathteki dosyalar sıralanarak ilk olarak xarray kütüphanesinin datasetine aktarılır.
        --> Ardından da hepsi dataframe olması için birer liste olur ve bunlar concat edilerek merge
    edilmiş bir dataframe elde edilir.
        --> Ardından BC 4713'e göre jday.00 değerleri düzenlenir. Bunun için yeni bir column'a bu değerler atanır.
        --> Ardından gregoryan tarihlerinin elde edilmesi için cdate adında yeni bir columnd oluşturulur ve jday
    tarihleri calendar date'e çevrilir.
        --> Fakat elde edilen "cdate" değerleri de tuple'lar içerisinde kalır. Bundan dolayı yeni bir liste
    oluşturulur ve yazılan for loopu ile "cdate_2" adı verilen ve sadece yıl-ay-gün bilgilerini içeren
    yeni bir liste elde edilir.
        --> Son olarak bu veriler dataframe'e aktarılarak sonuç ürün elde edilir.

        input: path
        output: dataframe
    """
    paths = sorted(glob.glob(files))
    datasets = [xr.open_dataset(p) for p in paths]
    dataframes = [p.to_dataframe() for p in datasets]
    dfs = pd.concat(dataframes)

    # Julian günü değişim
    # 1 Ocak 2000 12:00 UTM günü Julian günü olarak (4713 BC'e göre) 2451545.00000 gününe denk gelmekte.
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim

    jday4713 = [i + 2451545 for i in dfs["jday.00"]]
    dfs.insert(loc=13, column="jday.4713", value=jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in dfs["jday.4713"]]
    dfs.insert(loc=14, column="cdate", value=cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    dfs.insert(loc=15, column="cdate_t", value=cdate_2)

    dfs["cdate_t"] = pd.to_datetime(dfs["cdate_t"])

    dfs["sla"] = (dfs["ssh.55"] - dfs["mssh.05"])  #metre biriminde

    return dfs

def merge_df(frames):
    """
        --> Bu fonksiyonun amacı birden fazla aynı türdeki verinin (ALES, LRM)
        dataframelerinin birleştirilmesidir.
        --> Farklı veriler bir liste halinde girilmelidir.

        input: liste
        output: dataframe
    """
    result = pd.concat(frames)
    result = result.sort_values(by="cdate_t", ascending=True)
    return result

def filter_ales_05(df):
    """
        --> Bu fonksiyonun amacı ALES verileri için verilen kısıtlamaların veriye uygulanmasıdır.
        --> 05 uzantılı columnlar için geçerlidir (jason1, jason2 vb).

        input: dataframe
        output: dataframe
    """
    df_result = df[df["distance.00"] > 3]
    df_result = df_result[df_result["swh.05"] < 11]
    df_result = df_result[df_result["stdalt.05"] < 0.20]
    return df_result

def filter_ales_06(df):
    """
        --> Bu fonksiyonun amacı ALES verileri için verilen kısıtlamaların veriye uygulanmasıdır.
        --> 06 uzantılı columnlar için geçerlidir (sentinel).

        input: dataframe
        output: dataframe
    """
    df_result = df[df["distance.00"] > 3]
    #df_result = df_result[df_result["swh.06"] < 11]    --> sentinel verilerinde swh genelde Nan
    df_result = df_result[df_result["stdalt.06"] < 0.20]
    return df_result

#Verilerin aylık ve yıllık olarak elde edilmesi

def aylik(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
    """

    df_aylık = df.resample("MS", on="cdate_t").mean()
    return df_aylık

def yillik(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
        """

    df_yillik = df.groupby(df['cdate_t'].dt.year).mean()
    return df_yillik

#Dataframe olan dosyalardan istenilen indexteki verilerin çekilmesi.
#Not: alc = alçalan yörünge, yuks = yükselen yörünge

def alc_time_ilk_degerler(df):
    """
        --> Bu fonksiyonun amacı elde bulunan herhangi bir ALES verisinin time indexinin 0 olduğu
    değerlerinin alınmasıdır.
        --> Bu fonksiyon kullanılırken TUDES istasyonunun konumu ile indirilen ALES verisinin
    konumları önemlidir.
        --> Eğer TUDES istasyonu ALES verisine göre yukarda ise ve eğer ALES verisi alçalan
    yörüngeden elde edildiyse bu fonksiyon kullanılmalıdır.
        --> Çıktı ürün olarak sadece time indexi 0 olan yani yukarıdaki şarta göre yapılan ilk
    ölçmeler alınacaktır.

        input: dataframe
        output: dataframe
    """
    yeni_df = df.iloc[df.index == 0]
    return yeni_df

def alc_time_son_degerler(df):
    """
        --> Bu fonksiyonun amacı elde bulunan herhangi bir ALES verisinin time indexinin son olduğu
    değerlerinin alınmasıdır.
        --> Bu fonksiyon kullanılırken TUDES istasyonunun konumu ile indirilen ALES verisinin
    konumları önemlidir.
        --> Eğer TUDES istasyonu ALES verisine göre aşağıda ise ve eğer ALES verisi alçalan
    yörüngeden elde edildiyse bu fonksiyon kullanılmalıdır.
        --> Çıktı ürün olarak sadece time indexi son olan yani yukarıdaki şarta göre yapılan son
    ölçmeler alınacaktır.
        --> ANA SIKINTI INDEX DEĞERİ EN SON OLAN DEĞERLERİ ÇEKEMEDİM, VERİ BOYUTUNA GÖRE INDEX ATADIM.

        input: dataframe
        output: dataframe
    """
    yeni_df = df.iloc[df.index == 1]
    return yeni_df

def yuks_time_ilk_degerler(df):
    """
        --> Bu fonksiyonun amacı elde bulunan herhangi bir ALES verisinin time indexinin 0 olduğu
    değerlerinin alınmasıdır.
        --> Bu fonksiyon kullanılırken TUDES istasyonunun konumu ile indirilen ALES verisinin
    konumları önemlidir.
        --> Eğer TUDES istasyonu ALES verisine göre aşağıda ise ve eğer ALES verisi yükselen
    yörüngeden elde edildiyse bu fonksiyon kullanılmalıdır.
        --> Çıktı ürün olarak sadece time indexi 0 olan yani yukarıdaki şarta göre yapılan ilk
    ölçmeler alınacaktır.

        input: dataframe
        output: dataframe
    """
    yeni_df = df.iloc[df.index == 3]
    return yeni_df

def yuks_time_son_degerler(df):
    """
        --> Bu fonksiyonun amacı elde bulunan herhangi bir ALES verisinin time indexinin son olduğu
    değerlerinin alınmasıdır.
        --> Bu fonksiyon kullanılırken TUDES istasyonunun konumu ile indirilen ALES verisinin
    konumları önemlidir.
        --> Eğer TUDES istasyonu ALES verisine göre yukarıda ise ve eğer ALES verisi yükselen
    yörüngeden elde edildiyse bu fonksiyon kullanılmalıdır.
        --> Çıktı ürün olarak sadece time indexi 0 olan yani yukarıdaki şarta göre yapılan ilk
    ölçmeler alınacaktır.
        --> ANA SIKINTI INDEX DEĞERİ EN SON OLAN DEĞERLERİ ÇEKEMEDİM, VERİ BOYUTUNA GÖRE INDEX ATADIM.

        input: dataframe
        output: dataframe
        """
    yeni_df = df.iloc[df.index == 4]
    return yeni_df

def distance_filter(df):
    """
        --> Bu fonkisyonun amacı karmakarışık olan ölçülerin filtrelenerek minimum değerlerinin alınması.

        input: df
        output: df
    """

    df_result = df[df["distance.00"] > 3]
    df_result = df[df["distance.00"] < 12]
    return df_result

def igneada_icin(df):
    """
        --> Bu fonkisyonun amacı karmakarışık olan ölçülerin filtrelenerek minimum değerlerinin alınması.

        input: df
        output: df
    """

    df_result = df[df["ssh.55"] > 37]
    return df_result

def merge_nc_sla(files):
    """
        --> Bu fonksiyonun ana amacı indirilen SLA nc dosyalarının path'inin fonksiyona girdi olarak girilmesidir.
        --> Ardından pathteki dosyalar sıralanarak ilk olarak xarray kütüphanesinin datasetine aktarılır.
        --> Ardından da hepsi dataframe olması için birer liste olur ve bunlar concat edilerek merge
    edilmiş bir dataframe elde edilir.
        --> Ardından BC 4713'e göre jday.00 değerleri düzenlenir. Bunun için yeni bir column'a bu değerler atanır.
        --> Ardından gregoryan tarihlerinin elde edilmesi için cdate adında yeni bir columnd oluşturulur ve jday
    tarihleri calendar date'e çevrilir.
        --> Fakat elde edilen "cdate" değerleri de tuple'lar içerisinde kalır. Bundan dolayı yeni bir liste
    oluşturulur ve yazılan for loopu ile "cdate_2" adı verilen ve sadece yıl-ay-gün bilgilerini içeren
    yeni bir liste elde edilir.
        --> Son olarak bu veriler dataframe'e aktarılarak sonuç ürün elde edilir.

        input: path
        output: dataframe
        """
    paths = sorted(glob.glob(files))
    datasets = [xr.open_dataset(p) for p in paths]
    dataframes = [p.to_dataframe() for p in datasets]
    dfs = pd.concat(dataframes)

    # Julian günü değişim
    # 1 Ocak 2000 12:00 UTM günü Julian günü olarak (4713 BC'e göre) 2451545.00000 gününe denk gelmekte.
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim

    jday4713 = [i + 2451545 for i in dfs["jday.00"]]
    dfs.insert(loc = 7, column="jday.4713", value=jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in dfs["jday.4713"]]
    dfs.insert(loc = 8, column="cdate", value=cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    dfs.insert(loc = 9, column="cdate_t", value=cdate_2)

    dfs["cdate_t"] = pd.to_datetime(dfs["cdate_t"])

    return dfs

def aylik_sla(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir SLA dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.les_sla_filter
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
    """

    df_aylık = df.resample("MS", on="cdate_t").mean()
    return df_aylık

def yillik_sla(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
        """

    df_yillik = df.groupby(df['cdate_t'].dt.year).mean()
    return df_yillik

def sifir_index(df):
    yeni_df = df.iloc[df.index == 0]
    return yeni_df

def bir_index(df):
    yeni_df = df.iloc[df.index == 1]
    return yeni_df

def iki_index(df):
    yeni_df = df.iloc[df.index == 2]
    return yeni_df

def uc_index(df):
    yeni_df = df.iloc[df.index == 3]
    return yeni_df

def dort_index(df):
    yeni_df = df.iloc[df.index == 4]
    return yeni_df

def bes_index(df):
    yeni_df = df.iloc[df.index == 5]
    return yeni_df

def alti_index(df):
    yeni_df = df.iloc[df.index == 6]
    return yeni_df

def yedi_index(df):
    yeni_df = df.iloc[df.index == 7]
    return yeni_df

def sekiz_index(df):
    yeni_df = df.iloc[df.index == 8]
    return yeni_df

def dokuz_index(df):
    yeni_df = df.iloc[df.index == 9]
    return yeni_df

def on_index(df):
    yeni_df = df.iloc[df.index == 10]
    return yeni_df

def ondort_index(df):
    yeni_df = df.iloc[df.index == 14]
    return yeni_df

def ales_sla_filter(df):
    """
        --> SLA'lara göre noiselu verileri elimine etmek için
    :param df:
    :return:
        """
    df_result = df[df["sla"] < 0.7]
    df_result = df_result[df_result["sla"] > -0.7]
    return df_result

def lrm_sla_filter(df):
    """
        --> SLA'lara göre noiselu verileri elimine etmek için
    :param df:
    :return:
    """
    df_result = df[df["sla.40"] < 0.7]
    df_result = df_result[df_result["sla.40"] > -0.7]
    return df_result

def mean_square_aylik(df):
    """
        --> SLA için karesel ortalama hata hesabı yapar.
    """

    #NaN değerlerin alınmaması
    df = df[df["sla"].notna()]

    #Ortalama anomali hesabı
    ort_sla = df["sla"].mean()

    # v = x - l eşitliği için liste
    v_list = []

    for i in df.sla:
        v = ort_sla - i
        v_list.append(v)
        i += 1

    # v lerin kareleri
    v_list_kare = []

    for i in v_list:
        v_kare = i * i
        v_list_kare.append(v_kare)
        i += 1

    differences_in_years = relativedelta(df.index[-1], df.index[0]).years

    # Karesel ortalama hata hesabı
    mse = m.sqrt(sum(v_list_kare) / len(v_list_kare))#m
    mse = mse / differences_in_years #m
    mse = mse * 1000 #mm
    return mse

def mean_square_gunluk(df):
    """
        --> SLA için karesel ortalama hata hesabı yapar.
    """

    #NaN değerlerin alınmaması
    df = df[df["sla"].notna()]

    #Ortalama anomali hesabı
    ort_sla = df["sla"].mean()

    # v = x - l eşitliği için liste
    v_list = []

    for i in df.sla:
        v = ort_sla - i
        v_list.append(v)
        i += 1

    # v lerin kareleri
    v_list_kare = []

    for i in v_list:
        v_kare = i * i
        v_list_kare.append(v_kare)
        i += 1

    differences_in_years = relativedelta(df["cdate_t"].iat[-1], df["cdate_t"].iat[0]).years

    # Karesel ortalama hata hesabı
    mse = m.sqrt(sum(v_list_kare) / len(v_list_kare))#m
    mse = mse / differences_in_years #m
    mse = mse * 1000 #mm
    return mse

def mean_square_gunluk_lrm(df):
    """
        --> SLA için karesel ortalama hata hesabı yapar.
    """

    #NaN değerlerin alınmaması
    df = df[df["sla.40"].notna()]

    #Ortalama anomali hesabı
    ort_sla = df["sla.40"].mean()

    # v = x - l eşitliği için liste
    v_list = []

    for i in df["sla.40"]:
        v = ort_sla - i
        v_list.append(v)
        i += 1

    # v lerin kareleri
    v_list_kare = []

    for i in v_list:
        v_kare = i * i
        v_list_kare.append(v_kare)
        i += 1

    differences_in_years = relativedelta(df["cdate_t"].iat[-1], df["cdate_t"].iat[0]).years

    # Karesel ortalama hata hesabı
    mse = m.sqrt(sum(v_list_kare) / len(v_list_kare))#m
    mse = mse / differences_in_years #m
    mse = mse * 1000 #mm
    return mse

def mean_square_aylik_lrm(df):
    """
        --> SLA için karesel ortalama hata hesabı yapar.
    """

    #NaN değerlerin alınmaması
    df = df[df["sla.40"].notna()]

    #Ortalama anomali hesabı
    ort_sla = df["sla.40"].mean()

    # v = x - l eşitliği için liste
    v_list = []

    for i in df["sla.40"]:
        v = ort_sla - i
        v_list.append(v)
        i += 1

    # v lerin kareleri
    v_list_kare = []

    for i in v_list:
        v_kare = i * i
        v_list_kare.append(v_kare)
        i += 1

    differences_in_years = relativedelta(df.index[-1], df.index[0]).years

    # Karesel ortalama hata hesabı
    mse = m.sqrt(sum(v_list_kare) / len(v_list_kare))#m
    mse = mse / differences_in_years #m
    mse = mse * 1000 #mm
    return mse



