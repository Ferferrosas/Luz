%% Crear vector de tiempo

function[Tiempo]=Vector_tiempo(Datos,fs)

L_total=(length(Datos(:,1)))/fs;
Tiempo = (0:1/fs:L_total-(1/fs))';

end