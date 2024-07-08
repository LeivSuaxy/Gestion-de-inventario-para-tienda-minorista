import { Component } from '@angular/core';
import {CartService} from "../cartservice.service";
import {Venta} from "../cartservice.service";
import {NgForOf, NgIf} from "@angular/common";
import { SharedService } from '../shared.service';

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
  constructor(protected cartService: CartService, private sharedService: SharedService) {
    //this.ventas = this.cartService.getCart();
  }

  ngOnInit(){
  }

  // Incrementa la cantidad de un elemento específico
  incrementarCantidad(index: number): void {
    this.cartService.getCart()[index].cantidad += 1;
    this.cartService.preciototal += Number(this.cartService.getCart()[index].precio);
  }

  // Decrementa la cantidad de un elemento específico
  decrementarCantidad(index: number): void {
    this.cartService.preciototal -= Number(this.cartService.getCart()[index].precio);
    if (this.cartService.getCart()[index].cantidad > 1) {
      this.cartService.getCart()[index].cantidad -= 1;
    } else {
      this.removerDelCarrito(index);
    }
  }

  // Remueve un elemento del carrito
  removerDelCarrito(index: number): void {
    this.cartService.getCart().splice(index, 1);
  }

  // Comprobar si el carrito esta vacio
  carroVacio(): boolean {
    return this.cartService.getCart().length == 0;
  }

  openPost() {
    this.sharedService.triggerFunction('openDialog');
  }

}
