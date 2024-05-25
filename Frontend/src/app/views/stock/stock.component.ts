import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {CartService, Venta} from "./cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {RouterLink, RouterLinkActive} from "@angular/router";
@Component({
  selector: 'app-stock',
  standalone: true,
    imports: [
        CarouselComponent,
        StockcardsComponent,
        NgForOf,
        ShoppingcarComponent,
        ModalwithshopComponent,
        HttpClientModule,
        RouterLink,
        RouterLinkActive,
    ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {
  ventas: Venta[] = []
  data: any;

  constructor(service: CartService, private http: HttpClient) {
    this.http.get('http://localhost:8000/api/stockelement/').subscribe(data  => {
      this.data = data;
      this.traslate();
    })

  }

  traslate():void {
    for (let i = 0; i < this.data.length; i++) {
      this.ventas.push({
        id: this.data[i].id,
        image: this.data[i].image,
        name: this.data[i].name,
        price: this.data[i].price,
        description: this.data[i].description,
        stock: this.data[i].stock
      })
    }
  }
}
