import { Component, OnInit } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {CommonModule, NgForOf, NgIf} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {Venta} from "./cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {PaginationComponent} from "./pagination/pagination.component";
import {StockService} from "./stock.service";

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
    CommonModule,
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css',
})
export class StockComponent {
  ventas: Venta[] = []
  data: any;
  counterPage: number = 0;
  apiurl? = 'http://localhost:8000/api/objects/?page='+this.counterPage;
  apiurlnext? : string;
  apiurlprev? : string;
  nombre?: string;
  id_producto?: number;
  precio?: number;
  stock?: number;
  categoria?: string;
  descripcion?: string;
  imagen?: string;
  load: any;


  constructor(private http: HttpClient, private StockService: StockService) {
    this.load = this.StockService.loading$;
  }

  ngOnInit() {
    this.apicall();
  }


  private apicall(): void {
    this.StockService.show();
    if (this.apiurl) {
      this.http.get(this.apiurl).subscribe(data => {
        this.data = data;
        if (this.data['urls'].next) this.apiurlnext = this.data['urls'].next;
        if (this.data['urls'].previous) this.apiurlprev = this.data['urls'].previous;
        this.traslate();
        this.StockService.hide();
      }, error => {
        console.error(error);
        this.StockService.hide();
      });
    }
  }
  
  traslate(): void {
    this.ventas = this.data['elements'].map((element: any) => ({
      nombre: element.nombre,
      id_producto: element.id_producto,
      precio: element.precio,
      stock: element.stock,
      categoria: element.categoria,
      descripcion: element.descripcion,
      imagen: element.imagen
    }));
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
