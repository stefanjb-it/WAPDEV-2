import { Injectable } from '@angular/core';
import { Movie } from '../model/Movie';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MovieService {

  constructor(private http:HttpClient) { }

  getMovies(){
    return this.http.get<Movie[]>('/api/movies/')
  }
  getMovie(pk: string){
    return this.http.get<Movie[]>(`/api/movies/${pk}/`)
  }
  createMovie(movie: Movie) {
    return this.http.post('/api/movies/', movie)
  }
  updateMovie(movie: Movie) {
    return this.http.put(`/api/movies/${movie.pk}/`, movie)
  }
  deleteMovie(movie: Movie) {
    return this.http.delete(`/api/movies/${movie.pk}/`)
  }
}
