Ejecutar proyecto
=================
El proyeto esta dockerizado, incluyendo django, postgres, redis y celery.
Para ejecutar el proyecto ejecutar:
1. docker-compose build
2. docker-compose up

Ejemplo de prueba
=================
Para facilitar la utilización de la aplicación se creó un comando que crea monedas, usuarios y que le brinda a uno de estos balance positivo en dichas monedas para dejar todo listo para realizar transacciones entre usuarios. Esta pensado para ser ejecutado solo una vez (fallará en una segunda ejecución por existencia de los usuarios), y se ejecuta de la siguiente manera:

docker-compose run app python manage.py create_example

Este comando creará:
* Monedas: Bitcoin, Dolar, Peso, Ethereum
* Usuarios: un super usuario admin.user@challenge.com (password:password123) con acceso a la administración, dos usuarios sin acceso a la administracion: simple.user@challenge.com (password: supersecret), simple.user2@challenge.com (password: supersecret)
* Creará movimientos para que el usuario admin.user@challenge.com tenga balance positivo: 1000 Dolar, 10 Bitcoin, 50 Ethereum, 50000 Pesos.

De todas maneras pueden crearse nuevos usuarios utilizando el endpoint correspondiente:

http://localhost:8000/api/users/create/


Explicación del funcionamiento
==============================
El balance para una moneda y un usuario determinado se calcula en función de los movimientos que dicho usuario tiene para la moneda especifica.
Las transacciones modelan el intento de transferencia de dinero de una cuenta a otra, y puede ser rechazada si el usuario que realiza la transacción no tiene monto suficiente para satisfacer la misma. Las transacciones se realizan indicando cuenta de destino, monto y moneda. La cuenta de origen de la transacción será la del usuario logueado. El valor pasado como destino debe ser un ID de un usuario, el monto un decimal positivo, y la moneda un ID de moneda.

No hay endpoint para cambiar directamente el balance de un usuario, pero ingresando a la administración de django pueden crearse movimientos para un usuario indicando la moneda en pos de posibilitar futuras transacciones. Para darle balance positivo en una momeda determinada a un usuario se debe crear un movimiento desde la administración. Esto es una decision de diseño que acota la implementación a lo estrictamente solicitado, considerando que en una aplicación realista habría un broker donde los usuarios puedan comprar moneda.

Las transacciones son manejadas por una cola de trabajo de Celery para garantizar que no haya problemas por concurrencia. Para garantizar esto se acude a un lock de tarea que minimiza las transacciones bloqueadas utilizando como id de lock el string "{user_id}-lock-{moneda_id}", de esta manera solo serán bloqueadas aquellas transacciones para las que existe otra transacción siendo procesada para la misma cuenta origen y la misma moneda. Se reintenta el procesamiento de la transacción bloqueada luego de 10 segundos.

Si una transacción es procesada satisfactoriamente, se crearan dos movimientos, uno para la cuenta de origen (con monto negativo) y otro para la cuenta destino (con monto positivo). Si el monto indicado por una transacción es mayor al balance del usuario para la moneda correspondiente, la transacción queda rechazada y no se crean movimientos.

Testing
=======
Para correr los tests:
docker-compose run app python manage.py test

Hay algunos casos de prueba muy triviales dada la complejidad de la aplicación, sobre todo esto sucede para las pruebas de la api restful que no hacen mucho mas allá de lo realizado por defecto por DRF. Sin embargo se decide dejarlas para mostrar conocimiento al respecto.

ENDPOINTS
==========
2. api/users/create/
3. api/users/token/
4. api/users/me/
5. api/users/balance/<int:coin_id>/
6. api/users/balance/
8. api/coins/
9. api/transactions/
