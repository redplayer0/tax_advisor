import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000'; // Replace with your FastAPI backend URL

  constructor(private http: HttpClient) { }

  signup(username: string, password: string): Observable<any> {
    const payload = { username, password };
    return this.http.post(`${this.apiUrl}/signup`, payload);
  }

  login(username: string, password: string): Observable<any> {
    const payload = { username, password };
    return this.http.post(`${this.apiUrl}/login`, payload, { withCredentials: true });
  }

  logout(): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout`, {}, { withCredentials: true });
  }

  /**
   * Function to check if a user is authenticated
   * (You can enhance this to check tokens, etc.)
   * @returns Observable with the API response
   */
  isAuthenticated(): Observable<any> {
    return this.http.get(`${this.apiUrl}/auth-status`, { withCredentials: true });
  }
}
