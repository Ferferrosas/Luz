function grafica(Datos,Nombres_canales,Nombre_archivo,Tiempo,N_senales,N_canales)
    figure()
    for i=1:1:N_senales
        subplot(N_canales,3,i)
        plot(Tiempo,Datos(:,i));
        sgtitle(Nombre_archivo+" registro completo" )
        title(Nombres_canales(i))

    end
end