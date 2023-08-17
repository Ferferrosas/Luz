%% Graficar Fourier

function[]=Ver_frecuencias(Datos,fs)

s_fft = fft(Datos(:,6));
N = length(Datos(:,6)); % Longitud de la señal
frequencies = (0:N-1) * (fs/N);

amplitude_spectrum = abs(s_fft);
figure()
plot(frequencies, amplitude_spectrum);
xlabel('Frecuencia (Hz)');
ylabel('Amplitud');
title('Espectro de Amplitud');