#Ejecucion del proyecto local

Para la correcta ejecucion empezar instalando lo siguiente:
pip install --upgrade pip
pip install -r requirements-test.txt

Luego de ello en el terminal ejecutar

uvicorn challenge.api:app --reload


#Ejecucion Docker

escribir los comandos
docker build -t challenge-latam:latest .
docker run -p 8000:8000 challenge-latam

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

#Modelo Seleccionado
En cuanto a la elección del modelo para la implementación final, se optó por Logistic Regression. Esta decisión se basa en consideraciones prácticas como limitaciones de tiempo, dependencias de paquetes y la facilidad de uso. Al seleccionar Logistic Regression, se reduce la dependencia de terceros para el componente, y la simplicidad inherente de esta biblioteca contribuye a ofrecer una solución completa de manera eficiente.

Esta elección se alinea con la orientación del Científico de Datos, quien indicó que se debía seleccionar uno de los modelos con Feature Importance y Balance. Dado que ambos modelos presentaron resultados similares en el classification report, con ligeras variaciones en el recall, la elección de Logistic Regression se basa en su mayor facilidad de interpretación. Esta característica permitirá comprender con mayor claridad el impacto de cada Feature en los resultados del entrenamiento del modelo. En este caso, se valora la capacidad de entender el razonamiento detrás de los resultados para mejorar el desempeño en futuras iteraciones del proyecto.


#APIS
Se implemento la solucion que permite cargar el archivo el modelo unicamente al inicio de la ejecucion y asi tenerlo en memoria.

En nuestra aplicación FastAPI, hemos establecido un punto final que aprovecha el modelo previamente generado para realizar predicciones basadas en los datos de entrada. Los usuarios tienen la capacidad de enviar solicitudes a este punto final, y el modelo responderá con predicciones de manera ágil.