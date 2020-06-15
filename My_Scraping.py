# -*- coding: utf-8 -*-
"""
Created on Thu May 28 18:06:47 2020

@author: buttl
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
years_list=[1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,
            2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]

def SelBest(arr:list, X:int)->list:
    '''
    returns the set of X configurations with shorter distance
    '''
    dx=np.argsort(arr)[:X]
    return arr[dx]

def create_df(year):

    # NBA season we will be analyzing
    #year = 2013
    ####### URL page we will scraping NBA Rookies ########
    url = "https://www.basketball-reference.com/leagues/NBA_{}_rookies-season-stats.html".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)
    
    # use findALL() to get the column headers
    keep=soup.findAll('tr', limit=2) not in soup.findAll('tr', limit=1)
    keep=soup.findAll('tr', limit=2)[keep]
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in keep.findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    headers
    
    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    
    rookie_stats = pd.DataFrame(player_stats, columns = headers)
    rookie_stats.head(10)
    
    
    
    #### Grab Per 36 Minutes stats ########
    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_minute.html".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)
    
    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    headers
    
    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    
    min_stats = pd.DataFrame(player_stats, columns = headers)
    min_stats.head(10)
    
    ###### Grab Advanced Stats as well #####
    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)
    
    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    headers
    
    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    
    advanced_stats = pd.DataFrame(player_stats, columns = headers)
    advanced_stats.head(10)
    
    
    #Keep only Rookie per 36 minute stats
    joined_rookie_stats = pd.merge(rookie_stats[['Player','Age']],min_stats,  how='left', left_on=['Player','Age'], right_on = ['Player','Age'])
    joined_rookie_stats=joined_rookie_stats.dropna()
    
    #Keep only Total season stats
    tot_players=joined_rookie_stats[joined_rookie_stats.Tm == 'TOT']
    removed_players=(~joined_rookie_stats.iloc[:,0].isin(tot_players.iloc[:,0]))

    joined_rookie_stats=joined_rookie_stats[removed_players]

    joined_rookie_stats=joined_rookie_stats.append(tot_players)
    
    tot_players=advanced_stats[advanced_stats.Tm == 'TOT']
    removed_players=(~advanced_stats.iloc[:,0].isin(tot_players.iloc[:,0]))

    advanced_stats=advanced_stats[removed_players]

    #Join the dataframes together
    advanced_stats=advanced_stats.append(tot_players)
    advanced_stats.drop(['Pos','Tm', 'G', 'MP'], axis = 1,inplace=True)
    joined_rookie_stats= pd.merge(joined_rookie_stats, advanced_stats,  how='left', left_on=['Player','Age'], right_on = ['Player','Age'])
    joined_rookie_stats.drop(joined_rookie_stats.columns[[40, 45]], axis = 1,inplace=True)
    
    #store in year specific dataframe
    locals()["rookies_"+str(i)]=pd.DataFrame(joined_rookie_stats)
    
    return locals()["rookies_"+str(i)]


for i in years_list:
    locals()["rookies_"+str(i)]=create_df(i)


all_rookies=rookies_1980.append([rookies_1981,rookies_1982,rookies_1983,rookies_1984,rookies_1985,rookies_1986,
                                 rookies_1987,rookies_1988,rookies_1989,rookies_1990,rookies_1991,rookies_1992,
                                 rookies_1993,rookies_1994,rookies_1995,rookies_1996,rookies_1997,rookies_1998,
                                 rookies_1999,rookies_2000,rookies_2001,rookies_2002,rookies_2003,rookies_2004,
                                 rookies_2005,rookies_2006,rookies_2007,rookies_2008,rookies_2009,rookies_2010,
                                 rookies_2011,rookies_2012,rookies_2013,rookies_2014,rookies_2015,rookies_2016,
                                 rookies_2017,rookies_2018,rookies_2019,rookies_2020])

# resetting index 
all_rookies.reset_index(inplace = True) 

all_rookies=all_rookies.iloc[:,1:]

#Adjusting the data type and NA values
all_rookies.G=all_rookies.G.astype('int')
all_rookies[["Age", "G","GS","MP","FG","FGA","FG%","3P","3PA","3P%","2P","2PA","2P%","FT","FTA","FT%",
             "ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS",'PER', 'TS%', '3PAr',
             'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
             'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']] = all_rookies[["Age", "G","GS","MP",
             "FG","FGA","FG%","3P","3PA","3P%","2P","2PA","2P%","FT","FTA","FT%",
             "ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS",'PER', 'TS%', '3PAr',
             'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
             'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']].apply(pd.to_numeric)

all_rookies.GS=all_rookies.GS.fillna(0)

#Keep only Rookies who played at least 10 games, more than 90 minutes, and more than an average of 9 mpg                                                                                
kept_rookies=all_rookies[all_rookies.G >9]

kept_rookies=kept_rookies[kept_rookies.MP > 90]

kept_rookies.loc[:,'avg_min']=kept_rookies['MP']/kept_rookies['G']

kept_rookies=kept_rookies[kept_rookies.avg_min > 9]

kept_rookies.reset_index(inplace = True) 

kept_rookies=kept_rookies.iloc[:,1:]

kept_rookies=kept_rookies.fillna(0)

#Write to csv
kept_rookies.to_csv('C:\\Users\\buttl\\OneDrive\\DAProjects\\NBA_Web_Scraping\\Kept_Rookies.csv', index=False)
all_rookies.to_csv('C:\\Users\\buttl\\OneDrive\\DAProjects\\NBA_Web_Scraping\\All_Rookies.csv', index=False)





######### Attempting PCA ############
#####################################
features = ["G","GS","MP",
             "FG","FGA","FG%","3P","3PA","3P%","2P","2PA","2P%","FT","FTA","FT%",
             "ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS",'PER', 'TS%', '3PAr',
             'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',
             'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP','avg_min']

off_features=["AST","PTS",'OWS','OBPM']
def_features=["STL","BLK",'DWS','DBPM']
#use_features=["G","GS","MP",'USG%']
use_features=["avg_min",'USG%']
eff_features=['VORP','PER','TS%']
reb_features=["ORB","DRB","TRB"]

off_pca_values = kept_rookies.loc[:, off_features].values
def_pca_values = kept_rookies.loc[:, def_features].values
use_pca_values = kept_rookies.loc[:, use_features].values
eff_pca_values = kept_rookies.loc[:, eff_features].values
reb_pca_values = kept_rookies.loc[:, reb_features].values

y = kept_rookies.loc[:, ['Player']].values

off_pca_values = StandardScaler().fit_transform(off_pca_values)
def_pca_values = StandardScaler().fit_transform(def_pca_values)
use_pca_values = StandardScaler().fit_transform(use_pca_values)
eff_pca_values = StandardScaler().fit_transform(eff_pca_values)
reb_pca_values = StandardScaler().fit_transform(reb_pca_values)


#Create teh pcas
pca = PCA(n_components=1)

principalComponents_off = pca.fit_transform(off_pca_values)
principalComponents_def = pca.fit_transform(def_pca_values)
principalComponents_use = pca.fit_transform(use_pca_values)
principalComponents_eff = pca.fit_transform(eff_pca_values)
principalComponents_reb = pca.fit_transform(reb_pca_values)


pca_off_Dataframe = pd.DataFrame(data = principalComponents_off, columns = ['PCA_Off'])
pca_def_Dataframe = pd.DataFrame(data = principalComponents_def, columns = ['PCA_Def'])
pca_use_Dataframe = pd.DataFrame(data = principalComponents_use, columns = ['PCA_Use'])
pca_eff_Dataframe = pd.DataFrame(data = principalComponents_eff, columns = ['PCA_Eff'])
pca_reb_Dataframe = pd.DataFrame(data = principalComponents_reb, columns = ['PCA_Reb'])



#Add names back to PCA values
targetDataframe = kept_rookies[['Player']]

pca_Dataframe = pd.concat([pca_off_Dataframe, pca_def_Dataframe, pca_use_Dataframe,pca_eff_Dataframe,
                           pca_reb_Dataframe, targetDataframe],axis = 1)




########## determine appropriate number of clusters ###############
### Calculating AIC and BIC, lower values are the most ideal for number of clusters

#columns=['PTS','AST%','TRB%','PER','DWS','avg_min']
#columns=['PTS','AST%','TRB%','PER','DWS','OWS','avg_min']
pca_col=['PCA_Off','PCA_Def','PCA_Use','PCA_Eff','PCA_Reb']
x=pca_Dataframe[pca_col]
n_components=np.arange(1,50)
models=[GaussianMixture(n,covariance_type='full',n_init=10,random_state=0).fit(x) for n in n_components]

plt.plot(n_components,[m.bic(x) for m in models],label='BIC')
plt.plot(n_components,[m.aic(x) for m in models],label='AIC')
plt.legend(loc='best')
plt.xlabel('n_components')

# Creating a Silhouette score
## This wont work because there are not any "Correct" Clusters
# n_clusters=np.arange(2, 50)
# sils=[]
# sils_err=[]
# iterations=20
# for n in n_clusters:
#     tmp_sil=[]
#     for _ in range(iterations):
#         gmm=GaussianMixture(n, n_init=2).fit(x) 
#         labels=gmm.predict(x)
#         sil=metrics.silhouette_score(x, labels, metric='euclidean')
#         tmp_sil.append(sil)
#     val=np.mean(SelBest(np.array(tmp_sil), int(iterations/5)))
#     err=np.std(tmp_sil)
#     sils.append(val)
#     sils_err.append(err)

# plt.errorbar(n_clusters, sils, yerr=sils_err)
# plt.title("Silhouette Scores", fontsize=20)
# plt.xticks(n_clusters)
# plt.xlabel("N. of clusters")
# plt.ylabel("Score")


###########################
# Begin Clustering
###########################
# training gaussian mixture model 
#columns=['PTS','AST%','TRB%','PER','DWS','avg_min']
pca_col=['PCA_Off','PCA_Def','PCA_Use','PCA_Eff','PCA_Reb']
x=pca_Dataframe[pca_col]

gmm = GaussianMixture(n_components=42,n_init=500, random_state=0)
gmm.fit(x)
gmm.get_params
gmm.aic(x)
gmm.bic(x)
#predictions from gmm
labels = gmm.predict(x)
frame = pd.DataFrame(x)
frame['cluster'] = labels
frame['Player']=kept_rookies['Player']
#frame.columns = ['Weight', 'Height', 'cluster']

color=['blue','green','cyan', 'black']
for k in range(0,4):
    data = frame[frame["cluster"]==k]
    plt.scatter(data["PTS"],data["avg_min"],c=color[k])
plt.show()

cluster_averages=frame.groupby(['cluster']).mean()
cluster_averages['Cluster_Score']=cluster_averages.sum(axis=1)



frame.to_csv('C:\\Users\\buttl\\OneDrive\\DAProjects\\NBA_Web_Scraping\\pca_Rookie_cluster.csv', index=False)
cluster_averages.to_csv('C:\\Users\\buttl\\OneDrive\\DAProjects\\NBA_Web_Scraping\\cluster_scores.csv', index=True)


frame.cluster.value_counts()


