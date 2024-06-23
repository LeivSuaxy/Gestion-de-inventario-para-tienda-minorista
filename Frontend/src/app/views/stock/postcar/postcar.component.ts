import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {ChangeDetectionStrategy} from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-postcar',
  standalone: true,
  imports: [
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './postcar.component.html',
  styleUrl: './postcar.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PostcarComponent {
  name? : string;
  price? : number;
  description? : string;
  image? : File;
  stock? : number;
  
  constructor(private http : HttpClient) {
  }

  posMethod(): void {
    let url = 'http://localhost:8000/api/objects/?page=0';
    const formData = new FormData();
    formData.append('image', this.image? this.image : '');
    formData.append('name', this.name?.toString() ?? '');
    formData.append('price', this.price?.toString() ?? '');
    formData.append('description', this.description?.toString() ?? '');
    formData.append('stock', this.stock?.toString() ?? '');

    fetch(url, {
      method: 'GET',
      body: formData
    }).then(() => {
      this.name = undefined;
      this.price = undefined;
      this.description = undefined;
      this.image = undefined;
      this.stock = undefined;
    });


  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target && target.files && target.files.length > 0) {
      this.image = target.files[0];
    }
  }

}
