%% solo para graficar los datos
clc; close all; clear;
%% Definición de banderas
%Tiempo_contracion=9;
Banderas_Movimientos=[301,401,501,601,701,801,901,1001,1101,1201,1301,1401,1501,1601];
%Banderas_Movimientos=[601,501,301,401];
%Nombres_Movimientos=["Mano abierta","Puño","Flexión muñeca","Extensión muñeca"];

Nombres_Movimientos=["Flexión muñeca","Extensión muñeca","Puño","Mano abierta","Aducción muñeca"...
 ,"Abducción muñeca","Señalar","Pinza doble","Pinza simple","Pinza medio",...
"Pinza anular","Pinza meñique"];
%% Extracción de datos
%data = table2array(readtable('fer.csv'));
data=readmatrix('fer.csv');
fs = 190;
N_canales=3;
N_senales=(N_canales*3);
Registro_banderas=data(:,N_senales+1);
N_movimientos=12;
N_repeticiones=20;
N_pulsos=N_repeticiones*N_movimientos;
Nombres_canales=["IR Canal 1", "R Canal 1","EMG Canal 1",  "IR Canal 2", "R Canal 2", "EMG Canal 2"];

Datos= data;
%% Graficar datos
%Declarar vector de tiempo
L_total=(length(data(:,1)))/190;
Tiempo = (0:1/190:L_total-(1/190))';


figure()
for i=1:1:N_senales
    subplot(N_canales,3,i)
    plot(Tiempo,Datos(:,i));
    sgtitle("Sujeto 1 registro completo" )
    title(Nombres_canales(i))
end

%% borrar valores atipicos
for i=1:1:N_senales
    promedio=mean(Datos(:,i));
    borrarbajos=find(promedio*.10 >=Datos(:,i));
    borraraltos=find(promedio*1.1 <=Datos(:,i));
    borrar=[borrarbajos,borraraltos];
    senal=Datos(:,i);
    senal(borrar)=promedio;
    Datos(:,i)=senal;
end

figure()
for i=1:1:N_senales
    subplot(N_canales,3,i)
    plot(Tiempo,Datos(:,i));
    sgtitle("Sujeto 1 registro completo" )
    title(Nombres_canales(i))
end

%% Juntar los canales por tipo de señal

figure()
subplot(3,1,1)
hold on;
plot(Tiempo,Datos(:,1));
plot(Tiempo,Datos(:,4));
%plot(Tiempo,Datos(:,7));
title(Nombres_canales(1))
subplot(3,1,2)
hold on;
plot(Tiempo,Datos(:,2));
plot(Tiempo,Datos(:,5));
%plot(Tiempo,Datos(:,8));
title(Nombres_canales(2))
subplot(3,1,3)
hold on;
plot(Tiempo,Datos(:,3));
plot(Tiempo,Datos(:,6));
%plot(Tiempo,Datos(:,9));
title(Nombres_canales(3))
sgtitle("Sujeto 1 registro completo" )

%% Fourier
emg_fft = fft(Datos(:,6));
N = length(Datos(:,6)); % Longitud de la señal
frequencies = (0:N-1) * (fs/N);

amplitude_spectrum = abs(emg_fft);
figure()
plot(frequencies, amplitude_spectrum);
xlabel('Frecuencia (Hz)');
ylabel('Amplitud');
title('Espectro de Amplitud');
%% Filtro EMG

for i=3:3:N_senales
    senal=Datos(:,i); %cambiar este por 3 y 6
    Datos(:,i)= bandpassfilt(93,94,190,8,senal);
    
    figure ();
    subplot(2,1,1);
    plot(Tiempo, senal);
    title('Señal de EMG Original');
    xlabel('Tiempo (ms)');
    ylabel('Amplitud');
    subplot(2,1,2);
    plot(Tiempo, Datos(:,i));
    title('Señal de EMG Filtrada');
    xlabel('Tiempo (ms)');
    ylabel('Amplitud');
end

%% restar la media para ver bien las señales
Datos_bajados=zeros(length(Datos(:,1)),N_senales);
mean_data = Datos(1,:);
for i=1:1:N_senales
    Datos_bajados(:,i) = Datos(:,i) - mean_data(i);
end
%Datos_bajados= Datos;
%% Marcar movimientos
Posiciones_contracciones=zeros(N_repeticiones,N_movimientos);
%buscar los incios de las banderas
for i=1:1:N_movimientos%movimientos
    Posiciones_contracciones(:,i)=find(Banderas_Movimientos(i)==Registro_banderas);
end
x=reshape(Posiciones_contracciones, N_pulsos, 1);

%line([Tiempo(x(1)) Tiempo(x(1))], ylim, 'Color', 'g', 'LineStyle', '--')

figure()
subplot(3,1,1)
hold on;
plot(Tiempo,Datos_bajados(:,1));
plot(Tiempo,Datos_bajados(:,4));
xlim([-inf, inf])
ylim([-1000, 1000])
for i=1:1:N_pulsos
    if(rem(i-1, N_repeticiones)~=0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'g', 'LineStyle', '--')
    elseif(rem(i-1, N_repeticiones)==0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'k', 'LineStyle', '--')
    end
end

title("Ir")
subplot(3,1,2)
hold on;
plot(Tiempo,Datos_bajados(:,2));
plot(Tiempo,Datos_bajados(:,5));
xlim([-inf, inf])
ylim([-2000, 2000])
for i=1:1:N_pulsos
    if(rem(i-1, N_repeticiones)~=0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'g', 'LineStyle', '--')
    elseif(rem(i-1, N_repeticiones)==0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'k', 'LineStyle', '--')
    end
end
title("R")
subplot(3,1,3)
hold on;
plot(Tiempo,Datos_bajados(:,3));
plot(Tiempo,Datos_bajados(:,6));
for i=1:1:N_pulsos
    if(rem(i-1, N_repeticiones)~=0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'g', 'LineStyle', '--')
    else
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'k', 'LineStyle', '--')
    end
end
xlim([-inf, inf])
ylim([-inf, inf])
title("emg")
sgtitle("Sujeto 1 registro completo menos promedio" )

%% Ver orden y movimientos realizados
Movs=Registro_banderas;
Zeros=find(0==Registro_banderas);
Movs(Zeros)=[];
disp("Mano abierta , Puño , Flexión muñeca , Extensión muñeca");

%% Segmentar movimientos

Ir=[]; R=[]; Emg=[];Ir2=[]; R2=[]; Emg2=[];
for m=1:1:N_movimientos %movimientos
    for rep=1:1:N_repeticiones %repetición
        Ir=[Ir;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,1)'];
        R=[R;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,2)'];
        Emg=[Emg;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,3)'];
        Ir2=[Ir2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,4)'];
        R2=[R2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,5)'];
        Emg2=[Emg2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,6)'];
    end
end

for m=1:1:N_pulsos
    [env_Emg(m,:),] = envelope(abs(Emg(m,:)),190);
    [env_Emg2(m,:),] = envelope(abs(Emg2(m,:)),190);
end

%% Promedios y Std

m=1;
Inicio_Mov=N_repeticiones-1;
for mov=N_repeticiones:N_repeticiones:N_pulsos
    promedios_Ir(m,:)=mean(Ir(mov-Inicio_Mov:mov,:));
    promedios_R(m,:)=mean(R(mov-Inicio_Mov:mov,:));
    promedios_Env(m,:)=mean(env_Emg(mov-Inicio_Mov:mov,:));
    std_Ir(m,:)=std(Ir(mov-Inicio_Mov:mov,:));
    std_R(m,:)=std(R(mov-Inicio_Mov:mov,:));
    std_Env(m,:)=std(env_Emg(mov-Inicio_Mov:mov,:));
    
    promedios_Ir2(m,:)=mean(Ir2(mov-Inicio_Mov:mov,:));
    promedios_R2(m,:)=mean(R2(mov-Inicio_Mov:mov,:));
    promedios_Env2(m,:)=mean(env_Emg2(mov-Inicio_Mov:mov,:));
    std_Ir2(m,:)=std(Ir2(mov-Inicio_Mov:mov,:));
    std_R2(m,:)=std(R2(mov-Inicio_Mov:mov,:));
    std_Env2(m,:)=std(env_Emg2(mov-Inicio_Mov:mov,:));
    m=m+1;
end


%% Graficas

L_pulso=(length(promedios_Ir(1,:)))/190;
Tiempo = (0:1/190:L_pulso-(1/190))';

colores=["g" "b" "y" "c" "k"  "r" "m" "w"];
i=0;
figure()
for mov=1:1:N_movimientos
    subplot(3,1,1)
    plot(Tiempo,promedios_Ir(mov,:),colores(mov), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(1))
    xlabel("Tiempo (seg)")
    hold on
    subplot(3,1,2)
    plot(Tiempo,promedios_R(mov,:),colores(mov), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(2))
    xlabel("Tiempo (seg)")
    hold on
    subplot(3,1,3)
    plot(Tiempo,promedios_Env(mov,:),colores(mov), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(3))
    xlabel("Tiempo (seg)")
    hold on
    %    legend("Mano abierta" , "Puño" , "Flexión muñeca" , "Extensión muñeca");
    sgtitle(" Promedios de movimientos Sensor 1" )
end

figure()
for mov=1:1:N_movimientos
    subplot(3,1,1)
    plot(Tiempo,promedios_Ir2(mov,:),colores(mov+3), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(4))
    xlabel("Tiempo (seg)")
    hold on
    subplot(3,1,2)
    plot(Tiempo,promedios_R2(mov,:),colores(mov+3), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(5))
    xlabel("Tiempo (seg)")
    hold on
    subplot(3,1,3)
    plot(Tiempo,promedios_Env2(mov,:),colores(mov+3), 'LineWidth',1);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(6))
    xlabel("Tiempo (seg)")
    hold on
    %legend("Mano abierta" , "Puño" , "Flexión muñeca" , "Extensión muñeca");
    sgtitle(" Promedios de movimientos Sensor 1" )
end

%% STD

for mov=1:1:N_movimientos
    figure()
    subplot(3,1,1)
    %sensor 1
    curve1 = promedios_Ir(mov+i,:) + std_Ir(mov,:);
    curve2 = promedios_Ir(mov+i,:) - std_Ir(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir(mov,:), colores(mov), 'LineWidth',2);
    %sensor 2
    curve1 = promedios_Ir2(mov+i,:) + std_Ir2(mov,:);
    curve2 = promedios_Ir2(mov+i,:) - std_Ir2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir2(mov,:), colores(mov+3), 'LineWidth',2);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(1))
    xlabel("Tiempo (seg)")
    %rojo
    subplot(3,1,2)
    curve1 = promedios_R(mov,:) + std_R(mov,:);
    curve2 = promedios_R(mov,:) - std_R(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R(mov,:),colores(mov), 'LineWidth',2);
    %sensor 2
    curve1 = promedios_R2(mov,:) + std_R2(mov,:);
    curve2 = promedios_R2(mov,:) - std_R2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(2))
    xlabel("Tiempo (seg)")
    % env
    subplot(3,1,3)
    curve1 = promedios_Env(mov,:) + std_Env(mov,:);
    curve2 = promedios_Env(mov,:) - std_Env(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env(mov,:),colores(mov), 'LineWidth',2);
    %sensor 2
    curve1 = promedios_Env2(mov,:) + std_Env2(mov,:);
    curve2 = promedios_Env2(mov,:) - std_Env2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-inf inf])
    xlim([-inf inf])
    title(Nombres_canales(3))
    xlabel("Tiempo (seg)")
    
    sgtitle("Promedio " + Nombres_Movimientos(mov) )
    
end


figure()
n=1;
for mov=1:1:N_movimientos
    
    subplot(3,5,n)
    hold on;
    curve1 = promedios_Ir(mov,:) + std_Ir(mov,:);
    curve2 = promedios_Ir(mov,:) - std_Ir(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir(mov,:), colores(mov), 'LineWidth',2);
    ylim([-400 700])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " IR ")
    xlabel("Tiempo (seg)")
    
    
    subplot(3,5,n+5)
    curve1 = promedios_R(mov,:) + std_R(mov,:);
    curve2 = promedios_R(mov,:) - std_R(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R(mov,:),colores(mov), 'LineWidth',2);
    ylim([-400 1300])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " R" )
    xlabel("Tiempo (seg)")
    
    
    subplot(3,5,n+10)
    curve1 = promedios_Env(mov,:) + std_Env(mov,:);
    curve2 = promedios_Env(mov,:) - std_Env(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env(mov,:),colores(mov), 'LineWidth',2);
    ylim([-1 6])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " EMG" )
    xlabel("Tiempo (seg)")
    
    sgtitle("Promedios + std sensor 1")
    n=n+1;
end

figure()
n=1;
for mov=1:1:4
    %Sensor 2
    
    subplot(3,5,n)
    hold on;
    curve1 = promedios_Ir2(mov,:) + std_Ir2(mov,:);
    curve2 = promedios_Ir2(mov,:) - std_Ir2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir2(mov,:), colores(mov+3), 'LineWidth',2);
    ylim([-400 700])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " IR ")
    xlabel("Tiempo (seg)")
    
    
    subplot(3,5,n+5)
    curve1 = promedios_R2(mov,:) + std_R2(mov,:);
    curve2 = promedios_R2(mov,:) - std_R2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-400 1300])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " R" )
    xlabel("Tiempo (seg)")
    
    
    subplot(3,5,n+10)
    curve1 = promedios_Env2(mov,:) + std_Env2(mov,:);
    curve2 = promedios_Env2(mov,:) - std_Env2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-1 6])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " EMG" )
    xlabel("Tiempo (seg)")
    
    sgtitle("Promedios + std sensor 2 ")
    n=n+1;
    
end

% std  juntas

figure()
n=1;
for mov=1:1:N_movimientos
    
    subplot(3,1,1)
    hold on;
    curve1 = promedios_Ir(mov,:) + std_Ir(mov,:);
    curve2 = promedios_Ir(mov,:) - std_Ir(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir(mov,:), colores(mov), 'LineWidth',2);
    ylim([-800 800])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " IR ")
    xlabel("Tiempo (seg)")
    
    
    subplot(3,1,2)
    curve1 = promedios_R(mov,:) + std_R(mov,:);
    curve2 = promedios_R(mov,:) - std_R(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R(mov,:),colores(mov), 'LineWidth',2);
    ylim([-2000 2000])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " R" )
    xlabel("Tiempo (seg)")
    
    
    subplot(3,1,3)
    curve1 = promedios_Env(mov,:) + std_Env(mov,:);
    curve2 = promedios_Env(mov,:) - std_Env(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env(mov,:),colores(mov), 'LineWidth',2);
    ylim([-1 6])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " EMG" )
    xlabel("Tiempo (seg)")
    
    sgtitle("Promedios + std sensor 1")
    n=n+1;
end

figure()
n=1;
for mov=1:1:N_movimientos
    %Sensor 2
    
    subplot(3,1,1)
    hold on;
    curve1 = promedios_Ir2(mov,:) + std_Ir2(mov,:);
    curve2 = promedios_Ir2(mov,:) - std_Ir2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Ir2(mov,:), colores(mov+3), 'LineWidth',2);
    ylim([-800 800])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " IR ")
    xlabel("Tiempo (seg)")
    
    
    subplot(3,1,2)
    curve1 = promedios_R2(mov,:) + std_R2(mov,:);
    curve2 = promedios_R2(mov,:) - std_R2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_R2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-2000 2000])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " R" )
    xlabel("Tiempo (seg)")
    
    
    subplot(3,1,3)
    curve1 = promedios_Env2(mov,:) + std_Env2(mov,:);
    curve2 = promedios_Env2(mov,:) - std_Env2(mov,:);
    Tiempo2 = [Tiempo', fliplr(Tiempo')];
    inBetween = [curve1, fliplr(curve2)];
    Relleno=fill(Tiempo2, inBetween,colores(mov+3),'FaceAlpha',0.1);
    Relleno.EdgeColor = colores(mov+3);
    Relleno.LineWidth = .5;
    hold on;
    plot(Tiempo,promedios_Env2(mov,:),colores(mov+3), 'LineWidth',2);
    ylim([-1 6])
    xlim([-inf inf])
    title(Nombres_Movimientos(mov)+ " EMG" )
    xlabel("Tiempo (seg)")
    
    sgtitle("Promedios + std sensor 2 ")
    n=n+1;
    
end

%% Sacar caracteristicas

%Toolbox de features de matlab %https://la.mathworks.com/matlabcentral/fileexchange/
% 71514-emg-feature-extraction-toolbox


caractetistica=["fzc" "ewl" "emav" "asm" "ass"  "ltkeo" "card" "ldasdv"...
    "ldamv" "dvarv" "mfl" "myop" "ssi" "vo" "tm" "aac" "mmav"...
    "mmav2" "iemg" "dasdv" "damv" "rms" "vare" "wa" "ld" "mav" "zc"...
    "ssc" "wl" "mad" "iqr" "kurt" "skew" "cov" "sd" "var" "ae"];

for m = 1:1:N_pulsos
    for n =1:length(caractetistica)
        Ir_ft(n,m) = jfemg(caractetistica(n), Ir(m,:));
        R_ft(n,m) = jfemg(caractetistica(n), R(m,:));
        Emg_ft(n,m) = jfemg(caractetistica(n), Emg(m,:));
        Ir2_ft(n,m) = jfemg(caractetistica(n), Ir2(m,:));
        R2_ft(n,m) = jfemg(caractetistica(n), R2(m,:));
        Emg2_ft(n,m) = jfemg(caractetistica(n), Emg2(m,:));
    end
end


%Matriz de 40x223, que representa los 4 movimientos repetidos 10 veces, las
%37 caracteristicas de cada canal, 37*6=222 + 1 fila que define el
%movmiento

m=1;
guia=[];
for im = 1:N_movimientos
    for i = 1:N_repeticiones
        guia=[guia;Banderas_Movimientos(im)];
        m=m+1;
    end
end

%close all

%% Sacar caracteristicas en un excel

Mat_completa =[Ir_ft',Ir2_ft',R_ft',R2_ft',Emg_ft',Emg2_ft',guia];
% Especificar el nombre del archivo
nombreArchivo = 'matriz_Ft.csv';
writematrix( Mat_completa, nombreArchivo);
%% Chi2

% Graficas de disperción
color=["g" "b" "y" "c" "k"  "r" "m" "w"];

% disperción de las 3 mejores caracteristicas generales

Mat_completa =[Ir_ft',Ir2_ft',R_ft',R2_ft',Emg_ft',Emg2_ft'];
%caractetistica=[caractetistica,caractetistica,caractetistica,caractetistica,caractetistica,caractetistica];
[idx,scores] = fscchi2(Mat_completa,guia);

cnt = 1;
figure()
for n = 1:N_repeticiones:N_pulsos
    scatter3(Mat_completa(n:n+Inicio_Mov,idx(1)), Mat_completa(n:n+Inicio_Mov,idx(2)),Mat_completa(n:n+Inicio_Mov,idx(3)),color(cnt),'filled')
    hold on
    title("Todos los canales FT")
    cnt = cnt+1;
end
legend

%% Ranking de las caracteriticas
%vector con el nombre de las caracteristicas y el canal
nombres_caracterisiticas=[];
%nombre de canales acomodados como la matriz de caracteristicas
canales=["IR Canal 1" "IR Canal 2" "R Canal 1" "R Canal 2" "EMG Canal 1"  "EMG Canal 2"];

for i=1:1:N_senales
    for  c=1:1:37    %caracteristicas
        nombres_caracterisiticas=[nombres_caracterisiticas,caractetistica(1,c)+' ' + canales(1,i) ];
    end
end

for i=1:1:3 %cambiar segun el numero de caracteriticas que quiera ver m = [10,15,20,25,30,50]
    fprintf('La característica N° %d es : %s \n', i, nombres_caracterisiticas(idx(i)));
end

%% graficas ranking

idxInf = find(isinf(scores));
figure()
bar(scores(idx))
xlabel('Predictor rank')
ylabel('Predictor importance score')

%% Clasificación

% Apply Croos-Validation and Different Classifiers to predict data (LDA, SVM, KNN, DT,NB),
% returns the variable Fran with the average after apply the classifiers.

A=5;
N_movimientos=4;
N_repeticiones=10;
%m = [3,10,15,20,25,30,50]; % Select quantity of best features.
m = [15,20,25,30,50];
%close all;
for n = 1:length(m)
    [LDA_FRan(:,n),SVM_FRan(:,n),KNN_FRan(:,n),DT_FRan(:,n), NB_FRan(:,n)] = ...
        xvalidation_FtRan(Mat_completa, guia, A, N_movimientos,N_repeticiones,idx,m,n);
end

LDA_FRan
SVM_FRan
KNN_FRan
DT_FRan
NB_FRan

LDA = mean(LDA_FRan);
SVM = mean(SVM_FRan);
KNN = mean(KNN_FRan);
DT = mean(DT_FRan);
NB = mean(NB_FRan);

ResultT= [LDA SVM KNN DT NB]
%ResultT = [LDA NB]

% -------------------------------------------------------------------------
%%  Pruebas con diferentes combinaciones de caracterisisticas
% -------------------------------------------------------------------------
% propuesta de pruebas de caracteristicas para la clasificación

Mat={Ir_ft',Ir2_ft',R_ft',R2_ft',Emg_ft',Emg2_ft'};

for i=1:1:6
    [idx,scores] = fscchi2(Mat{1,i},guia);
    
    cnt = 1;
    figure()
    for n = 1:10:40
        scatter3(Mat{1,i}(n:n+9,idx(1)), Mat{1,i}(n:n+9,idx(2)),Mat{1,i}(n:n+9,idx(3)),color(cnt),'filled')
        hold on
        title("Mejores 3 caracteristica de " + canales(i))
        cnt = cnt+1;
    end
    
    %fprintf('La característica N° 1, 2 y 3 del canal %d son: %s ,%s , %s \n',i,caractetistica(idx(1)), caractetistica(idx(2)), caractetistica(idx(3)));
end

%% Clasificación con diferentes combinaciones

Mat_completa =[Ir_ft',Ir2_ft',R_ft',R2_ft',Emg_ft',Emg2_ft'];
Mat_EMG=[Emg_ft',Emg2_ft'];
Mat_IR=[Ir_ft',Ir2_ft'];
Mat_R=[R_ft',R2_ft'];
Mat_EMG_IR=[Ir_ft',Ir2_ft',Emg_ft',Emg2_ft'];
Mat_EMG_R=[R_ft',R2_ft',Emg_ft',Emg2_ft'];
Mat_IR_R=[Ir_ft',Ir2_ft',R_ft',R2_ft'];

Mat={Mat_EMG,Mat_IR,Mat_R,Mat_EMG_IR,Mat_EMG_R,Mat_IR_R};
Result=[];
for Nm=1:1:length(Mat) % numero de matrices
    
    %Chi2
    % Graficas de disperción
    color=["g" "b" "y" "c" "k"  "r" "m" "w"];
    
    % disperción de las 3 mejores caracteristicas generales
    
    [idx,scores] = fscchi2(Mat{1,Nm},guia);
    
    cnt = 1;
    figure()
    for n = 1:N_repeticiones:N_pulsos
        scatter3(Mat{1,Nm}(n:n+9,idx(1)), Mat{1,Nm}(n:n+9,idx(2)),Mat{1,Nm}(n:n+9,idx(3)),color(cnt),'filled')
        hold on
        title("Mejores 3 caracteristica")
        cnt = cnt+1;
    end
    legend
    
    % Ranking de las caracteriticas
    %vector con el nombre de las caracteristicas y el canal
    nombres_caracterisiticas=[];
    %nombre de canales acomodados como la matriz de caracteristicas
    canales_Mat_EMG=["Emg_ft","Emg2_ft"];
    canales_Mat_IR=["Ir_ft","Ir2_ft"];
    canales_Mat_R=["R_ft","R2_ft"];
    canales_Mat_EMG_IR=["Ir_ft","Ir2_ft","Emg_ft","Emg2_ft"];
    canales_Mat_EMG_R=["R_ft","R2_ft","Emg_ft","Emg2_ft"];
    canales_Mat_IR_R=["Ir_ft","Ir2_ft","R_ft","R2_ft"];
    
    Todos_los_canales={canales_Mat_EMG,canales_Mat_IR,canales_Mat_R,canales_Mat_EMG_IR,canales_Mat_EMG_R,canales_Mat_IR_R};
    
    
    for i=1:1:length(Todos_los_canales{1,Nm}) %canales
        for  c=1:1:37    %caracteristicas
            nombres_caracterisiticas=[nombres_caracterisiticas,caractetistica(1,c)+' ' + Todos_los_canales{1,Nm}(1,i) ];
        end
    end
    
    for i=1:1:10 %cambiar segun el numero de caracteriticas que quiera ver m = [10,15,20,25,30,50]
       % fprintf('La característica N° %d es : %s \n', i, nombres_caracterisiticas(idx(i)));
    end
    
    % graficas ranking
    
    idxInf = find(isinf(scores));
    figure()
    bar(scores(idx))
    xlabel('Predictor rank')
    ylabel('Predictor importance score')
    
    % Clasificación
    
    A=5;
    m = [5,10,15];
    for n = 1:length(m)
        [LDA_FRan(:,n),SVM_FRan(:,n),KNN_FRan(:,n),DT_FRan(:,n), NB_FRan(:,n)] = ...
            xvalidation_FtRan(Mat{1,Nm}, guia, A, N_movimientos,N_repeticiones,idx,m,n);
    end
    
    LDA_FRan;
    SVM_FRan;
    KNN_FRan;
    DT_FRan;
    NB_FRan;
    
    LDA = mean(LDA_FRan);
    SVM = mean(SVM_FRan);
    KNN = mean(KNN_FRan);
    DT = mean(DT_FRan);
    NB = mean(NB_FRan);
    
    %Result = [LDA SVM KNN DT NB]
    Result = [Result;LDA SVM KNN DT NB];
end

Result

%% Caracteriticas temporales

incremento=47;

Ir_t=[]; R_t=[]; Env_t=[];Ir2_t=[];R2_t=[];Env2_t=[];
for rep=1:1:N_pulsos
    ventana=380;
    for punto=1:1:9
        Ir_t(rep,punto) = Ir(rep,ventana);
        R_t(rep,punto) = R(rep,ventana);
        env_Emg_t(rep,punto) = env_Emg(rep,ventana);
        Ir2_t(rep,punto) = Ir2(rep,ventana);
        R2_t(rep,punto) = R2(rep,ventana);
        env_Emg2_t(rep,punto) = env_Emg2(rep,ventana);
        ventana=ventana+incremento;
    end
end

%% Reconstrucción de la señal

L_pulso_T=(9*40)/4.5;
Tiempo_T = (0:1/4.5:L_pulso_T-(1/4.5))';
temporales={Ir_t,R_t,env_Emg_t,Ir2_t,R2_t,env_Emg2_t};
%if(rem(mov-1, 10)~=0)
incremento=8;

figure()
for i=1:1:N_senales
    inicio=1;
    for mov=1:1:N_pulsos
        subplot(3,2,i)
        plot(Tiempo_T(inicio:inicio+incremento,:),temporales{1,i}(mov,:),'LineWidth',1);
        ylim([-inf inf])
        xlim([-inf inf])
        title(Nombres_canales(1))
        hold on
        sgtitle("Reconstruccion senales caracteristicas temporales" )
        inicio=inicio+incremento;
    end
end

%% Clasificación caracteristicas temporales

Mat_completa_t =[Ir_t,Ir2_t,R_t,R2_t,env_Emg_t,env_Emg2_t];


%Chi2
% Graficas de disperción
color=["g" "b" "y" "c" "k"  "r" "m" "w"];

% disperción de las 3 mejores caracteristicas generales

[idx,scores] = fscchi2(Mat_completa_t,guia);

cnt = 1;
figure()
for n = 1:N_repeticiones:N_pulsos
    scatter3(Mat_completa_t(n:n+Inicio_Mov,idx(1)), Mat_completa_t(n:n+Inicio_Mov,idx(2)),Mat_completa_t(n:n+Inicio_Mov,idx(3)),color(cnt),'filled')
    hold on
    title("todos los canales FT temporales")
    cnt = cnt+1;
end
legend

% Clasificación

A=5;
m = [20,30,40,50,54];
for n = 1:length(m)
    [LDA_FRan(:,n),SVM_FRan(:,n),KNN_FRan(:,n),DT_FRan(:,n), NB_FRan(:,n)] = ...
        xvalidation_FtRan(Mat_completa_t, guia, A, N_movimientos,N_repeticiones,idx,m,n);
end

LDA_FRan
SVM_FRan
KNN_FRan
DT_FRan
NB_FRan

LDA = mean(LDA_FRan);
SVM = mean(SVM_FRan);
KNN = mean(KNN_FRan);
DT = mean(DT_FRan);
NB = mean(NB_FRan);

%Result = [LDA SVM KNN DT NB]
ResultT_t = [LDA SVM KNN DT NB]



%% Clasificación con diferentes combinaciones temporales
Mat_EMG_t=[env_Emg_t,env_Emg2_t];
Mat_IR_t=[Ir_t,Ir2_t];
Mat_R_t=[R_t,R2_t];
Mat_EMG_IR_t=[Ir_t,Ir2_t,env_Emg_t,env_Emg2_t];
Mat_EMG_R_t=[R_t,R2_t,env_Emg_t,env_Emg2_t];
Mat_IR_R_t=[Ir_t,Ir2_t,R_t,R2_t];

Mat_t={Mat_EMG_t,Mat_IR_t,Mat_R_t,Mat_EMG_IR_t,Mat_EMG_R_t,Mat_IR_R_t};
Result_t=[];
for Nm=1:1:length(Mat_t) % numero de matrices
    
    %Chi2
    % Graficas de disperción
    color=["g" "b" "y" "c" "k"  "r" "m" "w"];
    
    % disperción de las 3 mejores caracteristicas generales
    
    [idx,scores] = fscchi2(Mat_t{1,Nm},guia);
    
    cnt = 1;
    figure()
    for n = 1:N_repeticiones:N_pulsos
        scatter3(Mat_t{1,Nm}(n:n+Inicio_Mov,idx(1)), Mat_t{1,Nm}(n:n+Inicio_Mov,idx(2)),Mat_t{1,Nm}(n:n+Inicio_Mov,idx(3)),color(cnt),'filled')
        hold on
        title("Mejores 3 caracteristica")
        cnt = cnt+1;
    end
    legend
    
    % Clasificación
    
    A=5;
    m = [6,12,18];
    for n = 1:length(m)
        [LDA_FRan(:,n),SVM_FRan(:,n),KNN_FRan(:,n),DT_FRan(:,n), NB_FRan(:,n)] = ...
            xvalidation_FtRan(Mat_t{1,Nm}, guia, A, N_movimientos,N_repeticiones,idx,m,n);
    end
    
    LDA_FRan;
    SVM_FRan;
    KNN_FRan;
    DT_FRan;
    NB_FRan;
    
    LDA = mean(LDA_FRan);
    SVM = mean(SVM_FRan);
    KNN = mean(KNN_FRan);
    DT = mean(DT_FRan);
    NB = mean(NB_FRan);
    
    %Result = [LDA SVM KNN DT NB]
    Result_t = [Result_t;LDA SVM KNN DT NB];
end

Result_t