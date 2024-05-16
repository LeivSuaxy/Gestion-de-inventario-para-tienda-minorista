import { Component } from '@angular/core';
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-carousel',
  standalone: true,
  imports: [
    NgForOf
  ],
  templateUrl: './carousel.component.html',
  styleUrl: './carousel.component.css'
})
export class CarouselComponent {
  imagesURLs : string[] = [
    'Frontend/src/app/views/stock/carousel/img/First.jpeg',
    './img/Second.jpeg',
    './img/R.jpeg',
  ]

}
