import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { ViewsComponent } from './views/views.component';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { StyleManagerService } from './styleManager.service';
import { Subscription } from 'rxjs';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    NavbarComponent,
    ViewsComponent,
    HttpClientModule,
    CommonModule,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'] // Corregido a 'styleUrls' y debe ser un array
})
export class AppComponent {
  blurActive = false;
  private blurSub!: Subscription;

  constructor(private styleManager: StyleManagerService, public authService: AuthService) {} // Inyección del servicio

  ngOnInit() {
    this.blurSub = this.styleManager.blurState$.subscribe(isBlurred => {
      const footer = document.getElementById('footer');
      if (isBlurred) {
        footer?.classList.add('blur-background');
      } else {
        footer?.classList.remove('blur-background');
      }
    });
  }

  ngOnDestroy() {
    this.blurSub.unsubscribe();
  }
}
