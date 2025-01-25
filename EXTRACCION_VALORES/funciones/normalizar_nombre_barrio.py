def normalizar_nombre_barrio(nombre):
    # Convertir todo a minúsculas
    nombre = nombre.lower()
    # Reemplazar acentos por caracteres sin acento
    nombre = nombre.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    # Reemplazar "S." por "San" en cualquier parte del nombre
    nombre = nombre.replace('s.lluis', 'san luis')
    # Eliminar el punto intermedio (·)
    nombre = nombre.replace('marcel.li', 'marceli')  # Eliminamos el punto intermedio
    # Eliminar el guion (-) para hacer los nombres equivalentes
    nombre = nombre.replace('-', '')  # Eliminamos el guion
    # Si es necesario, manejar otras reglas de normalización adicionales aquí...
    return nombre