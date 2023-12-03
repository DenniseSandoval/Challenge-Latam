#Ejecucion del proyecto local

Para la correcta ejecucion empezar instalando lo siguiente:
pip install --upgrade pip
pip install -r requirements-test.txt

Luego de ello en el terminal ejecutar

uvicorn challenge.api:app --reload


#Ejecucion Docker

escribir los comandos
docker build -t challenge-latam:latest .
docker run -p 8000 challenge-latam

Ejecucion Test
Los UnitTest fueron ejecutados correctamente cubriendo todos los casos de prueba establecidos en el proyecto, unicamente en el test_model.py se cambio la ruta de acceso al archivo data_path = Path(os.getcwd(),"data/data.csv") en la funcion setUp

make model-test
make api-test

#Deploy GCP

Para el deploy en la nube se configuro el archivo app.yaml, asi mismo se configuro los archivos cd/ci con las ramas correspondientes y los pasos para el correcto deploy de la aplicacion.

URL servidor GCP: https://latam-challenge-407003.ue.r.appspot.com
#APIS
 get: https://latam-challenge-407003.ue.r.appspot.com/health
 post: https://latam-challenge-407003.ue.r.appspot.com/predict
        body: {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                }
            ]
        }
