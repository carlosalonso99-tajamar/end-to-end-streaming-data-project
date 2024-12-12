## **README: Configuración de Imágenes y Contenedores en Azure**

## **1. Introducción**
Este documento describe los pasos necesarios para construir, etiquetar, subir y desplegar el contenedor Docker del servidor en Azure, utilizando Azure Container Registry (ACR) y Azure Container Instances (ACI). Además, detalla cómo ejecutar el cliente localmente como una aplicación Python normal.

---

## **2. Requisitos Previos**

1. **Herramientas Instaladas:** Docker, Azure CLI, Python (para ejecutar el cliente localmente).
2. **Registro en ACR:** Nombre del registro: `contenedorapp.azurecr.io`; Acceso configurado:
   ```bash
   az acr login --name contenedorapp
   ```
3. **Grupo de Recursos:** Nombre: `streaming-car_group`.
4. **Cadenas de conexión y variables de entorno:**
   - **Client:** `EVENT_HUB_NAME=streamingread`, `HOST` (IP del servidor desplegado en Azure), `PORT=65432` (puerto del servidor para la comunicación).
   - **Server:** `HOST=0.0.0.0`, `PORT=65432` (puerto expuesto para la comunicación), `TRAYECTO_DIR=data` (directorio para guardar trayectos).
5. **Región:** `northeurope`.

---

## **3. Estructura del Proyecto**

```
project-root/
├── server/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
├── client/
│   ├── app.py
│   ├── requirements.txt
```

---

## **4. Paso a Paso**

### **4.1. Preparar el Entorno**
1. Asegúrate de que Docker esté corriendo:
   ```bash
   docker info
   ```
2. Inicia sesión en Azure y conecta tu ACR:
   ```bash
   az login && az acr login --name contenedorapp
   ```

### **4.2. Construir la Imagen Docker del Servidor**
1. **Server:**
   ```bash
   cd server && docker build -t server:latest . && docker tag server:latest contenedorapp.azurecr.io/server:latest
   ```

### **4.3. Subir la Imagen al ACR**
1. **Server:**
   ```bash
   docker push contenedorapp.azurecr.io/server:latest
   ```

### **4.4. Obtener Credenciales del Registro**
Antes de crear el contenedor, asegúrate de obtener el nombre de usuario y la contraseña del registro:

1. **Obtener el nombre de usuario del registro:**
   ```bash
   az acr credential show --name contenedorapp --query username --output tsv
   ```

2. **Obtener la contraseña del registro:**
   ```bash
   az acr credential show --name contenedorapp --query passwords[0].value --output tsv
   ```

Guarda estos valores para usarlos en la creación del contenedor.

### **4.5. Desplegar el Contenedor en Azure**

#### **4.5.1. Desplegar el Server**
1. Crear el contenedor:
   ```bash
   az container create --resource-group streaming-car_group --name server-container --image contenedorapp.azurecr.io/server:latest --ports 65432 --ip-address Public --location northeurope --environment-variables HOST=0.0.0.0 PORT=65432 TRAYECTO_DIR=data
   ```
2. Obtener la IP pública del servidor:
   ```bash
   az container show --resource-group streaming-car_group --name server-container --query "ipAddress.ip" --output tsv
   ```

---

### **4.6. Configurar y Ejecutar el Cliente Localmente**
1. Crea un archivo `.env` en el directorio del cliente con el siguiente contenido, sustituyendo `<SERVER_IP>` por la IP pública obtenida anteriormente:
   ```env
   HOST=<SERVER_IP>
   PORT=<SERVER_PORT>
   EVENT_HUB_NAME=<YOUR_EVENT_HUB_NAME>
   EVENT_HUB_CONNECTION_STRING=<YOUR_EVENT_HUB_CONNECTION_STRING>
   RESOURCE_GROUP=<YOUR_RESOURCE_GROUP>
   ```
2. Instala las dependencias necesarias en el entorno local:
   ```bash
   cd client && pip install -r requirements.txt
   ```
3. Ejecuta el cliente:
   ```bash
   python app.py
   ```

---

## **5. Verificar el Despliegue**
1. Verifica el estado del contenedor del servidor:
   ```bash
   az container list --resource-group streaming-car_group --output table
   ```
2. Revisa los logs del servidor para verificar la conexión:
   ```bash
   az container logs --resource-group streaming-car_group --name server-container
   ```

---

## **6. Solución de Problemas**
- **Docker no está corriendo:**
   ```bash
   sudo systemctl start docker
   ```
- **Error de autenticación en Event Hub:** Verifica que la cadena de conexión sea válida y que las credenciales tengan permisos adecuados en Event Hub.
- **Puertos no accesibles:** Asegúrate de que los puertos estén abiertos y configurados correctamente en Azure.

---

## **7. Notas Finales**
- Este README asume que las aplicaciones están configuradas correctamente para usar las variables de entorno mencionadas.
- Asegúrate de actualizar las dependencias en los archivos `requirements.txt` antes de ejecutar las aplicaciones.

---

Con esta guía, deberías poder realizar todo el proceso de construcción, despliegue y ejecución sin problemas. ¡Buena suerte!

[Siguiente: Crear un workspace de **Azure Databricks**, conectar con Event Hubs y Configurar las capas **Bronze**, **Silver** y **Gold** en Delta Lake.](../04-databricks/README.md)