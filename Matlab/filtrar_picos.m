%% Borrar valores atipicos

function[Datos]=filtrar_picos(Datos,N_senales,Nombre_archivo,N_canales,Tiempo,Nombres_canales,n)

for x=1:1:n
    for i=[2]
        promedio=mean(Datos(:,i));
        borrarbajos=find(promedio*.10 >=Datos(:,i));
        borraraltos=find(promedio*1.1 <=Datos(:,i));
        borrar=[borrarbajos,borraraltos];
        senal=Datos(:,i);
        senal(borrar)=senal(borrar-1);
        Datos(:,i)=senal;
    end

    figure()
    for i=1:1:N_senales
        subplot(N_canales,3,i)
        plot(Tiempo,Datos(:,i));
        sgtitle(Nombre_archivo+" registro completo" )
        title(Nombres_canales(i))
    end
end