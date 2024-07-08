import { Component } from '@angular/core';
import {StockcardsComponent} from "./stockcards/stockcards.component";
import {CommonModule, NgForOf, NgIf} from "@angular/common";
import {ShoppingcarComponent} from "./shoppingcar/shoppingcar.component";
import {Venta} from "./cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {StockService} from "./stock.service";
import { Post_clientComponent } from './post_client/post_client.component';
import { StyleManagerService } from '../../styleManager.service';
import { SharedService } from './shared.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-stock',
  standalone: true,
  imports: [
    StockcardsComponent,
    NgForOf,
    ShoppingcarComponent,
    HttpClientModule,
    RouterLink,
    RouterLinkActive,
    NgIf,
    CommonModule,
    Post_clientComponent
  ],
  templateUrl: './stock.component.html',
  styleUrl: './stock.component.css',
})
export class StockComponent {
  ventas: Venta[] = []
  data: any;
  counterPage: number = 0;
  apiurl? = 'http://localhost:8000/api/public/objects/?page='+this.counterPage;
  apiurlnext? : string;
  apiurlprev? : string;
  load: any;
  showConfirmDialog = false;
  private subscription?: Subscription;


  constructor(private http: HttpClient, private StockService: StockService, private styleManager: StyleManagerService, private sharedService: SharedService) {
    this.load = this.StockService.loading$;
  }

  ngOnInit() {
    this.sharedService.currentBooleanValue.subscribe(value => {
      console.log(value);
      this.showConfirmDialog = value;
    });
    this.subscription = this.sharedService.triggerFunction$.subscribe((functionName) => {
      if (functionName === 'closeDialog') {
        this.closeConfirmDialog();
      } else if (functionName === 'openDialog') {
        this.openConfirmDialog();
      }
    });
    this.apicall();
  }

  ngOnDestroy() {
    if (this.subscription){
      this.subscription.unsubscribe();
    }
  }


  openConfirmDialog() {
    this.showConfirmDialog = true;
    const body = document.getElementById("screen");
  
    if (body instanceof HTMLElement) {
      body.classList.add('blur-background');
    }
    this.styleManager.setBlurBackground(true);
  }
  
  closeConfirmDialog() {
    this.showConfirmDialog = false;
    const body = document.getElementById("screen");
  
    if (body instanceof HTMLElement) {
      body.classList.remove('blur-background');
    }
    this.styleManager.setBlurBackground(false);
  }


  private apicall(): void {
    this.StockService.show();
    if (this.apiurl) {
      this.http.get(this.apiurl).subscribe(data => {
        this.data = data;
        if (this.data['urls'].next) this.apiurlnext = this.data['urls'].next;
        else this.apiurlnext = undefined;
        if (this.data['urls'].previous) this.apiurlprev = this.data['urls'].previous;
        else this.apiurlprev = undefined;
        this.traslate();
        this.StockService.hide();
      }, error => {
        console.error(error);
        this.StockService.hide();
      });
    }
  }

  traslate(): void {
    this.ventas = this.data['elements'].map((element: any) => ({
      nombre: element.name,
      id_producto: element.id_product,
      precio: element.price,
      stock: element.stock,
      categoria: element.category,
      descripcion: element.description,
      imagen: element.image
    }));
  }



  next(){
    new Promise(resolve => {
      window.scrollTo({top: 0, behavior: 'smooth'});
      setTimeout(resolve, 400);
    }).then(() => {
      this.apiurl = this.apiurlnext;
      this.apicall();
    });
  }

  prev() {
    new Promise(resolve => {
      window.scrollTo({top: 0, behavior: 'smooth'});
      setTimeout(resolve, 400);
    }).then(() => {
      this.apiurl = this.apiurlprev;
      this.apicall();
    });
  }
}
