import {Component, Input} from '@angular/core';
import {Venta} from "../stock.component";
import {CartService} from "../cartservice.service";

@Component({
  selector: 'app-stockcards',
  standalone: true,
  imports: [],
  templateUrl: './stockcards.component.html',
  styleUrls: ['./stockcards.component.css']
})
export class StockcardsComponent {
  @Input() venta!: Venta;

  constructor(private cartService: CartService) { }

  addToCart(venta: Venta) {
    this.cartService.addToCart(venta);
    console.log(venta.titulo + ' added to cart')
  }
}
