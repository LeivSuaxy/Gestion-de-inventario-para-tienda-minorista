import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet} from "@angular/router";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {routes} from "../app.routes";
import {ModalwithshopComponent} from "../views/stock/modalwithshop/modalwithshop.component";

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

}
