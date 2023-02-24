clc, clear, close all

%ANTALYAYA AİT VERİLER

%Veri
antalya_aylik_lrm = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/REVİZE/antalya_lrm_idw.xlsx");
antalya_aylik_sar = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/ANTALYA/REVİZE/antalya_sar_idw.xlsx");

%TUDES istasyonlarına ait bilgier
istasyonlar = readtable("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonlarin_konumlari.xlsx");

%Verilerin çizdirilmesi
figure;
geoscatter(istasyonlar.Latitude, istasyonlar.Longitude, "filled", "^", "MarkerEdgeColor", "r",...
           "MarkerFaceColor", "r", "DisplayName", "TUDES İstasyonları");

hold on

geoscatter(antalya_aylik_lrm.glat_00, antalya_aylik_lrm.glon_00, "filled", "o", "MarkerEdgeColor", "c", ...
           "MarkerFaceColor","c", "DisplayName", "LRM");

hold on;

geoscatter(antalya_aylik_sar.glat_00, antalya_aylik_sar.glon_00, "filled", "o", "MarkerEdgeColor", "g", ...
           "MarkerFaceColor","g", "DisplayName", "SAR");

hold on;

geobasemap satellite;
title("Aylık ALES Verileri ile TUDES İstasyonlarının Koordinatları");
legend();
grid on;
%İstasyonların isimlerinin haritaya yazdırılması
txt = strcat(istasyonlar.Station);
text(istasyonlar.Latitude-0.01,istasyonlar.Longitude-0.01,txt, "Color", "white", "FontWeight", "Bold");

lat_ort = 36.78593152222222;
lon_ort = 30.97990823333333;

geoscatter(lat_ort, lon_ort, "filled", "square", "MarkerEdgeColor", "m", "MarkerFaceColor", "m", "DisplayName", "Ortalama Koordinat");




