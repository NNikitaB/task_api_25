# Для запуска:
## Локально
### Установите venv 
```python
python -m venv .venv
```
### Установите зависимости
```python
python -m pip install -r internal\requirements.txt
```
### Запустите проект
```python
python cmd\run.py
```
## Локально с docker-compose
### Запустите compose из папки build
```
docker-compose up --build
```
