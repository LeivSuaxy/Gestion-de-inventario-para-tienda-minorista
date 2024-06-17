import {Component, Input} from '@angular/core';
import { Venta} from "../cartservice.service";
import {CartService} from "../cartservice.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-stockcards',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './stockcards.component.html',
  styleUrls: ['./stockcards.component.css']
})
export class StockcardsComponent {
  @Input() venta!: Venta;

  constructor(private cartService: CartService) { }
  added: boolean = false;

  addToCart(venta: Venta) {
    this.cartService.addToCart(venta);
    console.log(venta.nombre + ' added to cart')
  }

  removeFromCart(venta: Venta) {
    this.cartService.removeFromCart(venta.id_producto);
  }


  setadded(venta: Venta){
    this.addToCart(venta)
    this.added = !this.added;
  }

  isAdded(venta: Venta): boolean{
    return this.cartService.isInCar(venta);
  }
}
