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
import matplotlib.dates as dates
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.ticker import FormatStrFormatter

#PLOTLARIN ÇİZİMİ

def plot_ssh_gunluk(df, title):
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

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["ssh.55"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Hareketli Ortalama")

    #Sadece year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Günlük Deniz Seviyesi Yüksekliği (m)", fontsize=13)

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = df["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, df["ssh.55"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label = "Trend")

    #MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = df["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = mean_squared_error(df["ssh.55"], df["mssh.05"])   #Bu değer metre biriminde
    mse_cm = mse  * 100   #Bu değer santimetre biriminde
    mse_cm = "%.2f" % mse_cm

    #Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2018, 1, 1), 25, f"Trend: {ort_ssh} m ± {mse_cm} cm")

    plt.title(title)
    ax.legend(loc="best")
    plt.grid(True)
    plt.show()

def plot_ssh_aylik(df, title):
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

    #Nan değerlerinin alınmaması
    dff = dff[dff["ssh.55"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.plot_date(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    dff["EWMA3"] = dff["ssh.55"].ewm(span=3).mean()
    ax.plot_date(dff["cdate_t"], dff["EWMA3"], "red", label="Hareketli Ortalama")

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = dff["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, dff["ssh.55"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = dff["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = mean_squared_error(dff["ssh.55"], dff["mssh.05"])  # Bu değer metre biriminde
    mse_cm = mse * 100  # Bu değer santimetre biriminde
    mse_cm = "%.2f" % mse_cm

    #Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2018, 1, 1), 35, f"Trend: {ort_ssh} m ± {mse_cm} cm")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=18))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

def plot_ssh_yillik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Yıllık fonksiyonu ile elde edilen veriler için geçerli.
        --> Trend hesabı yapılarak ardından MSE hesabı yapılır. MSE hesabı yapılırken SLA = SSH -MSS eşitliği kullanılır.
        --> Önceki fonksiyonlarda datetime object değiştirildiği için integer olarak kullanılıyor.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.locator_params(integer=True)
    ax.plot(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Yüksekliği (m)", fontsize=13)

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(dff["cdate_t"], dff["ssh.55"], 1)
    fit = np.poly1d(trend)
    ax.plot(dff["cdate_t"], fit(dff["cdate_t"]), "k--", label="Trend")

    #MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = dff["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = mean_squared_error(dff["ssh.55"], dff["mssh.05"])  # Bu değer metre biriminde
    mse_cm = mse * 100  # Bu değer santimetre biriminde
    mse_cm = "%.2f" % mse_cm

    #Trend değerlerinin plota yazdırılması
    plt.text(2018, 40, f"Trend: {ort_ssh} m ± {mse_cm} cm")

    plt.title(title)
    plt.legend(loc = "best")
    plt.grid(True)
    plt.show()

def plot_sla_gunluk(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.

        input: dataframe
        output: plot
    """

    #Ardından normal bir fig, ax ile grafik çizdirilir
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(df["cdate_t"], df["sla"], "royalblue", label="Deniz Seviyesi Anomalisi")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["sla"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Hareketli Ortalama")

    #Sadece year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Günlük Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    ax.legend(loc="best")
    plt.grid(True)
    plt.show()

def plot_sla_aylik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Nan değerlerinin alınmaması
    dff = dff[dff["sla"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["sla"], "royalblue", label="Deniz Seviyesi Anomalisi")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    dff["EWMA3"] = dff["sla"].ewm(span=3).mean()
    ax.plot_date(dff["cdate_t"], dff["EWMA3"], "red", label="Hareketli Ortalama")

    #Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval = 18))
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Anomalisi (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

def plot_sla_yillik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.
        --> Yıllık fonksiyonu ile elde edilen veriler için geçerli.
        --> Önceki fonksiyonlarda datetime object değiştirildiği için integer olarak kullanılıyor.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.locator_params(integer=True)
    ax.plot(dff["cdate_t"], dff["sla"], "royalblue", label="Deniz Seviyesi Anomalisi")

    # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    plt.legend(loc = "best")
    plt.grid(True)
    plt.show()