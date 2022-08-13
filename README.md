# Prueba DataQu
Para realizar la carga de datos un una base de datos inicial que está vacía luego de ejecutar las migraciones, se creo el archivo data.json el cual se encuentra en el directorio principal del proyecto.

Para cargar los datos del archivo json se debe utilizar el comando "loaddata" en la consola de la siguiente forma:

* ubicado en la carpeta del proyecto /arriendo_autos digitamos $ Python manage.py loaddata data.json

Por otra parte, para acceder a la aplicación una vez ejecutado el comando runserver:

* Api Endpoints
- localhost:8000/api/arriendo-autos/cliente/
- localhost:8000/api/arriendo-autos/arriendo/
- localhost:8000/api/arriendo-autos/empresa/
 
 * App 
 - localhost:8000/
