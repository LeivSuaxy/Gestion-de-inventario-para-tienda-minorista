import { Injectable } from '@angular/core';


export interface Venta{
  id: number;
  image?: string;
  name: string;
  price: number;
  description: string;
  stock: number;
}

@Injectable({
  providedIn: 'root'
})
export class CartService {
  cart: Venta[] = [];
  preciototal: number = 0;


  data : any;


  constructor() {
  }

  addToCart(product: Venta) {
    if(!this.cart.includes(product)) this.cart.push(product);
    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += this.cart[i].price;
    }
  }

  removeFromCart(productid: number) {
    this.cart = this.cart.filter(product => product.id !== productid);

    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += this.cart[i].price;
    }
  }

  getCart() {
    return this.cart;
  }

  getPrecioTotal() {
    return this.preciototal;
  }

  isInCar(venta: Venta):boolean{
    for(let i = 0; i < this.cart.length; i++){
      if(this.cart[i].id == venta.id){
        return true;
      }
    }

    return false;
  }

  clearCart() {
    this.cart = [];
    return this.cart;
  }
}
