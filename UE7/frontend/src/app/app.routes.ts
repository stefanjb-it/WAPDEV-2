import { Routes } from '@angular/router';
import {MovieListComponent} from "./movie-list/movie-list.component";
import {MovieFormComponent} from "./movie-form/movie-form.component";

export const routes: Routes = [
  {path: '', redirectTo: '/movie-list', pathMatch: 'full'},
  {path: 'movie-list', component: MovieListComponent},
  {path: 'movie-form', component: MovieFormComponent},
  {path: 'movie-form/:pk', component: MovieFormComponent}
];
