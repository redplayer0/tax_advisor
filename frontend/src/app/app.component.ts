import { Component } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from './services/auth.service';
import { NgIf } from '@angular/common';
import { jwtDecode } from 'jwt-decode';

interface JwtToken {
  exp: number;
}

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLinkActive, RouterLink, NgIf],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Tax Advisor';
  remainingTime: string = '';
  private intervalId: any;

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.startTokenTimer();
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  isLoggedIn(): boolean {
    return !this.authService.isTokenExpired();
  }

  logout(): void {
    this.authService.clearToken();
    this.router.navigate(['/']);
  }

  startTokenTimer(): void {
    const token = this.authService.getAccessToken();
    if (!token) return;

    try {
      const { exp } = jwtDecode<JwtToken>(token);
      const expirationTime = exp * 1000;
      const currentTime = Date.now();
      const initialTimeLeft = expirationTime - currentTime;

      if (initialTimeLeft <= 0) {
        this.logout();
        return;
      }
      this.updateRemainingTime(expirationTime);
      this.intervalId = setInterval(() => {
        this.updateRemainingTime(expirationTime);
        if (Date.now() >= expirationTime) {
          this.logout();
          clearInterval(this.intervalId);
        }
      }, 1000);
    } catch (error) {
      console.error('Error decoding token:', error);
      this.logout();
    }
  }

  updateRemainingTime(expirationTime: number): void {
    const now = Date.now();
    const timeLeft = Math.max(0, expirationTime - now);
    const minutes = Math.floor(timeLeft / 60000);
    const seconds = Math.floor((timeLeft % 60000) / 1000);
    this.remainingTime = `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
}
