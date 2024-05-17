import { Component } from '@angular/core';
import {NgForOf, NgOptimizedImage} from "@angular/common";

@Component({
  selector: 'app-carousel',
  standalone: true,
  imports: [
    NgForOf,
    NgOptimizedImage
  ],
  templateUrl: './carousel.component.html',
  styleUrls: ['./carousel.component.css']
})
export class CarouselComponent {
  imagesURLs : string[] = [
    '../../../../assets/img/First.jpeg',
    '../../../../assets/img/Second.jpeg',
    '../../../../assets/img/R.jpeg',
  ]

}
