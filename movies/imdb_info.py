import imdb

ia = imdb.IMDb()

def get_movie_id(name):

    movies = ia.search_movie(name)
    movie = movies[0]
    return movie.movieID

id = get_movie_id('matrix')

def get_movie_details(id):
    try:
        movie = ia.get_movie(id, info=['main'])
        movie.infoset2keys

        certificates = movie.get('certificates')
        certificate = 'Unknown'
        print(type(certificates))
        if type(certificates) == list:
            for item in certificates:
                if 'United States' in item:
                    certificate = item.split(':')[1]
                    break
        else:
            certificate = certificates

        movie_info = {
            'id': id,
            'title': movie.get('title'),
            'certificate': certificate,
            'score': movie.get('rating'),
            'genres': ','.join(movie.get('genres')),
            'runtime': movie.get('runtimes')[0],
            'cover': movie.get('cover url')
        }
        score = float(movie_info['score'])
        if score > 6:
            return movie_info
        else:
            return False
    except Exception as e:
        print(e)

print(get_movie_details(id))