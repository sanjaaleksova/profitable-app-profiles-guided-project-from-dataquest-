#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles
#    
#    For this project we will be focusing on building apps that are avaliable in Google Play Store and Apple Store. We will focus our interest in building apps that are free to downlad. Our main source of revenue would be the in-app ads. This means the more users the app will have, the better the revenue. One of our goals is to find out what type of apps would be worth developing in order to have a bigger target audience. Analysing data from two csv files should help us understand what type of apps are likely to attract more users. 

# ## Exploring data from csv files

# Collecting data for over four million apps requires a significant amount of time and money, so we'll try to analyze a sample of data instead. To avoid spending resources with collecting new data ourselves, we should first try to see whether we can find any relevant existing data at no cost. Luckily, these are two data sets that seem suitable for our purpose:
# 
# A data set containing data about approximately ten thousand Android apps from Google Play. You can download the data set directly from [this link](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv).
# A data set containing data about approximately seven thousand iOS apps from the App Store. You can download the data set directly from [this link](https://dq-content.s3.amazonaws.com/350/AppleStore.csv).
# 
# Let's start by opening the two data sets and then continue with exploring the data.

# In[2]:


from csv import reader 

opened_file = open('googleplaystore.csv',encoding='utf8')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

opened_file = open('AppleStore.csv', encoding='utf8')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]




# We define a function called explore_data(), which takes in four parameters: dataset, start, end and rows_and columns. We use it to slice the data set and loop through the slice. We can reuse this function troughout our project.

# In[3]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')
        
        if rows_and_columns:
            print('Number of rows: ', len(dataset))
            print('Number of columns: ', len(dataset[0]))


# In[4]:


print(android_header)
print('n/')
explore_data(android, 0, 3, True)


# In[5]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# As we can see from the result printed above, the Play Store apps data set has 10841 apps and 13 columns containing data about the app's genre, ratings, price, number of installs etc. The Apple Store data set has 7197 apps and 16 columns that contain data about the genre, size, price, ratings etc.

# ## Deleting wrong data
# 
# As we mentioned before for this project we will be focusing only on free apps avaliable for both Apple Store and Google Play. But the data we collected above contains most of the apps avaliable for these two stores. But we would only need to collect data about apps that are free to install AND are in English. So we'd like to go ahead and remove data we collected from the data sets about apps that are not in English, and apps that are paid. 
# 
# The google play data set has a dedicated [discusion section](https://www.kaggle.com/lava18/google-play-store-apps/discussion) and we can see that [one of the discusssions](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015) points to an error for row 10472. We're going to print this row and compare it to the header and another row that is correct.

# In[6]:


print(android_header)  # header
print('\n')
print(android[10472])  # incorrect row
print('\n')
print(android[0])      # correct row


# The row 10472 corresponds to the app Life Made WI-Fi Touchscreen Photo Frame, and we can see that the rating is 19. This is clearly off because the maximum rating for a Google Play app is 5. As a consequence, we'll delete this row.

# In[9]:


print(len(android))
#del(android[10472])  #we run this code only once
print(len(android))


# # Removing duplicate entries
# 

# ## Part one
# 
# If we explore the Google Play data set long enough, we'll find that some apps have more than one entry. For instance, the application Instagram has four entries:
# 

# In[10]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# Next we will look for all of the duplicate apss throughout the android data set:

# In[11]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
        
    else:
        unique_apps.append(name)

    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# We can see from the code above that we have 1181 duplicate entries in the android data set. We would like to remove these entries, but rather than removing them randomly, we will take a look at the number of reviews of each duplicate and keep only the entry that has the highest number of reviews (assuming that that is the most recent entry, making the data more accurate. 
# 
# To do that, we will:
# 
# * Create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app
# * Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)
# 

# ## Part two
# 
# Let's start by bulding the dictionary:
# 

# In[12]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
            reviews_max[name] = n_reviews

print(app)


# In[13]:


print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# As we can see we have our expected length right, now we will go ahead and remove the duplicate data using the dictionary we created.
# 
# * First we will create two empty lists: android_clean and already_added
# * We will loop through the data set (header excluded), and for each iteration we will:
#     * We isolate the name of the app and the number of reviews.
#     * We add the current row (app) to the android_clean list, and the app name (name) to the already_added list if:
#         * The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
#         * The name of the app is not already in the already_added list. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.

# In[14]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])

    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# Now let's confirm that the number of rows is 9,659:

# In[15]:


explore_data(android_clean, 0, 4, True)


# Number of rows is 9,659 just as expected.

# # Removing Non-English Apps
# 
# ## Part One 
# 
# 
# In our data set we have data stored about apps that are not in English, as we said we would be focusing only on English apps, we would like to go ahead and remove the non-English apps. Below we can see some examples of these apps that are not directed towards an English-speaking audience.
# 

# In[16]:


print(ios[813][1])
print(ios[6731][1])

print(android_clean[4412][0])
print(android_clean[7940][0])


# We are not interested in keeping these apps, so we'll remove them. How can we do that? We can remove these file by looking for apps that contain symbols that aren't commonly used in the English language. English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;), and other symbols (+, *, /).
# 
# Behind the scenes, each character we use in a string has a corresponding number associated with it. For instance, the corresponding number for character 'a' is 97, character 'A' is 65, and character '爱' is 29,233. We can get the corresponding number of each character using the ord() built-in function.
# 
# **The numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system. Based on this number range, we can build a function that detects whether a character belongs to the set of common English characters or not. If the number is equal to or less than 127, then the character belongs to the set of common English characters.**
# 
# In Python, strings are indexable and iterable, which means we can use indexing to select an individual character, and we can also iterate on the string using a for loop.
# 
# We will go ahead and build a function that detects if the characters belong toa an English text or not.

# In[17]:


def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False     
   
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# ## Part Two
# 
# The function seems to work fine, but some English app names use emojis or other symbols (™, — (em dash), – (en dash), etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form. We would need to change our function so if there are more than three non-ascii characters it would be labeled as non-English, but if it has up to three non-ascii characters it would be labeled as an English app. This function will not be perfect but it will still be pretty accurate. 
# 

# In[18]:


print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))

print(ord('™'))
print(ord('😜'))


# In[19]:


def is_english(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
            
    if non_ascii > 3:
            return False
    else:
            return True
        
    
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))
    


# What we want to do next is use this newly built function to loop though both our data sets and filter out our English applications, the function is not perfect but for now we will not waste any more time on optimization.

# In[20]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# As we can see we are left with 9614 Android apps and 6183 iOS apps.

# # Isolating the Free Apps
# 
# As we mentioned before in this project we will be focusing only on the free apps. Our main source of revenue would be from the in-app ads. Right now our data set contains both free and paid appps. Below, we will isolate the free apications.
# 

# In[21]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)

for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))
    
    


# As we can see, now we are left with 8864 apps in the Android data set and 3222 apps in the iOS data set. This should be enough for our analysis. 

# # Most Common Apps by genre
# 
# ## Part One
# 
# As we mentioned earlier in this project we will be focusing on apps that are free, english and most likely to attract more users, because our revenue is highly influenced by the number of people using our apps. To minimize the risks, we will be using the following validation strategy.
# 
# - Firstly we would develop a minimal version of the app and upload it on the Google Play Store. 
# - If the app has a good response from users, we develop it further
# - If the app is profitable in the next six months, we build an app for iOS and upload it to the App Store.
# 
# As our end goal is to build apps for both platforms, we need to find app profiles that are successful on both platforms.
# For this we'll need to build frequency tables for a few columns in our data sets.
# 
# ## Part two
# We'll build two functions that we can uset to analyze the frequency tables:
# 
# - One function to generate frequency tables that show percentages
# - Another function that we can use to display the percentages in a descending order.
# 

# In[22]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse=True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
    


# ## Part Three
# 
# We will start by examining the frequency table for the prime_genre column of the App Store dataset.
# 

# In[23]:


display_table(ios_final, 11)


# We can observe that more than half free English apps are games. Entertainmet apps are almost 8 percent, photo and video apps close to 5% , education apps 3.6%, the social networking apps 3.2% The general impression is that most of the apps that are free are designed for entertainment, while apps with practical purposes such as education, productivity and utilities are more rare. However, the fact that entertainment apps are more numerous does not imply that they have highee number of users.
# 
# We'll continue by examining the genres and category columns on the Google Play data set.

# In[24]:


display_table(android_final, 1) #Category


# We can see that the most numerous category is Family with almost 19 percent, followed by Games with almost 9 percent, Tools with 8.4 percent, business, 4.5 percent and lifestyle and productivity close to 4 percent. It seems that in the Google play store most apps are designed for practical purposes. But if we investingate the Google Play Store's Family category we will get to the conclusion that most of the apps in the [Family category](https://play.google.com/store/apps/category/FAMILY?hl=en) are games for kids.
# 
# Even so, pracical apps sem to have a better representation on the Google Play Store, compared to the app store.

# In[25]:


display_table(android_final, 9) #Genres


# We can see the Genres columns is much more granular, it consitsts of many more subgenres, so for our project we will be sticking with the Category column that paints the bigger picture. To this pont we found out that the App store is dominated by apps that are designed for entertainment, while the apps on the Google Play Store is much more balanced. Next, we'd like to get an idea about the kinds of apps that have the most users. 

# # Most Popular Apps by Genre on the App Store
# 
# One way to find out which genres are more popular with the users is to look at the "Installs" column, but we can notice that in the Apple Store data set this column is missing, so what we can do instead as a workaroun is look at the total number of user ratings as proxy, which we can find in the rating_count_tot app. 
# 
# For calculating the average number of user ratings per app in the Apple Store, we'll need to:
# 
# - isolate the apps of each genre
# - sum up the user ratungs for the apps of that genre 
# - divide the sum by the number of apps belonging to that genre (not the total number of apps)
# 
# For calculating the average number of user ratings for each genre, we'll use a for loop inside of a for loop **(nested loops)**
# 

# In[26]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0 
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)

            


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:
# 
# 

# In[27]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# Social networking apps are also the ones with the most reviews, but in my opinion this genre is dominated by already very established social networks and to develop a social networking site that is new, unique and likely to catch up is not very probable, as over the years there have been so many social networks, but the only ones who managed to be relevant for users are Facebok, Instagram, Twitter and LinkedIn. In my opinion they are still relevant because each one of them is unique in it's own way and these companies have many employees. So in my opinion the best strategy would be to develop a game app that is likely to have a great number of users, or another option I would choose wolud be some kind of a productivity app with nice features and nice design that users would be likely to install and engage with. 

# ## Most Popular Apps by Genre on Google Play
# 
# Now that we have come up with some app profile recommendations for the App Store, we will continue by looking at the Google Play's "Installs" column, which contains the number of times an app has been installed. 
# 

# In[29]:


display_table(android_final, 5) #the Installs column


# As we can see, these numbers don't seem too precise enough (most values are open- ended - 100+, 5000+, etc.). We wouldn't know if an app with 100.000+ installs has 100.000 installs, 200.000 instals or 350.000 installs. However, we don't need very precise data for our purposes - we only want to find out which app genres attract the most users, and we don't need perfect precision with respect to the number of users. We are going to leave the numbers as they are, which means that we'll consider that an app with 100.000+ installs has 100.000 installs and so on. To be able to perform computations, however, we'll need to convert each install number from ***string*** to ***float***, this means that we need to remove the commas and the plus characters. To remove characters form strings we can use the str.replace(old, new) method. 

# In[34]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0 
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)
            


# We can see that on average, communication apps have the most installs. This number is heavily influenced by few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail and Hangouts), and a few more with over 100 and 500 million installs:

# In[41]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communications apps that have over 100 million installs, the average would be reduced roughly ten times:
# 

# In[42]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# We could say the same about the video players category. The market is dominates by apps like Youtube, Google Play Movies, Netflix, etc. The pattern is also the same with the social apps ehere the market is dominated by giants like Facebook, Instagram, Twitter etc. The main concern is that these genres might seem more popular than they really are. And these genres seem to be dominated with giants that would be hard to compete against. 
# 
# The books and reference seems to be pretty popular as well, it would be interesting enough to explore in more depth.
# 
# The game genre seems to be pretty popular as well, the market is a bit saturated but it might be worth it if we could build design a game with a nice design that has the potential to attracto more users.
# 
# Let's take a look at the apps from the Books and Reference genre, so we can see if alternatively would be worth it to develol an app from this genre. 

# In[43]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The Books and Reference genre seems to have a variety of different apps like libreries, dictionaries, tutorials on programming languages etc. But, it seems that there's still a small number of extremely popular apps that skew the average:
# 

# In[47]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# It looks like it only has a few apps that have such popularity so this genre shows potential. 
# 
# I would like to go ahead and look at the game genre and the productivity genre so we can draw some conclusion:
# 

# In[48]:


for app in android_final:
    if app[1] == 'GAME':
        print(app[0], ':', app[5])


# The game market is definitely saturated, if we were to build a game app we would have to compete against some very popular apps, but I wouldn't dismiss the idea of building a game app just yet, if we were innovative enough it might be a profitable app genre to develop. Next, I would like to go ahead and look at the productity genre.
# 

# In[54]:


for app in android_final:
    if app[1] == 'PRODUCTIVITY':
        print(app[0], ':', app[5])
        


# Let's explore the average for under 100 million installs for this genre so we can get an in-depth view of the genre's landscape:
# 

# In[55]:


under_100_m_prod = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'PRODUCTIVITY') and (float(n_installs) < 100000000):
        under_100_m_prod.append(float(n_installs))
        
sum(under_100_m_prod) / len(under_100_m_prod)


# This genre of apps would be a good candidate to look into for building apps, maybe a pproductivity app with a nice clean and minimal look that includes features like to-do, calendar, pomodoro clock, and an app that would be able to track the usage of apps on the phone it would be very profitable to build, even more so than the game genre. One last genre that we find interestinga and would like to look into would be the beauty genre, so let's go ahead and have a lok there before we draw our final conclusions

# In[58]:


for app in android_final:
    if app[1] == 'BEAUTY':
        print(app[0], ':', app[5])


# # Conclusions
# 
# 
# With all of this in mind, I would be making two app profiles recommendations. Because the game genre is overly saturated it would be best if we only have that genre for future considerations. For now we can say that building both a productivity app or a beauty app would be the best option for our current goals.
# 
# - My personal initial idea of the productivity app would be an app that hac nice clean, minimal design, includes features like reminders, to-dos, calendars, pomodoro clocks that increases productivity, and also an app that tracks phone usage and gives stats about which apps the user spends the most time on. If it has an interactive desingn and asks the user questions like what's on their mind and gives daily insights so the users canorganize their time, notes and thoughts it surely be loved by users and would surely like it.
# 
# - The second recommendation for a profitable app profile would be an app from the Beauty genre, that would recommend beauty products based on skin type, also featuring articles by beauty bloggers giving recommendations about skin care and cosmetic products. This would be profitable because from this kind of app, our revenue would not only depend from the in-app ads, it might be profitable because cosmetic and beauty companies would be interested in partnerships. 
# 
# However, these ideas are only initial, we can expand on them and comntinue our research based on trial and error.
