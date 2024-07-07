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
    this.http.post<{token: string, expiresIn: number}>('http://localhost:8000/api/auth/login/', {username, password})
      .subscribe(response => {
        this.token = response.token;
        sessionStorage.setItem('auth_token', this.token); // Cambiado a sessionStorage
        this.router.navigate(['/main']);
      });
  }

  isLoggedIn(): boolean {
    const token = sessionStorage.getItem('auth_token'); // Cambiado a sessionStorage
    if (!token) {
      return false;
    }
    return true;
  }

  logout() {
    sessionStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }
}
