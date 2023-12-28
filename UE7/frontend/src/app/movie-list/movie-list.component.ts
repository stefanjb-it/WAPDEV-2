import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {DatePipe, NgForOf} from "@angular/common";
import {RouterLink} from "@angular/router";
import {Movie} from "../model/Movie"
import {MovieService} from "../services/movie.service";

@Component({
  selector: 'app-movie-list',
  standalone: true,
  imports: [
    NgForOf,
    DatePipe,
    RouterLink
  ],
  templateUrl: './movie-list.component.html',
  styleUrl: './movie-list.component.css'
})
export class MovieListComponent implements OnInit {
  movies: Movie[] = []

  constructor(private http:HttpClient, private movieService:MovieService) {

  }

  ngOnInit() {
    this.movieService.getMovies().subscribe(movies => {
      this.movies = movies
    })
  }

  deleteMovie(movie: Movie) {
    this.movieService.deleteMovie(movie).subscribe(() => {
      this.ngOnInit()
    })
  }

}
