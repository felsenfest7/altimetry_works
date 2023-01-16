import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib
from netCDF4 import Dataset as dt
import glob
import xarray as xr
import pandas as pd
import cartopy as ca
import os
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
import statsmodels


def plot_ssh(df):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.

        input: dataframe
        output: plot
    """
    #SSH GRAFİĞİ ÇİZDİRME
    #df["cdate_t"] = pd.to_datetime(df["cdate_t"]) --> RNM'YE EKLEDİM BUNU

    #Ardından normal bir fig, ax ile grafik çizdirilir
    fig, ax = plt.subplots()
    ax.plot_date(df["cdate_t"], df["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    #Moving average hesabı
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["ssh.55"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Kayan Ortalama")

    #Sadede year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.show()

def plot_ssh_yillik(df):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotların çizdirilmesi ve gerekli bilgilerinin yazılması
    plt.plot(dff["cdate_t"], dff["ssh.55"], label = "Deniz Seviyesi Yüksekliği")
    plt.title("Title")
    plt.xlabel("Yıl")
    plt.ylabel("Deniz Seviyesi Yüksekliği (m)")
    plt.legend(loc = "best")
    plt.show()

def plot_ssh_aylik(df):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.plot_date(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    # Sadede year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval = 6))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.show()







