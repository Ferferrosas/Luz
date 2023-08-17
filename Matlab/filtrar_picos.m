%% Borrar valores atipicos

function[Datos]=filtrar_picos(Datos,N_senales,Nombre_archivo,N_canales,Tiempo,Nombres_canales)

for x=1:1:1
    for i=[1, 2, 4, 5, 7, 8]
        promedio=mean(Datos(:,i));
        borrarbajos=find(promedio*.10 >=Datos(:,i));
        borraraltos=find(promedio*1.1 <=Datos(:,i));
        senal=Datos(:,i);
        senal(borrarbajos)=senal(borrarbajos-1);
        senal(borraraltos)=senal(borraraltos-1);
        Datos(:,i)=senal;
    end
end

figure()
for i=1:1:N_senales
    subplot(N_canales,3,i)
    plot(Tiempo,Datos(:,i));
    sgtitle(Nombre_archivo+" registro completo" )
    title(Nombres_canales(i))
end