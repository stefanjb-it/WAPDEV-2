import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {JwtHelperService} from "@auth0/angular-jwt";
import {MatSnackBar} from "@angular/material/snack-bar";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  readonly accessTokenLocalStorageKey = 'access_token';
  isLoggedIn$ = new BehaviorSubject(false);

  constructor(private http: HttpClient, private router: Router, private jwtHelperService: JwtHelperService,
              private snackbar: MatSnackBar) {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    if (token) {
      console.log('Token expiration date: ' + this.jwtHelperService.getTokenExpirationDate(token));
      const tokenValid = !this.jwtHelperService.isTokenExpired(token);
      this.isLoggedIn$.next(tokenValid);
    }
  }
  login(userData: { username: string, password: string }): void {
    this.http.post('/api/token/', userData)
      .subscribe({
        next: (res: any) => {
          this.isLoggedIn$.next(true);
          localStorage.setItem('access_token', res.access);
          this.router.navigate(['movie-list']);
          this.snackbar.open('Successfully logged in', 'OK', {duration: 3000});
        },
        error: () => {
          this.snackbar.open('Invalid credentials', 'OK', {duration: 3000})
        }
      });
  }

  logout(): void {
    localStorage.removeItem(this.accessTokenLocalStorageKey);
    this.isLoggedIn$.next(false);
    this.router.navigate(['/login']);
  }

  hasPermission(permission: string):boolean {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    const decodedToken = this.jwtHelperService.decodeToken(token ? token: '');
    const permissions = decodedToken?.permissions;
    return permissions ? permission in permissions : false;
  }

  hasGroup(group: string):boolean {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    const decodedToken = this.jwtHelperService.decodeToken(token ? token: '');
    const groups = decodedToken?.groups;
    return groups ? group in groups : false;
  }

  isSu():boolean {
    const token = localStorage.getItem(this.accessTokenLocalStorageKey);
    const decodedToken = this.jwtHelperService.decodeToken(token ? token: '');
    return decodedToken?.su;
  }

}
