import { Injectable } from '@angular/core';


export interface Venta{
  id_producto: number;
  imagen?: string;
  nombre: string;
  precio: number;
  descripcion: string;
  stock: number;
  categoria: string;
  fecha_entrada: string;
  cantidad: number;
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
    product.cantidad = 1;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += Number(this.cart[i].precio) * Number(this.cart[i].cantidad);
    }
  }

  removeFromCart(productid: number) {
    this.cart = this.cart.filter(product => product.id_producto !== productid);

    this.preciototal = 0;
    for (let i = 0; i < this.cart.length; i++) {
      this.preciototal += Number(this.cart[i].precio) * Number(this.cart[i].cantidad);
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
      if(this.cart[i].id_producto == venta.id_producto){
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
