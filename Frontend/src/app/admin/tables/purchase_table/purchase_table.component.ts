import { Component, OnInit, ViewChild } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTable } from '@angular/material/table';
import { forkJoin } from 'rxjs';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { StyleManagerService } from '../../../styleManager.service';

export interface Purchase_order {
  id_purchase_order: number;
  date_done: Date;
  total_amount: number;
  id_client: string;
  processed: boolean;
}

@Component({
  selector: 'app-purchase_table',
  standalone: true,
  imports: [
    HttpClientModule,
    MatTableModule,
    MatCheckboxModule,
    TablesComponent,
    StockComponent,
    MatIconModule,
    MatButtonModule,
    ButtonsComponent,
    MatFormFieldModule,
    MatInputModule,
    CommonModule,
    RouterLink
  ],
  templateUrl: './purchase_table.component.html',
  styleUrl: './purchase_table.component.css'
})
export class Purchase_tableComponent implements OnInit{
  showConfirmDialog = false; // Controla la visibilidad del diálogo

  openConfirmDialog() {
    this.showConfirmDialog = true;
    const body = document.getElementById("contain");

    if (body instanceof HTMLElement) {
      body.classList.add('blur-background');
    }
    this.styleManager.setBlurBackground(true);
  }

  closeConfirmDialog() {
    this.showConfirmDialog = false;
    const body = document.getElementById("contain");

    if (body instanceof HTMLElement) {
      body.classList.remove('blur-background');
    }
    this.styleManager.setBlurBackground(false);
  }

  deleteConfirmed() {
    this.showConfirmDialog = false;
    let filas: string[] = this.getSelectedRowsData();
    filas.forEach((element) => {
      this.eliminarElemento(element);
    });
    this.deletePurachaseOrders();
  }

  @ViewChild(MatTable) table!: MatTable<any>;

  eliminarElemento(id: string) {
    // Eliminar el elemento de la fuente de datos
    // TODO fix this
    const index = this.dataSource.data.findIndex(item => item.id_purchase_order.toString() === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }

  // Datos para configurar la tabla
  data: any;
  purchases: Purchase_order[] = []
  dataSource: MatTableDataSource<Purchase_order> = new MatTableDataSource<Purchase_order>(this.purchases);
  displayedColumns: string[] = ['select', 'id_purchase_order', 'date_done', 'total_amount', 'id_client', 'processed'];
  selection = new SelectionModel<Purchase_order>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/get_all_purchase_orders/'

  constructor(private http: HttpClient, private router: Router, private styleManager: StyleManagerService) {}

  // Llamada a la API para extraer los datos y guardarlos en dataSource
  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Purchase_order>(this.purchases);
  }

  // Extracción de datos de la API
  private async apicall(): Promise<void> {
    if (this.apiUrl) {
      try {
        const response = await this.http.get(this.apiUrl).toPromise();
        this.data = response;
        this.traslate();
      } catch (error) {
        console.error(error);
      }
    }
  }

  // Traducción de los datos obtenidos de la API
  traslate(): void {
    this.purchases.push(...this.data['elements'].map((element: any) => ({
      id_purchase_order: element.id_purchase_order,
      date_done: element.date_done,
      total_amount: element.total_amount,
      id_client: element.id_client,
      processed: element.processed
    })));
  }

  // Busqueda de datos en la tabla
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  // Devuelve si estan todas las filas seleccionadas
  isAllSelected() {
    console.log(this.getSelectedRowsData());
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  // Selecciona todas las filas, si ya todas estan seleccionadas las deselecciona
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  // Devuelve en un arreglo todas las filas seleccionadas
  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.id_purchase_order);
    });

    return ids;
  }

  // TODO REVIEW Make function to delete purchase :l
  eliminarOrdenesCompra(carnetIds: string[]) {
    const observables = this.http.post('http://localhost:8000/api/admin/delete_purchases_orders/', { employee: carnetIds })

    return forkJoin(observables);
  }

  deletePurachaseOrders() {
    this.eliminarOrdenesCompra(this.getSelectedRowsData()).subscribe({
      next: (response) => this.notification('success'),
      error: (error) => this.notification('error')
    });
    this.closeConfirmDialog();
  }

  // Muestra en consola las filas seleccionadas
  showSelectedRowsData(): void {
    const selectedRows = this.getSelectedRowsData();
    console.log('Filas seleccionadas:', selectedRows);
  }

  // Selecciona una casilla
  checkboxLabel(row?: Purchase_order): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id_purchase_order + 1}`;
  }

  notification(type: 'error' | 'success'): void {
    const notification = document.getElementById('notification');
    if (notification instanceof HTMLElement) {
      notification.classList.add('notification-transition'); // Asegura que la transición esté aplicada
      notification.style.position = 'fixed';
      notification.style.right = '2vh';
      notification.style.bottom = '2vh';
      notification.style.display = 'block';
      notification.style.opacity = '0'; // Inicia invisible para la animación


      if (type === 'error') {
        notification.style.backgroundColor = 'red';
        notification.textContent = 'Employee could not be deleted';
      } else if (type === 'success') {
        notification.style.backgroundColor = 'chartreuse';
        notification.textContent = 'Employee has been removed';
      }

      // Inicia visible para la animación
      setTimeout(() => {
        notification.style.opacity = '0.7';
      }, 10); // Un pequeño retraso asegura que el navegador aplique la transición

      // Inicia la desaparición después de 2 segundos
      setTimeout(() => {
        notification.style.opacity = '0';
        // Oculta completamente después de que la transición de opacidad termine
        setTimeout(() => {
          notification.style.display = 'none';
        }, 500); // Coincide con la duración de la transición de opacidad
      }, 2000);
    }
  }
}
