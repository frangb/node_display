# Display para nodo de Bitcoin

El siguiente tutorial explica como añadir un pequeño display a un nodo de Bitcoin. Esta probado en un nodo con raspiblitz, pero debería servir para cualquier nodo (quizá con alguna pequeña modificación)

![Frontal](/docs/node_front.jpeg "Frontal")

## Material necesario

Precio aproximado de todo: 4 Euros

A modo ilustrativo, dejo enlaces de aliexpress para cada uno de los componentes. No obstante, son dispositivos bastante estándar, por lo que los podéis comprar en cualquier otra tienda.

- Pantalla modelo SSD1306 de 0,91 pulgadas (128 x 32 píxeles)
https://es.aliexpress.com/item/32927682460.html
- 4 cables dupont hembra-hembra (preferiblemente los colores rojo, negro, amarillo, verde. Puedes comprar un surtido y así tienes algunos extra para otros proyectos)
https://es.aliexpress.com/item/1005003269498051.html

## Preparación

Primero debemos soldar el conector de 4 pines que acompaña a la pantalla, de manera que los cables los podamos conectar por la parte trasera

![Conexiones](/docs/pines.jpeg "Conexiones")

Una vez hecho esto, conectaremos los cables dupont como sigue:

* GND (tierra): Negro
* VCC (+5V): Rojo
* SCL (reloj): Verde
* SDA (datos): Azul

El otro extremo de los cables los conectaremos a la raspberry pi como sigue

* Pin 4: Rojo
* Pin 6: Negro
* Pin 3: Verde
* Pin 5: Azul

![Conexiones](/docs/conexiones.png "Conexiones")

Si tienes algún otro dispositivo conectado, como por ejemplo un ventilador, y los pines 4 y 6 están ocupados, no te preocupes, ya que la raspberry tiene más pines de 5V y de tierra, puedes consultar este diagrama y conectarlo a cualquier otro que cumpla la misma función.

![GPIO pines](/docs/gpio.png "GPIO pines")

## Activación de las comunicaciones por I2C

Los pines de I2C de Raspberry Pi son una manera extremadamente útil de comunicarse con distintos tipos de periféricos externos, y son los que usaremos para conectar nuestra pantalla al dispositivo.

Este módulo del kernel viene desactivado por defecto, por lo que tendremos que activarlo de la siguiente manera

    sudo raspi-config

Tras ejecutar este comando veremos el siguiente menú:

![raspi-config](/docs/raspi-config.png "raspi-config menu")

Debemos seleccionar la opción 3 (Interface Options), y una vez dentro, seleccionar la opción I5 (enable/disable automatic loading of I2C kernel module)

Una vez hecho esto, podemos pulsar en "Back" y posteriormente en "Finish"

## Permisos del usuario Admin para acceder a los pines I2C

Para que el usuario `admin` pueda leer y escribir de los pines i2c, debemos añadirlo a ese grupo de usuarios con el siguiente comando:

    sudo usermod -a -G i2c admin

## Instalación

Desde un terminal de linea de comandos, conectamos a nuestro nodo por ssh:

    ssh admin@192.168.x.x

Descargamos el repositorio en nuestro directorio home:

    git clone https://github.com/frangb/node_display

Instalamos las dependencias:

    cd node_display
    pip install -r requirements.txt

Editamos el archivo de configuración, para añadir el usuario y contraseña de nuestro servidor RCP

    nano config.txt

Ahora vamos a crear un servicio para poder ejecutar cómodamente el script y también hacer que se ponga en marcha automáticamente al iniciar el sistema

Copiamos el archivo node_display.service en la carpeta `/lib/systemd/system/`

    sudo cp ./node_display.service /lib/systemd/system/node_display.service

Actualizamos los permisos

    sudo chmod 644 /lib/systemd/system/node_display.service
    chmod +x ./node_display.py

Iniciamos el servicio

    sudo systemctl daemon-reload
    sudo systemctl enable node_display.service
    sudo systemctl start node_display.service