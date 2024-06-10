import { Routes } from '@angular/router';
import {ViewsComponent} from "./views/views.component";
import {StockComponent} from "./views/stock/stock.component";
import {FormComponent} from "./views/form/form.component";
import {PostcarComponent} from "./views/stock/postcar/postcar.component";
import {RegistroComponent} from "./views/registro/registro.component";

export const routes: Routes = [
  { path: '', component: ViewsComponent},
  { path: 'main', component: ViewsComponent},
  { path: 'stock', component: StockComponent},
  { path: 'login', component: FormComponent},
  { path: 'stockadd', component: PostcarComponent},
  { path: 'register', component: RegistroComponent}
];
