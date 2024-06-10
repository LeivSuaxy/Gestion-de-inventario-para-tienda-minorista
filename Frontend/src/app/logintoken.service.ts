import { Injectable } from '@angular/core';
import { HttpClient, HttpClientModule } from "@angular/common/http";


@Injectable({
  providedIn: 'root',
  useClass: HttpClientModule,
})
export class LogintokenService {

  constructor(private http: HttpClient) { }

  loginAPI(username: string, password: string) {
    const body = {username: username, password: password};
    this.http.post('http://localhost:8000/api/auth/token/', body).subscribe(
      response => console.log(response),
      error => console.log(error)
    );
  }
}
