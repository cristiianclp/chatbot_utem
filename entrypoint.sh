#!/bin/sh

# Ejecuta ollama en background
ollama serve &

# Espera hasta que ollama esté disponible completamente
sleep 10

# Descarga el modelo (si no está ya descargado)
ollama pull deepseek-r1:7b

# Espera unos segundos más para asegurar estabilidad
sleep 5

# Deja ollama corriendo en primer plano ahora
wait
