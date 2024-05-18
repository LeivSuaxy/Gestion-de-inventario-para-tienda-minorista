import { Injectable } from '@angular/core';
import { Venta } from './stock.component';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  cart: Venta[] = [];

  addToCart(product: Venta) {
    this.cart.push(product);
  }

  getCart() {
    return this.cart;
  }

  clearCart() {
    this.cart = [];
    return this.cart;
  }
}
