clc, clear, close all

%ANTALYAYA AİT VERİLER

%Veri
erdemli_aylik_lrm = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/ERDEMLİ/REVİZE/erdemli_lrm_idw.xlsx");
erdemli_aylik_sar = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/ERDEMLİ/REVİZE/erdemli_sar_idw.xlsx");

%TUDES istasyonlarına ait bilgier
istasyonlar = readtable("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonlarin_konumlari.xlsx");

%Verilerin çizdirilmesi
figure;
geoscatter(istasyonlar.Latitude, istasyonlar.Longitude, "filled", "^", "MarkerEdgeColor", "r",...
           "MarkerFaceColor", "r", "DisplayName", "TUDES İstasyonları");

hold on

geoscatter(erdemli_aylik_lrm.glat_00, erdemli_aylik_lrm.glon_00, "filled", "o", "MarkerEdgeColor", "c", ...
           "MarkerFaceColor","c", "DisplayName", "LRM");

hold on;

geoscatter(erdemli_aylik_sar.glat_00, erdemli_aylik_sar.glon_00, "filled", "o", "MarkerEdgeColor", "g", ...
           "MarkerFaceColor","g", "DisplayName", "SAR");

hold on;

geobasemap satellite;
title("Aylık ALES Verileri ile TUDES İstasyonlarının Koordinatları");
legend();
grid on;
%İstasyonların isimlerinin haritaya yazdırılması
txt = strcat(istasyonlar.Station);
text(istasyonlar.Latitude-0.01,istasyonlar.Longitude-0.01,txt, "Color", "white", "FontWeight", "Bold");

lat_ort = 36.558750305882356;
lon_ort = 34.362634105882350;

geoscatter(lat_ort, lon_ort, "filled", "square", "MarkerEdgeColor", "m", "MarkerFaceColor", "m", "DisplayName", "Ortalama Koordinat");