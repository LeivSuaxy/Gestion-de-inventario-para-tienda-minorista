import { Component } from '@angular/core';
import {ShoppingcarComponent} from "../shoppingcar/shoppingcar.component";

@Component({
  selector: 'app-modalwithshop',
  standalone: true,
  imports: [
    ShoppingcarComponent
  ],
  templateUrl: './modalwithshop.component.html',
  styleUrl: './modalwithshop.component.css'
})
export class ModalwithshopComponent {

}
