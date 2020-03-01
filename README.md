# Distinguishing between subreddits: "One Punch Man" VS "Death Note"

## Problem Statement

An devious troll has hacked Reddit! They posted the following:

> When an anime character can simply kill opponents in one punch or by writing a name in a notebook, the plot quickly becomes stale and boring! Such shows become indistinguishable from each other. As proof, I've randomly swapped posts between r/OnePunchMan and r/deathnote - not that anyone could tell the difference, since there is virtually no difference between these shows.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - *Boop*

Fortunately, I've recently stored posts from both r/OnePunchMan and r/deathnote.   

Using Natural Language Processing, I should be able to develop a Logistic Regression, K-nearest Neighbors, Naive Bayes, or other model to accurately predict which subreddit a post belongs to based on its title alone. Accuracy will be used to assess model effectiveness.

If an effective model can be found, I can undo the havoc caused by the troll hacker, while also disproving their belief these shows are the same! __"One Punch Man" and "Death Note" fans on Reddit__ will be able to enjoy their online spaces in peace and __Reddit developers__ would have a potential model to use, should such an incident were to happen again.

## Project Data
The data obtained come from the [r/OnePunchMan](https://www.reddit.com/r/OnePunchMan/) and [r/deathnote](https://www.reddit.com/r/deathnote/) subreddits using the [Reddit API](https://www.reddit.com/dev/api/) on Wednesday July 10th, 2019.

## Executive Summary
When I started this project, I assumed the difference between the r/deathnote and r/OnePunchMan would be simply reliant on words related to their unique named characters and places as well as topics, such as "death" in Death Note. During the EDA and afterwards, while investigating my final model, it was clear the data had more going on than I gave it credit for. Of course there were tight associations with the named characters, but I was not anticipating seeing temporal features. Likewise, there were some words that had a strong connection with r/deathnote that I still cannot explain.

Given the vast number of classification models and combining them with 2 different vectorizors quickly got out of hand. This forced me to streamline the model exploration process and develop a deliberate and repeatable workflow. I first attempted to resolve the issue by creating a complex `EnsembleGridSearchCV`, which worked much like `GridSearchCV`, but for  multiple models. It took in a list of transformers and estimators as well as a dictionary of parameters and did a grid search across all transformer + estimator combinations, returning a `VotingClassifier` combining all of the optimized models into one model. This was ultimately scrapped for being overly complicated (not to mention it took too long to process!).

I settled for a more lightweight solution in creating the `AdvancedGridSearch` function to simply handle a single `Pipeline` estimator and optimize for it.  

I was also surprised by the high model accuracy I began seeing right away. The distinct nature of the subreddits were clearly strong, but the reason for that distinction had little to do with the shows themselves, but rather an indirect indicator of whether the show was currently in production or not (One Punch Man only recently ended its 2nd season, while Death Note was finished years ago). 

I was also surprised to find the optimum model was not one of the more typically high performing ones, like one of the ensemble classifiers. I learned that, as great as the ensemble class of models are, there is still benefit in exploring simplier models first. It really is better to start exploring the data with a basic model and use those findings to make informed decisions in progressing onto more complex and fine-tuned models. I realize now, how overzealous I was in trying to test so many newly learned models. After seeing such high accuracy with the Logistic Regression or even the Naive Bayes models, there really was little rational to continue exploring more complicated models - especially those designed to address problems of overfitting or high variance (something I was not seeing!).

## Conclusion:
- After assessing the data from both subreddits, it was clear there were distinguishing features present.  
- The data were cleaned by lowercasing all text, removing special characters and numbers, and removing the lowest impact stop words. Each word was also stemmed using SnowballStemmer (english).    
- A model baseline for accuracy was established by using the most frequent outcome, r/deathnote at ~61% accuracy.  
- Then, after fitting various combinations of vectorizers and models, a single model was selected, the CVEC + MultNB model.
- This selected model performed well, with a 97% accuracy on the testing dataset.

__Therefore, it is possible to thwart the hacker's actions! With ~97% accuracy, the swapped posts can successfully be assigned to their respective subreddits.__ 

## Assumptions:
In order to arrive at this conclusion, a number of assumptions were made.
1. It was assummed removing casing, special characters and numbers would not have a significant effect on the result. It is possible some of these missing features could have played some role in helping to distinguish subreddits and improve accuracy.
2. The Naive Bayes model assumes features are independent and unrelated. However, this requirement is most certainly violated in this case, since language necessarily has order and rules associated with it.
3. After using the TfidfVectorizer (TFIDF) for a few models, I stopped including it in my model experiments, assuming it was inferior to CVEC. It is possible if the TFIDF was used in all model combinations, an even more accurate model could have been discovered.
4. The starting data was unbalanced, favoring r/deathnote. By keeping these classes unbalanced, it is assumed this imbalance will not affect the model, however it is possible some bias against r/OnePunchMan exists.

## Recommendations:
This model has a high dependence on the temporal markers found in the One Punch Man subreddit. As such, I would not recommend using this model after the One Punch Man anime is out of season or has concluded.

The issue over unbalanced classes could be rectified using bootstrapping as a means to "boost" the number of observations for the minority class (r/OnePunchMan).

I was surprised to find my best model to not be the VotingClassifier. However, I know ensemble models tend to require more fine-tuning and if I could go back and work on this problem again I would consider adding weights for each model's vote as a way to increase the ensemble's accuracy.

Another weakness of the production model is its lack of portability. The model will only work well on determining the r/deathnote and r/OnePunchMan subreddits, the data it was trained on, and even then only for a short period of time! To better accomodate for more subreddits/classes, a larger number of subreddits would need consideration. With that said, the immediate issue of returning the subreddits to their intended state can be effectively addressed using the produced model. Also, Reddit developers can use this model in some instances in the future (when One Punch Man is active).

## Sources
1. [Reddit API](https://www.reddit.com/dev/api/)
2. [r/OnePunchMan](https://www.reddit.com/r/OnePunchMan/) 
3. [r/deathnote](https://www.reddit.com/r/deathnote/) 