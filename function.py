import pandas as pd
from pandas import DataFrame
from load_data import *

infocan = infocan.set_index('Canteen')
df = df.set_index(['Canteen'])
#takes in foodtype = ['Food1','food2' etc], pricerange = [lower, higher as floats/int], rating = int(1 to 5) or 0 if not specified
def searchfood(foodtype, pricerange, rating, search, df):
    #copy the dataframe to temporary.
    search_df = df.copy()
    #filter by foodtype
    if foodtype != []:
        foodcond = search_df['Food Type'].isin(foodtype)
        search_df = search_df[foodcond]
    # filter by price range
    low_price = pricerange[0]
    high_price = pricerange[1]
    pricecond1 = search_df['Price'] >= low_price
    pricecond2 = search_df['Price'] <= high_price
    search_df = search_df[ pricecond1 & pricecond2 ]
    # filter by rating, shows all above specified rating
    if rating != 0:
        ratingcond = search_df['Rating'] >= rating
        search_df = search_df[ ratingcond ]
    # filter by menu Item
    if search != ' ':
        lst = search.lower().split()
        for word in lst:
            wordcond = search_df['Menu Item'].str.lower().str.contains(word)
            search_df = search_df[wordcond]
    # Transform results to List
    return search_df
#function to sort by rating given the list of index searched, the output is a list of indexes
def sort_by_rating(filter_df):
    return filter_df.sort_values("Rating")[:10]
#function to sort by price given the list of index searched, the output is a list of indexes
def sort_by_price(filter_df):
    return filter_df.sort_values("Price")[:10]
#function to sort by distance based on the user location, the filtered DataFrame and list of canteen location
def sort_by_location(user_loc, filter_df, infocan):
    lst_loc = filter_df.index.unique()
    lst_dist = {}
    frames = []
    for loc in lst_loc:
        lst_dist[loc] = ((user_loc[0] - infocan.loc[loc]['loc x'])**2 + (user_loc[1] - infocan.loc[loc]['loc y'])**2)**(1/2)
    if lst_dist!={}:
        lst_dist = sorted(lst_dist, key = lst_dist.get)
    count = 1
    for loc in lst_dist:
        a = filter_df.loc[loc]
        frames.append(a)
        if count == 10:
            break
        count += 1
    if frames !=[]:
        return pd.concat(frames)
    else:
        return pd.DataFrame()
result = searchfood([], [1,100], 1, 'Rice', df)
t = sort_by_location((333,222), result, infocan)
print(t.index.unique())
