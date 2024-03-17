from scipy import stats
from statistics import median
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import scipy.stats as scs


# Funciones para el analisis exploratorio de datos
# ------------------------------------------------

# función para el calculo de la curtosis y asimetria
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
      ax = sns.histplot(df[column], kde=True, ax=ax, color='skyblue', bins=15)
      ax.lines[0].set_color('gray')

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

#--------------------

def describe1(dfColumn):
  pd.set_option('display.float_format', lambda x: '%.3f' % x)
  describe = dfColumn.describe()
  dic_describe = describe.to_dict()
  dk = stats.kurtosis(dfColumn)
  ds = stats.skew(dfColumn)
  nIdx = 0
  for clave, valor in dic_describe.items():
    valor['curtosis']= dk[nIdx]
    valor['asimetria']= ds[nIdx]
    nIdx+=1
  dfEstat = pd.DataFrame(dic_describe)
  dfEstat
  return dfEstat

def describe2(df):
  oLista = []
  oIndex = []
  nCol = 0
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
      describe['p-value']= p

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

  print('')
  print('ESTADISTICOS DESCRIPTIVOS UNIVARIADOS')
  print('_____________________________________')
  print(dfEstat.T)
  print('')
  print('ANALISIS DE VALORES NULOS')
  print('_____________________________________')
  # print(df.info())
  df_info = pd.DataFrame({'type': df.dtypes,
                        'nulos': df.isnull().sum(),
                        'no_nulos': df.notnull().sum()})
  print(df_info)

  plt.rcParams['figure.figsize']=(4,3)

  # Mapa de Calor
  sns.heatmap(dfContinuo.isnull())
  plt.show()

  print('')
  print('HISTOGRAMAS')
  print('_____________________________________')
  histograma(df)

  print('')
  print('GRAFICOS BOXPLOT (variables continuas)')
  print('___________________________________________')
  boxplot2(df, dfContinuo.columns)

  print('')
  print('GRAFICOS XY')
  print('___________')
  graficosxy(df)

  plt.show()

  plt.rcParams['figure.figsize']=(6,6)