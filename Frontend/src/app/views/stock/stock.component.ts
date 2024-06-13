import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgIf} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {Venta} from "./cartservice.service";
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
  counterPage: number = 0;
  apiurl? = 'http://localhost:8000/api/objects/?page='+this.counterPage;
  apiurlnext? : string;
  apiurlprev? : string;


  constructor(private http: HttpClient) {
    this.apicall()
  }

  private apicall(): void{
    if(this.apiurl != null) {
      this.http.get(this.apiurl).subscribe(data => {
        this.data = data;
        this.apiurlnext = `http://localhost:8000/api/objects/?page=${this.counterPage + 1}`;
        this.apiurlprev = `http://localhost:8000/api/objects/?page=${this.counterPage}`;
        this.counterPage++;
        this.traslate();
      })
    }
  }

  traslate():void {
    this.ventas = [];



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
