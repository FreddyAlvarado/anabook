# Programado por Freddy Alvarado - 2022/03/01
# freddy.alvarado.b1@gmail.com
#------------------------------------------------------------

from scipy import stats
from statistics import median
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import scipy.stats as scs

#------------------------------------------------------------
# FUCNIONES para el analisis exploratorio de datos
#------------------------------------------------------------

def simetria(column):
  kurt = 0.00
  skew = 0.00
  kurt = stats.kurtosis(column)
  skew = stats.skew(column)
  return kurt, skew

def graficosxy(df):
  df.plot(
      kind='line',
      subplots=True,
      layout =(8,3),
      figsize=(10,12)
  )
  plt.tight_layout()
  plt.show()
  
def histograma(df):
  
  nrows = len(df.columns)
  npar = nrows%2
  if (npar==1):
    nrows+=1
  nrows = nrows//2
  nh = nrows * 3
  
  # Setting up the figure and axes
  fig, axs = plt.subplots(nrows, 2, figsize=(8,nh))
  plt.subplots_adjust(hspace=0.5,wspace=0.3)
  
  # Plotting data
  columns = df.columns

  for i, column in enumerate(columns):
               
        ax = axs[i//2, i%2]

        # Plot histogram and KDE
        # Pasar, cuando no hay datos suficientes para el KDE
        ax = sns.histplot(df[column], kde=True, ax=ax, color='skyblue', bins=15)
        try:
            ax.lines[0].set_color('gray')
        except:
            pass
            
        # Plot average
        mean_value = df[column].mean()
        std_value = df[column].std()
        ax.axvline(mean_value, color='r', linestyle='--')

        ax.set_title(f"Campo: {column} - Media: {mean_value:.2f}", fontsize=10)

        # Setting x and y labels
        ax.set_xlabel('')
        ax.set_ylabel("Frecuencia")


  plt.tight_layout()
  plt.show()

def dispersion_index(df):
  
  nrows = len(df.columns)
  npar = nrows%2
  if (npar==1):
    nrows+=1
  nrows = nrows//2
  nh = nrows * 3
  ncols = len(df.columns)
  
  # Setting up the figure and axes
  fig, axs = plt.subplots(nrows, 2, figsize=(8,nh))
  plt.subplots_adjust(hspace=0.5,wspace=0.5)
  
  # Plotting data
  columns = df.columns

  for i, column_name in enumerate(columns):
               
      ax = axs[i//2, i%2]
                  
      row_index = i // ncols
      col_index = i % ncols

      ax.scatter(df.index, df[column_name])

      ax.set_title(column_name)
      # ax.set_xlabel('Index')
      ax.set_ylabel('Value')    


  plt.tight_layout()
  plt.show() 
 
def areaTrazadoBoxPlot(qcol):
  # Setea el area de dibujo
  nw = 0
  nh = 0
  if (qcol<=2):
    nw= 3
    nh= 6
  elif (qcol > 2 and qcol<=4):
    nw= 8
    nh= 6
  elif (qcol > 4):
    nw= 14
    nh= 6

  plt.rcParams['figure.figsize']=(nw,nh)
  return (nw,nh)
  
# inputs, lista de campos numericos
def boxplot2(df, inputs):
    num_inputs = len(inputs)
    fig, axs = plt.subplots(1, num_inputs, figsize=areaTrazadoBoxPlot(num_inputs))
    axs = np.array(axs)
    for i, (ax, curve) in enumerate(zip(axs.flat, inputs), 1):
        sns.boxplot(y=df[curve], ax=ax, color='cornflowerblue', showmeans=True,
                meanprops={"marker":"o",
                           "markerfacecolor":"white",
                           "markeredgecolor":"black",
                          "markersize":"10"},
               flierprops={'marker':'o',
                          'markerfacecolor':'darkgreen',
                          'markeredgecolor':'darkgreen'})

        ax.set_title(inputs[i-1])
        ax.set_ylabel('')

    plt.subplots_adjust(hspace=0.15, wspace=1.25)
    plt.show()   

#------------------------------------------------------------
# EDA
#------------------------------------------------------------

def categorical(df):
  print('')
  print('GRAFICOS DE BARRAS')
  print('')

  # Variables string
  colCat = []
  for i in df.columns:
    if (df[i].dtype !='float64'):
        colCat.append(i)      

  # Calculo del numero de filas necesario basado en el numero de columnas categoricas
  num_col = 3  # Numero de columnas por fila en la grilla
  num_filas = np.ceil(len(colCat) / num_col).astype(int)

  # Crear una figura y un conjunto de subgraficos
  fig, axes = plt.subplots(num_filas, num_col, figsize=(12, 3*num_filas))

  # Aplanar el array de axes para facilitar su uso en un loop
  axes = axes.flatten()

  for i, columna in enumerate(colCat):
    # Contar la frecuencia de cada categoria en la columna actual
    conteo = df[columna].value_counts()
    
    # Crear el grafico de barras en el subplot correspondiente
    conteo.plot(kind='bar', ax=axes[i])
    axes[i].set_ylabel('Frecuencia')
    axes[i].set_xlabel(columna)
    
    # Verificar la cantidad de etiquetas del eje X
    if len(conteo) > 20:
        # Si hay más de 20 etiquetas, ocultarlas
        axes[i].set_xticklabels([])
    else:
        # Si hay 20 etiquetas o menos, rotarlas para mejor legibilidad
        axes[i].tick_params(axis='x', rotation=45)


  # Ocultar los axes adicionales si el numero de columnas categoricas no llena la ultima fila
  for j in range(i+1, num_filas * num_col):
    fig.delaxes(axes[j])

  plt.tight_layout()  # Ajustar automaticamente los parametros de la subtrama
  plt.show()
    
def continuos(df):
  import warnings 
  warnings.filterwarnings('ignore')
  from tabulate import tabulate
  
  pd.set_option('display.float_format', lambda x: '%.3f' % x)
  oLista = []
  oIndex = []
  nCol = 0
  
  # Variables float64
  colNum = []
  for i in df.columns:
    if (df[i].dtype.kind in 'fi'):
        colNum.append(i)
        
  # Setea solo las columnas numericas
  df = df[colNum]

  dfContinuo = pd.DataFrame()

  for i in df.columns:

    if (df[i].dtype=='decimal' or df[i].dtype=='float'):

      nCol +=1
      dfContinuo[i] = df[i]
      describe = df[i].describe()

      for j in range(len(describe)):
        varNum = describe.iloc[j:j+1].values[0]
        describe[describe.index[j]] = '{:.5f}'.format(varNum)

      dk = stats.kurtosis(df[i])
      ds = stats.skew(df[i])
      dmedian = median(df[i])

      stat, p = scs.normaltest(df[i])

      describe['median']= '{:.5f}'.format(dmedian)
      describe['kurt']= '{:.5f}'.format(dk)
      describe['skew']= '{:.5f}'.format(ds)
      describe['test_stat']= '{:.5f}'.format(stat)
      describe['p-value']= '{:.5f}'.format(p)

      # H0, muestra proviene de una dist normal
      # H1, nuestra NO  proviene de una dist normal
      if (float(p) < float(0.05)):
        # Se rechaza H0
        describe['norm 5%']= 'no'
      else:
        #Se acepta H0
        describe['norm 5%']= 'si'

      oLista.append(describe)
      # Indices
      oIndex.append(i)
      #end for

  dfEstat = pd.DataFrame(oLista, index=oIndex)
  
  print('\033[1mANALISIS EXPLORATORIO DE DATOS PARA VARIABLES CONTINUAS\033[0m')
  print('')
  print('\033[1mESTADISTICOS DESCRIPTIVOS UNIVARIADOS\033[0m')
  table = tabulate(dfEstat.T, headers='keys', tablefmt='fancy_grid')
  print(table)
  print('')
  
  print('\033[1mANALISIS DE VALORES NULOS\033[0m')
  df_info = pd.DataFrame({'type': df.dtypes,
                        'nulos': df.isnull().sum(),
                        'no_nulos': df.notnull().sum()})
  
  table = tabulate(df_info, headers='keys', tablefmt='fancy_grid')
  print(table)

  plt.rcParams['figure.figsize']=(4,3)
  # Mapa de Calor
  sns.heatmap(dfContinuo.isnull())
  plt.show()

  print('')
  print('\033[1mHISTOGRAMAS\033[0m')
  histograma(df)
  
  print('')
  print('\033[1mGRAFICOS BOXPLOT\033[0m')
  boxplot2(df, dfContinuo.columns)

  print('')
  print('\033[1mGRAFICOS DE DISPERSION\033[0m')
  dispersion_index(df)

  print('')
  print('\033[1mGRAFICOS XY\033[0m')
  graficosxy(df)
  plt.show()
  plt.rcParams['figure.figsize']=(6,6)

#------------------------------------------------------------
# ANALISIS BIVARIADO (solo variables numericas)
#------------------------------------------------------------

def bivariado(df):
  
  # Variables float64
  colNum = []
  for i in df.columns:
    if (df[i].dtype.kind in 'fi'):
        colNum.append(i)
        
  # Setea solo las columnas numericas
  df = df[colNum]

  print('  ANALISIS BIVARIADO  ')
  print('  --------------------')
  dispersion(df)
  correlograma(df)

def dispersion(df):
  print('  GRAFICOS DE DISPERSION POR CADA PAR DE CAMPOS  ')
  pairplot = sns.pairplot(df)
  pairplot.fig.subplots_adjust(right=0.5, bottom=0.5)
  plt.show()
  
def correlograma(df):
  nrows = len(df.columns)
  nw =0
  nh=0
  if (nrows<= 6 ):
    nw = 4
    nh = 3
  elif (nrows <= 12):
    nw = 8
    nh = 6
  else:
    nw = 10
    nh = 8

  print('  GRAFICO CORRELOGRAMA  ')
  plt.rcParams['figure.figsize'] = (nw, nh)
  # Correlograma
  df_corr = df.corr()
  sns.heatmap(df_corr,
            xticklabels = df_corr.columns,
            yticklabels = df_corr.columns,
            cmap='coolwarm',
            annot=True)
  plt.show()
  #------------------------------------------------------------