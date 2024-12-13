# Configuración de Power BI Service
Para la visualización en streaming de los datos se usa 
**[Power BI Service](https://www.microsoft.com/es-es/power-platform/products/power-bi).** de Fabric, en caso de no tener cuenta se puede hacer una prueba de 60 días de manera gratuita.
 
## 1️⃣ Crear un Streaming Dataset
 
1. Dentro de Power BI, ve a **"Áreas de trabajo"** y selecciona o crea una.
2. Una vez en el área de trabajo, crea un nuevo elemento:
 
   ![Crear nuevo elemento](img/image-18.png)
 
3. Elige **Streaming Dataset (Conjunto de datos en streaming):**
 
   ![Elegir Streaming Dataset](img/image-19.png)
 
4. Selecciona **API** como origen de datos y haz clic en **Siguiente**:
 
   ![Seleccionar API](img/image-20.png)
 
5. Asigna un nombre al dataset y define la estructura con la que recibirá los datos desde Databricks (NO hagas clic en "Crear" aún):
 
   ![Definir estructura](img/image-5.png)
 
6. Habilita el **análisis histórico:**
 
   ![Habilitar análisis histórico](img/image-6.png)
 
7. Comprueba el esquema del dataset:
 
   ![Comprobar esquema](img/image-8.png)
 
---
 
## 2️⃣ Conectar el Streaming Dataset con Databricks
 
1. Copia la **URL de acceso** al dataset y pégala en el método que enviará los datos desde Databricks a Power BI:
 
   ![Copiar URL de acceso](img/image-21.png)  
   ![Ejemplo de uso](img/image-22.png)
 
2. Copia la **URL de inserción:**
 
   ![Copiar URL de inserción](img/image-11.png)
 
3. Indica dónde has copiado la URL:
 
   ![Especificar ubicación de URL](img/image-12.png)
 
---
 
## 3️⃣ Crear un Informe
 
1. Selecciona **"Crear informe"** sobre el dataset:
 
   ![Crear informe](img/image-23.png)
 
2. Establece la frecuencia de actualización del informe:
 
   ![Establecer actualización](img/image-28.png)
 
3. Guarda el informe:
 
   ![Guardar informe](img/image-29.png)
 
---
 
## 4️⃣ Uso de Dashboards
 
1. **Ancla el informe** a un dashboard:
 
   ![Anclar informe](img/image-24.png)
 
2. Busca la opción de **"Anclar a un panel"**:
 
   ![Anclar a panel](img/image-25.png)
 
3. Crea un nuevo panel o selecciona uno existente y guarda los cambios:
 
   ![Guardar en panel](img/image-26.png)
 
---
 
## 5️⃣ Visualizar el Dashboard
 
![Visualizar el dashboard](img/image43.png)
---
 
# Power BI Desktop
 
## 1️⃣ Obtener los datos conectando a Databricks
 
![Obtener Datos](img/image30.png)
 
## 2️⃣ Filtrar datos, agrupar, ordenar...
 
1. **En la ventana de inicio, hacer click en transformar datos**
 
    ![Transformar Datos](img/image-31.png)
 
2. **Quitar duplicados del dataset**
 
    ![Quitar duplicados](img/image-34.png)
 
 
3. **Hacer las transformaciones necesarias**
 
    ![Filtro id](img/image-32.png)
    ![Orden](img/image-33.png)
 
4. **Guardar el dataset transformado**
 
    ![Guardar transformaciones](img/image-35.png)
 
## 3️⃣ Crear las visualizaciones
 
![Visualizaciones normales](img/image-36.png)
 
## 4️⃣ Usar funciones DAX para sacar datos de interés.
 
![Funciones dax](img/image-37.png)
 
## 5️⃣ Publicar el informe a Power BI Service
 
![Publicar en Power BI Service](img/image-38.png)
 
![Informe y dataset](img/image-39.png)
 
## 6️⃣ Anclar al mismo panel
 
1. **Seleccionar anclar panel**
 
    ![Anclar](img/image40.png)
 
2. **Seleccionar panel ya existente**
 
    ![Panel ya existente](img/image41.png)
   
## 7️⃣ Visualizar el panel completo
 
![Panel completo](img/image-42.png)