import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { NgIf } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  imports: [NgIf, ReactiveFormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  signupForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.signupForm = this.fb.group(
      {
        username: ['', [Validators.required]],
        password: ['', [Validators.required, Validators.minLength(8)]],
        confirmPassword: ['', Validators.required],
      },
      { validators: this.passwordsMatchValidator }
    );
  }

  passwordsMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { passwordMismatch: true };
  }

  onSignup() {
    if (this.signupForm.valid) {
      const { username, password } = this.signupForm.value;
      this.authService.signup(username, password).subscribe({
        next: () => {
          alert('Signup successful!')
          this.router.navigate(['/login']);
        },
        error: (err) => {
          if (err.error?.detail) {
            alert(`Signup failed: ${err.error.detail}`);
          } else {
            alert('Signup failed');
          }
        },
      });
    }
  }
}
