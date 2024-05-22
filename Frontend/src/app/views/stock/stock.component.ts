import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {CartService, Venta} from "./cartservice.service";
@Component({
  selector: 'app-stock',
  standalone: true,
  imports: [
    CarouselComponent,
    StockcardsComponent,
    NgForOf,
    ShoppingcarComponent,
    ModalwithshopComponent
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {
  ventas: Venta[];


  constructor(service: CartService) {
    this.ventas = service.ventas;
  }
}
