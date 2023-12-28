import {Component, forwardRef, OnInit} from '@angular/core';
import {
  AbstractControl,
  AsyncValidator,
  AsyncValidatorFn,
  FormControl,
  FormGroup, NG_VALUE_ACCESSOR,
  ReactiveFormsModule, ValidationErrors,
  Validators
} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {ActivatedRoute} from "@angular/router";
import {KeyValueItem} from "../models/KeyValueItem";
import {Movie} from "../models/Movie";
import {NgForOf, NgIf} from "@angular/common";
import {MovieService} from "../movie.service";
import {MatInputModule} from "@angular/material/input";
import {MatSelectModule} from "@angular/material/select";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatCardModule} from "@angular/material/card";
import {DatePickerNewComponent} from "../date-picker-new/date-picker-new.component";
import {MatButtonModule} from "@angular/material/button";
import {CountryService} from "../country.service";
import {map, Observable} from "rxjs";
import {StarRatingModule} from "angular-star-rating";
import {MatSliderModule} from "@angular/material/slider";
import {RatingSliderComponent} from "../rating-slider/rating-slider.component";
import {StarsComponent} from "../stars/stars.component";

@Component({
  selector: 'app-movie-form',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf,
    MatInputModule,
    MatSelectModule,
    MatCheckboxModule,
    MatCardModule,
    DatePickerNewComponent,
    MatButtonModule,
    NgForOf,
    StarRatingModule,
    MatSliderModule,
    RatingSliderComponent,
    StarsComponent
  ],
  providers: [],
  templateUrl: './movie-form.component.html',
  styleUrl: './movie-form.component.scss'
})
export class MovieFormComponent implements OnInit {
  movieFormGroup: FormGroup;
  selection : string | undefined | null;
  countryOptions: KeyValueItem[] = [];
  genreList: number[] = [];

  ngOnInit(): void {
    this.selection = this.route.snapshot.paramMap.get('id');
    this.countryService.getCountries().subscribe((countries: KeyValueItem[]) => {
      this.countryOptions = countries;
    });
    console.log(this.selection);
    if (this.selection) {
      /*this.http.get<Movie>('/api/movies/' + this.selection).subscribe((movie: Movie) => {
        this.movieFormGroup.patchValue({...movie, genre: movie.genres.map((current_genre: KeyValueItem) => current_genre.pk)});
      })*/
      this.movieService.getMovie(this.selection).subscribe((movie: Movie) => {
        this.movieFormGroup.patchValue({...movie, genre: movie.genres.map((current_genre: KeyValueItem) => current_genre.pk)});
      });
    }
    this.movieFormGroup.valueChanges.subscribe((newValue) => {
      console.log(newValue);
    });
  }

  titleValidator():AsyncValidatorFn{
    return (control:AbstractControl):Observable<ValidationErrors | null> => {
      return new Observable((observer) => {
        this.movieService.getMovies().subscribe((movies: Movie[]) => {
          const currentId = this.movieFormGroup.value.pk;
          const currentTitle = this.movieFormGroup.value.movie_title;
          const existingMovie = movies.find((movie: Movie) => movie.movie_title === currentTitle && movie.pk !== currentId);
          if(existingMovie){
            console.log(existingMovie);
            observer.next({titleAlreadyExists: true});
            observer.complete();
          } else {
            console.log(existingMovie);
            observer.next(null);
            observer.complete();
          }
        })
      })
    }
  }

  constructor(private http: HttpClient, private route: ActivatedRoute, private movieService: MovieService, private countryService: CountryService) {
    this.movieFormGroup = new FormGroup({
      pk: new FormControl(null),
      movie_title: new FormControl('', [Validators.required], [this.titleValidator()]),
      genres: new FormControl([]),
      released: new FormControl(new Date()),
      runtime: new FormControl(),
      black_and_white: new FormControl(false),
      country: new FormControl(null),
      rating: new FormControl(0),
    });
  }

  changeRatingValue(r:any){
    this.movieFormGroup.patchValue({rating: r.value});
  }

  createMovie() {
    if (this.movieFormGroup.value.pk) {
      this.movieService.updateMovie(this.movieFormGroup.value);
    } else {
      this.movieService.createMovie(this.movieFormGroup.value);
    }
  }

}
