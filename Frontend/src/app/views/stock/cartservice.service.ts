import { Injectable } from '@angular/core';
import { Venta } from './stock.component';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  cart: Venta[] = [];
  preciototal: number = 0;

  addToCart(product: Venta) {
    if(!this.cart.includes(product)) this.cart.push(product);
    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += this.cart[i].precio;
    }
  }

  getCart() {
    return this.cart;
  }

  getPrecioTotal() {
    return this.preciototal;
  }

  clearCart() {
    this.cart = [];
    return this.cart;
  }
}
