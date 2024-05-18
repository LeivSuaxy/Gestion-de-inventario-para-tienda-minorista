import { Component } from '@angular/core';
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";

@Component({
  selector: 'app-carousel',
  standalone: true,
  imports: [
    NgForOf,
    NgOptimizedImage,
    NgIf
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

  slidesNumbers : string[];

  constructor() {
    this.slidesNumbers = [];
    for (let i = 0; i < this.imagesURLs.length; i++) {
      this.slidesNumbers.push(i.toString());
    }
  }

}
