function [] = picos(Datos,ventana_mediana,)

for rep=1:1:3
    for i=[1,2]
        senal_original = Datos(:,i);

        ventana_mediana = 5; 
        Datos(:,i) = medfilt1(senal_original, ventana_mediana);
       
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
end