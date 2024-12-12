# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del cliente al contenedor
COPY . .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del cliente Flask
EXPOSE 5000

# Comando para iniciar el cliente Flask
CMD ["python", "app.py"]
