# Recommender System by: Jasmin Shah
# Student ID: 16203646

import sys
import statistics
import math
import itertools
import time
import csv
from collections import defaultdict
from collections import Counter

if float(sys.version.split()[0][:3]) < 3.4:
    print("Python version: 3.4 or higher required to run this code," +
          str(sys.version.split()[0]) + " detected, exiting.")
    sys.exit()

ratings_by_movie = defaultdict(list)
ratings_by_user = defaultdict(list)
movies_by_user = defaultdict(list)
ratings = {}
mean_user_rating = {}
pearson_scores = {}


def user_stats(userid, writer):
    '''Generates User Statistics and writes a row in CSV file.'''

    try:  # if user has given more than one rating, it will succeed
        writer.writerow({'user_id': userid,
                         'mean': statistics.mean(ratings_by_user[userid]),
                         'median': statistics.median(ratings_by_user[userid]),
                         'stdev': statistics.stdev(ratings_by_user[userid]),
                         'max': max(ratings_by_user[userid]),
                         'min': min(ratings_by_user[userid])})
    # in case there's only one rating by user,
    # the stdev calculation won't be possible
    except statistics.StatisticsError:
        writer.writerow({'user_id': userid,
                         'mean': statistics.mean(ratings_by_user[userid]),
                         'median': statistics.median(ratings_by_user[userid]),
                         'stdev': None, 'max': max(ratings_by_user[userid]),
                         'min': min(ratings_by_user[userid])})


def movie_stats(movieid, writer):
    '''Generates Movie Statistics and writes a row in CSV file.'''

    try:  # if user has given more than one rating, it will succeed
        writer.writerow({'movie_id': movieid,
                         'mean': statistics.mean(ratings_by_movie[movieid]),
                         'median':
                         statistics.median(ratings_by_movie[movieid]),
                         'stdev': statistics.stdev(ratings_by_movie[movieid]),
                         'max': max(ratings_by_movie[movieid]),
                         'min': min(ratings_by_movie[movieid])})
    # in case there's only one rating for movie,
    # the stdev calculation won't be possible
    except statistics.StatisticsError:
        writer.writerow({'movie_id': movieid,
                         'mean': statistics.mean(ratings_by_movie[movieid]),
                         'median':
                         statistics.median(ratings_by_movie[movieid]),
                         'stdev': None,
                         'max': max(ratings_by_movie[movieid]),
                         'min': min(ratings_by_movie[movieid])})


def mean_movie_rating(userid, movieid):
    '''Gives mean movie rating, excluding given user's rating if it exists'''

    temp = list(ratings_by_movie[movieid])

    if (userid, movieid) in ratings:  # removes user's rating, if it exists
        temp.remove(ratings[userid, movieid])

    return statistics.mean(temp)


def cosine(user1, user2, o1):
    '''Measures cosine similarity between given two users'''

    # Find out movies which are rated by both users
    common_movies = [movies for movies in movies_by_user[user1]
                     if movies in movies_by_user[user2]]

    p, q, r = 0, 0, 0

    if len(common_movies) <= o1:  # Minimum Neighbour Overlap #1
        return 0  # lowest possible cosine score

    else:
        for movie in common_movies:
            x = ratings[user1, movie]
            y = ratings[user2, movie]
            p += x * x
            q += y * y
            r += x * y
        return round((r / math.sqrt(p * q)), 4)




def pearson(user1, user2, o1):
    '''Calculates Person coefficient between two users'''

    # Find out movies which are rated by both users
    common_movies = [movies for movies in movies_by_user[user1]
                     if movies in movies_by_user[user2]]

    p, q, r = 0, 0, 0

    if len(common_movies) <= o1:  # Minimum Neighbour Overlap #1
        pearson_scores[user1, user2] = 0  # no correlation between 2 users
        pearson_scores[user2, user1] = 0
        return pearson_scores[user1, user2]

    else:
        for movie in common_movies:
            x = ratings[user1, movie] - mean_user_rating[user1]
            y = ratings[user2, movie] - mean_user_rating[user2]
            p += x * x
            q += y * y
            r += x * y

        try:
            pearson_scores[user1, user2] = round((r / math.sqrt(p * q)), 4)
        # when the differences are the same, it means that the correlation
        # between the users is good
        except ZeroDivisionError:
            pearson_scores[user1, user2] = 1

        pearson_scores[user2, user1] = pearson_scores[user1, user2]
        return pearson_scores[user1, user2]


def neighbourhood(method, k, o1, o2):
    '''Finds k closest neighbours for given method'''

    # stores k highest weighted neighbours
    neighbours = defaultdict(list)

    '''itetools.combinations gives all possible unique pairs, which reduces
       total number of calculations and makes sure that the user's rating
       never gets involved in its own prediction calculation'''

    if (method == "cosine"):
        similarity = [(x, y, cosine(x, y, o1)) for x, y in
                      itertools.combinations(range(1,
                                                   len(ratings_by_user)+1), 2)]

        # Overlap #2
        similarity = [tup for tup in similarity if tup[2] > o2]

        # descending sort, since high cosine value = less distance
        similarity.sort(key=lambda x: x[2], reverse=True)

    elif (method == "pearson"):
        similarity = [(x, y, pearson(x, y, o1)) for x, y in
                      itertools.combinations(range(1,
                                                   len(ratings_by_user)+1), 2)]

        # Overlap #2
        similarity = [tup for tup in similarity if tup[2] > o2]

        # descending sort, since high pearson value = better correlation
        similarity.sort(key=lambda x: x[2], reverse=True)

    else:
        sys.exit(0)

    # populating list of neighbours of each user
    for x, y, z in similarity:
        neighbours[x].append(y)
        neighbours[y].append(x)

    # picking only top k neighbours
    neighbours = {key: value[:k] for key, value in neighbours.items()}

    return neighbours


def mean_rating():
    '''Predicts rating for mostly all user-movie pairs
       using mean_movie_rating method'''

    failures = 0
    mean_prediction = {}  # dictionary to store all predicted ratings

    # iterating over all given 100k user-movie pairs
    for (x, y), z in ratings.items():
        try:
            mean_prediction[x, y] = mean_movie_rating(
                x, y)  # stores rating y mo
        # when there are no ratings for the selected movie
        except statistics.StatisticsError:
            failures += 1

    find_coverage(failures)
    rmse_calculator(mean_prediction)
    csv_writer("Mean.csv", mean_prediction)


def distance_sim(k, o1, o2):
    '''Predicts rating for mostly all user-movie pairs using
       cosine similarity (distance-based) method'''

    failures = 0
    cosine_prediction = {}  # dictionary to store all predicted ratings
    # fetch k neighbours of all users
    neighbours = neighbourhood("cosine", k, o1, o2)

    for (x, y), z in ratings.items():

        temp, watched = 0, 0

        try:  # whether there are any neighbours available for user x
            for neighbour in neighbours[x]:
                try:
                    temp += ratings[neighbour, y]
                    watched += 1
                except KeyError:  # when the neighbour hasn't rated movie y
                    temp += 0
        except KeyError:  # when there are no neighbours of user x
            watched = 0

        if watched == 0:  # When not a single neighbour has rated the movie,
            failures += 1  # the prediction fails
        else:
            # only dividing by no. of users who has rated the movie
            cosine_prediction[x, y] = temp/watched

    find_coverage(failures)
    rmse_calculator(cosine_prediction)
    csv_writer("Distance_Sim.csv", cosine_prediction)


def resnick(k, o1, o2):
    '''Predicts rating for mostly all user-movie pairs using pearson
       coefficient (correlation-based) method'''

    failures = 0
    resnick_prediction = {}  # dictionary to store all predicted ratings
    # fetch k neighbours of all users
    neighbours = neighbourhood("pearson", k, o1, o2)

    for (x, y), z in ratings.items():
        p, q, watched = 0, 0, 0

        try:
            for neighbour in neighbours[x]:
                try:
                    p += (ratings[neighbour, y] - mean_user_rating[neighbour])\
                        * pearson_scores[x, neighbour]
                    watched += 1
                except KeyError:  # when the neighbour hasn't rated movie y
                    p += 0
                q += abs(pearson_scores[x, neighbour])
        except KeyError:  # when there are no neighbours of the x user
            watched = 0

        if watched == 0:  # When not a single neighbour has rated the movie,
            failures += 1  # the prediction fails
        else:
            resnick_prediction[x, y] = mean_user_rating[x] + (p/q)

    find_coverage(failures)
    rmse_calculator(resnick_prediction)
    csv_writer("Resnick.csv", resnick_prediction)


def find_coverage(failures):
    '''Finds coverage of any given method by recieving how many times
       it failed to predict'''

    print("Coverage: ", ((len(ratings)-failures)/len(ratings)))


def rmse_calculator(predicted_rating):
    '''Finds root-mean-square error by comparing predicted rating
       with actual rating'''

    squared_error = 0
    failures = 0

    for (x, y), z in ratings.items():
        try:
            squared_error += ((predicted_rating[x, y] - ratings[x, y])**2)
        # when there's no prediction for target user-movie pair
        except KeyError:
            failures += 1

    print("failures in RMSE calculation:", failures)

    print("RMSE:", math.sqrt(squared_error/1))


def csv_writer(csvname, predicted_rating):
    '''Writes results on a CSV file for each prediction technique'''

    with open(csvname, 'w') as csvfile:
        fieldnames = [
            'user_id', 'item_id', 'actual_rating', 'predicted_rating', 'RMSE']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for (x, y), z in ratings.items():
            try:
                writer.writerow({'user_id': x, 'item_id': y,
                                 'actual_rating': ratings[x, y],
                                 'predicted_rating': predicted_rating[x, y],
                                 'RMSE': abs(predicted_rating[x, y] -
                                             ratings[x, y])})
            # when there's no predicted rating,
            # it will leave last two fields blank
            except KeyError:
                writer.writerow({'user_id': x, 'item_id': y,
                                 'actual_rating': ratings[x, y],
                                 'predicted_rating': None, 'RMSE': None})


def populate():
    '''Populates all dictionaries used in the program from ratings.txt file'''

    with open('epinions/rating.txt', 'r') as f:
        data = f.readlines()

    for line in data:
        words = line.split(' ')

        for x in range(len(words)):
            words[x] = int(words[x])

        ratings[words[0], words[1]] = words[3]
        ratings_by_user[words[0]].append(words[3])
        ratings_by_movie[words[1]].append(words[3])
        movies_by_user[words[0]].append(words[1])

    for x in range(1, len(ratings_by_user)+1):
        try:
            mean_user_rating[x] = statistics.mean(ratings_by_user[x])
        except statistics.StatisticsError:
            mean_user_rating[x] = 0

def generate_stats():
    '''Generates all statistics as part of task 1'''

    # total number of users
    print("Total users:", len(ratings_by_user))

    # total number of movies
    print("Total movies:", len(ratings_by_movie))

    # total number of ratings
    print("Total ratings:", len(ratings))

    # calculation of ratings Density metric
    print("Density:", len(ratings) /
          (len(ratings_by_user)*len(ratings_by_movie))*100)

    # generating user statistics
    print("\nGenerating User Statistics and writing in user_stats.csv...")
    with open('user_stats.csv', 'w') as csvfile:
        fieldnames = ['user_id', 'mean', 'median', 'stdev', 'max', 'min']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(1, len(ratings_by_user)+1):
            user_stats(x, writer)
    print("Done. \n")

    # generating movie statistics
    print("Generating Movie Statistics and writing in movie_stats.csv...")
    with open('movie_stats.csv', 'w') as csvfile:
        fieldnames = ['movie_id', 'mean', 'median', 'stdev', 'max', 'min']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(1, len(ratings_by_movie)+1):
            movie_stats(x, writer)
    print("Done. \n")

    # number of ratings per each class
    c = Counter(ratings.values())
    for x in range(1, 6):
        print("Number of ratings for rating", x, "is", c[x])


def main():
    '''Tweaks the parameters by user inputs and starts prediction process
       by different techniques'''

    populate()


    # print(ratings)


    # generate_stats()

    print("---------------------------------------------------------")
    start_time = time.time()
    print("Starting prediction using mean rating method...")
    mean_rating()
    print("Execution time: ", (time.time() - start_time))
    print("---------------------------------------------------------")

    print("A test suite has been created for Distance based"
          " prediction method with following default values: \n"
          "Number of neighbours = 50\n"
          "Overlap #1 (minimum number of common movies required to"
          " be considered as a neighbour) = 5\n"
          "Overlap #2 (minimum cosine similarity value) = 0.6 \n")

    ask = 'N'

    if ask == 'Y':

        try:
            k = int(input("Please enter number of neighbours"
                          " (ideally, between 1 to 100): "))
        except ValueError:
            print("Please enter an integer for value of number of neighbours,"
                  " terminating for now...")
            sys.exit()

        try:
            o1 = int(input("Overlap #1 (minimum number of common movies"
                           " required to be considered as a neighbour)"
                           " (ideally, between 1 to 20): "))
        except ValueError:
            print("Please enter an integer for value of overlap #1,"
                  " terminating for now...")
            sys.exit()

        try:
            o2 = float(input("Overlap #2 (minimum cosine similarity value)"
                             " (between 0.0 to 1.0): "))
        except ValueError:
            print("Please enter a float for value of overlap #2,"
                  " terminating for now...")
            sys.exit()

    else:
        k = 5
        o1 = 1
        o2 = 0.6

    print("---------------------------------------------------------")
    start_time = time.time()
    print("Starting prediction using Distance based method...")
    distance_sim(k, o1, o2)
    print("Execution time: ", (time.time() - start_time))
    print("---------------------------------------------------------")

main()
