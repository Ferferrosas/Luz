
limpiar

Nombre_archivo='fer.csv';
fs=190;
N_canales=2;
N_movimientos=4;
N_repeticiones=10;

[Datos,Registro_banderas,N_pulsos,Nombres_canales,Tiempo,N_senales] = Visualizar_registro(Nombre_archivo,fs,N_canales,N_movimientos,N_repeticiones);

%Ver_frecuencias(Datos,fs)

 for i=3:3:N_senales
     Datos(:,i)= bandpassfilt(93,94,fs,8,Datos(:,i));

    % figure ();
    % subplot(2,1,1);
    % plot(Tiempo, senal);
    % title('Señal de EMG Original');
    % xlabel('Tiempo (ms)');
    % ylabel('Amplitud');
    % subplot(2,1,2);
    % plot(Tiempo, Datos(:,i));
    % title('Señal de EMG Filtrada');
    % xlabel('Tiempo (ms)');
    % ylabel('Amplitud');
 end

for rep=1:1:1
    for i=[1,2,4,5]
        senal_original = Datos(:,i);

        ventana_mediana = 5; 
        senal_filtrada = medfilt1(senal_original, ventana_mediana);
        Datos(:,i)=senal_filtrada;

        figure()
        subplot(2, 1, 1);
        plot(Tiempo, senal_original);
        title('Señal Original');
        subplot(2, 1, 2);
        plot(Tiempo, senal_filtrada);
        title('Señal Filtrada (Filtro Mediano)');
    end
end 

figure()
    for i=1:1:N_senales
        subplot(N_canales,3,i)
        plot(Tiempo,Datos(:,i));
        sgtitle(Nombre_archivo+" registro completo" )
        title(Nombres_canales(i))
    end