function [Datos] = picos(Datos,ventana_mediana)
    for i=[1,2,4,5]
        senal_original = Datos(:,i);
        Datos(:,i) = medfilt1(senal_original, ventana_mediana);
        % figure()
        % subplot(2, 1, 1);
        % plot(Tiempo, senal_original);
        % title('Señal Original');
        % subplot(2, 1, 2);
        % plot(Tiempo, senal_filtrada);
        % title('Señal Filtrada (Filtro Mediano)');
    end

end