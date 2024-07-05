import { Component, HostListener } from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import { ViewChild, ElementRef } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    RouterLink,
    NgOptimizedImage,
    RouterLinkActive,
    RouterOutlet,
    CommonModule,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  showConfirmDialog = false;

  constructor(public router: Router, public authService: AuthService) { }

  @ViewChild('menuButton', { static: true }) menuButton!: ElementRef;
  @ViewChild('menu', { static: true }) menu!: ElementRef;
  @ViewChild('navbar', { static: true }) navbar!: ElementRef;

  menuOpen = false;

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
    this.menuButton.nativeElement.checked = this.menuOpen; // Actualiza el estado del checkbox
    if (this.menuOpen) {
      const rect = this.navbar.nativeElement.getBoundingClientRect();
      this.menu.nativeElement.style.top = `${rect.bottom}px`;
      this.menu.nativeElement.style.left = `${rect.left}px`;
      this.menu.nativeElement.style.maxHeight = '500px';
    } else {
      this.closeMenu();
    }
  }
  
  closeMenu() {
    this.menuOpen = false;
    this.menu.nativeElement.style.maxHeight = '0';
    this.menuButton.nativeElement.checked = false; // Asegura que el checkbox se desmarque
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    if (!this.navbar.nativeElement.contains(event.target) && !this.menuButton.nativeElement.contains(event.target) && this.menuOpen) {
      this.closeMenu();
    }
  }
}


