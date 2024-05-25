import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";

@Component({
  selector: 'app-postcar',
  standalone: true,
  imports: [
    FormsModule,
    HttpClientModule,
  ],
  templateUrl: './postcar.component.html',
  styleUrl: './postcar.component.css'
})
export class PostcarComponent {
  id? : number;
  name? : string;
  price? : number;
  description? : string;
  image? : string;
  stock? : number;

  constructor(private http : HttpClient) {
  }

  posMethod(): void {
    let url = 'http://localhost:8000/api/stockelement/';
    let formData = {
      id: this.id,
      name: this.name,
      price: this.price,
      description: this.description,
      stock: this.stock
    }

    this.http.post(url, formData).subscribe(
      (response) => {
        console.log(response);
      },
      (error) => {
        console.log(error);
      }
    );
  }

}
