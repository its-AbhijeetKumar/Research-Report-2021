


import tweepy
from tweepy.streaming import StreamListener
from tweepy import * 
import pandas as pd

from .clean import cleanTweet



def extraction():
    api_key = "..........................................."
    api_secret = "......................................."

    access_token = "................................."
    access_secret = ".................................."

    auth=tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)
            
    apitweet=tweepy.API(auth)
                      
    trends=apitweet.trends_place(2282863) #WOEID for India https://codebeautify.org/jsonviewer/f83352
        
    trends_dic={}
    
    for i in trends[0]['trends']:
        if i['tweet_volume'] !=None:
            trends_dic[i['name']]=i['tweet_volume']
                
    return trends_dic
    '''    
    df_dic={}
    
    for i in trends_dic.keys():
        df=extractTweets(i,100,apitweet)
           
        df_dic={'dataframe':df,'volumes':trends_dic[i]}
    
    return df_dic
    '''
    
def extractTweets(keyword,count):
    api_key = ".........................................."
    api_secret = "........................................."

    access_token = "......................................."
    access_secret = "............................................."


    auth=tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)

    apitweet=tweepy.API(auth)

    
    df=pd.DataFrame(columns=['DateTime','Tweet_Id','Tweet','User_Id','Retweet','Location','Label'])
        
    n=0
    tweets=tweepy.Cursor(apitweet.search,wait_on_rate_limit=True,q=keyword,
                                 lang="en",count=count).items(200)
    for tw in tweets:
                
            try:
                    df.loc[n,'DateTime']=tw.created_at
                    df.loc[n,'Location']=tw.user.location
                    df.loc[n,'Retweet'] = tw.retweet_count
                    df.loc[n,'Tweet_Id'] = tw.id
                    df.loc[n,'User_Id'] = tw.entities['user_mentions'][0]['id']
                    df.loc[n,'Tweet']=tw.text
                    
                    n+=1                         
            
            except:
                    pass


    df.drop_duplicates(subset ="Tweet",keep=False,inplace=True)

    df.reset_index(inplace = True)
    df=df.drop(columns=['index'])




    for i in range(len(df)):

        df['Tweet'][i]=cleanTweet(df['Tweet'][i])

        
    return df

        
       
