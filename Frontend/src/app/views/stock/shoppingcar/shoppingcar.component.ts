import { Component } from '@angular/core';
import {CartService} from "../cartservice.service";
import {Venta} from "../stock.component";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-shoppingcar',
  standalone: true,
  imports: [
    NgForOf
  ],
  templateUrl: './shoppingcar.component.html',
  styleUrl: './shoppingcar.component.css'
})
export class ShoppingcarComponent {
  ventas: Venta[] = []

  constructor(private cartService: CartService) {
    this.ventas = this.cartService.getCart();
  }

}
