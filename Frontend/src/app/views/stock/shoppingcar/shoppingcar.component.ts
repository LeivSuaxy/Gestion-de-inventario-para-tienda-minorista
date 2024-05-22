import { Component } from '@angular/core';
import {CartService} from "../cartservice.service";
import {Venta} from "../cartservice.service";
import {NgForOf, NgIf} from "@angular/common";

@Component({
  selector: 'app-shoppingcar',
  standalone: true,
  imports: [
    NgForOf,
    NgIf
  ],
  templateUrl: './shoppingcar.component.html',
  styleUrl: './shoppingcar.component.css'
})
export class ShoppingcarComponent {
  ventas: Venta[] = []
  constructor(protected cartService: CartService) {
    this.ventas = this.cartService.getCart();
  }

  ngOnInit(){
    this.ventas = this.cartService.getCart();
  }


}
