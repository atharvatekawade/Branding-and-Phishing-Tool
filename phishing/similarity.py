import numpy as np

class Similarity:
     def __init__(self,w1,w2,weight=1):
          self.w1=w1
          self.w2=w2
          self.lev=0
          self.jaro=0
          self.weight=weight
          self.score=0

     def levenshtein_ratio(self):
          s=self.w1
          t=self.w2
          rows = len(s)+1
          cols = len(t)+1
          distance = np.zeros((rows,cols),dtype = int)

          for i in range(1, rows):
               for k in range(1,cols):
                    distance[i][0] = i
                    distance[0][k] = k

          for col in range(1, cols):
               for row in range(1, rows):
                    if s[row-1] == t[col-1]:
                         cost = 0
                    else:
                         cost=2
                         distance[row][col] = min(distance[row-1][col] + 1,distance[row][col-1] + 1,distance[row-1][col-1] + cost)   
          
          Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
          self.lev=Ratio

     def jaro_ratio(self,p=0.1):
          s=self.w1
          t=self.w2
          d1={}
          d2={}

          for i in s:
               if i not in d1:
                    d1[i]=0
               else:
                    d1[i]=d1[i]+1

          for i in t:
               if i not in d2:
                    d2[i]=0
               else:
                    d2[i]=d2[i]+1

          m=0
          for i in d1:
               if i in d2:
                    m=m+min(d1[i],d2[i])
          
          mis=0
          for i in range(min(len(s),len(t))):
               if(s[i]!=t[i]):
                    mis=mis+1

          mis=mis/2

          if(len(s)==0 or len(t)==0 or m==0):
               self.jaro=0
               return
          
          dist_j=1+m/len(s)+m/len(t)-mis/m
          dist_j=dist_j/3


          l=0
          for i in range(0,min(len(s),len(t),4)):
               if(s[i]==t[i]):
                    l=l+1
               else:
                    break
          
          self.jaro=dist_j+l*p*(1-dist_j)

     def final_score(self):
          self.levenshtein_ratio()
          self.jaro_ratio()
          self.score=self.weight*self.lev+(1-self.weight)*self.jaro

