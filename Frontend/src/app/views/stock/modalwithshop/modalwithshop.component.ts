import { Component } from '@angular/core';
import {ShoppingcarComponent} from "../shoppingcar/shoppingcar.component";
import {CartService, Venta} from "../cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";

@Component({
  selector: 'app-modalwithshop',
  standalone: true,
  imports: [
    ShoppingcarComponent,
    HttpClientModule
  ],
  templateUrl: './modalwithshop.component.html',
  styleUrl: './modalwithshop.component.css'
})
export class ModalwithshopComponent {
  constructor(private service: CartService) { }


  sendTo(){
    let carList: Venta[] = this.service.getCart();


  }
}
