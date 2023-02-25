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
import read_merge_nc as rmn
from dateutil.relativedelta import relativedelta
import math as m

#PLOTLARIN ÇİZİMİ
#-----------------------------------------------------------------------------------------------------------------------
def plot_ssh_aylik(df_lrm, df_sar, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff_lrm = df_lrm
    dff_sar = df_sar

    #Nan değerlerinin alınmaması
    dff_lrm = dff_lrm[dff_lrm["ssh_idw"].notna()]
    dff_sar = dff_sar[dff_sar["ssh_idw"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff_lrm["cdate_t"], dff_lrm["ssh_idw"], "#87bc45", label="ALES LRM Verileri")
    ax.plot_date(dff_sar["cdate_t"], dff_sar["ssh_idw"], "#f46a9b", label="ALES SAR Verileri")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=36))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

def plot_ssh_aylikv2(df_lrm, df_sar, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff_lrm = df_lrm
    dff_sar = df_sar

    #Nan değerlerinin alınmaması
    dff_lrm = dff_lrm[dff_lrm["ssh_idw"].notna()]
    dff_sar = dff_sar[dff_sar["ssh_idw"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff_lrm["cdate_t"], dff_lrm["ssh_idw"], "#87bc45", label="Altimetri LRM Verileri")
    ax.plot_date(dff_sar["cdate_t"], dff_sar["ssh_idw"], "#f46a9b", label="Altimetri SAR Verileri")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=36))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

