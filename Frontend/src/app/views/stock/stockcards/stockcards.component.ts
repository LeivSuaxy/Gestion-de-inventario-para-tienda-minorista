import {Component, Input} from '@angular/core';

interface Venta {
  imagen: string;
  titulo: string;
  precio: number;
  descripcion: string;
}

@Component({
  selector: 'app-stockcards',
  standalone: true,
  imports: [],
  templateUrl: './stockcards.component.html',
  styleUrls: ['./stockcards.component.css']
})
export class StockcardsComponent {
  @Input() venta!: Venta;
}
