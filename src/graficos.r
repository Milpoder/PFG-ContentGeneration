#vectores de tiempo
talg1 <- c(2.05,3.32,4.34,4.65,5.06,7.50,11.65,16.49,27.31,44.67);
talg2 <- c(9.47,24.70,67.09,155.33,278.37,446.81,1144.14,1240.22,1500.64,1924.82)
talg3 <- c(1.09,1.23,1.34,5.01,10.14,13.9,28.21,30.64,36.88,64.91)

#vectores de memoria
malg1 <- c(1.81,1.85,1.87,1.95,2.11,2.23,2.38,2.53,2.64,2.82)
malg2 <- c(2.27,3.81,5.12,7.77,10.9,14.1,19.4,24.1,29.6,31.8)
malg3 <- c(0.5,0.68,0.80,1.01,1.25,1.50,1.93,2.12,2.28,2.50)

tamanio <- c(100,400,900,1600,2500,3600,4900,6400,8100,10000)

#funciones
#x^2
z = seq(0,1000,10)
y = z^2
#x
u = seq(0,4000,400)
t = u

#Gráficas

#TIEMPO
plot(talg2, type="o", col="green", x=tamanio, xlab= "tamaño", ylab= "Tiempo (s)")
lines(talg1, type="o", col="red", x=tamanio)
lines(talg3, type="o", col="blue", x=tamanio)
title(main="TIEMPO", col.main="blue", font.main=4)
legend("topleft", c("Algoritmo 1", "Algoritmo 2", "Algoritmo 3"), cex=0.6, fill = c("red","green","blue"))

#TIEMPO FINAL
plot(z[-11],y[-11], type="o", col="violet", xlab= "tamaño", ylab= "Tiempo (s)",xlim=c(0,10000),ylim=c(0,2000))
lines(u[-11],t[-11],type="o", col="yellow")
lines(talg1, type="o", col="red", x=tamanio)
lines(talg3, type="o", col="blue", x=tamanio)
lines(talg2, type="o", col="green", x=tamanio)
title(main="TIEMPO", col.main="blue", font.main=4)
legend("topleft", c("Algoritmo 1", "Algoritmo 2", "Algoritmo 3", "O(n^2)","O(n)"), cex=0.6, fill = c("red","green","blue","violet","yellow"))

#MEMORIA
plot(malg2, type="o", col="green", xlab= "tamaño", ylab= "Memoria (Gb)")
lines(malg1, type="o", col="red")
lines(malg3, type="o", col="blue")
title(main="MEMORIA RAM", col.main="blue", font.main=4)
legend("topleft", c("Algoritmo 1", "Algoritmo 2", "Algoritmo 3"), cex=0.6, fill = c("red","green","blue"))

