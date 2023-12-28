import {Component} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";
import {Movie} from "../model/Movie"
import {MovieService} from "../services/movie.service";

@Component({
  selector: 'app-movie-form',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './movie-form.component.html',
  styleUrl: './movie-form.component.css'
})
export class MovieFormComponent {

  movieFormGroup: FormGroup;
  pk: string | null = this.route.snapshot.paramMap.get('pk')

  constructor(private http: HttpClient, private route: ActivatedRoute, private movieService:MovieService) {
    this.movieFormGroup = new FormGroup({
      pk: new FormControl(null),
      movie_title: new FormControl(''),
      genres: new FormControl([]),
      released: new FormControl(new Date()),
      runtime: new FormControl(),
      black_and_white: new FormControl(false),
      country: new FormControl(null)
    })
  }

  ngOnInit(): void {
    if (this.pk) {
      this.http.get<Movie>(`/api/movies/${this.pk}`)
        .subscribe(movie => {
          this.movieFormGroup.patchValue({...movie,
          genres: movie.genres.map(genre => genre.pk)})
        })
    }
  }

  createMovie() {
    if (this.pk) {
      this.movieService.updateMovie(this.movieFormGroup.value).subscribe(() => {
        alert('Movie modified successfully!')
      })
    } else {
      this.movieService.createMovie(this.movieFormGroup.value).subscribe(() => {
        alert('Movie created successfully!');
      })
    }
  }
}
