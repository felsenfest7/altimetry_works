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

    return dfs

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

def alc_time_ilk_degerleri(df):
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

def alc_time_son_degerleri(df):
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
    yeni_df = df.iloc[df.index == 20]
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
    yeni_df = df.iloc[df.index == 0]
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
    yeni_df = df.iloc[df.index == 20]
    return yeni_df
