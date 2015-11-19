import json
import sys

#Find location of the happiest tweet
#-----------------------------------
def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    #sent_file = open(sys.argv[1])
    #tweet_file = open(sys.argv[2])
    sent_file = open("AFINN-111.txt")
    tweet_file = open("output.txt")
    
    twdata = [] # list containing all the tweets
    
    for line in tweet_file: #parse each line and store it as a list at data[index] 
        twdata.append(json.loads(line))
    
    scores = {} # initialize an empty dictionary
    for line in sent_file:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    
    #print len(twdata) # this is 40780
    
    #for i in range(len(twdata)):
    for i in range(70):
        
        if "text" in twdata[i].keys():
            unicode_string = twdata[i]["text"]
            encoded_string = unicode_string.encode('utf-8')
            tweet = encoded_string
            words = tweet.split()
            tweet_score = 0
        
            for w in words:
                if w in scores:
                    tweet_score+=scores[w]
                    #print w, scores[w]
                    
            #print i , twdata[i]["place"]# tweet, tweet_score
            if twdata[i]["place"]:
                 print i 
            #print tweet_score        
        else:  
            tweet_score = 0     
            tweet="no text"
            #print i, tweet, tweet_score
            print tweet_score, "no text"
   
    #print type(twdata[11])
    #print twdata[11].keys() # print keys of the dictionary twdata[11]
    #print type(twdata[11]["user"])
    print twdata[49]["place"].keys() #this is a dictionary as well! The keys should be
    print twdata[49]["place"]["country"] 
    #print type(twdata[49]["place"]["place_type"])
    print twdata[49]["place"]["full_name"]
    print type(twdata[49]["place"]["full_name"])
    ## country_code = US, country = United States, full_name : Dorall, FL
    print twdata[29]["place"]["country"] 
    print twdata[29]["place"]["full_name"]
    unicode_string = twdata[29]["place"]["full_name"]
    encoded_string = unicode_string.encode('utf-8')
    print encoded_string
    print type(encoded_string)
    location = encoded_string.split()
    print type(location)
    print location[0]
    print location[1]
    
    

if __name__ == '__main__':
    main()
