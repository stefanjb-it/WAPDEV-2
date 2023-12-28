import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Movie} from "./models/Movie";
import {KeyValueItem} from "./models/KeyValueItem";
import {Observable, Subscription} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class MovieService {

  constructor(private http:HttpClient) { }

  getMovies(){
      return this.http.get<Movie[]>('/api/movies/')
  }

  getMoviesSync(){
    return this.http.get<Movie[]>('/api/movies/').subscribe((movies: Movie[]) => {
      return movies;
    })
  }

  getMovie(id:string){
      return this.http.get<Movie>('/api/movies/' + id + '/')
  }

  createMovie(movie:Movie){
    movie.released = (new Date(movie.released)).toISOString().split('T')[0];
    this.http.post('/api/movies/', movie).subscribe(() => {
      alert('Movie created successfully!');
    }, error => {
      alert('Error creating movie: ' + error.message);
    })
  }

  updateMovie(movie:Movie){
    movie.released = (new Date(movie.released)).toISOString().split('T')[0];
    this.http.put('/api/movies/' + movie.pk + '/', movie).subscribe(() => {
      alert('Movie updated successfully!');
    }, error => {
      alert('Error updating movie: ' + error.message);
    })
  }

  deleteMovie(mov:number){
    return new Observable<void>((observer) => {
    this.http.delete('/api/movies/' + mov + '/').subscribe(() => {
      observer.next();
      observer.complete();
    },error => {
      observer.error(error);
    })
  })
  }
}
