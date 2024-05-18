import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {ModalwithshopComponent} from "./modalwithshop/modalwithshop.component";

export interface Venta{
  id: number;
  imagen: string;
  titulo: string;
  precio: number;
  descripcion: string;
}
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
  ventas: Venta[] = [
    {
      id: 1,
      imagen: '../../../../assets/img/Telefono.jpeg',
      titulo: 'S23',
      precio: 1200,
      descripcion: 'Un telefono mangrino'
    },
    {
      id: 2,
      imagen: '../../../../assets/img/Laptop.jpeg',
      titulo: 'Macbook',
      precio: 3400,
      descripcion: 'Una macbook mangrina'
    },
    {
      id: 3,
      imagen: '../../../../assets/img/RAM.jpeg',
      titulo: 'RAM DDR5 16GB',
      precio: 5000,
      descripcion: 'Una RAM claramente hecha con IA'
    },
    {
      id: 4,
      imagen: '../../../../assets/img/Carro.jpeg',
      titulo: 'Ferrari',
      precio: 5000000,
      descripcion: 'Un carro que nunca tendremos, pero ahi esta en una venta ficticia'
    },
    {
      id: 5,
      imagen: '../../../../assets/img/Grafica.jpeg',
      titulo: 'NVIDIA RTX 7090',
      precio: 4000,
      descripcion: 'Una tarjeta grafica de NVIDIA que no se si sea asi porque bueno, tiene mas rgb que potencia'
    },
    {
      id: 6,
      imagen: '../../../../assets/img/Raton.jpeg',
      titulo: 'Mouse GAMING 3000',
      precio: 150,
      descripcion: 'Erdiavlo pero que mouse papa que hacemos con esta vaina'
    },
    {
      id: 7,
      imagen: '../../../../assets/img/RatonApple.jpeg',
      titulo: 'Mouse michi michi',
      precio: 5000,
      descripcion: 'Super caro, pero que mas da, total la gente de apple compra por comprar'
    },
    {
      id: 8,
      imagen: '../../../../assets/img/Boligrafo.jpeg',
      titulo: 'Boligrafo',
      precio: 1,
      descripcion: 'La mejor oferta del mercado.'
    },
  ]
}
