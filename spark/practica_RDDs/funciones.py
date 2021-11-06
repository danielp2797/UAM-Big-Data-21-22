import numpy as np 

def preprocesa_rdd(rdd, sep=','):
    # descripcion
    #----------------
    
    #Borra espacios en blanco al inicio y final de las lineas y separa los datos
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd 
    #<sep> | tipo: str
    
    # resultado: 
    #----------------
    
    #<result> | tipo: pyspark.rdd  | descriptivo: rdd separado por lineas
        
    rdd_lines = rdd.map(lambda x: x.strip().split(sep))
    return rdd_lines

def compute_agg_mean(rdd):
    
    # descripcion
    #----------------
    
    #Calcula la media de los valores agregados por la clave suministrada. Asume que las lineas del RDD
    # de entrada estan en un par (clave, valor). Admite que "valor" sea una tupla, en ese caso se calcula
    # la media marginal de cada componente.
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd     
    # resultado: 
    #----------------
    
    #<rdd_means> | tipo: pyspark.rdd  | descriptivo: (clave, valor(es))
    
    # en el primer map se añade un 1 al inicio para que recuente observaciones. Se elimina al final.
    rdd_means = rdd.map(lambda x: (x[0], [1]+x[1]))\
                    .reduceByKey(lambda x, y: [x[i]+y[i] for i in range(len(x))])\
                    .mapValues(lambda x: [value/x[0] for value in x[1:]])
    return rdd_means

def compute_agg_std(rdd):
        
    # descripcion
    #----------------
    
    #Calcula la desv. tipica de los valores agregados por la clave suministrada. Asume que las lineas del RDD
    # de entrada estan en un par (clave, valor). Admite que "valor" sea una tupla, en ese caso se calcula
    # la desv. tipica de cada componente. Se calcula la media usando la función "compute_agg_mean".
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd  
    
    # resultado: 
    #----------------
    
    #<rdd_std> | tipo: pyspark.rdd  | descriptivo: (clave, valor(es))
    
    # en el primer map se añade un 1 al inicio para que recuente observaciones. Se elimina al final.
    rdd_means = compute_agg_mean(rdd)
    rdd_sqmean = rdd_means.mapValues(lambda x: [mean**2 for mean in x])
    
    # en el primer map se añade un 1 al inicio para que recuente observaciones
    rdd_sqsums = rdd.map(lambda x: (x[0], [1]+[value**2 for value in x[1]]))\
                        .reduceByKey(lambda x, y: [x[i]+y[i] for i,_ in enumerate(x)])\
                        .mapValues(lambda x: [value/x[0] for value in x[1:]]) 
    
    rdd_std = rdd_sqsums.join(rdd_sqmean)\
                        .mapValues(lambda x: [np.sqrt(x[0][i]-x[1][i]) for i,_ in enumerate(x[0])])
    return rdd_std
    
def compute_agg_min(rdd):
    
    # descripcion
    #----------------
    
    #Calcula el minimo de los valores agregados por la clave suministrada. Asume que las lineas del RDD
    # de entrada estan en un par (clave, valor). Admite que "valor" sea una tupla, en ese caso se calcula
    # el minimo de cada componente.
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd  
    
    # resultado: 
    #----------------
    
    #<rdd_min> | tipo: pyspark.rdd  | descriptivo: (clave, valor(es))
    
    rdd_min = rdd.reduceByKey(lambda x, y: [min(x[i], y[i]) for i,_ in enumerate(x)])
    
    return rdd_min

def compute_agg_max(rdd):
    
    # descripcion
    #----------------
    
    #Calcula el maximo de los valores agregados por la clave suministrada. Asume que las lineas del RDD
    # de entrada estan en un par (clave, valor). Admite que "valor" sea una tupla, en ese caso se calcula
    # el maximo de cada componente.
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd   
    
    # resultado: 
    #----------------
    
    #<rdd_max> | tipo: pyspark.rdd  | descriptivo: (clave, valor(es))
    
    rdd_max = rdd.reduceByKey(lambda x, y: [max(x[i], y[i]) for i,_ in enumerate(x)])
    
    return rdd_max

def flatten(rdd):
    
    # descripcion
    #----------------
    
    # Al hacer varios joins sobre una clave, se anidan los valores en varias tuplas y listas. En este caso
    # Se hacen 4 joins con los estadisticos pedidos, algo que vuelve dificil leer los resultados.
    # Esta función se encarga de deshacer las tuplas y listas anidadas de manera recurrente.
    # Para ello, busca iteradores que no sean de tipo str y devuelve un generador para cada elemento de los mismos.
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd   
    
    # resultado: 
    #----------------
    
    #<x, y> | tipo: depende del contenido de las listas/tuplas anidadas
    # | descriptivo: generadores de los elementos de las tuplas/listas anidadas.
    
    for x in rdd:
        if hasattr(x, '__iter__') and not isinstance(x, str):# and not isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x
            
def summary(rdd, features=[3, 4 , 5], agg=[6, 7, 9], std='all'):
    
    # descripcion
    #----------------
    
    # Esta funcion une a todas las funciones que calculan los estadisticos pedidos en una unica funcion.
    # Tambien se encarga de devolver un resultado legible para cada RDD de entrada.
    
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd
    #<features> | tipo: pyspark.rdd | descriptivo: indices en cada linea donde estan las variable a resumir
    # Por defecto se dejan los parametros adecuados al ejercicio propuesto.
    #<agg> | tipo: list | descriptivo: indices de cada linea donde se encuentran las claves para agregar
    # Por defecto se dejan los parametros adecuados al ejercicio propuesto.
    #<std> | tipo: str o lista de str | descriptivo: indica que estadisticos calcula. Si se pasa 'all' se
    # calcula la media, std, minimo y maximo. Por ejemplo, si solo se quiere la media y std se pasaria 
    # [std, mean].
    
    # resultado: 
    #----------------
    
    #<rdd_summary> | tipo: pyspark.rdd 
    # | descriptivo: rdd con un par (clave, valor). En clave estan los grupos y en valor, una lista
    # con los valores de los estadisticos resumen. Si hay x1,...,xn variables, aparecen en este orden: 
    # (media(x1,...,xn), min(x1,...,xn), max(x1,...,xn), std(x1,...,xn))
    
    # se crean los pares clave valor y un rdd experimental con las claves para ir concatenando los estadisticos.
    # El RDD experimental tiene como valor un 1 en cada clave. Se hace por motivos de compatibilidad con los join.
        
    rdd_data = rdd.map(lambda x: ('-'.join([x[a] for a in agg]), [float(x[b]) for b in features]))
    rdd_summary = rdd_data.map(lambda x: (x[0], 1)).distinct()

    if std == 'all':
        std = ['mean', 'std', 'min', 'max']
        
        
    if 'mean' in std:
        rdd_means = compute_agg_mean(rdd_data)
        rdd_summary = rdd_summary.join(rdd_means)

    if 'min' in std:
        rdd_min = compute_agg_min(rdd_data)
        rdd_summary = rdd_summary.join(rdd_min)

    if 'max' in std:
        rdd_max = compute_agg_max(rdd_data)
        rdd_summary = rdd_summary.join(rdd_max)

    if 'std' in std:
        rdd_std = compute_agg_std(rdd_data)
        rdd_summary = rdd_summary.join(rdd_std)

    # Se alisan los resultados (flatten) y se elimina el valor experimental del inicio.
    rdd_summary = rdd_summary.map(lambda x: (x[0], tuple(flatten(x))[2:]))
    return rdd_summary

def remove_null_keys(rdd, null_value='null'):
    
    # descripcion
    #----------------
    
    # FIltra un RDD en pares (clave, valor) por las claves que no contengan valores null
    # argumentos:
    #----------------
    
    #<rdd> | tipo: pyspark.rdd   
    #<null_value> | tipo: str | descriptivo: cadena que representa los valores missing
    
    # resultado: 
    #----------------
    
    #<no_null_keys> | tipo: pyspark.rdd
    # | descriptivo: RDDn sin claves null
    
    no_null_keys = rdd.filter(lambda x: null_value not in x[0])
    return no_null_keys

if __name__ == 'funciones':
    print(f'package "funciones" succesfully loaded')