# SistemasMultiagentes

# Instrucciones de instalación

## Instalación de herramientas
Para poder ejecutar el proyecto de forma correcta, se requiere de lo siguiente:

- [VsCode](code.visualstudio.com)

- [Python](python.org)

- [Unity](unity.com)

## Instalación del proyecto
1. Clonar el repositorio 
```bash 
git clone https://github.com/A01750817/SistemasMultiagentes.git
``` 
Este proceso puede ser tardado, por lo que se puede decargar el .zip de igual forma 
2. Instalar dependencias
```bash
pip install mesa fastapi matplotlib flask uvicorn
```
En caso de tener problemas con la instalación verificar que pip este actualizando utilizando:
```bash
pip install --upgrade pip
```
4. Moverse al directorio del repositorio
```bash
code SistemasMultiagentes
```
5. Ejecutar simulación en Matplotlib
Para ejecutar la simulación con visualización en Matplotlib seguir los siguientes comandos:
```bash
cd sma
```
```bash
python tablero.py
```
6. Ejecutar simulación en Unity
Para ejecutar la simulación con visualización en Unity se debe de seguir los siguientes pasos:
- **En Python**:
Ejecutar los siguientes comandos:
```bash
cd sma
```
```bash
python server.py
```
- En Unity:
1. Añadir desde Unity Hub la carpeta de la simulación con nombre `Maqueta`
2. Abrir el proyecto
3. Dar click en el botón de play para visualizar la simulación
4. Presionar las teclas 1, 2, 3, 4 si se quiere cambiar la vista de la cámara
