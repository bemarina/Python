import json
import sys

#Find location of the happiest tweet
#--------------------------------------

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
                    
            if twdata[i]["place"]:
                 print i 
        else:  
            tweet_score = 0     
            tweet="no text"
            print tweet_score, "no text"
   
    print twdata[49]["place"].keys() #this is a dictionary as well! The keys should be
    print twdata[49]["place"]["country"] 
    print twdata[49]["place"]["full_name"]
    print type(twdata[49]["place"]["full_name"])
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
