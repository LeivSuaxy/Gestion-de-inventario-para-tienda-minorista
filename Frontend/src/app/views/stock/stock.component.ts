import { Component } from '@angular/core';
import {CarouselComponent} from "./carousel/carousel.component";

@Component({
  selector: 'app-stock',
  standalone: true,
  imports: [
    CarouselComponent
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css'
})
export class StockComponent {

}
