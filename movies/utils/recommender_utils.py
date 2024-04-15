from movies.models import Movie, Rating
from authentication.models import CustomUser
import numpy as np
from movies.constants import MoviesConstants
from movies.serializers import MovieSerializer


class Recommender:

    def __init__(self):
        self.movies = Movie.objects.all()
        self.users = CustomUser.objects.all()

    def get_rated_movies(self, user):
        # Get all ratings of the user
        user_ratings = Rating.objects.filter(user=user)

        return user_ratings

    def generate_matrix(self): 
        # Create a matrix of users and movies
        matrix = np.zeros((self.users.last().id+1, self.movies.last().id+1))

        # Fill the matrix with ratings
        for user in self.users:
            user_ratings = self.get_rated_movies(user)
            for rating in user_ratings:
                matrix[user.id][rating.movie.id] = rating.rating

        return matrix


class UserBasedRecommender(Recommender):
    # Oriented towards the user
    def find_k_nearest_neighbors(self, matrix, user, k):
        # Find the user's row
        user_index = user.id    
        user_row = matrix[user_index]

        # Calculate the similarities using MSD
        similarities = []

        for i, other_row in enumerate(matrix):
            if other_row.sum() == 0 or i == user_index:
                continue
            similarity = round(np.sum((user_row - other_row) ** 2)/len(user_row), 2)
            similarities.append((i, similarity))


        print("Similarities: ", similarities)

        # Sort the similarities and get the index of top k
        similarities.sort(key=lambda x: x[1])
        neighbors = similarities[:k]

        return neighbors

    # find Aggregate rating of unrated items
    def find_aggregate_ratings(self, matrix, user, k):
        # Find the user's row
        user_index = user.id
        user_row = matrix[user_index]

        # Find the k nearest neighbors
        neighbors = self.find_k_nearest_neighbors(matrix, user, k)

        # Find the unrated items
        unrated_items = np.where(user_row == 0)[0]
        print("Unrated items: ", unrated_items)

        # Calculate the aggregate ratings
        aggregate_ratings = []

        for item in unrated_items:
            ratings = []
            for neighbor, _ in neighbors:
                if matrix[neighbor, item] != 0:
                    ratings.append(matrix[neighbor, item])
            if ratings:
                aggregate_rating = round(np.mean(ratings), 2)
                aggregate_ratings.append((item, aggregate_rating))
        
        return aggregate_ratings
    

    # find Aggregate rating using Weighted Sum
    def find_aggregate_ratings_weighted_sum(self, matrix, user, k):
        # Find the user's row
        user_index = user.id
        user_row = matrix[user_index]

        # Find the k nearest neighbors
        neighbors = self.find_k_nearest_neighbors(matrix, user, k)

        # Find the unrated items
        unrated_items = np.where(user_row == 0)[0]
        print("Unrated items: ", unrated_items)

        # Calculate the aggregate ratings
        aggregate_ratings = []

        for item in unrated_items:
            ratings = []
            weights = []
            for neighbor, similarity in neighbors:
                if matrix[neighbor, item] != 0:
                    ratings.append(matrix[neighbor, item])
                    weights.append(similarity)
            if ratings:
                aggregate_rating = round(np.sum(np.array(ratings) * np.array(weights))/np.sum(weights), 2)
                aggregate_ratings.append((item, aggregate_rating))
        
        return aggregate_ratings
    

    def knn_users_recommend_movies(self, user, n):
        # Generate the matrix
        matrix = self.generate_matrix()
        print("Matrix: ", matrix)

        # Find the aggregate ratings
        aggregate_ratings = self.find_aggregate_ratings_weighted_sum(matrix, user, MoviesConstants.K_NEIGHBORS)
        print("Aggregate ratings: ", aggregate_ratings)

        # Sort the aggregate ratings
        aggregate_ratings.sort(key=lambda x: x[1], reverse=True)

        # Get the top n recommendations
        if n > len(aggregate_ratings):
            recommendations = aggregate_ratings
        else:
            recommendations = aggregate_ratings[:n]

        recommended_movie_data = []
        for i, rating in recommendations:
            movie = Movie.objects.get(id=i)
            serializer_data = MovieSerializer(movie).data
            serializer_data['predicted_rating'] = rating
            recommended_movie_data.append(serializer_data)

        return recommended_movie_data
        

class MovieBasedRecommender(Recommender):

    def find_k_nearest_neighbors(self, matrix, movie, k):
        # Find the movie's column
        movie_index = movie.id
        movie_column = matrix[:, movie_index]

        # Calculate the similarities using MSD
        similarities = []

        for i, other_column in enumerate(matrix.T):
            if other_column.sum() == 0 or i == movie_index:
                continue
            similarity = round(np.sum((movie_column - other_column) ** 2)/len(movie_column), 2)
            similarities.append((i, similarity))

        print("Similarities: ", similarities)

        # Sort the similarities and get the index of top k
        similarities.sort(key=lambda x: x[1])
        neighbors = similarities[:k]

        return neighbors
    

    def find_aggregate_ratings_weighted_sum(self, matrix, movie, k):
        # Find the movie's column
        movie_index = movie.id
        movie_column = matrix[:, movie_index]

        # Find the k nearest neighbors
        neighbors = self.find_k_nearest_neighbors(matrix, movie, k)

        # Find the unrated users
        unrated_users = np.where(movie_column == 0)[0]
        print("Unrated users: ", unrated_users)

        # Calculate the aggregate ratings
        aggregate_ratings = []

        for user in unrated_users:
            ratings = []
            weights = []
            for neighbor, similarity in neighbors:
                if matrix[user, neighbor] != 0:
                    ratings.append(matrix[user, neighbor])
                    weights.append(similarity)
            if ratings:
                aggregate_rating = round(np.sum(np.array(ratings) * np.array(weights))/np.sum(weights), 2)
                aggregate_ratings.append((user, aggregate_rating))
        
        return aggregate_ratings
    

    def knn_movies_suggest_users(self, user, movie, n):
        
        movie = Movie.objects.get(id=movie)

        # Generate the matrix
        matrix = self.generate_matrix()
        print("Matrix: ", matrix)

        # Find the aggregate ratings
        aggregate_ratings = self.find_aggregate_ratings_weighted_sum(matrix, movie, MoviesConstants.K_NEIGHBORS)
        print("Aggregate ratings: ", aggregate_ratings)

        # Sort the aggregate ratings
        aggregate_ratings.sort(key=lambda x: x[1], reverse=True)
        print(aggregate_ratings)

        # Get the top n recommendations
        if n > len(aggregate_ratings):
            recommendations = aggregate_ratings
        else:
            recommendations = aggregate_ratings[:n]

        print("Recommendations: ", recommendations)

        data = {
            'movie': MovieSerializer(movie).data,
            'suggested_users_to_recommend_movie': []
        }
        recommended_user_data = []
        for i, rating in recommendations:
            user = CustomUser.objects.get(id=i)
            recommended_user_data.append({
                'user': user.username,
                'predicted_rating': rating
            })
        
        data['suggested_users_to_recommend_movie'] = recommended_user_data

        return data