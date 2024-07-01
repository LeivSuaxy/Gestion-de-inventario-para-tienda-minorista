import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private token: string | null = null;
  //isLoggedIn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string) {
    this.http.post<{token: string}>('http://localhost:8000/api/auth/login/', {username, password})
      .subscribe(response => {
        this.token = response.token;
        localStorage.setItem('auth_token', this.token);
        this.router.navigate(['/main']);
      });
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  logout() {
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }
}
