#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm
Main:
    assigns filepointer by referencing open_file function
    assigns master dictionary by referencing read_file function using fp
    adds the per capita values to each list of lists in master dictionary using add per capita function
    prints data for each region in master dictionary using display data function
    closing statement
"""

import csv
from operator import itemgetter

def open_file():
    '''prompts for a filename until it can be opened
    returns filepointer
    '''
    i = 0#sets variable to exit loop
    while i ==0:#continues loop until variable is changed
        try:
            file_name = input("Input a file: ")#prompts for file name
            fp = open(file_name,'r')#tries to open the file
            return fp#returns filepointer if file can be opened
            i = 1#changes variable to exit loop
        except FileNotFoundError:
            print("Error: file does not exist. Please try again.")#error statemen t if file cannot be opened
            
       

def max_in_region(D,region):
    '''
    Finds the country with the max per capita of diabetes
    returns the country and their per capita
    '''
    D[region].sort(key=itemgetter(3),reverse=True)#sorts the list of lists by each lists' per capita decreasing
    return(D[region][0][0],D[region][0][3])#returns the country name and per capita of the max per capita country

def min_in_region(D,region):
    '''Finds the country with the min per capita of diabetes
    returns the country and their per capita
    '''
    D[region].sort(key=itemgetter(3))#sorts the list of lists by each lists's per capita increasing
    while D[region][0][3] == 0:#no 0 values for per capita
        D[region].remove(D[region][0])#removes per capita of 0's from list of lists
    return (D[region][0][0],D[region][0][3])#returns the country name and per capita of the min per capita country

def read_file(fp):
    '''Uses csv reader to read filepointer and skips header line
    creates a dictionary with regions as keys and list of lists of country's statistics as values
    returns master dictionary
    '''
    reader = csv.reader(fp)#uses csv to read filepointer
    next(reader,None)#skips header line
    master_dict = {}#initializes master dictionary
    for line in reader:#reads through each line as a list
        #adds region key to master dictionary with empty list as value if region isn't in masterdict
        if line[1] not in master_dict:
            master_dict[line[1]] = []
        country = line[2]#sets country to 2nd index of list
        try:
            diabetes = float(line[9])#tries to set diabetes count to float of 9th index of list
            population = float(line[5].replace(',',''))#removes commas from 5th index of list and tries to set float of it to population
            country_list = [country,diabetes,population]#sets list for eah country with stats
            master_dict[line[1]].append(country_list)#adds list to lists of lists for the region
        except ValueError:
            continue#continues if number cannot be a float
    #sorts each list of listw
    for key in master_dict:
        master_dict[key].sort()
    return master_dict#returns master dictionary
        
def add_per_capita(D):
    '''
    Calculates the per capita of diabetes for each country and appends it to each list
    returns master dictionary
    '''
    for key in D:#goes through each region
        for listt in D[key]:#goes through each list in list of lists
            listt.append(listt[1]/listt[2])#appends the diabetes cases divided by population(per capita)
    return D#returns master dictionary
            

def display_region(D,region):
    '''
    Displays the data for each region
    Displays the country data of the region
    displays max and min per capita data
    '''
    for listt in D[region]:#goes through each list of list in region
        if listt[0] == region:#finds the region as a list
            index = D[region].index(listt)#sets the index of the region
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Region","Cases","Population","Per Capita"))#prints header
    print("{:<37s} {:>9.0f} {:>12,.0f} {:>11.5f}".format(D[region][index][0],D[region][index][1],D[region][index][2],D[region][index][3]))#prints data for region
    D[region].remove(D[region][index])#removes region from list of lists, leaving only countries
    L = D[region]#sets variable to lists of lists to easily access
    L.sort(key=itemgetter(3),reverse=True)#sorts by per capita decreasing
    print("\n{:<37s} {:>9s} {:>12s} {:>11s}".format("Country","Cases","Population","Per Capita"))#prints header
    for listt in L:#goes through each list in list of lists
        num = D[region].index(listt)#sets index of each list to easily print data for each country
        print("{:<37s} {:>9.1f} {:>12,.0f} {:>11.5f}".format(L[num][0],L[num][1],L[num][2],L[num][3]))#prints data for each country
    print("\nMaximum per-capita in the {} region".format(region))#prints header
    print("{:<37s} {:>11s}".format("Country","Per Capita"))#prints data header
    print("{:<37s} {:>11.5f}".format(max_in_region(D, region)[0],max_in_region(D, region)[1]))#prints max in region using max region function
    print("\nMinimum per-capita in the {} region".format(region))#header
    print("{:<37s} {:>11s}".format("Country","Per Capita"))#prints data header
    print("{:<37s} {:>11.5f}".format(min_in_region(D, region)[0],min_in_region(D, region)[1]))#prints min in region using min region function

def main():
    fp = open_file()#gets filepointer by referncing open file
    master_dictionary = read_file(fp)#Sets master dictionary by referencing read file function
    master_dictionary = add_per_capita(master_dictionary)#adds per capita values to list of lists for each country
    for key in master_dictionary:#goes through each region in master dictionary
        print("Type1 Diabetes Data (in thousands)")#prints header
        display_region(master_dictionary,key)#displays data for each region using display region function
        print('-'*72)#prints line after each region's data
    print('\n Thanks for using this program!\nHave a good day!')#closing statement
        

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__": 
    main()