
limpiar

Nombre_archivo='sujeto_2_hombre.csv';
fs=190;
N_canales=3;
N_movimientos=12;
N_repeticiones=20;

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

 [Datos]=filtrar_picos(Datos,N_senales,Nombre_archivo,N_canales,Tiempo,Nombres_canales);
 