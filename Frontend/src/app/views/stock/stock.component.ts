import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";
import {CartService, Venta} from "./cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
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
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {
  ventas: Venta[] = [
    {
      id: 1,
      image: '../../../../assets/img/Telefono.jpeg',
      name: 'S23 Ultra',
      price: 1200,
      description: 'Samsung Galaxy S23 Ultra, con 512GB de almacenamiento interno, 12GB de RAM, 5 camaras, 1 principal con' +
        '200MP, 1 gran angular de 50MP, 1 telefoto de 20MP, 1 macro de 5MP y 1 de profundidad de 2MP. Ademas de una pantalla' +
        'Super AMOLED.',
      stock: 270
    },
    {
      id: 2,
      image: '../../../../assets/img/Laptop.jpeg',
      name: 'Macbook',
      price: 3400,
      description: 'Una macbook mangrina',
      stock: 70
    },
    {
      id: 3,
      image: '../../../../assets/img/RAM.jpeg',
      name: 'RAM DDR5 16GB',
      price: 5000,
      description: 'Una RAM claramente hecha con IA',
      stock: 120
    },
    {
      id: 4,
      image: '../../../../assets/img/Carro.jpeg',
      name: 'Ferrari',
      price: 5000000,
      description: 'Un carro que nunca tendremos, pero ahi esta en una venta ficticia',
      stock: 20
    },
    {
      id: 5,
      image: '../../../../assets/img/Grafica.jpeg',
      name: 'NVIDIA RTX 7090',
      price: 4000,
      description: 'Una tarjeta grafica de NVIDIA que no se si sea asi porque bueno, tiene mas rgb que potencia',
      stock: 120
    },
    {
      id: 6,
      image: '../../../../assets/img/Raton.jpeg',
      name: 'Mouse GAMING 3000',
      price: 150,
      description: 'Erdiavlo pero que mouse papa que hacemos con esta vaina',
      stock: 200
    },
    {
      id: 7,
      image: '../../../../assets/img/RatonApple.jpeg',
      name: 'Mouse michi michi',
      price: 5000,
      description: 'Super caro, pero que mas da, total la gente de apple compra por comprar',
      stock: 100
    },
    {
      id: 8,
      image: '../../../../assets/img/Boligrafo.jpeg',
      name: 'Boligrafo',
      price: 1,
      description: 'La mejor oferta del mercado.',
      stock: 1000
    },
  ]
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
