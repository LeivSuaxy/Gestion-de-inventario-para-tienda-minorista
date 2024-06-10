import { Injectable } from '@angular/core';
import { HttpClient, HttpClientModule } from "@angular/common/http";


@Injectable({
  providedIn: 'root',
  useClass: HttpClientModule,
})
export class LogintokenService {

  constructor(private http: HttpClient) { }

  loginAPI(username: string, password: string) {
    return this.http.post('http://localhost:8000/api/auth/token/', {username, password}).toPromise()
      .then((response: any) => {
        //console.log(response.access)
        localStorage.setItem('acces_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
      });
  }
}
