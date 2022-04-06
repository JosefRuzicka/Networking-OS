## Kentucky Fried Computines

Este equipo está conformado por Josef Ruzicka, Samantha Romero, Axel Matus y 	Wendy Ortiz.



### Descripción del proyecto

El objetivo es diseñar e implementar un sistema distribuido para registro de vacunación. Se trata de un país en el que cada ciudadano puede vacunarse en cualquier lugar, pero el sistema debe guardar registro de esa vacuna en las bases de datos específicas del lugar donde reside el ciudadano. Este país está formado por provincias, que a su vez cuentan con cantones y estos con áreas de salud específicas.
Las bases de datos donde se almacena la información de vacunación se encuentran en las áreas de salud. No obstante, es posible también que un área de salud esté encargada de almacenar la información de otras áreas. Por otra parte, las áreas de salud son también las encargadas de recibir ciudadanos para vacunación y de ingresar los datos respectivos. Por esta razón, en las áreas de salud hay un servidor y múltiples clientes con una aplicación que permite a un usuario ingresar información de vacunación. Finalmente, existe una red de comunicación que conecta todas las áreas de salud del país.

 - ### Etapa I -Anillo Externo: Recolección de datos
En cada área de salud hay un servidor y n máquinas cliente que se conectan al servidor para que funcionarios del área de salud ingresen la información de vacunación del día. 
Para cumplir con los requerimientos anteriores se realizó lo siguiente:

 #### Diagrama Diseño:
Con el fin de entender el programa y su estructura de manera rápida y sencilla, se puede analizar el siguiente diagrama:

![](https://i.imgur.com/bNVYBO8.png)



 
 #### Algunas funcionalidades de esta etapa:
 1. En esta etapa el usuario es autentificado por el servidor, con un usuario y contraseña.
2. Además el usuario podrá ingresar un archivo con la información referente a la vacunación de las personas, este archivo se definió de forma grupal como un .csv, para poder utilizar como delimitador la coma, además de poder manejar la información de una manera más óptima. Los datos descritos en este archivo tendrán la forma de: cédula, Provincia, Cantón y Área de salud, lo anterior para tener un archivo general para cumplir con el requerimiento de que todos los proyectos deben funcionar entre sí. 
3. Para esta etapa la comunicación entre cliente y servidor se realizó haciendo la simulación del protocolo UDP, en donde el paquete se simula con un string que al final incluye el número de paquete de tantos, esto para poder mantener el control de flujo y una transmisión confiable. El formato luego de simular el paquete quedaría de la siguiente forma:  117000951,01,02,03,0000,0026,0001,0000, donde los primeros 0000 indican número de mensaje que se va enviar, 0026 total de mensajes por enviar, el 0001 es el window size, y el último 0000 es el tamaño del paquete. En caso de no enviar el paquete se vuelve a realizar el proceso hasta que llegue correctamente, si llega corrupto se envía un cero en cuatro Bytes, que indica error y si llega correctamente el server responde de forma óptima. 
5. El Servidor es capaz de atender a distintos clientes en hilos separados, por lo que se logra un servidor concurrente para esto se crea un hilo por cliente.
6. Para esta etapa se simula un pipe con una librería.
7. Con respecto a los procesos se crea un proceso padre y uno hijo, con el cual se simula la comunicación entre procesos.


## Compilación y Corrida
En dos terminales de linux distintas buscamos nuestro proyecto, en una digitamos "python3 server.py", luego de establecer esa conexión y que server.py esté corriendo. En la otra terminal escribimos python3 UDPClient.py para conectar al cliente


