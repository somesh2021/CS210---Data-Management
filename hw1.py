# Task 1
def read_ratings_data(f):
    ratings = {}
    for line in open(f):
        movie, rating, id = line.split('|')
        if (movie.strip()) in ratings:
            ratings[movie.strip()].append((rating.strip(),id.strip()))
        else:
            ratings[movie.strip()] = [(rating.strip(),id.strip())]
    for keys in ratings.keys():
        v = set()
        new = []
        for a,b in ratings[keys]:
            if not b in v:
                v.add(b)
                new.append((a,b))
        ratings[keys] = new
    for keys in ratings.keys():
        ratings[keys] = [(a) for a,b in ratings[keys]]
    ratingsf = {}
    for keys in ratings.keys():
        ratingsf[keys] = ratings[keys]
    return ratingsf

def read_movie_genre(f):
    genres = {}
    for line in open(f):
        genre, sid, movie = line.split('|')
        genres[movie.strip()] = genre.strip()
    return genres

# Task 2
def create_genre_dict(genres):
    genre_dict = {}
    for keys in genres.keys():
        genre = genres[keys]
        if genre in genre_dict:
            genre_dict[genre.strip()].append(keys.strip())
        else:
            genre_dict[genre.strip()] = [keys.strip()]
    return genre_dict

def calculate_average_rating(ratings):
    average_dict = {}
    for keys in ratings.keys():
        ratinglist = ratings[keys]
        for i in range(0, len(ratinglist)):
            ratinglist[i] = float(ratinglist[i])
        avg = sum(ratinglist) / len(ratinglist)
        average_dict[keys] = avg
    return average_dict

# Task 3
def get_popular_movies(avg, n=10):
    popular = sorted(avg.items(), key = lambda kv: kv[1])
    popular = reversed(popular)
    popular = dict(popular)
    count = 0
    for keys in list(popular.keys()):
        count += 1
        if(count > n):
            del popular[keys]
    return popular

def filter_movies(mta, threshold = 3.0):
    filter_movies = {}
    for keys in mta.keys():
        if(mta[keys] >= threshold):
            filter_movies[keys] = mta[keys]
    return filter_movies

def get_popular_in_genre(genre, genredict, avgdict, n = 5):
    ret = {}
    movies = []
    movieratings = []
    for keys in genredict.keys():
        if (genre == keys):
            movies.extend(genredict[keys])
    for keys in avgdict.keys():
        for i in range(0, len(movies)):
            if(movies[i] == keys):
                movieratings.append(avgdict[keys])
    ret = dict(zip(movies, movieratings))
    retpop = sorted(ret.items(), key = lambda kv: kv[1])
    retpop = reversed(retpop)
    retpop = dict(retpop)
    count = 0
    for keys in list(retpop.keys()):
        count += 1
        if(count > n):
            del retpop[keys]
    return retpop

def get_genre_rating(genre, genredict, avgdict):
    movies = []
    movieratings = []
    for keys in genredict.keys():
        if (genre == keys):
            movies.extend(genredict[keys])
    for keys in avgdict.keys():
        for i in range(0, len(movies)):
            if(movies[i] == keys):
                movieratings.append(avgdict[keys])
    ret = dict(zip(movies, movieratings))
    sum = 0
    for keys in ret.keys():
        sum += float(ret[keys])
    avgrating = sum/len(ret)
    return avgrating

def genre_popularity(genredict, avgdict, n = 5):
    ret = {}
    genres = []
    genreratings = []
    for keys in genredict.keys():
        genres.append(keys)
        genreratings.append(get_genre_rating(keys, genredict, avgdict))
    ret = dict(zip(genres, genreratings))
    retpop = sorted(ret.items(), key = lambda kv: kv[1])
    retpop = reversed(retpop)
    retpop = dict(retpop)
    count = 0
    for keys in list(retpop.keys()):
        count += 1
        if(count > n):
            del retpop[keys]
    return retpop

# Task 4
def read_user_ratings(f):
    users = {}
    for line in open(f):
        movie, rating, id = line.split('|')
        if (id.strip()) in users:
            users[id.strip()].append((movie, rating))
        else:
            users[id.strip()] = [(movie, rating)]
    return users

def get_user_genre(uid, umd, genres):
    ratings = {}
    avgdict = {}
    for tup in umd[uid]:
        movie = genres[tup[0]]
        rating = tup[1]
        if movie in ratings:
            ratings[movie].append(rating)
        else:
            ratings[movie] = [rating]
    for keys in ratings:
        sum = 0
        for x in ratings[keys]:
            x = float(x)
            sum += x
            avg = sum / len(ratings[keys])
            avgdict[keys] = avg
    top = max(avgdict, key = avgdict.get)
    return top

def recommend_movies(uid, umd, genres, avgdict):
    rec = {}
    movies = []
    topgenre = get_user_genre(uid, umd, genres)
    for keys in genres:
        if genres[keys] == topgenre:
            movies.append(keys)
    for movie in movies[:]:
        for tup in umd[uid]:
            if(movie == tup[0]):
                movies.remove(movie)
    for movie in movies:
        rating = avgdict[movie]
        rec[movie] = rating
    recpop = sorted(rec.items(), key = lambda kv: kv[1])
    recpop = reversed(recpop)
    recpop = dict(recpop)
    count = 0
    for keys in list(recpop.keys()):
        count += 1
        if(count > 3):
            del recpop[keys]
    return recpop
