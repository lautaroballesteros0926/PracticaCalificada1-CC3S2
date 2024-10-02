# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y la aplicación
COPY requirements.txt .
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt



# Comando para ejecutar la aplicación
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
