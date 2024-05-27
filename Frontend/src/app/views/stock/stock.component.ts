import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgIf} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {CartService, Venta} from "./cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {PaginationComponent} from "./pagination/pagination.component";
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
    PaginationComponent,
    NgIf,
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {
  ventas: Venta[] = []
  data: any;
  counterPage: any;
  apiurl? = 'http://localhost:8000/api/stockelement/?page=1';
  apiurlnext? : string;
  apiurlprev? : string;


  constructor(service: CartService, private http: HttpClient) {
    this.apicall()
  }

  private apicall(): void{
    if(this.apiurl != null) {
      this.http.get(this.apiurl).subscribe(data => {
        this.data = data;
        if (this.data.next != null) this.apiurlnext = this.data.next;
        if (this.data.previous != null) this.apiurlprev = this.data.previous;
        this.traslate();
      })
    }
  }

  traslate():void {
    this.ventas = [];



    for (let i = 0; i < this.data.results.length; i++) {
      this.ventas.push({
        id: this.data.results[i].id,
        image: this.data.results[i].image,
        name: this.data.results[i].name,
        price: this.data.results[i].price,
        description: this.data.results[i].description,
        stock: this.data.results[i].stock
      })
    }
  }

  next(){
    new Promise(resolve => {
      window.scrollTo({top: 0, behavior: 'smooth'});
      setTimeout(resolve, 400);
    }).then(() => {
      this.apiurl = this.apiurlnext;
      this.apicall();
    });
  }

  prev() {
    new Promise(resolve => {
      window.scrollTo({top: 0, behavior: 'smooth'});
      setTimeout(resolve, 400);
    }).then(() => {
      this.apiurl = this.apiurlprev;
      this.apicall();
    });
  }
}
