clc, clear, close all

%Veriler
gunluk_data = readtable("/home/furkan/deus/ALTIMETRY/processler/tum_gunluk_ales_verileri.xlsx");
aylik_data = readtable("/home/furkan/deus/ALTIMETRY/processler/tum_aylik_ales_verileri.xlsx");

%TUDES istasyonlarına ait bilgier
istasyonlar = readtable("/home/furkan/deus/ALTIMETRY/processler/istasyonlarin_konumlari.xlsx");

%Verilerin çizdirilmesi
figure;
geoscatter(istasyonlar.Latitude, istasyonlar.Longitude, "filled", "^", "MarkerEdgeColor", "r",...
           "MarkerFaceColor", "r", "DisplayName", "TUDES İstasyonları");

hold on

geoscatter(aylik_data.glat_00, aylik_data.glon_00, "filled", "o", "MarkerEdgeColor", "c", ...
           "MarkerFaceColor","c", "DisplayName", "Aylık ALES Verisi");
geobasemap satellite;

title("Aylık Ortalama ALES Verileri ile TUDES İstasyonlarının Koordinatları");
legend();
grid on;
%İstasyonların isimlerinin haritaya yazdırılması
txt = strcat(istasyonlar.Station);
text(istasyonlar.Latitude-0.07,istasyonlar.Longitude-0.1,txt, "Color", "white", "FontWeight", "Bold");


