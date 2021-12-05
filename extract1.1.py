
import tweepy

from tweepy import * 
import pandas as pd
import csv


    
def extractTweets(keyword,count):
    api_key = "UrPC07rW7E0Ro2IcxMELfZclI"
    api_secret = "lMROraf7SNl82yxoChuB7UcYVMlzDqnBlU8ISswjilhwpB1XxZ"

    access_token = "1405058774684078081-0mA6iWrM2K7MJLKc3wzbmjeNo99wia"
    access_secret = "k1FPEiyM4pns3e4DRLQToY7rCipk5WhsTfhiTSihCa4z2"


    auth=tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)

    apitweet=tweepy.API(auth)
    
    
    
    

    
    df=pd.DataFrame(columns=['DateTime','Tweet_Id','Tweet','User_Id','Retweet','Location','Label'])
        
    n=0
    tweets=tweepy.Cursor(apitweet.search,wait_on_rate_limit=True,q=keyword,
                                 lang="en",count=count).items(50)
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

        
    return df

csvFile = open('final-universal', 'a')
csvWriter = csv.writer(csvFile)

df=extractTweets("POTUS",50)
#print(df)
csvWriter.writerow([df])

        
       
