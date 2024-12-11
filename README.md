# Guía para Crear y Desplegar una Azure Function

Esta guía te lleva paso a paso a través del proceso de creación, configuración, prueba y despliegue de una Azure Function utilizando Visual Studio Code.

---

## 1. Crear una Function App en Azure

1. **Accede al portal de Azure:**
   - Dirígete al [portal de Azure](https://portal.azure.com) y crea una nueva Function App.
   - Elige el plan que sea más conveniente para tus necesidades.

   ![Creación de la Function App]({A03F8AA8-6C79-4409-8572-AE88DD7B3853}.png)


   ![Detalles de la Function App]({A1E5C132-6FB1-453A-BCA8-F223B645198A}.png)

   - Puedes usar configuraciones por defecto para el resto de las opciones. Una vez creada, puedes ver los detalles en el portal.

---

## 2. Configurar Visual Studio Code

1. **Instala la extensión de Azure Functions:**
   - Abre Visual Studio Code.
   - Descarga la extensión de Azure Functions desde el marketplace de extensiones.

     ![Instalación de la extensión]({0EBF62FB-EEAE-42C5-B141-AD23B6756EAB}.png)

2. **Verifica el icono de Azure Functions:**
   - Una vez instalada, aparecerá un icono en la barra lateral izquierda.

     ![Icono de Azure Functions]({7608C350-FDAF-4C9C-BA24-71BDED22AB77}.png)

3. **Crea una nueva Function:**
   - Haz clic en el icono de Azure Functions y selecciona la opción para crear una nueva Function.
   - Configura las opciones según tus necesidades.

     ![Creación de la Function]({0BC3F783-6C69-429A-9E14-99B5FFFFB2C0}.png)

4. **Estructura del proyecto:**
   - Visual Studio Code creará la estructura del proyecto en el directorio seleccionado.

---

## 3. Configurar el entorno virtual

1. **Activa el entorno virtual generado por el proyecto:**
   - En **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate
     ```
   - En **Windows (cmd):**
     ```cmd
     .venv\Scripts\activate
     ```
   - En **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```

2. **Instala las dependencias necesarias:**
   - Si tienes un archivo `requirements.txt`:
     ```cmd
     pip install -r requirements.txt
     ```
   - Si no lo tienes, instala los paquetes manualmente y guárdalos:
     ```cmd
     pip freeze >> requirements.txt
     ```

3. **Archivo `.env`:**
   - Crea un archivo `.env` en la raíz del proyecto con las siguientes configuraciones:
     ```plaintext
     # URL de la API que proporciona los datos
     API_URL=https://api.example.com/car/state

     # Cadena de conexión para el Event Hub
     EVENT_HUB_CONNECTION_STRING=Endpoint=sb://<your-event-hub-namespace>.servicebus.windows.net/;SharedAccessKeyName=<your-key-name>;SharedAccessKey=<your-key>

     # Nombre del Event Hub al que se enviarán los datos
     EVENT_HUB_NAME=your-event-hub-name
     ```

---

## 4. Probar la Function en Local

1. **Instala Azurite:**
   - Para simular servicios de Azure en local, instala Azurite con Node.js:
     ```cmd
     npm install azurite
     ```

2. **Inicia el servicio de Azurite:**
   ```cmd
   azurite
   ```
   ![Inicio de Azurite]({A7DBAD55-14EF-4375-975F-87C98900AE45}.png)

3. **Ejecuta la Function en local:**
   ```cmd
   func start --verbose
   ```
   ![Ejecución de la Function en local]({2965F868-2A91-466E-AABD-EEEB2DE99ACE}.png)

---

## 5. Desplegar en Azure

1. **Abre la pestaña de Azure en Visual Studio Code:**
   ![Pestaña de Azure]({C9F23CFB-4E6A-43AD-8CEC-7C8AD43BEF54}.png)

2. **Selecciona el proyecto:**
   - Haz clic en el icono de la nube con la flecha hacia arriba.
   - Elige la Function App donde deseas desplegar tu proyecto.

3. **Verifica el despliegue:**
   - Una vez completado, verifica que tu Function esté activa en Azure.

     ![Despliegue exitoso]({CE7075E5-D73D-4AD2-B8E5-109D1C32BECA}.png)

4. **Comprobar en Azure:**
   - Revisa que la Function esté lista en el portal de Azure.
     ![Function activa en Azure](image-1.png)

---

## Notas Finales

- Asegúrate de configurar correctamente el archivo `.env`.
- Prueba completamente tu Function en local antes de desplegarla.

Con estos pasos, tu Function estará lista y operativa en Azure. ¡Buena suerte! 🚀

