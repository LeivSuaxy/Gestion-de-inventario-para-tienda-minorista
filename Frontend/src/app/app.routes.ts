import { Routes } from '@angular/router';
import {ViewsComponent} from "./views/views.component";
import {StockComponent} from "./views/stock/stock.component";
import {FormComponent} from "./views/form/form.component";
import {PostcarComponent} from "./admin/tables/product_table/postcar/postcar.component";
import {RegistroComponent} from "./views/registro/registro.component";
import { AdminComponent } from './admin/admin.component';
import { TablesComponent } from './admin/tables/tables.component';
import { Employee_tableComponent } from './admin/tables/employee_table/employee_table.component';
import { Inventory_tableComponent } from './admin/tables/inventory_table/inventory_table.component';
import { Product_tableComponent } from './admin/tables/product_table/product_table.component';
import { Post_inventoryComponent } from './admin/tables/inventory_table/post_inventory/post_inventory.component';
import { AboutComponent } from './views/about/about.component';
import { ContactComponent } from './views/contact/contact.component';

export const routes: Routes = [
  { path: '', component: ViewsComponent },
  { path: 'main', component: ViewsComponent },
  { path: 'stock', component: StockComponent },
  { path: 'login', component: FormComponent },
  { path: 'stock_add', component: PostcarComponent },
  { path: 'register', component: RegistroComponent },
  { path: 'admin', component: AdminComponent },
  { path: 'tables', component: TablesComponent },
  { path: 'tables/employee_table', component: Employee_tableComponent },
  { path: 'tables/inventory_table', component: Inventory_tableComponent },
  { path: 'tables/product_table', component: Product_tableComponent },
  { path: 'inventory_add', component: Post_inventoryComponent },
  { path: 'about', component: AboutComponent },
  { path: 'contact', component: ContactComponent }
];
