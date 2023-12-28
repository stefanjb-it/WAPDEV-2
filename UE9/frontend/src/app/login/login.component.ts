import {Component, OnInit} from '@angular/core';
import {MatCardModule} from "@angular/material/card";
import {MatFormFieldModule} from "@angular/material/form-field";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";
import {HttpClient} from "@angular/common/http";
import {Router} from "@angular/router";
import {MatSnackBar} from "@angular/material/snack-bar";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    MatCardModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent implements OnInit{
  loginFormGroup: FormGroup;

  constructor(private fb: FormBuilder, private http: HttpClient, private router: Router,
              private snackbar: MatSnackBar) {
    this.loginFormGroup = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  ngOnInit(): void {
  }

  login(): void {
    this.http.post('/api/token/', this.loginFormGroup.value)
      .subscribe({
        next: (res: any) => {
          localStorage.setItem('access_token', res.access);
          this.router.navigate(['movie-list']);
          this.snackbar.open('Successfully logged in', 'OK', {duration: 3000})
        },
        error: () => {
          this.snackbar.open('Invalid credentials', 'OK', {duration: 3000})
        }
      });
  }
}
