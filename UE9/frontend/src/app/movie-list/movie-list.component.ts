import {Component, OnInit} from '@angular/core';
import {Movie} from "../models/Movie";
import {HttpClient} from "@angular/common/http";
import {DatePipe, NgForOf, NgIf} from "@angular/common";
import {RouterLink} from "@angular/router";
import {MovieService} from "../movie.service";
import {MatTableModule} from "@angular/material/table";
import {MatButtonModule} from "@angular/material/button";
import {StarRatingModule, StarRatingConfigService} from "angular-star-rating";
import {UserService} from "../user.service";
import {filter, map} from "rxjs";

@Component({
  selector: 'app-movie-list',
  standalone: true,
  imports: [
    DatePipe,
    NgForOf,
    RouterLink,
    MatTableModule,
    MatButtonModule,
    StarRatingModule,
    NgIf
  ],
  templateUrl: './movie-list.component.html',
  styleUrl: './movie-list.component.scss'
})
export class MovieListComponent implements OnInit {
  movies: Movie[] = []
  testText = ""

  displayed_columns = ['movie_title', 'released', 'runtime', 'rating', 'genres', 'edit', 'delete']

  constructor(private http: HttpClient, private movieService: MovieService, private starRatingConfigService: StarRatingConfigService, public userService: UserService) {
  }

  mapToName(genres: any[]) {
    return genres.map((genre: any) => genre.name).join(', ')
  }

  ngOnInit() {
    this.updateList()
    const myPromise = new Promise<void>((resolve, reject) => {
      setTimeout(() => resolve(), 1000);
    });

    myPromise.then(
      (success) => console.log('Success'),
      (error) => console.log('Error')
    );
    console.log('Hello World');
  }

  updateList() {
    console.log(this.userService.isSu())
    if (this.userService.isSu()) {
      this.movieService.getMovies().subscribe(movies => {
        this.movies = movies
        console.log(this.movies)
      });
    }
    else {
      this.movieService.getMovies().pipe(map(movies => movies.filter(movie => movie.black_and_white))).subscribe(movies => {
        this.movies = movies
        console.log(this.movies)
      });
    }
  }

  deleteMovie(mov:number) {
    this.movieService.deleteMovie(mov).subscribe(() => {
      this.updateList()
    }, error => {
      alert('Error deleting movie: ' + error.message);
    })
  }
}
