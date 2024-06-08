import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class LogintokenService {

  constructor(private http: HttpClient) { }

  login(username: string, password: string) {
    return this.http.post('', {username, password}).toPromise()
      .then((response: any) => {
        localStorage.setItem('acces_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
      });
  }
}
