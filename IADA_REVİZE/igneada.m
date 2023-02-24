clc, clear, close all

%İĞNEADA AİT VERİLER

%Veri
igneada_aylik_lrm = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/IGNEADA/REVİZE/igneada_lrm_idw.xlsx");
igneada_sar_lrm = readtable("/home/furkan/deus/ALTIMETRY/processler/ALES/IGNEADA/REVİZE/igneada_sar_idw.xlsx");

%TUDES istasyonlarına ait bilgier
istasyonlar = readtable("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonlarin_konumlari.xlsx");

%Verilerin çizdirilmesi
figure;
geoscatter(istasyonlar.Latitude, istasyonlar.Longitude, "filled", "^", "MarkerEdgeColor", "r",...
           "MarkerFaceColor", "r", "DisplayName", "TUDES İstasyonları");

hold on

geoscatter(igneada_aylik_lrm.glat_00, igneada_aylik_lrm.glon_00, "filled", "o", "MarkerEdgeColor", "c", ...
           "MarkerFaceColor","c", "DisplayName", "LRM");

hold on;

geoscatter(igneada_sar_lrm.glat_00, igneada_sar_lrm.glon_00, "filled", "o", "MarkerEdgeColor", "g", ...
           "MarkerFaceColor","g", "DisplayName", "SAR");
hold on;

geobasemap satellite;
title("Aylık ALES Verileri ile TUDES İstasyonlarının Koordinatları");
legend();
grid on;
%İstasyonların isimlerinin haritaya yazdırılması
txt = strcat(istasyonlar.Station);
text(istasyonlar.Latitude-0.01,istasyonlar.Longitude-0.01,txt, "Color", "white", "FontWeight", "Bold");

lat_ort = 41.830990125;
lon_ort = 28.042240999999997;

geoscatter(lat_ort, lon_ort, "filled", "square", "MarkerEdgeColor", "m", "MarkerFaceColor", "m", "DisplayName", "Ortalama Koordinat");