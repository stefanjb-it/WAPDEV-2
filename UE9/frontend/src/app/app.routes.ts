import { Routes } from '@angular/router';
import {MovieListComponent} from "./movie-list/movie-list.component";
import {MovieFormComponent} from "./movie-form/movie-form.component";
import {LoginComponent} from "./login/login.component";
import {authGuard} from "./auth.guard";

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'movie-list',
    pathMatch: 'full'
  },
  {
    path: 'movie-list',
    component: MovieListComponent,
    canActivate: [authGuard]
  },
  {
    path: 'movie-form',
    component: MovieFormComponent,
    canActivate: [authGuard]
  },
  {
    path: 'movie-form/:id',
    component: MovieFormComponent,
    canActivate: [authGuard]
  },
  {
    path: 'login',
    component: LoginComponent
  },
  /*{
    path: 'movie-detail',
    loadChildren: './movie-detail/movie-detail.module#MovieDetailModule'
  }*/
];
