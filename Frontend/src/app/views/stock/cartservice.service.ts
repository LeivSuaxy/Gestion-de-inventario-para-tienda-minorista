import { Injectable } from '@angular/core';
import {HttpClient, HttpClientModule} from "@angular/common/http";
//import { HttpClientModule } from "@angular/common/http";
//import { Component, OnInit } from "@angular/core";

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
  /*tankeFunction(): void {
    this.http.get('http://localhost:8000/api').subscribe(data => {
      this.data = data;
      alert(data)
    })
  }*/



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
    return this.cart.includes(venta);
  }

  clearCart() {
    this.cart = [];
    return this.cart;
  }
}
