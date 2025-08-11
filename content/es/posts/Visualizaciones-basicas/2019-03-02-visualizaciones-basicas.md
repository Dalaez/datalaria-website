---
title: Visualizaciones básicas
date: 2019-03-02
draft: False
categories: ["fundamentos"]
tags: ["estadística", "visualizaciones", "distribucion", "gráficos", "representaciones"]
myVar: "myValue"

weight: 10
image: img/visualizaciones/visualizaciones_basicas.png
authorAvatar: datalaria-logo.png
---

Continuando con la información expuesta en el post [estadística descriptiva](https://www.datalaria.com/post/fundamentos/2018-10-07-estadistica-descriptiva/), a continuación, vamos a conocer las maneras más básicas de visualizar los datos o la información a analizar. Concretamente:

- **[Gráficos de tarta](#grafico_tarta)**
- **[Gráficos de línea](#grafico_linea)**
- **[Gráficos de rectángulo y proyección solar](#grafico_jerarquico)**
- **[Histogramas y diagramas de barras](#histogramas)**
- **[Gráficos de densidad](#grafico_densidad)**
- **[Gráficos de caja (Boxplots)](#grafico_caja)**
- **[Gráficos de violin](#grafico_violin)**
- **[Gráficos de dispersión](#grafico_dispersion)**
- **[Gráficos de Pareto](#grafico_pareto)**

*Nota: Para todos los ejemplos (excepto para los gráficos de línea por sus características) se va a utilizar como dataset el fichero train.csv un subconjunto de 891 individuos representativo de la población del Titanic utilizado para el entrenamiento de modelos de Aprendizaje automático.*

## <a name="grafico_tarta"></a>Gráficos de tarta

Los gráficos de tarta o circulares (en inglés *pie charts*) son utilizados para representar la proporción de los datos de una variable o característica según su valor respecto al total de los mismos. Este tipo de gráficos presentan multitud de variantes y son ampliamente utilizados debido a su sencillez de preparación e interpretación. Sin embargo, muchas veces se abusa de este tipo de gráficos o se utilizan indebidamente (ver el siguiente [artículo sobre el mal uso de los gráficos de tarta](https://www.elartedepresentar.com/2011/11/las-tartas-son-para-el-postre-5-razones-por-las-que-no-uso-graficos-circulares/)).

 * Ejemplo: Proporciones de pasajeros del Titanic por estatus socioeconómico

![Grafico_tarta](/img/visualizaciones/grafico_tarta.png)

## <a name="grafico_linea"></a>Gráficos de Línea
Los gráficos de línea se utilizan para mostrar los datos de una variable sobre una secuencia de datos continuados. Generalmente, se utilizan para representar tendencias o relaciones (en agrupación con más variables) entre los datos durante un intervalo de tiempo continuo.

*Nota: Con el fin de visualizar un caso de uso en un intervalo de tiempo continuo, para los siguientes ejemplos se ha utilizado el dataset de la biblioteca de datos públicos del Gobierno de España sobre [los datos de población por comunidades autónomas en la serie histórica desde 1997 a 2017.](https://datos.gob.es/es/catalogo/ea0010587-poblacion-por-comunidades-y-ciudades-autonomas-y-tamano-de-los-municipios-anual-comunidades-autonomas-cifras-oficiales-de-poblacion-de-los-municipios-espanoles-revision-del-padron-municipal-identificador-api-2915)*  
</br>

 * Ejemplo: Población española desde 1997
![Grafico_linea_1](/img/visualizaciones/grafico_linea1.png)
</br>

 * Ejemplo: Población española por comunidades desde 1997
![Grafico_linea_21](/img/visualizaciones/grafico_linea2.png)


## <a name="grafico_jerarquico"></a>Gráficos de rectángulo y proyección solar
Los gráficos de rectángulos (en inglés *treemaps*) y los gráficos de proyección solar (en inglés *sunburst*) son visualizaciones para representar datos jerárquicos y resumir la información en áreas proporcionales a los valores correspondientes.

En el caso gráficos de rectángulos, la representación consiste en agrupaciones de los datos mediante rectángulos con un área proporcional a su valor respecto al total.  
</br>

 * Ejemplo: Proporción de pasajeros según su estatus socioeconómico clasificados por género (gráfico rectángulo)  

![Grafico_rectangulo](/img/visualizaciones/grafico_rectangulo.png)

En el caso de los gráficos de proyección solar, la representación consiste en agrupaciones de los datos mediante diferentes anillos según el nivel representado, y éstos a su vez, se dividen a en partes proporcionales al valor de los datos que representan.
</br>

 * Ejemplo: Proporción de pasajeros según su estatus socioeconómico clasificados por género (gráfico proyección solar)

![Grafico_rectangulo](/img/visualizaciones/grafico_proyeccion_solar.png)

Sobre el ejemplo representado, se puede apreciar rápidamente información sobre los datos jerarquizados representados como por ejemplo que el número de pasajeros hombres era de casi 2/3 de la tripulación, así como que los pasajeros hombres y de estatus socioeconómico bajo representaban algo más de 1/3 de la tripulación.

## <a name="histogramas"></a>Histogramas y Gráficos de barras
Recopilando la información ya recogida en la entrada [Estadística descriptiva](https://www.datalaria.com/post/fundamentos/2018-10-07-estadistica-descriptiva/), se explican dos de las representaciones más utilizadas en los análisis de datos, cuyo principal objetivo es representar la distribución de los datos respecto a una variable o característica del conjunto de datos. Así pues, los histogramas permiten visualizar datos continuos y los diagramas de barras representan datos discretos.  
</br>

 * Ejemplo: Distribución de pasajeros por precio del pasaje

![Histograma](/img/visualizaciones/histograma.png)
</br>

 * Ejemplo: Distribución de pasajeros por estatus socioeconómico

![Diagrama_barras](/img/visualizaciones/diagrama_barras.png)

Como ya se vio en la entrada sobre “Estadística Descriptiva”, representando sobre estos gráficos medidas de estadística descriptiva (como la media o la mediana), podemos caracterizar la distribución de la variable bajo análisis y con ello extraer más información al respecto.

## <a name="grafico_densidad"></a>Gráficos de densidad
También conocidos como gráficos de densidad de Kernel, sirven para visualizar la distribución de los datos en un intervalo continuo. Este tipo de gráficos es una variación de los Histogramas donde se representa de manera suavizada la forma de la distribución.
</br>

* Ejemplo: Distribución de la edad de los pasajeros del Titanic  

![Gráfico_Densidad](/img/visualizaciones/grafico_densidad.png)

## <a name="grafico_caja"></a>Diagramas de caja
Los diagramas de caja o de bigote (en inglés “boxplots”) así llamados por la forma de representación, sirven para representar una variable o característica en función de su rango y sus cuartiles.

*Nota: Los cuartiles son 3 valores que dividen un conjunto de datos ordenados en 4 partes porcentualmente iguales.*

La visualización del boxplot consiste en una caja que comprende los datos desde el primer cuartil (Q1 - 25% de los datos bajo éste) al tercer cuartil (Q3 - 75% de los datos bajo éste) de los valores de la variable representada (rango intercuartil – IQR). Dentro de dicha caja, mediante una línea horizontal se representa el valor de la mediana y opcionalmente, mediante un asterisco o una estrella el valor de la media.

Además de la caja, en el gráfico también se visualizan 2 líneas horizontales que representan los valores típicos máximos y mínimos de nuestra variable, y a partir de los cuales se visualizan mediante puntos los valores atípicos de la distribución.

*Nota estadística: Los valores atípicos son aquellos que son numéricamente distantes del resto de datos de la variable. Tomando el Rango Intercuartil (IQR), se consideran valores atípicos aquellos que están por debajo de Q1 – 1,5 IQR o por encima de Q3 + 1,5 IQR*.  
</br>

* Ejemplo: Distribución de los pasajeros del Titanic por edad  

![Gráfico_Caja](/img/visualizaciones/grafico_caja.png)

## <a name="grafico_violin"></a>Diagramas de Violin
Los diagramas de violín se utilizan para visualizar simultáneamente la distribución de los datos y su densidad de probabilidad. Estos gráficos tan visuales consisten en una combinación de un diagrama de cajas (boxplots) y un diagrama de densidad. De esta manera tenemos representado mediante una línea negra gruesa o caja pequeña el intervalo intercuartil, mediante una línea negra fina el conjunto de datos típicos y mediante un punto blanco la mediana de la distribución.  
</br>

* Ejemplo: Distribución y densidad de los pasajeros del Titanic por edad  

![Gráfico_Violin](/img/visualizaciones/grafico_violin.png)

## <a name="grafico_dispersion"></a>Gráficos de dispersión
Los gráficos de dispersión (en inglés “scatter plots”) consisten en visualizaciones que muestran la relación de 2 variables de un conjunto de datos sobre dos ejes cartesianos. Son bastante útiles dado que permiten extraer información sobre la correlación entre dichas variables.  
</br>

* Ejemplo: Representación del precio del ticket por edad y género de los pasajero  

![Gráfico_Dispersion](/img/visualizaciones/grafico_dispersion.png)

## <a name="grafico_pareto"></a>Gráficos de Pareto
Los gráficos de Pareto sirven para representar visualmente aquellas distribuciones o conjuntos de datos que responden a la ley de Pareto o regla del 80/20.
Ley de Pareto: también conocida como la regla del 80/20, establece que de forma general en un conjunto de datos relacionado mediante una relación de causa-efecto, aproximadamente el 80% de los resultados o consecuencias proviene del 20% de las causas.
</br>

* Ejemplo: Representación de los datos de ingresos por tickets vendidos del Titanic  

![Gráfico_Pareto](/img/visualizaciones/grafico_pareto_1.png)  

![Gráfico_Pareto](/img/visualizaciones/grafico_pareto_2.png)

Sobre el ejemplo se observa la utilidad de este gráfico dado que rápidamente se visualiza como el 90% de los ingresos de venta de tickets del Titanic provienen de los tickets vendidos a los pasajeros de estatus socioeconómico Alto. O de manera más detallada sobre el segundo gráfico aproximadamente el 80% de los ingresos por venta de tickets procedían de ~20% de los pasajeros de la tripulación.  
</br>

#### Fuentes de interés:
- Kaggle – [Titanic Machine Learning from Disaster](https://www.kaggle.com/c/titanic)
- Datos abiertos del Gobierno de España – [datos.gob.es](https://datos.gob.es/es)
- El Arte de Presentar – [Las tartas son para el postre: 5 razones por las que no uso gráficos circulares](https://www.elartedepresentar.com/2011/11/las-tartas-son-para-el-postre-5-razones-por-las-que-no-uso-graficos-circulares/)
- Curso _“[Essential Statistics for Data Analysis using Excel](https://courses.edx.org/courses/course-v1:Microsoft+DAT222x+1T2017/course/)”_ perteneciente al Microsoft Data Science Program
- Catálogo de Visualización de Datos - [Catálogo de Visualización de Datos](https://datavizcatalogue.com/ES/)
