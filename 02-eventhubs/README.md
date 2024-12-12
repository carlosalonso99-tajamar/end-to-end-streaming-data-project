# Creación de un servicio de Azure Event Hubs

Azure Event Hubs es un servicio de ingesta de datos en tiempo real, altamente escalable y totalmente administrado. A continuación, se detallan los pasos para la instalación y configuración de un servicio de Azure Event Hubs.

## Prerrequisitos

1. **Cuenta de Azure**: Necesitas una suscripción activa de Azure. Si no tienes una, puedes crear una [aquí](https://azure.microsoft.com/free/).
2. **Azure CLI**: Asegúrate de tener instalada la Azure CLI. Puedes descargarla e instalarla desde [aquí](https://docs.microsoft.com/es-es/cli/azure/install-azure-cli).

## Pasos para la instalación

### 1. Iniciar sesión en Azure

Abre una terminal y ejecuta el siguiente comando para iniciar sesión en tu cuenta de Azure:

```bash
az login
```

### 2. Crear un grupo de recursos

Crea un grupo de recursos donde se alojará tu Event Hub, si es que aún no lo tienes creado:

```bash
az group create --name MiGrupoDeRecursos --location francecentral
```

### 3. Crear un espacio de nombres de Event Hubs

Crea un espacio de nombres para tu Event Hub:

```bash
az eventhubs namespace create --resource-group MiGrupoDeRecursos --name MiEspacioDeNombres --location francecentral
```

### 4. Crear un Event Hub

Crea un Event Hub dentro del espacio de nombres:

```bash
az eventhubs eventhub create --resource-group MiGrupoDeRecursos --namespace-name MiEspacioDeNombres --name MiEventHub
```

### 5. Obtener la cadena de conexión

Para conectar aplicaciones a tu Event Hub, necesitas la cadena de conexión. Puedes obtenerla con el siguiente comando:

```bash
az eventhubs namespace authorization-rule keys list --resource-group MiGrupoDeRecursos --namespace-name MiEspacioDeNombres --name RootManageSharedAccessKey
```
Ese comando, nos proporciona una cadena en formato JSON, donde podemos ver nuestras cadenas de conexiones, tanto primarias como secundarias.
## Conclusión

Siguiendo estos pasos, habrás configurado un servicio de Azure Event Hubs listo para recibir y procesar datos en tiempo real. Para más detalles y opciones avanzadas, consulta la [documentación oficial de Azure Event Hubs](https://docs.microsoft.com/es-es/azure/event-hubs/).
