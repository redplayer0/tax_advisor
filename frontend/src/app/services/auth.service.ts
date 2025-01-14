import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  signup(username: string, password: string): Observable<any> {
    const payload = { username, password };
    return this.http.post(`${this.apiUrl}/signup`, payload);
  }

  login(username: string, password: string): Observable<any> {
    const payload = new URLSearchParams();
    payload.append('username', username);
    payload.append('password', password);
    payload.append('grant_type', 'password');

    return this.http.post(`${this.apiUrl}/token`, payload.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout`, {}, { withCredentials: true });
  }

  isAuthenticated(): Observable<any> {
    return this.http.get(`${this.apiUrl}/users/me`, { withCredentials: true });
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  saveToken(token: string, tokenType: string): void {
    localStorage.setItem('access_token', token);
    localStorage.setItem('token_type', tokenType);
  }

  clearToken(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
  }
}

