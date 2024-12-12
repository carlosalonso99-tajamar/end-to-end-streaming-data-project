# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del servidor al contenedor
COPY . .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del servidor
EXPOSE 65432

# Comando para iniciar el servidor
CMD ["python", "server.py"]
