# Material necesario

- Pantalla modelo SSD1306
https://es.aliexpress.com/item/32927682460.html
- 4 cables dupont hembra-hembra (preferiblemente los colores rojo, negro, amarillo, verde. Puedes comprar un surtido y así tienes algunos extra para otros proyectos)
https://es.aliexpress.com/item/1005003269498051.html

# Preparación

Primero debemos soldar la pieza de 4 pines qie acompaña a la pantalla a los 4 conectores que trae esta, de manera que los cables los podamos conectar por la parte trasera

![Conexiones](/docs/pines.jpeg "Conexiones")

una vez hecho esto, conectaremos los cables como sigue:

* GND (tierra): Negro
* VCC (+5V): Rojo
* SCL (reloj): Verde
* SDA (datos): Azul

el otro extremo de los cables los conectaremos a la raspberry pi como sigue

* Pin 4: Rojo
* Pin 6: Negro
* Pin 3: Verde
* Pin 5: Azul

![Conexiones](/docs/conexiones.png "Conexiones")

Si tienes algun otro dispositivo conectado, como por ejemplo un ventilador, y los pines 4 y 6 están ocupados, no te preocupes, ya que la raspberry tiene mas pines de 5V y de tierra, puedes consultar este diagrama y conectarlo a cualquier otro que cumpla la misma función

![GPIO pines](/docs/gpio.png "GPIO pines")

# Instalación
Conectamos a nuestro nodo por ssh

    ssh admin@192.168.x.x

Descargamos el repositorio

    git clone https://github.com/frangb/node_display

Editamos el archivo de configuración, para añadir el usuario y contraseña de nuestro servidor RCP

    cd node_display
    nano config.txt

Ejecutamos el script

    nohup python main.py &



