# -*- coding: utf-8 -*-
"""
Created in August 2021

@author: chirayu
"""
import numpy as np
from matplotlib import pyplot as plt
import random
'''Read the README.md file in the repository for an explanation of the model'''
percentage=0.02 #Proportion that buyer or seller is willing to adjust their price
Days_till_bankrupt=5
class seller():
    def __init__(self):
        self.min=abs(np.random.normal(100, 15))
        self.sold=False #Records if they sold in current day or not
        self.hist=0 #Adds a history to the seller, if they cant sell anything for a certain amount of days in a row then bankrupt 
        
class buyer():
    def __init__(self):
        self.max=abs(np.random.normal(150, 15))
        self.bought=False #Records whether the buyer succesfully bought in the current day

Days=100
Total_buyers=50
Total_sellers=50

def make_buyers(Total_buyers):
    buyers=[]
    for i in range(Total_buyers):
        buyers.append(buyer())
    return buyers
def make_sellers(Total_sellers):
    sellers=[]
    for i in range(Total_sellers):
        sellers.append(seller())
    return sellers


        
def barter(b1, s1):
    '''sd is short for standard deviation and is proportional to the difference
    in the min selling and max buying price. The final bartered price that the buyer buys
    for is normally distributed, with the mean as the halfway point between the seller min and 
    buyer max. In the rare case the normal dist gives a price below the min seller price then
    sold for min seller price and if above max buyer price then price equals the max buyer price.'''
    sd=(b1.max-s1.min)/50
    mean=(b1.max+s1.min)/2
    p=np.random.normal(mean, sd)
    if p>s1.min and p<b1.max:
        price=p
    elif p<=s1.min:
        price=s1.min
    elif p>=b1.max:
        price=b1.max
        
    return price

'''The two functions below adjust the prices for sellers and buyers repectilvely, in proportion to their surplus'''
def sell_adjust(price, s1):
    if s1.sold:  #If seller sold then depending on how much above his min he sold for he will increase min price
        s1.min=price-0.2*(price-s1.min)#s1.min=s1.min+0.1*(price-s1.min) #little bit less than the price he sold at the previous day
    else:
        s1.min=s1.min*(1-percentage) #decreases the min asking price by 5%
        
def buy_adjust(price, b1):
    if b1.bought:
        b1.max=price+0.1*(b1.max-price)#b1.max-0.1*(b1.max-price) #Since he bought he lowers the max price he is willing to pay
    else:
        b1.max=b1.max*(1+percentage) #Willing to pay 5% more since he didn't buy the previous day
        

def mean(arr):
    tot=0
    for i in arr:
        tot+=i
    return tot/len(arr)

def resetsold(buyers, sellers):#At the beginning of the day everything is reset
    for i in buyers:
        i.bought=False
    for j in sellers:
        j.sold=False
    return buyers, sellers
        
def bankruptcy(arr):
    '''If the seller does not sell for 3 consecutive days then becomes bankrupt, 
    nd the seller is removed. Note that this functionality of bankruptcy can be removed by commenting
    out line 109'''
    for s in arr:
        if s.hist>=4:
            arr.remove(s)
    return arr


av_prices=[]# List for average prices each day
days=[]
sellers_left=[]
def main():
    buyers=make_buyers(Total_buyers)
    sellers=make_sellers(Total_sellers)
    for i in range(Days):
        sellers=bankruptcy(sellers)
        prices=[]
        buyers, sellers=resetsold(buyers, sellers)
        random.shuffle(buyers) #random order of buyers for each day
        random.shuffle(sellers)
        for b in range(len(buyers)):
            sell_found=False
            for s in range(len(sellers)):
                
                if buyers[b].max>=sellers[s].min and sellers[s].sold==False:
                    price=barter(buyers[b], sellers[s])
                    prices.append(price)
                    #print('price: ', price)
                    buyers[b].bought=True
                    sellers[s].sold=True
                    sell_adjust(price, sellers[s])
                    buy_adjust(price, buyers[b])
                    sell_found=True
                    break
            if sell_found==False:
                buyers[b].bought=False
                buy_adjust(0, buyers[b])
        for a in sellers:
            if a.sold==False:
                sell_adjust(0, a)
                a.hist+=1
            else:
                a.hist-=1
            if a.hist<0:
                a.hist=0
                
        if len(prices)>0:
            average=mean(prices)
        else:
            average=0
        av_prices.append(average)# av_prices is a measure of the average selling price if sold for each day
        sellers_left.append(len(sellers))
        days.append(i)
    
    fig, axs=plt.subplots(2)
    axs[0].plot(days, av_prices)
    axs[0].set_xlabel('Days')
    axs[0].set_ylabel('Average selling price')
    axs[0].set_title('Average price against days for {0} initial buyers and {1} initial sellers'.format(Total_buyers, Total_sellers ))
    
    #comment the following 5 lines if the program is run without the bankruptcy 
    
    axs[1].plot(days, sellers_left)
    axs[1].set_ylabel('Sellers left')
    axs[1].set_xlabel('Days')#
    axs[1].set_title('Remaining buyers against number of trading days' )
       
main()


    

        
