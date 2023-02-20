#Kütüphane
import pandas as pd

#Tüm TUDES istasyonlarının dataframe'inin oluşturulması için hazırlanan python file.
#İstasyonlar
iada = ["IADA", 41.88890424, 28.02351594]
istn = ["ISTN", 41.15984017, 29.07412648]
sile = ["SILE", 41.17636462, 29.60537553]
amsr = ["AMSR", 41.74398816, 32.39032924]
snop = ["SNOP", 42.02306816, 35.14945865]
trbz = ["TRBZ", 41.00197800, 39.74454939]
merg = ["MERG", 40.96896672, 27.96215236]
ylva = ["YLVA", 40.66197489, 29.27760959]
erdk = ["ERDK", 40.38988004, 27.84518123]
gada = ["GADA", 40.23171234, 25.89349329]
mnts = ["MNTS", 38.42960155, 26.72214568]
brdm = ["BDRM", 37.03217553, 27.42345750]
aksa = ["AKSA", 36.84867631, 28.28226596]
antl = ["ANTL", 36.83042146, 30.60868263]
bzyz = ["BZYZ", 36.09619554, 32.94011772]
tscu = ["TSCU", 36.28146292, 33.83622766]
erdm = ["ERDM", 36.56372030, 34.25539255]
arsz = ["ARSZ", 36.41558863, 35.88519394]

#Tüm verilerin bir listeye aktarılması
liste = [iada, istn, sile, amsr, snop, trbz, merg, ylva, erdk, gada, mnts, brdm, aksa, antl, bzyz, tscu, erdm, arsz]

#Dataframe oluşturulması
df = pd.DataFrame(liste, columns = ["Station", "Latitude", "Longitude"])

#Dataframe'in bir excel tablosuna aktarılması
tablo = df.to_excel("/home/furkan/deus/ALTIMETRY/processler/istasyonların_konumları.xlsx")







