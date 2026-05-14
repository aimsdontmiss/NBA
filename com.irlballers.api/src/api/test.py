# List and objects for testing purposes

l1 = [1, 2, 3, 4, 5]
print(l1)

i = 0
for obj in l1:
    l1[i] = { "mscd": [
        { 'month': 'january', 'g': [ { 'gid': 7 }, { 'gid': 8 } ] },
        { 'month': 'february', 'g': [ { 'gid': 9 }, { 'gid': 10 } ] },
        { 'month': 'march', 'g': [ { 'gid': 11 }, { 'gid': 12 } ] },  
        { 'month': 'april', 'g': [ { 'gid': 13 }, { 'gid': 14 } ] },
        # here is where the season actually starts...in october 
        { 'month': 'october', 'g': [ { 'gid': 1 }, { 'gid': 2 } ] },
        { 'month': 'november', 'g': [ { 'gid': 3 }, { 'gid': 4 } ] },
        { 'month': 'december', 'g': [ { 'gid': 5 }, { 'gid': 6 } ] },
    ] }
    i += 1

# for month in l1[0]['mscd']:
#     month[:4] = month[]
#     print(month)
#
# 
# what is the simplest way to put october first, then november, then december, then january, etc.?
# we can do this by sorting the list of months based on a predefined order of months
# we can define a list of months in the desired order and then sort the list of months based on their index in that list
# we can also use a dictionary to map month names to their desired order and then sort based on the values in that dictionary
# let's implement the dictionary approach
# define the desired order of months

month_order = {
    'october': 1,
    'november': 2,
    'december': 3,
    'january': 4,
    'february': 5,
    'march': 6,
    'april': 7,
}

# sort the list of months based on their order in the month_order dictionary
l1[0]['mscd'].sort(key=lambda month: month_order[month['month']])
# print(l1[0]['mscd'])

for month in l1[0]['mscd']:
    print(month)


