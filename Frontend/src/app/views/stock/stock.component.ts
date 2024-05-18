import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {NgForOf, NgOptimizedImage} from "@angular/common";

interface Venta{
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
    NgForOf
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {
  ventas: Venta[] = [
    {
      imagen: '../../../../assets/img/Telefono.jpeg',
      titulo: 'S23',
      precio: 1200,
      descripcion: 'Un telefono mangrino'
    },
    {
      imagen: '../../../../assets/img/Laptop.jpeg',
      titulo: 'Macbook',
      precio: 3400,
      descripcion: 'Una macbook mangrina'
    },
    {
      imagen: '../../../../assets/img/RAM.jpeg',
      titulo: 'RAM DDR5 16GB',
      precio: 5000,
      descripcion: 'Una RAM claramente hecha con IA'
    },
    {
      imagen: '../../../../assets/img/Telefono.jpeg',
      titulo: 'S23',
      precio: 1200,
      descripcion: 'Un telefono mangrino'
    },
    {
      imagen: '../../../../assets/img/Laptop.jpeg',
      titulo: 'Macbook',
      precio: 3400,
      descripcion: 'Una macbook mangrina'
    },
    {
      imagen: '../../../../assets/img/RAM.jpeg',
      titulo: 'RAM DDR5 16GB',
      precio: 5000,
      descripcion: 'Una RAM claramente hecha con IA'
    },
    {
      imagen: '../../../../assets/img/Telefono.jpeg',
      titulo: 'S23',
      precio: 1200,
      descripcion: 'Un telefono mangrino'
    },
    {
      imagen: '../../../../assets/img/Laptop.jpeg',
      titulo: 'Macbook',
      precio: 3400,
      descripcion: 'Una macbook mangrina'
    },
    {
      imagen: '../../../../assets/img/RAM.jpeg',
      titulo: 'RAM DDR5 16GB',
      precio: 5000,
      descripcion: 'Una RAM claramente hecha con IA'
    }
  ]
}
