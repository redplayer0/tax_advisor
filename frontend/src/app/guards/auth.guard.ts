import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) { }

  canActivate(): boolean {
    const token = this.authService.getAccessToken();
    if (token) {
      if (this.authService.isTokenExpired()) {
        this.authService.clearToken()
        this.router.navigate(['/login'], { queryParams: { redirect: 'advice' } });
        return false;
      }
      return true;
    } else {
      this.router.navigate(['/login'], { queryParams: { redirect: 'advice' } });
      return false;
    }
  }
}
