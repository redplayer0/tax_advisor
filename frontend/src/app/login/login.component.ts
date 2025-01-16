import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [NgIf, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  ngOnInit(): void {
    const redirect = this.route.snapshot.queryParamMap.get('redirect');
    if (redirect) {
      this.errorMessage = 'Please log in to access the requested page.';
    }
  }

  onLogin() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      this.authService.login(username, password).subscribe({
        next: (response) => {
          const { access_token, token_type } = response;
          this.authService.saveToken(access_token, token_type);
          // use this to force a refresh to show correct token time remaining..
          // TODO find way to avoid this hack
          window.location.href = '/';
          // this.router.navigate(['/advice']);
        },
        error: (err) => {
          if (err.error?.detail) {
            this.errorMessage = err.error.detail
          } else {
            alert('Login failed');
          }
        },
      });
    }
  }
}
