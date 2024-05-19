import { Component } from '@angular/core';
import {CartService} from "../cartservice.service";
import {Venta} from "../stock.component";
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
  preciototal: number;
  constructor(private cartService: CartService) {
    this.ventas = this.cartService.getCart();
    this.preciototal = this.cartService.getPrecioTotal();

  }


}
