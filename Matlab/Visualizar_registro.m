%% Leer un excel, extraer datos y graficarlos

function [Datos,Registro_banderas,N_pulsos,Nombres_canales,Tiempo,N_senales] = Visualizar_registro(Nombre_archivo,fs,N_canales,N_movimientos,N_repeticiones)
%function [Datos,Registro_banderas,N_pulsos,Nombres_canales,Tiempo] = Visualizar_registro('sujeto_3_hombre.csv',190,3,12,20)

% Extracción de datos
Datos=readmatrix(Nombre_archivo);
N_senales=(N_canales*3);
Registro_banderas=Datos(:,N_senales+1);
N_pulsos=N_repeticiones*N_movimientos;
Nombres_canales=["IR flexor", "R flexor","EMG flexor",  "IR extensor", "R extensor", "EMG extensor",  "IR braquiradial", "R braquiradial", "EMG braquiradial"];

%Declarar vector de tiempo
[Tiempo]=Vector_tiempo(Datos,fs);

%Graficar datos
figure()
for i=1:1:N_senales
    subplot(N_canales,3,i)
    plot(Tiempo,Datos(:,i));
    sgtitle(Nombre_archivo + " registro completo" )
    title(Nombres_canales(i))
end

end
