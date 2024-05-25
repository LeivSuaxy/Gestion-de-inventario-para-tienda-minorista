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
  image? : File;
  stock? : number;

  constructor(private http : HttpClient) {
  }

  posMethod(): void {
    let url = 'http://localhost:8000/api/stockelement/';
    const formData = new FormData();
    formData.append('id', this.id?.toString() ?? '');
    formData.append('image', this.image? this.image : '');
    formData.append('name', this.name?.toString() ?? '');
    formData.append('price', this.price?.toString() ?? '');
    formData.append('description', this.description?.toString() ?? '');
    formData.append('stock', this.stock?.toString() ?? '');

    fetch(url, {
      method: 'POST',
      body: formData
    });
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target && target.files && target.files.length > 0) {
      this.image = target.files[0];
      alert(this.image.type)
    }
  }

}
