import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service'; // Asume que tienes un servicio de autenticación

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(private AuthService: AuthService, private router: Router) { }

  canActivate(): boolean {
    if (this.AuthService.isLoggedIn()) {
      return true;
    }
    // Si no está logeado, redirige al login
    this.router.navigate(['/login']);
    return false;
  }
}