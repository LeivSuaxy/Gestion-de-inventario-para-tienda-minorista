import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {ModalwithshopComponent} from "../views/stock/modalwithshop/modalwithshop.component";
import {Router} from "@angular/router";
import { ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    RouterLink,
    NgOptimizedImage,
    RouterLinkActive,
    RouterOutlet,
    CommonModule,
    ModalwithshopComponent
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  constructor(public router: Router) { }

  @ViewChild('menuButton', { static: true }) menuButton!: ElementRef;
  @ViewChild('menu', { static: true }) menu!: ElementRef;
  @ViewChild('navbar', { static: true }) navbar!: ElementRef;

  menuOpen = false;

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
    if (this.menuOpen) {
      const rect = this.navbar.nativeElement.getBoundingClientRect();
      this.menu.nativeElement.style.top = `${rect.bottom}px`;
      this.menu.nativeElement.style.left = `${rect.left}px`;
      this.menu.nativeElement.style.maxHeight = '500px'; // Ajusta la maxHeight a un valor grande cuando el menú está abierto
    } else {
      this.menu.nativeElement.style.maxHeight = '0'; // Ajusta la maxHeight a '0' cuando el menú está cerrado
    }
  }
}


