%% solo para graficar los datos
clc; close all; clear;
%% Definición de banderas
%Tiempo_contracion=9;
%Banderas_Movimientos=[301,401,501,601,701,801,901,1001,1101,1201,1301,1401,1501,1601];
Banderas_Movimientos=[601,501,301,401];
Nombres_Movimientos=["Mano abierta","Puño","Flexión muñeca","Extensión muñeca"];

%Nombres_Movimientos=["Flexión muñeca","Extensión muñeca","Puño","Mano abierta","Aducción muñeca"...
% ,"Abducción muñeca","Señalar","Pinza doble","Pinza simple","Pinza medio",...
%"Pinza anular","Pinza meñique"];
%% Extracción de datos
%data = table2array(readtable('fer.csv'));
data=readmatrix('fer.csv');
fs = 190;
N_canales=2;
N_senales=(N_canales*3);
Registro_banderas=data(:,7);
Nombres_canales=["IR Canal 1", "R Canal 1","EMG Canal 1",  "IR Canal 2", "R Canal 2", "EMG Canal 2"];

Datos= data;
%% Graficar datos
%Declarar vector de tiempo
L_total=(length(data(:,1)))/190;
Tiempo = (0:1/190:L_total-(1/190))';


figure()
for i=1:1:6
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
    senal(borrar)=[promedio];
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

for i=3:3:6
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
Posiciones_contracciones=zeros(10,4);
%buscar los incios de las banderas
for i=1:1:4%movimientos
    Posiciones_contracciones(:,i)=find(Banderas_Movimientos(i)==Registro_banderas);
end
x=reshape(Posiciones_contracciones, 40, 1);

%line([Tiempo(x(1)) Tiempo(x(1))], ylim, 'Color', 'g', 'LineStyle', '--')

figure()
subplot(3,1,1)
hold on;
plot(Tiempo,Datos_bajados(:,1));
plot(Tiempo,Datos_bajados(:,4));
xlim([-inf, inf])
ylim([-1000, 1000])
for i=1:1:40
    if(rem(i, 10)~=0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'g', 'LineStyle', '--')
    elseif(rem(i, 10)==0)
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
for i=1:1:40
    if(rem(i, 10)~=0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'g', 'LineStyle', '--')
    elseif(rem(i, 10)==0)
        line([Tiempo(x(i)) Tiempo(x(i))], ylim, 'Color', 'k', 'LineStyle', '--')
    end
end
title("R")
subplot(3,1,3)
hold on;
plot(Tiempo,Datos_bajados(:,3));
plot(Tiempo,Datos_bajados(:,6));
for i=1:1:40
    if(rem(i, 10)~=0)
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
    for m=1:1:4 %movimientos
        for rep=1:1:10 %repetición
            Ir=[Ir;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,1)'];
            R=[R;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,2)'];
            Emg=[Emg;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,3)'];
            Ir2=[Ir2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,4)'];
            R2=[R2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,5)'];
            Emg2=[Emg2;Datos_bajados(Posiciones_contracciones(rep,m)-190:Posiciones_contracciones(rep,m)+1900,6)'];
        end
    end

for m=1:1:40
    [env_Emg(m,:),] = envelope(Emg(m,:),800);
    [env_Emg2(m,:),] = envelope(Emg2(m,:),800);
end

%% Promedios y Std

m=1;
for mov=10:10:40
    promedios_Ir(m,:)=mean(Ir(mov-9:mov,:));
    promedios_R(m,:)=mean(R(mov-9:mov,:));
    promedios_Env(m,:)=mean(env_Emg(mov-9:mov,:));
    std_Ir(m,:)=std(Ir(mov-9:mov,:));
    std_R(m,:)=std(R(mov-9:mov,:));
    std_Env(m,:)=std(env_Emg(mov-9:mov,:));
    
    promedios_Ir2(m,:)=mean(Ir2(mov-9:mov,:));
    promedios_R2(m,:)=mean(R2(mov-9:mov,:));
    promedios_Env2(m,:)=mean(env_Emg2(mov-9:mov,:));
    std_Ir2(m,:)=std(Ir2(mov-9:mov,:));
    std_R2(m,:)=std(R2(mov-9:mov,:));
    std_Env2(m,:)=std(env_Emg2(mov-9:mov,:));
    m=m+1;
end


%% Graficas

L_pulso=(length(promedios_Ir(1,:)))/190;
Tiempo = (0:1/190:L_pulso-(1/190))';

colores=["g" "b" "y" "c" "k"  "r" "m" "w"];
i=0;
figure()
for mov=1:1:4
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
    legend("Mano abierta" , "Puño" , "Flexión muñeca" , "Extensión muñeca");
    sgtitle(" Promedios de movimientos Sensor 1" )
end

figure()
for mov=1:1:4
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
    legend("Mano abierta" , "Puño" , "Flexión muñeca" , "Extensión muñeca");
    sgtitle(" Promedios de movimientos Sensor 1" )
end

%% STD

for mov=1:1:4
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
for mov=1:1:4
    
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
for mov=1:1:4
    
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
for mov=1:1:4
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

for m = 1:1:40
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
for im = 1:4
    for i = 1:10
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
for n = 1:10:40
    scatter3(Mat_completa(n:n+9,idx(1)), Mat_completa(n:n+9,idx(2)),Mat_completa(n:n+9,idx(3)),color(cnt),'filled')
    hold on
    title("Mejores 3 caracteristica")
    cnt = cnt+1;
end
legend
%% Clasificación

% Apply Croos-Validation and Different Classifiers to predict data (LDA, SVM, KNN, DT,NB),
% returns the variable Fran with the average after apply the classifiers.

A=5;
movement=4;
trial=10;
m = [10,15,20,25,30,50]; % Select quantity of best features.
%close all;
for n = 1:length(m)
    [LDA_FRan(:,n), SVM_FRan(:,n), KNN_FRan(:,n), DT_FRan(:,n), NB_FRan(:,n)] = ...
        xvalidation_FtRan(Mat_completa, guia, A, movement,trial,idx,m,n);
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

Result = [LDA SVM KNN DT NB]

