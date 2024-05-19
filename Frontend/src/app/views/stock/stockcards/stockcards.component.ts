import {Component, Input} from '@angular/core';
import {Venta} from "../stock.component";
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
    console.log(venta.titulo + ' added to cart')
  }

  setadded(venta: Venta){
    this.addToCart(venta)
    this.added = !this.added;
  }
}
